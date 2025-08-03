import dask.dataframe as dd
from datetime import datetime
from constant import URL_DATA, URL_DATA_LOOKUP_ITEM, TABLE_NAME, CONNECTION_STRING
from sqlalchemy import create_engine, types, text, MetaData, Table
from sqlalchemy.dialects.postgresql import insert

""" YEAR_MONTH =    ['2022-01', '2022-02', '2022-03', '2022-04', '2022-05', '2022-06',
                 '2022-07', '2022-08', '2022-09', '2022-10', '2022-11', '2022-12',
                 '2023-01', '2023-02', '2023-03', '2023-04', '2023-05', '2023-06',
                 '2023-07', '2023-08', '2023-09', '2023-10', '2023-11', '2023-12',
                 '2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06',
                 '2024-07', '2024-08', '2024-09', '2024-10', '2024-11', '2024-12',
                 '2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06', '2025-07'] """

def generate_year_months(start_year=2022, start_month=1):
    # Get list of YYYY-MM starting from 2022-01
    today = datetime.today()
    year_months = []
    current = datetime(start_year, start_month, 1)

    while current <= today:
        year_months.append(current.strftime('%Y-%m'))
        # Move to next month
        if current.month == 12:
            current = datetime(current.year + 1, 1, 1)
        else:
            current = datetime(current.year, current.month + 1, 1)

    #print(year_months)

    return year_months

def extract_data():
    try:
        print("Extracting data from source...")
        # Get the list of YYYY-MM
        year_months = generate_year_months()

        #print(year_months)

        # Extract data from 1 Jan 2022 until today
        df_list = [
            dd.read_parquet(URL_DATA.format(ym))
            .drop_duplicates(['date', 'premise_code', 'item_code'])
            for ym in year_months
        ]

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

def load_data(data):
    try:
        print("Loading data to database...")
        engine = create_engine(CONNECTION_STRING)

        # Create empty table
        with engine.connect() as conn:
            conn.execute(text(f"DROP TABLE IF EXISTS {TABLE_NAME} CASCADE"))
            conn.execute(text(f"""
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    date DATE,
                    premise_code INTEGER,
                    item_code INTEGER,
                    price NUMERIC(10, 2),
                    item VARCHAR(255),
                    unit VARCHAR(50),
                    item_group VARCHAR(100),
                    item_category VARCHAR(100),
                    PRIMARY KEY (date, premise_code, item_code)
                )
            """))
            conn.commit()

        # Load data in batches
        n_partitions = data.npartitions
        for i in range(n_partitions):
            print(f"Loading partition {i+1}/{n_partitions}...")
            partition = data.partitions[i].compute()
            
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

if __name__ == "__main__":
    df = extract_data()
    df = transform_data(df)
    load_data(df)