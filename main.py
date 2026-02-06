import pandas as pd
from clean_source import clean_source
from db_loader import load_to_db

def start_pipeline():

    print("--- Starting Data Pipeline ---")

    df_cleaned = clean_source()

    if df_cleaned is not None:
        load_to_db(df_cleaned, "daily_inventory")
        print("--- Pipeline Finished ---")
    else:
        print("--- No Data Returned ---")

if __name__ == "__main__":
    start_pipeline()
