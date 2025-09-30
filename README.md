# Data Engineer Mini Project

## Prerequisites

- Python 3.8+
- Node.js & npm (for React dashboard)
- PostgreSQL running locally (update credentials in `constant.py` (task_1 folder) and `settings.py` (task_2 folder))
- Install Python dependencies:
  ```
  pip install -r requirements.txt
  ```

---

## Step 1: Run the ETL Pipeline (`task_1`)

### Initial Full Load

1. Go to the ETL folder:
   ```
   cd task_1/src/etl_workflow
   ```
2. Run the full ETL script:
   ```
   python main_full.py
   ```
   This extracts all data from Jan 2022 to today and loads it into PostgreSQL.

### Incremental Updates

- For subsequent runs (to fetch only new data):
  ```
  python main_incremental.py
  ```

---

## Step 2: Run the API (`task_2`)

1. Go to the API folder:
   ```
   cd task_2
   ```
2. Make sure your `settings.py` is configured for PostgreSQL.
3. Start the Django server:
   ```
   python manage.py runserver
   ```
4. The API endpoint is available at:
   ```
   http://127.0.0.1:8000/api/price-data
   ```
   You can filter using query parameters:
   ```
   Examples:
   - http://127.0.0.1:8000/api/price-data?item_category=AYAM&year=2024&month=7&day=15
   - http://127.0.0.1:8000/api/price-data?year=2024&month=7&day=15
   - http://127.0.0.1:8000/api/price-data?month=7
   ```

---

## Step 3: Run the Dashboard (`task_3`)

1. Go to the React dashboard folder:
   ```
   cd task_3
   ```
2. Install dependencies:
   ```
   npm install
   ```
3. Start the dashboard:
   ```
   npm start
   ```
4. Open your browser and go to:
   ```
   http://localhost:3000
   ```
   - Use the input fields to filter by `item_category`, `year`, `month`, and `day`.
   - Click "Filter" to update the dashboard with filtered data from the API.

---

## Notes

- For best performance, use `main_incremental.py` for regular ETL updates.
- Make sure your database and Django API server are running before starting the dashboard.
- If you encounter issues, check error messages in the terminal or browser console for troubleshooting.

## Thought process and challenges
- To optimise this, I separated the `main_full.py` with `main_incremental.py`, which `main_full.py` is only needed to run on the first time whereas for the subsequent runs, we use `main_incremental.py`
- I also added the error handling for each of the functions for easier debugging process
- When I used Pandas, my Visual Studio Code crashed when running `main_full.py`, and then I tried using PySpark, but did not succeed, so I had decided to use Dask and insert the data by batches instead of the whole data at once
- After extracting and joining the data, I performed null removing and deduplication process to reduce the no of records to make the loading data process more efficient
- At first, I tried to hardcode the values of the 'YYYY-MM' for the parquet file names, but since in the instruction asked to get the recent data, I had to change to more dynamic approach
- As for the 'year', 'month', 'day' filtering requirements, I thought to split the 'date' column into those 3 columns, but then I found out Django can actually read and match the columns without needing to split it
- I used PostgreSQL because I have experienced in using it before
- I opt for Django because I think it's easier than Flask or FastAPI
- For the dashboard, I use React because I had experience in using Fetch() for consuming the API
- I used client-side pagination because I want to make the pie chart to be generated based on a single API response
- The pie chart is showing the item distribution based on the parameters/filters input by user
