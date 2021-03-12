from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

def push_cmd(**kwargs):
    ti = kwargs['ti']
    ti.xcom_push(value='cat /etc/passwd | wc -l', key='passwd_len')

def pull_result(**kwargs):
    ti = kwargs['ti']
    print(ti.xcom_pull(task_ids='bash_executor'))

with DAG(
    dag_id='xcom_pull_dag',
    start_date=datetime(2021, 3, 1),
    schedule_interval='@once',
) as dag:

    push_cmd_task = PythonOperator(
        task_id='push_cmd',
        python_callable=push_cmd,
    )

    cmd = BashOperator(
        task_id='bash_executor',
        bash_command='{{ ti.xcom_pull(task_ids="push_cmd", key="passwd_len") }}',
    )

    pull_result_task = PythonOperator(
        task_id='pull_result',
        python_callable=pull_result,
    )

    push_cmd_task >> cmd >> pull_result_task
