from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from bronze_etl import bronze_layer_etl
from silver_etl import silver_layer_etl
from gold_test import gold_layer_etl

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 12, 6),
    'email': ['sgogi9@unh.newhaven.edu'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'jobs_dag',
    default_args=default_args,
    description='Jobs DAG',
    schedule_interval='45 * * * *',
    catchup=False
)

run_bronze_etl = PythonOperator(
    task_id='run_bronze_etl',
    python_callable=bronze_layer_etl,
    dag=dag,
)

run_silver_etl = PythonOperator(
    task_id='run_silver_etl',
    python_callable=silver_layer_etl,
    dag=dag,
)

run_gold_etl = PythonOperator(
    task_id='run_gold_etl',
    python_callable=gold_layer_etl,
    dag=dag,
)


run_bronze_etl >> run_silver_etl >> run_gold_etl