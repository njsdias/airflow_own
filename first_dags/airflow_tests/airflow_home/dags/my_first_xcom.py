"""
1. Import Libraries
2. define arguments for your Dag
3. Define a DAG
4. Write tasks that are executed from your DAG

Source: https://www.youtube.com/watch?v=nVT5SgdvD0Q&ab_channel=RocketMan

To pass values between tasks we can use XCom
"""
from datetime import timedelta
from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
import random

args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

dag = DAG(dag_id='my_first_xcom',
          default_args=args,
          schedule_interval=None)


def push_to_xcom(**context):
    random_value = random.random()
    context['ti'].xcom_push(key='random_value', value=random_value)
    print('Im ok!!')


def run_this_func_mod(**context):
    received_value = context['ti'].xcom_pull(key='random_value')
    print(f'hi, I received the following {str(received_value)}')


run_this_task_xcom = PythonOperator(task_id='run_this_xcom',
                                    python_callable=push_to_xcom,
                                    provide_context=True,
                                    retries=10,
                                    retry_delay=timedelta(seconds=1),
                                    dag=dag
                                    )

run_this_task_mod = PythonOperator(task_id='run_this_mod',
                                   python_callable=run_this_func_mod,
                                   provide_context=True,
                                   dag=dag
                                   )


run_this_task_xcom >> run_this_task_mod
