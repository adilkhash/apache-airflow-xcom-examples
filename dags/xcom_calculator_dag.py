from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

def calculator_func(**kwargs):
    ti = kwargs['ti']
    tasks = [f'push_{i}' for i in range(1, 10)]
    values = ti.xcom_pull(task_ids=tasks)
    return sum(values)

with DAG(
    dag_id='xcom_multiple_tasks',
    start_date=datetime(2021, 3, 1),
    schedule_interval='@once',
) as dag:

    tasks = []

    for i in range(1, 10):
        task = PythonOperator(
            task_id=f'push_{i}',
            python_callable=lambda i=i: i,
        )

        tasks.append(task)

    calculator = PythonOperator(
        task_id='calculator',
        python_callable=calculator_func,
    )

    calculator.set_upstream(tasks)
