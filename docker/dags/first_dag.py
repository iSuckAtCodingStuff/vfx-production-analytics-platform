from airflow.sdk import DAG, task
from datetime import datetime

with DAG(
    dag_id = "first_dag",
    start_date = datetime(2026, 8, 1),
    schedule = "@daily",
    catchup = False
) as dag:

    @task
    def hello():
        print("hello")

    @task
    def airflow():
        print("airflow")

    hello_task = hello()

    airflow_task = airflow()

    hello_task >> airflow_task