import pandas as pd
import numpy as np

def wilder_smoothing_scalar(tr_series, n=14):
    """Calculate the last value of Wilder's smoothing."""
    if len(tr_series) < n:
        return np.nan
    
    res = np.zeros(len(tr_series))
    res[n-1] = tr_series.iloc[:n].mean()
    for i in range(n, len(tr_series)):
        res[i] = res[i-1] + (tr_series.iloc[i] - res[i-1]) / n
    return res[-1]

class Cand015SignalEngine:
    def __init__(self, identity):
        self.identity = identity
        # Buffers for incremental calculation
        self.m1_buffer_ndx = []
        self.m1_buffer_btc = []
        
        self.last_shock_time = None
        self.lockout_minutes = identity["lockout_minutes"]
        
    def process_tick(self, tick):
        """
        Process a new market data tick (M1 bar).
        Returns a signal dictionary if one is generated, else None.
        """
        if tick["symbol"] == "USATECHIDXUSD":
            self.m1_buffer_ndx.append(tick)
        elif tick["symbol"] == "BTCUSD":
            self.m1_buffer_btc.append(tick)
            
        # We only evaluate signals at the close of an M5 bar (i.e. when a new M5 begins)
        # However, the exact logic of CAND-015 evaluates the shock on the *completed* M5 bar.
        # So when we receive an M1 tick at 10:05, the 10:00-10:05 M5 bar is complete.
        
        # For simplicity in this forward engine, we will compute the signal whenever we have enough data.
        # But we need to ensure we don't look ahead.
        
        return self._evaluate_signal(tick["observation_timestamp"])
        
    def _evaluate_signal(self, current_time):
        if not self.m1_buffer_ndx:
            return None
            
        # Optimization: keep only the last ~40 days of M1 data to avoid memory bloat
        # 40 days * 1440 mins = 57600 bars
        if len(self.m1_buffer_ndx) > 60000:
            self.m1_buffer_ndx = self.m1_buffer_ndx[-60000:]
            
        df_ndx = pd.DataFrame(self.m1_buffer_ndx)
        df_ndx.set_index('observation_timestamp', inplace=True)
        
        # Resample to M5
        df_m5 = df_ndx.resample('5min', label='left', closed='left').agg({
            'open':'first', 'high':'max', 'low':'min', 'close':'last'
        }).dropna()
        
        if len(df_m5) < 8641: # We need 30 days of M5 bars for atr_30d
            return None
            
        # Calculate ATR on M5
        high = df_m5['high']
        low = df_m5['low']
        close = df_m5['close']
        tr = pd.concat([high - low, (high - close.shift()).abs(), (low - close.shift()).abs()], axis=1).max(axis=1)
        
        # For performance, only compute Wilder's on the end of the series, but since pandas is vectorized, we can do it:
        # Actually, let's just use a full pass for safety in this parity test
        res = np.zeros(len(tr))
        n = 14
        first_valid = tr.first_valid_index()
        if first_valid is None:
            return None
            
        idx_start = tr.index.get_loc(first_valid)
        if idx_start + n - 1 >= len(res):
            return None
            
        res[idx_start + n - 1] = tr.iloc[idx_start:idx_start+n].mean()
        for i in range(idx_start + n, len(tr)):
            res[i] = res[i-1] + (tr.iloc[i] - res[i-1]) / n
            
        df_m5['atr'] = res
        df_m5['atr_30d'] = df_m5['atr'].rolling(8640).mean()
        
        # Resample to D1
        df_d1 = df_ndx.resample('1D').agg({
            'open':'first', 'high':'max', 'low':'min', 'close':'last'
        }).dropna()
        
        if len(df_d1) < 31:
            return None
            
        d1_high = df_d1['high']
        d1_low = df_d1['low']
        d1_close = df_d1['close']
        d1_tr = pd.concat([d1_high - d1_low, (d1_high - d1_close.shift()).abs(), (d1_low - d1_close.shift()).abs()], axis=1).max(axis=1)
        
        d1_res = np.zeros(len(d1_tr))
        d1_idx_start = d1_tr.index.get_loc(d1_tr.first_valid_index())
        d1_res[d1_idx_start + n - 1] = d1_tr.iloc[d1_idx_start:d1_idx_start+n].mean()
        for i in range(d1_idx_start + n, len(d1_tr)):
            d1_res[i] = d1_res[i-1] + (d1_tr.iloc[i] - d1_res[i-1]) / n
            
        df_d1['d1_atr'] = d1_res
        df_d1['d1_atr_30d'] = df_d1['d1_atr'].rolling(30).mean()
        
        # Get latest COMPLETE M5 bar
        # The current_time might be e.g. 10:05, meaning the 10:00-10:05 M5 bar is complete.
        # We need to make sure we don't look ahead. df_m5.index[-1] is the left label of the last bar.
        # If current_time >= df_m5.index[-1] + 5min, then the bar is complete.
        latest_complete_idx = None
        for idx in reversed(df_m5.index):
            if current_time >= idx + pd.Timedelta(minutes=5):
                latest_complete_idx = idx
                break
                
        if latest_complete_idx is None:
            return None
            
        latest_m5 = df_m5.loc[latest_complete_idx]
        if pd.isna(latest_m5['atr_30d']):
            return None
            
        # Determine D1 state using PRE-ENTRY (shifted) values
        # "state_eval_time": "pre_entry"
        # This means we use the D1 bar from the *previous* day.
        latest_date = latest_complete_idx.date()
        d1_shifted = df_d1[df_d1.index.date < latest_date]
        if d1_shifted.empty:
            return None
            
        latest_d1 = d1_shifted.iloc[-1]
        
        d1_atr = latest_d1['d1_atr']
        d1_atr_30d = latest_d1['d1_atr_30d']
        
        if pd.isna(d1_atr) or pd.isna(d1_atr_30d):
            return None
            
        vol_state = "LOW VOL" if d1_atr < d1_atr_30d else "HIGH VOL"
        
        # Check Shock
        ndx_ret = abs(latest_m5['close'] - latest_m5['open'])
        is_shock = ndx_ret > (3 * latest_m5['atr_30d'])
        
        if is_shock:
            direction = 1 if latest_m5['close'] > latest_m5['open'] else -1
            
            # Check lockout
            if self.last_shock_time is not None:
                if current_time < self.last_shock_time + pd.Timedelta(minutes=self.lockout_minutes):
                    return None # locked out
            
            self.last_shock_time = current_time
            
            return {
                "candidate_id": self.identity["candidate_id"],
                "event_timestamp": current_time,
                "event_type": "SHOCK",
                "volatility_state": vol_state,
                "intended_direction": direction,
                "frozen_rule_identity": self.identity["version"]
            }
            
        return None
