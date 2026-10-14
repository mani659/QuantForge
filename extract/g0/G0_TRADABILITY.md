# G0 Tradability Inventory — MT5 Terminal Symbol Query (read-only)

Method: read-only MT5 terminal API calls only (`initialize`, `terminal_info`, `symbols_get`, `symbol_info`, `shutdown`). No orders, no `symbol_select`, no history/download calls, no terminal-setting changes, no credentials printed. Terminal answered in <1 s (357 symbols enumerated). Snapshot quotes taken 2026-10-07 ~18:55 UTC.

Null policy: fields returned as `null` are shown as `null`; no values substituted. `0` snapshot spread + `0` snapshot time = no quote cached for that symbol at query time (symbol not Market-Watch-subscribed; subscription was intentionally not performed). These rows' static properties (digits, contract size, volumes, swaps, trade mode) are still authoritative.

## Requested markets

| Market | Broker symbol | Path | Category | Digits | Point | Contract size | Tick size | Tick value | Vol min | Vol step | Swap mode | Swap long | Swap short | Trade mode (raw) | Spread snapshot (points) | Snapshot time (UTC) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S&P 500 | US500m | Standard\Indices\US500m | Indices | 2 | 0.01 | 1.0 | 0.01 | 0.01 | 0.14 | 0.01 | 1 | -164.9 | 0.0 | full (4) | 40 | 2026-10-07T18:55:15+00:00 |
| Nasdaq-100 | USTECm | Standard\Indices\USTECm | Indices | 2 | 0.01 | 1.0 | 0.01 | 0.01 | 0.05 | 0.01 | 1 | -696.4 | 0.0 | full (4) | 112 | 2026-10-07T18:55:15+00:00 |
| DAX | DE30m | Standard\Indices\DE30m | Indices | 1 | 0.1 | 1.0 | 0.1 | 0.0 | 0.07 | 0.01 | 1 | -42.8 | 0.0 | full (4) | 0 | 0 |
| FTSE 100 | UK100m | Standard\Indices\UK100m | Indices | 2 | 0.01 | 1.0 | 0.01 | 0.0 | 0.05 | 0.01 | 1 | -168.6 | 0.0 | full (4) | 0 | 0 |
| Nikkei 225 | JP225m | Standard\Indices\JP225m | Indices | 1 | 0.1 | 1.0 | 0.1 | 0.0006331718745053345 | 3.0 | 0.01 | 1 | 0.0 | 0.0 | full (4) | 0 | 0 |
| EURUSD | EURUSDm | Standard\Forex\EURUSDm | Majors | 5 | 1e-05 | 100000.0 | 1e-05 | 1.0 | 0.01 | 0.01 | 1 | -5.7 | 0.0 | full (4) | 0 | 0 |
| GBPUSD | GBPUSDm | Standard\Forex\GBPUSDm | Majors | 5 | 1e-05 | 100000.0 | 1e-05 | 1.0 | 0.01 | 0.01 | 1 | -2.2 | -0.5 | full (4) | 0 | 0 |
| USDJPY | USDJPYm | Standard\Forex\USDJPYm | Majors | 3 | 0.001 | 100000.0 | 0.001 | 0.6331718745053345 | 0.01 | 0.01 | 1 | 0.0 | -13.9 | full (4) | 10 | 2026-10-07T18:55:14+00:00 |
| AUDUSD | AUDUSDm | Standard\Forex\AUDUSDm | Majors | 5 | 1e-05 | 100000.0 | 1e-05 | 1.0 | 0.01 | 0.01 | 1 | 0.0 | -2.0 | full (4) | 0 | 0 |
| USDCAD | USDCADm | Standard\Forex\USDCADm | Majors | 5 | 1e-05 | 100000.0 | 1e-05 | 0.0 | 0.01 | 0.01 | 1 | 0.0 | -8.9 | full (4) | 0 | 0 |
| USDCHF | USDCHFm | Standard\Forex\USDCHFm | Majors | 5 | 1e-05 | 100000.0 | 1e-05 | 0.0 | 0.01 | 0.01 | 1 | 0.0 | -10.3 | full (4) | 0 | 0 |
| Gold | XAUUSDm | Standard\Forex\XAUUSDm | Metals | 3 | 0.001 | 100.0 | 0.001 | 0.1 | 0.01 | 0.01 | 1 | -536.7 | 0.0 | full (4) | 240 | 2026-10-07T18:55:14+00:00 |
| Silver | XAGUSDm | Standard\Forex\XAGUSDm | Metals | 3 | 0.001 | 5000.0 | 0.001 | 5.0 | 0.01 | 0.01 | 1 | -7.9 | 0.0 | full (4) | 0 | 0 |
| Brent | UKOILm | Standard\Energies\UKOILm | Energies | 3 | 0.001 | 1000.0 | 0.001 | 1.0 | 0.01 | 0.01 | 1 | 0.0 | -125.3 | full (4) | 0 | 0 |
| Bitcoin | BTCUSDm | Standard\Crypto\BTCUSDm | Crypto | 2 | 0.01 | 1.0 | 0.01 | 0.01 | 0.01 | 0.01 | 1 | -1886.4 | 0.0 | full (4) | 0 | 0 |

Notes: broker uses `DE30` (not GER40) for DAX and `UKOIL` for Brent — no GER40/DE40/DAX or BRENT/BRN listings exist. `swap_mode` 1 = points-based triple-Wednesday convention per repo precedent (raw code reported, not interpreted). `swap_short` 0.0 on long-negative-swap symbols is the returned value. Snapshot source: `symbol_info.spread` / `symbol_info.time`.

## Other index, metal and energy symbols offered (name + category)

Indices: AUS200m, DXYm, FR40m, HK50m, IN50m, STOXX50m, US30m, US30_x10m, US500_x100m, USTEC_x100m (all category Indices).
Metals: XAGAUDm, XAGEURm, XAGGBPm, XAGJPYm, XALUSDm (aluminium), XAUAUDm, XAUEURm, XAUGBPm, XAUUSD247m (24/7 gold), XAUUSDm-Test (test symbol), XCUUSDm (copper), XNIUSDm (nickel), XPBUSDm (lead), XPDUSDm (palladium), XPTUSDm (platinum), XZNUSDm (zinc) (all category Metals).
Energies: USOILm (WTI), XNGUSDm (natural gas) (category Energies).
Excluded from this list (not index/metal/energy CFDs): BTCXAGm, BTCXAUm (crypto crosses matching metal codes); USDDZDm, USDNGNm (exotic FX matching "GER" inside Algerian/Nigerian).

## NOT LISTED

None — all 15 requested markets are listed.

## Not fully tradable

None — all 15 listed symbols report trade_mode full (raw 4). No close-only, long-only, short-only, or disabled symbols among the requested markets. Rows with spread 0 / time 0 had no cached quote at snapshot time (see null policy); this is a quote-subscription observation, not a trading restriction.
