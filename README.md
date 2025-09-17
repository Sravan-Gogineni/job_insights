Here is an updated version of your **README.md** that includes the clarification about the `dags` folder needing to be placed in the **Airflow directory**:

---

# Job Insights ETL

**Job Insights** is an ETL pipeline designed to extract, clean, and load job listings data from the **Indeed API** using Apify, and ingest the data into a **PostgreSQL** database. The entire process is orchestrated using **Apache Airflow** to ensure smooth automation and scheduling.

## Overview

This project extracts job listings from the **Indeed API**, cleans the raw data, and stores it into a **PostgreSQL** database. The orchestration is handled using **Apache Airflow** to automate the ETL process, ensuring the pipeline runs regularly and efficiently.

### Key Features
- **Data Extraction**: Extract job listings data from the **Indeed API** using the Apify platform.
- **Data Cleaning**: Clean and preprocess the raw data to remove irrelevant entries, handle missing values, and standardize the format.
- **Data Ingestion**: Load the cleaned job data into a **PostgreSQL** database.
- **Task Orchestration**: Schedule and monitor the ETL pipeline using **Apache Airflow**.

## Architecture

- **Apify API**: Used to extract job listings from Indeed.
- **PostgreSQL**: Stores cleaned job listings data in a structured format.
- **Apache Airflow**: Orchestrates the entire ETL pipeline, handling tasks like extraction, transformation, and loading of data.


![Architecture Diagram](https://github.com/UNH-TCOE-ECECS/F25-TeamDino/blob/main/Dino-Architecture.png)

![Database Schema](https://github.com/UNH-TCOE-ECECS/F25-TeamDino/blob/main/order_taking_system_schemas-2_page-0001.jpg)

## Overview
...

## Installation and Setup

### Prerequisites

To set up the Job Insights ETL pipeline, you will need the following:

- **Python 3.12.3**
- **Apache Airflow** (for scheduling and managing tasks)
- **PostgreSQL** (for storing the job data)
- **Apify API key** (to access the Indeed API)

### Step 1: Clone the repository

```bash
git clone https://github.com/Sravan-Gogineni/job_insights.git
cd job-insights
```

### Step 2: Set up a virtual environment

It’s recommended to use a virtual environment to manage dependencies.

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Step 3: Install required dependencies

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

### Step 4: Configure Airflow

1. **Initialize Airflow Database**:

   ```bash
   airflow db init
   ```

2. **Start the Airflow Scheduler**:

   ```bash
   airflow scheduler
   ```

3. **Start the Airflow Web Server**:

   ```bash
   airflow webserver
   ```

   Access the Airflow UI at `http://localhost:8080` to monitor the DAGs and tasks.

### Step 5: Configure PostgreSQL

- Set up a **PostgreSQL** database. You can use Docker or a local installation for this purpose.
- Create a schema with tables that match the structure of your job listings data.
- Update the `DATABASE_URL` in the Airflow configuration (`~/.bashrc` or `airflow.cfg`) to connect Airflow to your PostgreSQL instance.

### Step 6: Configure Apify API

- Sign up for an **Apify** account and obtain your **API key**.
- Configure the **Apify API** endpoint in the DAG file to extract job listings from Indeed.

### Step 7: Add the `dags` Folder to Airflow

1. **Move the `dags` folder** into your Airflow directory. The folder contains the DAG scripts for running the ETL pipeline.

   By default, Airflow looks for DAGs in the `~/airflow/dags/` directory. To move the `dags` folder into your Airflow directory:

   ```bash
   mv /job_insights/dags /path/to/airflow/dags/
   ```

   Make sure the path to `dags` points to your Airflow DAGs directory (usually `~/airflow/dags/`).

2. **Restart Airflow Scheduler** to detect the new DAG:

   ```bash
   airflow scheduler
   ```

3. **Verify in the Airflow UI** that the DAG appears under the DAGs tab.

### Step 8: Run the ETL Pipeline

- You can trigger the DAG either from the Airflow UI or run it manually via the command line:

  ```bash
  airflow dags trigger jobs_dag
  ```

### Directory Structure

The project directory should look like this:

```
job-insights/
│
├── dags/                    # Folder containing Airflow DAGs
│   ├── jobs_dag.py   # Main DAG file
│   └── ...
│
├── requirements.txt          # List of dependencies
├── README.md                 # This file
├── config/                   # Configuration files (e.g., Airflow settings, database configs)
│   └── airflow.cfg           # Airflow configuration (optional)
└── ...
```

## How the Pipeline Works

1. **Extract Data**: The pipeline starts by calling the **Apify API** to extract job listings from the Indeed endpoint.
2. **Transform Data**: The raw job data is cleaned and processed by removing irrelevant fields, handling missing data, and standardizing fields.
3. **Load Data**: The cleaned job data is then ingested into the **PostgreSQL** database.
4. **Orchestrate with Airflow**: The pipeline is orchestrated using **Apache Airflow**, which schedules the DAG and manages task execution. The DAG triggers the job extraction, data cleaning, and ingestion processes.

## Technologies Used

- **Apache Airflow**: For orchestrating and scheduling the ETL tasks.
- **Apify**: For extracting job listings from the Indeed API.
- **PostgreSQL**: For storing the cleaned job listings data.
- **Python**: For building the ETL pipeline and handling API requests, data cleaning, and database interactions.


