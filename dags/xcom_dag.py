from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

def print_xcom(**kwargs):
    ti = kwargs['ti']
    print('The value is: {}'.format(
        ti.xcom_pull(task_ids='hello_world')
    ))

with DAG(
    dag_id='xcom_dag',
    start_date=datetime(2021, 3, 1),
    schedule_interval='@once',
) as dag:

    cmd = BashOperator(
        task_id='hello_world',
        bash_command='echo "Hello world"',
    )

    printer = PythonOperator(
        task_id='printer',
        python_callable=print_xcom,
    )

    cmd >> printer