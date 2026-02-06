from csv import excel

import pandas as pd
from attr.filters import exclude


# -- THIS FILE IS TO CLEAN THE DATA THAT FROM WHAT I NEED TO AFTER INSPECTION -- #

def clean_source():

    #Get Warning if any of the file goes missing
    try:
        #get source
        source = pd.read_csv('raw_data/daily_transactions.csv')
        pm = pd.read_csv("raw_data/products_master.csv")
    except FileNotFoundError:
        print("--- One of the CSV File is Missing ---")
        return None

    if source.empty:
        print("--- Daily Transaction File is mising ---")
        return None


    print("--- Extracting Data ---")

    #make sure ID from PM is real
    valid_ids = pm['product_id'].unique()

    # create a copy so original file isnt touched (we want ori not touch cus origin of source ma)
    df = source.copy()

    #changes needed to do according to NOTE BELOW

    # qty null changed to 0 and from FLOAT to INT
    df['qty'] = df['qty'].fillna(0).astype(int)

    # date change to DATETIME
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # remove dups
    df = df.drop_duplicates()

    # if prodID is in PM csv then it the transaction is valid
    df = df[df['product_id'].isin(valid_ids)]

    if df.empty:
        print("WARNING: ALL ROWS WERE REMOVED\nCHECK THE IDS ON THE PRODUCT IF IT MATCHES THE ONES IN PM")
        return None

    print("--- Transform Done ---")

    return df
