import os
import sys
import pandas as pd
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# --- 1. FORCE LOAD ENV ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

# Try loading .env from both current and root folder
load_dotenv(os.path.join(current_dir, ".env"))
load_dotenv(os.path.join(project_root, ".env"))

if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from zerodha_session import get_kite
    from backtest_equity import run_backtest
except ImportError:
    print("❌ ERROR: Missing files in 'backend' folder.")
    sys.exit()

def get_clean_data(token, days=365):
    kite = get_kite()
    
    # --- 2. SESSION SYNC ---
    if not kite.access_token:
        token_path = os.path.join(current_dir, "access_token.txt")
        if os.path.exists(token_path):
            with open(token_path, "r") as f:
                kite.set_access_token(f.read().strip())
                print(f"🔄 Session Synced from {token_path}")
        else:
            raise Exception("No active session found. Log in via dashboard first.")

    # --- 3. DATA FETCH ---
    to_date = datetime.now()
    from_date = to_date - timedelta(days=days)
    
    print(f"📡 Fetching Data for Token: {token}...")
    time.sleep(0.6) # Respect rate limits
    
    try:
        # We pass API_KEY explicitly if the library is being stubborn
        data = kite.historical_data(token, from_date, to_date, "day")
        if not data:
            raise Exception("Zero records returned.")
        
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date']).dt.tz_localize(None)
        df.set_index('date', inplace=True)
        return df
    except Exception as e:
        print(f"DEBUG: API_KEY being used is: {kite.api_key[:5]}***")
        raise e

def main():
    print("\n" + "="*40)
    print("   IEEE PAPER STATS GENERATOR")
    print("="*40)
    
    try:
        NIFTY_TOKEN = 256265 
        STOCK_TOKEN = 2863105 # IDFCFIRSTB
        
        df_nifty = get_clean_data(NIFTY_TOKEN)
        df_strategy = get_clean_data(STOCK_TOKEN)
        df_strategy['equity'] = df_strategy['close'] 

        run_backtest(df_strategy, df_nifty)
        
    except Exception as e:
        print(f"\n🛑 PROCESS HALTED: {str(e)}")

if __name__ == "__main__":
    main()