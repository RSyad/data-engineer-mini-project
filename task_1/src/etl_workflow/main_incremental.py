import dask.dataframe as dd
import pandas as pd
from datetime import datetime
from prefect import task, flow
from sqlalchemy import create_engine, types, text
from constant import URL_DATA, URL_DATA_LOOKUP_ITEM, TABLE_NAME, CONNECTION_STRING

def get_latest_month_in_db(engine):
    query = "SELECT MAX(date) FROM price_catcher"
    result = engine.execute(query).scalar()
    if result:
        return result.strftime('%Y-%m')
    else:
        return '2022-01' # because default start data is at Jan 2022

@task
def extract_data(latest_month):
    try:
        print("Extracting data from source...")
        # Get list of YYYY-MM starting from latest month
        today = datetime.today()
        year_months = []
        current = datetime.strptime(latest_month, '%Y-%m')

        while current <= today:
            year_months.append(current.strftime('%Y-%m'))
            if current.month == 12:
                current = datetime(current.year + 1, 1, 1)
            else:
                current = datetime(current.year, current.month + 1, 1)

        # Extract data from 1 Jan 2022 until today
        df_list = [dd.read_parquet(URL_DATA.format(ym)) for ym in year_months]

        # Concatenate all dataframes
        data1 = dd.concat(df_list)
        
        # Extract lookup item
        data2 = dd.read_parquet(URL_DATA_LOOKUP_ITEM)

        # Merge data
        data = data1.merge(data2, on='item_code', how='left')

        print("Extraction complete!")

        return data
    except Exception as e:
        print(f"Error in extract_data: {e}")
        raise

@task
def transform_data(data):
    try:
        print("Transforming data...")
        
        # Remove null values
        data = data.dropna()

        # Remove duplicates
        data = data.drop_duplicates(subset=['date', 'premise_code', 'item_code'])

        # Convert date types
        data['date'] = dd.to_datetime(data['date'])
        data['price'] = dd.to_numeric(data['price'], errors='coerce')

        # Persist the data to memory
        data = data.persist()

        #print(data)

        print("Transformation complete!")

        return data
    except Exception as e:
        print(f"Error in transform_data: {e}")
        raise

@task
def load_data(data, engine):
    try:
        print("Loading data to database...")

        # Load existing keys with Pandas
        existing = pd.read_sql('SELECT date, premise_code, item_code FROM price_catcher', engine)
        existing_dd = dd.from_pandas(existing, npartitions=2)

        # Merge in Dask and compute only final data
        merged = data.merge(existing_dd, on=['date', 'premise_code', 'item_code'], how='left', indicator=True)
        new_data = merged[merged['_merge'] == 'left_only'].drop('_merge', axis=1)
        
        # Load data in batches
        n_partitions = new_data.npartitions
        for i in range(n_partitions):
            print(f"Loading partition {i+1}/{n_partitions}...")
            partition = new_data.partitions[i].compute()
            
            partition.to_sql(
                TABLE_NAME,
                engine,
                if_exists='append',
                index=False,
                dtype={
                    'date': types.Date(),
                    'premise_code': types.Integer(),
                    'item_code': types.Integer(),
                    'price': types.Numeric(10, 2),
                    'item': types.String(255),
                    'unit': types.String(50),
                    'item_group': types.String(100),
                    'item_category': types.String(100)
                }
            )
        
        print("Data loading complete!")
    except Exception as e:
        print(f"Error in load_data: {e}")
        raise

@flow
def etl_workflow():
    engine = create_engine(CONNECTION_STRING)
    latest_month = get_latest_month_in_db(engine)
    df = extract_data(latest_month)
    df = transform_data(df)
    load_data(df, engine)

if __name__ == "__main__":
    etl_workflow()