from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
import pandas as pd
from sqlalchemy import create_engine

# Read the data into a Pandas DataFrame
def extraction():    
    data = pd.read_csv(r'/workspaces/codespaces-blank/.vscode/jamesbond.csv')
    return data

#transformation: Convert date column to datetime format
def transformation(ti):
    data=ti.xcom_pull(task_id=['Extract_data'])
    data['date'] = pd.to_datetime(data['date'])
    return data

# Create a SQLAlchemy engine to connect to the PostgreSQL database
def loading(ti):
    data=ti.xcom_pull(task_id=['Transform_data'])    
    engine = create_engine('postgresql://username:password@localhost:5432/database_name')
    data.to_sql('your_table_name', engine, if_exists='replace', index=False)
    return True

# Define the DAG
dag = DAG(
    'load_data_to_postgresql',
    start_date=datetime(2023, 6, 18),
    schedule_interval='@daily',
    catchup=False
)

# Task to Extract data from CSV
extraction_task = PythonOperator(
    task_id='Extract_data',
    python_callable=extraction,
    do_xcom_push=True,
    dag=dag
)

# Task to Transform data
transformation_task = PythonOperator(
    task_id='Transform_data',
    python_callable=transformation,
    do_xcom_push=True,
    dag=dag
)

# Task to load data into PostgreSQL
loading_task = PythonOperator(
    task_id='Load_data',
    python_callable=loading,
    dag=dag
)


# Set up task dependencies
extraction_task >> transformation_task >> loading_task
