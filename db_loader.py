import pandas as pd
from sqlalchemy import create_engine

# -- THIS FILE IS TO LOAD THE CLEANED DATA INTO POSTGRESQL -- #

def load_to_db(df: pd.DataFrame,table_name):
    username = ""
    password = ""
    host = ""
    port = ""
    database = ""

    connection_string = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
    engine = create_engine(connection_string)

    #this is by daily so we want the powerbi later to constantly
    # check for daily whether or not the stock is safe number or not so ill choose append
    df.to_sql(table_name, con=engine, if_exists='append', index=False)

    print('=' * 50)
    print("DATAFRAME FROM clean_source.py HAS BEEN TRANSFER TO INVENTORY DB")
    print('=' * 50)


# --- TEST BLOCK WHETHER THE DATA IS ACTUALLY GETTING TF OR NOT BABY ---
#if __name__ == "__main__":
    # 1. Create a fake little dataframe
#    data = {'id': [1, 2, 3], 'test_col': ['A', 'B', 'C']}
#    df_test = pd.DataFrame(data)

   # 2. Try to load it
#    print("Testing connection...")
#    load_to_db(df_test, "connection_test_table")
