# Data Science, Analytics & Engineering (DSAE)
# Screening Test for the FLE Roles

# #1: Hands-On Coding

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
- For the dashboard, I use React because I had experience in using Axios for consuming the API

# #2: Design and Scenarios

### Given the increasing data volume each day and the desire of users to access all available data, you anticipate that the storage capacity will be fully utilized in a few months. Unfortunately, your team has no budget to increase the storage size. As a FLE, what approach would you take to handle this situation? 
   1. Examine and create the indexes for the columns that are used as filters (date & item_category) 
   2. Examine the data model and see if the data can be partitioned. Normalise the table if needed
   3. Examine the query and see if it can be improved, like putting size limits, pagination etc. 
   4. Perform data compression if possible 
   5. Configure the max_connections to allow maximum number of parallel connections that the server can support 
   6. Perform Vacuum command to delete obsolete records or configure the Auto Vacuum command for it to run automatically 
   7. Engage stakeholders to reassess usage and alternatives 

### You receive a request from the Cybersecurity team to implement new security measures into the system. However, you foresee that implementing these measures will result in system downtime for a few days, which could affect its operation. How would you handle this situation? 
  <ins>Before the system downtime:</ins>
   1. Identify the days and time range that has the lowest user activity and schedule the system downtime to be on those days and time range 
   2. Inform the reporting manager, so that he can allocate a few resources to be on standby during the downtime and delegate the task accordingly 
   3. Inform the Comms team to communicate with the affected parties about the system downtime 
   4. Prepare the implementation steps and recovery plan a few days before the downtime 
   5. Backup the necessary data in case of implementation failure 
   6. Prepare an alternative process such as manual data transfer, so that the data can still be transferred even during the system downtime 

  <ins>During the system downtime:</ins>
   1. Put up a maintenance page to alert anyone who tries to access the system 
   2. Perform the implementation steps following the order 
   3. Sit together with other colleagues in a war room to ease the communication 
   4. If there is any issue, troubleshoot the issue and quickly let others know especially the reporting manager 
   5. If the implementation is not successful, perform the recovery plan and restore the backup data 
   6. If there is any delay in the implementation process, inform the Comms team to communicate with the affected parties 
   7. Once the implementation steps are completed, check with the Cybersecurity team if the new security measures have been implemented successfully 
   8. If the implementation is successful, validate and test the existing system functionality to make sure it is working correctly 

   <ins>After the system downtime (successful): </ins>
   1. Put down the maintenance page 
   2. Inform the Comms team to communicate with the affected parties that the system is up and running 
   3. Monitor for any bugs and issues from time to time 
   4. If required, perform a postmortem discussion with the team on what can be improved 

### One of the requests is to integrate a machine learning model into the data pipeline. How would you assess the feasibility of this request? What factors would you consider when evaluating the implementation of a machine learning model? 
   1. The computational resources (CPU/GPU/NPU, memory, storage) 
   2. The quality of the loaded data 
   3. Compatibility with the data pipeline 
   4. Potential for any bias or errors 
   5. Long-term requirements 

### The bank is exploring the use of cloud technologies like PaaS and SaaS to improve the system's performance and scalability. As a FLE, how would you evaluate the potential benefits and risks of moving the system to the cloud, and what factors would you consider when making this decision? 
   1. Cost 
   2. Scalability 
   3. Accessibility 
   4. Security and reliability 
   5. Compliance 

### As a FLE, how do you strike a balance between the necessity for innovation and experimentation and the need for reliability in the data operation, especially when your team is already operating at nearly 100% capacity? 
   1. First, need to ensure core data operations are always maintained 
   2. Only prioritise innovations that directly enhance efficiency, automation and data quality 
   3. If it’s 100% capacity, maybe we can delegate it to become 70-30 model where 70% of the team focusing on the BAU whereas the other 30% focusing on the R&D 
   4. Instead of doing full R&D, we can also implement low-risk experiments when doing BAU task 
   5. Another option is to collaborate with other teams to get more capacity 
