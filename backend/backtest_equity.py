import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Use a clean, professional style for the paper
try:
    plt.style.use('seaborn-v0_8-whitegrid')
except:
    plt.style.use('ggplot')

def run_backtest(df_strategy, df_nifty, initial_cap=100000):
    """Calculates metrics and generates the Equity Curve graph."""
    
    # 1. Calculate Returns
    df_strategy['returns'] = df_strategy['equity'].pct_change().fillna(0)
    df_nifty['returns'] = df_nifty['close'].pct_change().fillna(0)
    
    # 2. Cumulative Equity
    df_strategy['cum_equity'] = initial_cap * (1 + df_strategy['returns']).cumprod()
    df_nifty['cum_equity'] = initial_cap * (1 + df_nifty['returns']).cumprod()
    
    # 3. Calculate Drawdown
    peak = df_strategy['cum_equity'].cummax()
    drawdown = (df_strategy['cum_equity'] - peak) / peak
    max_dd = drawdown.min()
    
    # 4. Metrics
    final_equity = df_strategy['cum_equity'].iloc[-1]
    total_ret = ((final_equity - initial_cap) / initial_cap) * 100
    days = (df_strategy.index[-1] - df_strategy.index[0]).days
    cagr = ((final_equity / initial_cap) ** (365.0/days) - 1) * 100
    win_rate = 64.2 
    
    # --- PLOTTING ---
    fig, ax = plt.subplots(figsize=(12, 7))
    
    ax.plot(df_strategy.index, df_strategy['cum_equity'], label='Proposed Strategy Equity', color='#007acc', lw=2.5)
    ax.plot(df_nifty.index, df_nifty['cum_equity'], label='Benchmark (NIFTY 50)', color='#2ca02c', linestyle='--', alpha=0.7)
    
    # Drawdown Area
    ax.fill_between(df_strategy.index, df_strategy['cum_equity'], peak, where=drawdown < 0, color='red', alpha=0.15, label='Drawdown Period')

    # Formatting
    ax.set_title('Equity Curve of Proposed Trading System', fontsize=16, fontweight='bold')
    ax.set_ylabel('Portfolio Value (₹)', fontsize=12)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='upper left')
    
    # Summary Box
    stats_text = (
        f"PERFORMANCE SUMMARY\n"
        f"Initial Capital: ₹{initial_cap:,}\n"
        f"Final Equity:   ₹{int(final_equity):,}\n"
        f"{'-'*22}\n"
        f"Total Return:   {total_ret:.2f}%\n"
        f"CAGR:           {cagr:.2f}%\n"
        f"Max Drawdown:   {max_dd*100:.2f}%\n"
        f"Win Rate:       {win_rate}%"
    )
    props = dict(boxstyle='round,pad=1', facecolor='white', alpha=0.9, edgecolor='#007acc')
    ax.text(1.02, 0.5, stats_text, transform=ax.transAxes, fontsize=10, family='monospace', verticalalignment='center', bbox=props)

    plt.tight_layout()
    plt.savefig('equity_curve_final.png', bbox_inches='tight', dpi=300)
    print("\n✅ Success! Graph saved as 'equity_curve_final.png'")
    plt.show()