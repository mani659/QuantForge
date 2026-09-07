"""
BASE-001 V38A Stage 3 Economic Validation Script

Implements the registered BASE-001 decision process exactly as frozen:
- Structural level: rolling N=60 bar high/low
- Breakout: close strictly beyond level
- Validation: K=5 consecutive closes beyond frozen level
- Entry: open of bar E+K+1
- Exit: close of final bar before 23:59 UTC daily
- Direction: upside → LONG, downside → SHORT
- No stop, no target

This script does NOT modify any parameters. It evaluates the frozen Base.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# === FROZEN PARAMETERS (DO NOT MODIFY) ===
N = 60  # structural lookback
K = 5   # validation hold period
COST_BPS = 2  # round-trip cost in basis points

# === LOAD DATA ===
print("Loading USATECHIDXUSD M1 data...")
df = pd.read_csv('data/m1/USATECHIDXUSD_M1.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.sort_values('timestamp').reset_index(drop=True)

print(f"Total raw observations: {len(df)}")
print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
print(f"Data span: {(df['timestamp'].max() - df['timestamp'].min()).days} days")

# === DATA QUALITY GATE ===
print("\n=== DATA QUALITY GATE ===")

# Check for out-of-order timestamps
time_diffs = df['timestamp'].diff().dt.total_seconds()
out_of_order = (time_diffs < 0).sum()
print(f"Out-of-order timestamps: {out_of_order}")

# Check for malformed bars (H < L)
malformed = ((df['high'] < df['low'])).sum()
print(f"Malformed bars (H < L): {malformed}")

# Check for impossible OHLC (close outside H-L range)
impossible_close = ((df['close'] < df['low']) | (df['close'] > df['high'])).sum()
print(f"Impossible OHLC (close outside H-L): {impossible_close}")

# Check for zero/negative prices
zero_prices = ((df['open'] <= 0) | (df['high'] <= 0) | (df['low'] <= 0) | (df['close'] <= 0)).sum()
print(f"Zero/negative prices: {zero_prices}")

# Check for duplicate timestamps
duplicates = df['timestamp'].duplicated().sum()
print(f"Duplicate timestamps: {duplicates}")

# Apply data quality filter
df_clean = df.copy()
if duplicates > 0:
    df_clean = df_clean.drop_duplicates(subset='timestamp', keep='first')
    print(f"After dedup: {len(df_clean)} bars")

total_raw = len(df)
total_excluded = total_raw - len(df_clean)
print(f"Total excluded: {total_excluded}")
print(f"Final economically eligible dataset: {len(df_clean)} bars")

# === BASE-001 IMPLEMENTATION ===
print("\n=== BASE-001 OPPORTUNITY POPULATION ===")

# Compute rolling N-bar levels
df_clean = df_clean.reset_index(drop=True)
df_clean['rolling_high'] = df_clean['high'].rolling(window=N, min_periods=N).max().shift(1)
df_clean['rolling_low'] = df_clean['low'].rolling(window=N, min_periods=N).min().shift(1)

# State tracking
opportunities = []
active_validation = None  # {'direction', 'frozen_level', 'bar_e_idx', 'validation_count'}
active_trade = None  # {'direction', 'entry_price', 'entry_idx', 'entry_time'}

# UTC day tracking
current_utc_day = None

for i in range(N, len(df_clean)):
    row = df_clean.iloc[i]
    ts = row['timestamp']
    close = row['close']
    high = row['high']
    low = row['low']
    open_price = row['open']
    
    # Determine UTC day
    utc_day = ts.date()
    
    # === EXIT CHECK: 23:59 UTC daily ===
    # Exit at close of final bar of UTC day
    if active_trade is not None:
        # Check if this is the last bar of the UTC day
        next_row_idx = i + 1
        if next_row_idx < len(df_clean):
            next_ts = df_clean.iloc[next_row_idx]['timestamp']
            next_utc_day = next_ts.date()
        else:
            next_utc_day = utc_day + timedelta(days=1)
        
        # If next bar is different day (or we're at end), this is last bar of current day
        if next_utc_day != utc_day:
            exit_price = close
            exit_time = ts
            
            if active_trade['direction'] == 'LONG':
                gross_return = (exit_price - active_trade['entry_price']) / active_trade['entry_price']
            else:
                gross_return = (active_trade['entry_price'] - exit_price) / active_trade['entry_price']
            
            opportunities.append({
                'opportunity_id': len(opportunities) + 1,
                'direction': active_trade['direction'],
                'entry_time': active_trade['entry_time'],
                'entry_price': active_trade['entry_price'],
                'exit_time': exit_time,
                'exit_price': exit_price,
                'gross_return': gross_return,
                'exit_reason': 'session_close',
                'structural_level': active_trade.get('structural_level', None),
                'breakout_time': active_trade.get('breakout_time', None),
            })
            active_trade = None
    
    # === NEW DAY: reset ===
    if utc_day != current_utc_day:
        current_utc_day = utc_day
        # If there's an active trade from previous day, it should have been exited
        if active_trade is not None:
            # Force exit at previous bar
            prev_row = df_clean.iloc[i-1]
            exit_price = prev_row['close']
            exit_time = prev_row['timestamp']
            
            if active_trade['direction'] == 'LONG':
                gross_return = (exit_price - active_trade['entry_price']) / active_trade['entry_price']
            else:
                gross_return = (active_trade['entry_price'] - exit_price) / active_trade['entry_price']
            
            opportunities.append({
                'opportunity_id': len(opportunities) + 1,
                'direction': active_trade['direction'],
                'entry_time': active_trade['entry_time'],
                'entry_price': active_trade['entry_price'],
                'exit_time': exit_time,
                'exit_price': exit_price,
                'gross_return': gross_return,
                'exit_reason': 'day_boundary',
                'structural_level': active_trade.get('structural_level', None),
                'breakout_time': active_trade.get('breakout_time', None),
            })
            active_trade = None
    
    # === VALIDATION TRACKING ===
    if active_validation is not None:
        frozen_level = active_validation['frozen_level']
        direction = active_validation['direction']
        
        if direction == 'bullish':
            if close > frozen_level:
                active_validation['validation_count'] += 1
            else:
                # Rejection
                active_validation = None
        else:  # bearish
            if close < frozen_level:
                active_validation['validation_count'] += 1
            else:
                # Rejection
                active_validation = None
        
        # Check validation completion
        if active_validation is not None and active_validation['validation_count'] == K:
            # Validation confirmed!
            entry_idx = i + 1
            if entry_idx < len(df_clean):
                entry_row = df_clean.iloc[entry_idx]
                entry_price = entry_row['open']
                entry_time = entry_row['timestamp']
                
                # Only enter if we don't already have an active trade
                if active_trade is None:
                    active_trade = {
                        'direction': 'LONG' if active_validation['direction'] == 'bullish' else 'SHORT',
                        'entry_price': entry_price,
                        'entry_time': entry_time,
                        'entry_idx': entry_idx,
                        'structural_level': active_validation['frozen_level'],
                        'breakout_time': df_clean.iloc[active_validation['bar_e_idx']]['timestamp'],
                    }
            
            active_validation = None
    
    # === BREAKOUT DETECTION ===
    if active_validation is None and active_trade is None:
        rolling_high = df_clean.iloc[i]['rolling_high']
        rolling_low = df_clean.iloc[i]['rolling_low']
        
        if pd.isna(rolling_high) or pd.isna(rolling_low):
            continue
        
        # Check for bullish breakout
        if close > rolling_high:
            active_validation = {
                'direction': 'bullish',
                'frozen_level': rolling_high,
                'bar_e_idx': i,
                'validation_count': 0,
            }
        # Check for bearish breakout
        elif close < rolling_low:
            active_validation = {
                'direction': 'bearish',
                'frozen_level': rolling_low,
                'bar_e_idx': i,
                'validation_count': 0,
            }

# Handle any remaining active trade at end of data
if active_trade is not None:
    last_row = df_clean.iloc[-1]
    exit_price = last_row['close']
    exit_time = last_row['timestamp']
    
    if active_trade['direction'] == 'LONG':
        gross_return = (exit_price - active_trade['entry_price']) / active_trade['entry_price']
    else:
        gross_return = (active_trade['entry_price'] - exit_price) / active_trade['entry_price']
    
    opportunities.append({
        'opportunity_id': len(opportunities) + 1,
        'direction': active_trade['direction'],
        'entry_time': active_trade['entry_time'],
        'entry_price': active_trade['entry_price'],
        'exit_time': exit_time,
        'exit_price': exit_price,
        'gross_return': gross_return,
        'exit_reason': 'data_end',
        'structural_level': active_trade.get('structural_level', None),
        'breakout_time': active_trade.get('breakout_time', None),
    })

# Convert to DataFrame
opp_df = pd.DataFrame(opportunities)

print(f"Total opportunities: {len(opp_df)}")
if len(opp_df) > 0:
    print(f"LONG opportunities: {(opp_df['direction'] == 'LONG').sum()}")
    print(f"SHORT opportunities: {(opp_df['direction'] == 'SHORT').sum()}")
    print(f"Date range: {opp_df['entry_time'].min()} to {opp_df['exit_time'].max()}")

# === ECONOMIC CALCULATIONS ===
print("\n=== GROSS ECONOMICS ===")

if len(opp_df) == 0:
    print("NO OPPORTUNITIES GENERATED")
    print("Stage 3 BLOCKED: No eligible opportunities in the validation dataset")
else:
    gross_returns = opp_df['gross_return']
    
    winners = (gross_returns > 0).sum()
    losers = (gross_returns < 0).sum()
    breakeven = (gross_returns == 0).sum()
    
    print(f"Opportunity count: {len(opp_df)}")
    print(f"Winners: {winners}")
    print(f"Losers: {losers}")
    print(f"Breakeven: {breakeven}")
    print(f"Win rate: {winners/len(opp_df)*100:.1f}%")
    
    print(f"\nGross mean return: {gross_returns.mean()*100:.4f}%")
    print(f"Gross median return: {gross_returns.median()*100:.4f}%")
    print(f"Gross std deviation: {gross_returns.std()*100:.4f}%")
    print(f"Gross min return: {gross_returns.min()*100:.4f}%")
    print(f"Gross max return: {gross_returns.max()*100:.4f}%")
    print(f"Aggregate gross return: {gross_returns.sum()*100:.4f}%")
    
    # Best and worst
    best_idx = gross_returns.idxmax()
    worst_idx = gross_returns.idxmin()
    print(f"\nBest opportunity: #{opp_df.loc[best_idx, 'opportunity_id']} {opp_df.loc[best_idx, 'direction']} "
          f"entry={opp_df.loc[best_idx, 'entry_time']} return={gross_returns.loc[best_idx]*100:.4f}%")
    print(f"Worst opportunity: #{opp_df.loc[worst_idx, 'opportunity_id']} {opp_df.loc[worst_idx, 'direction']} "
          f"entry={opp_df.loc[worst_idx, 'entry_time']} return={gross_returns.loc[worst_idx]*100:.4f}%")
    
    # Profit factor
    gross_profits = gross_returns[gross_returns > 0].sum()
    gross_losses = abs(gross_returns[gross_returns < 0].sum())
    if gross_losses > 0:
        profit_factor = gross_profits / gross_losses
        print(f"\nProfit factor: {profit_factor:.2f}")
    else:
        print(f"\nProfit factor: INFINITE (no losses)")
    
    # === COST MODEL ===
    print("\n=== COST MODEL ===")
    cost_per_trade = COST_BPS / 10000  # 2 bps = 0.0002
    print(f"Round-trip cost: {COST_BPS} bps = {cost_per_trade*100:.4f}%")
    
    # === NET ECONOMICS ===
    print("\n=== NET ECONOMICS ===")
    net_returns = gross_returns - cost_per_trade
    
    net_winners = (net_returns > 0).sum()
    net_losers = (net_returns < 0).sum()
    
    print(f"Net winners: {net_winners}")
    print(f"Net losers: {net_losers}")
    print(f"Net win rate: {net_winners/len(opp_df)*100:.1f}%")
    
    print(f"\nNet mean return: {net_returns.mean()*100:.4f}%")
    print(f"Net median return: {net_returns.median()*100:.4f}%")
    print(f"Net std deviation: {net_returns.std()*100:.4f}%")
    print(f"Aggregate net return: {net_returns.sum()*100:.4f}%")
    
    # Profit factor (net)
    net_profits = net_returns[net_returns > 0].sum()
    net_losses = abs(net_returns[net_returns < 0].sum())
    if net_losses > 0:
        net_profit_factor = net_profits / net_losses
        print(f"Net profit factor: {net_profit_factor:.2f}")
    
    # === DISTRIBUTION ANALYSIS ===
    print("\n=== DISTRIBUTION ANALYSIS ===")
    print(f"Return percentiles:")
    for p in [5, 10, 25, 50, 75, 90, 95]:
        print(f"  {p}th: {gross_returns.quantile(p/100)*100:.4f}%")
    
    # Tail analysis
    top5_threshold = gross_returns.quantile(0.95)
    bottom5_threshold = gross_returns.quantile(0.05)
    top5_contribution = gross_returns[gross_returns >= top5_threshold].sum() / gross_returns.sum() * 100 if gross_returns.sum() != 0 else 0
    bottom5_contribution = gross_returns[gross_returns <= bottom5_threshold].sum() / gross_returns.sum() * 100 if gross_returns.sum() != 0 else 0
    
    print(f"\nTop 5% of trades contributed {top5_contribution:.1f}% of total return")
    print(f"Bottom 5% of trades contributed {bottom5_contribution:.1f}% of total return")
    
    # Concentration
    top10_pct = gross_returns.nlargest(int(len(gross_returns)*0.1)).sum() / gross_returns.sum() * 100 if gross_returns.sum() != 0 else 0
    print(f"Top 10% of trades contributed {top10_pct:.1f}% of total return")
    
    # === TEMPORAL ROBUSTNESS ===
    print("\n=== TEMPORAL ROBUSTNESS ===")
    opp_df['year'] = opp_df['entry_time'].dt.year
    opp_df['month'] = opp_df['entry_time'].dt.month
    opp_df['quarter'] = opp_df['entry_time'].dt.quarter
    
    # By year
    print("\nBy year:")
    for year in sorted(opp_df['year'].unique()):
        year_data = opp_df[opp_df['year'] == year]
        year_gross = year_data['gross_return']
        year_net = year_gross - cost_per_trade
        print(f"  {year}: {len(year_data)} trades, "
              f"gross mean={year_gross.mean()*100:.4f}%, "
              f"net mean={year_net.mean()*100:.4f}%, "
              f"win rate={((year_gross > 0).sum()/len(year_data)*100):.1f}%")
    
    # By quarter
    print("\nBy quarter:")
    for year in sorted(opp_df['year'].unique()):
        for quarter in sorted(opp_df[opp_df['year'] == year]['quarter'].unique()):
            q_data = opp_df[(opp_df['year'] == year) & (opp_df['quarter'] == quarter)]
            q_gross = q_data['gross_return']
            q_net = q_gross - cost_per_trade
            print(f"  {year}Q{quarter}: {len(q_data)} trades, "
                  f"gross mean={q_gross.mean()*100:.4f}%, "
                  f"net mean={q_net.mean()*100:.4f}%")
    
    # === DIRECTIONAL ANALYSIS ===
    print("\n=== DIRECTIONAL ANALYSIS ===")
    for direction in ['LONG', 'SHORT']:
        dir_data = opp_df[opp_df['direction'] == direction]
        if len(dir_data) > 0:
            dir_gross = dir_data['gross_return']
            dir_net = dir_gross - cost_per_trade
            print(f"\n{direction}:")
            print(f"  Count: {len(dir_data)}")
            print(f"  Gross mean: {dir_gross.mean()*100:.4f}%")
            print(f"  Gross median: {dir_gross.median()*100:.4f}%")
            print(f"  Net mean: {dir_net.mean()*100:.4f}%")
            print(f"  Win rate: {((dir_gross > 0).sum()/len(dir_data)*100):.1f}%")
            print(f"  Aggregate gross: {dir_gross.sum()*100:.4f}%")
            print(f"  Aggregate net: {dir_net.sum()*100:.4f}%")
        else:
            print(f"\n{direction}: No opportunities")
    
    # === SESSION/TIME CONCENTRATION ===
    print("\n=== SESSION/TIME CONCENTRATION ===")
    opp_df['hour'] = opp_df['entry_time'].dt.hour
    opp_df['dayofweek'] = opp_df['entry_time'].dt.dayofweek
    
    print("\nHour-of-day distribution:")
    hour_dist = opp_df.groupby('hour').agg(
        count=('opportunity_id', 'count'),
        gross_mean=('gross_return', 'mean'),
        net_mean=('gross_return', lambda x: x.mean() - cost_per_trade)
    )
    for hour in sorted(hour_dist.index):
        print(f"  {hour:02d} UTC: {hour_dist.loc[hour, 'count']} trades, "
              f"gross mean={hour_dist.loc[hour, 'gross_mean']*100:.4f}%, "
              f"net mean={hour_dist.loc[hour, 'net_mean']*100:.4f}%")
    
    print("\nDay-of-week distribution:")
    day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    dow_dist = opp_df.groupby('dayofweek').agg(
        count=('opportunity_id', 'count'),
        gross_mean=('gross_return', 'mean'),
        net_mean=('gross_return', lambda x: x.mean() - cost_per_trade)
    )
    for dow in sorted(dow_dist.index):
        print(f"  {day_names[dow]}: {dow_dist.loc[dow, 'count']} trades, "
              f"gross mean={dow_dist.loc[dow, 'gross_mean']*100:.4f}%, "
              f"net mean={dow_dist.loc[dow, 'net_mean']*100:.4f}%")
    
    # === LOSS STREAKS ===
    print("\n=== LOSS STREAKS ===")
    is_loss = (gross_returns < 0).values
    max_streak = 0
    current_streak = 0
    for loss in is_loss:
        if loss:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0
    print(f"Maximum consecutive losses: {max_streak}")
    
    # === MAX DRAWDOWN ===
    print("\n=== MAX DRAWDOWN ===")
    cumulative = (1 + net_returns).cumprod()
    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max
    max_dd = drawdown.min()
    print(f"Maximum drawdown: {max_dd*100:.4f}%")
    
    # === STATISTICAL INFERENCE ===
    print("\n=== STATISTICAL INFERENCE ===")
    n = len(net_returns)
    mean = net_returns.mean()
    std = net_returns.std()
    se = std / np.sqrt(n) if n > 1 else 0
    
    print(f"Sample size: {n}")
    print(f"Net mean: {mean*100:.4f}%")
    print(f"Standard error: {se*100:.4f}%")
    
    if n > 1 and se > 0:
        t_stat = mean / se
        print(f"t-statistic: {t_stat:.4f}")
        
        # Approximate p-value (two-tailed)
        from scipy import stats
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=n-1))
        print(f"p-value (two-tailed): {p_value:.6f}")
        
        # 95% CI
        ci_lower = mean - 1.96 * se
        ci_upper = mean + 1.96 * se
        print(f"95% CI: [{ci_lower*100:.4f}%, {ci_upper*100:.4f}%]")
    
    # === OPPORTUNITY FREQUENCY ===
    print("\n=== OPPORTUNITY FREQUENCY ===")
    total_days = (opp_df['exit_time'].max() - opp_df['entry_time'].min()).days
    trades_per_day = len(opp_df) / total_days if total_days > 0 else 0
    trades_per_week = trades_per_day * 5  # trading days
    trades_per_month = trades_per_day * 22
    print(f"Total trading days: {total_days}")
    print(f"Trades per day: {trades_per_day:.2f}")
    print(f"Trades per week (5-day): {trades_per_week:.2f}")
    print(f"Trades per month (22-day): {trades_per_month:.2f}")
    
    # === SAVE OPPORTUNITY TABLE ===
    opp_df.to_csv('output/base001_opportunity_table.csv', index=False)
    print(f"\nOpportunity table saved to output/base001_opportunity_table.csv")
    
    # === SUMMARY ===
    print("\n" + "="*60)
    print("STAGE 3 ECONOMIC VALIDATION SUMMARY")
    print("="*60)
    print(f"Base: BASE-001 (Structural Level Validation Flow)")
    print(f"Data: USATECHIDXUSD M1, {df_clean['timestamp'].min().date()} to {df_clean['timestamp'].max().date()}")
    print(f"Parameters: N={N}, K={K}, Cost={COST_BPS} bps")
    print(f"\nOpportunities: {len(opp_df)}")
    print(f"Win rate (gross): {winners/len(opp_df)*100:.1f}%")
    print(f"Win rate (net): {net_winners/len(opp_df)*100:.1f}%")
    print(f"Gross mean return: {gross_returns.mean()*100:.4f}%")
    print(f"Net mean return: {net_returns.mean()*100:.4f}%")
    print(f"Aggregate net return: {net_returns.sum()*100:.4f}%")
    print(f"Max drawdown: {max_dd*100:.4f}%")
    print(f"Trades per month: {trades_per_month:.2f}")
    print("="*60)
