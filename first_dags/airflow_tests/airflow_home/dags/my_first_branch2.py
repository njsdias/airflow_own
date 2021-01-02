"""
Source: https://www.youtube.com/watch?v=TXccRfbapY8&list=PLcoE64orFoVsyzbvfgiY5iNKo30fJ4IWm&index=5&ab_channel=RocketMan
"""

from datetime import timedelta
from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator, BranchPythonOperator
import random

args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

dag = DAG(dag_id='my_first_branch',
          default_args=args,
          schedule_interval=None)


def push_to_xcom(**context):
    random_value = random.random()
    context['ti'].xcom_push(key='random_value', value=random_value)
    print('Im ok!!')


def print_hi(**context):
    received_value = context['ti'].xcom_pull(key='random_value')
    print(f'hi, I received the following {str(received_value)}')


def print_hello(**context):
    received_value = context['ti'].xcom_pull(key='random_value')
    print(f'hello, I received the following {str(received_value)}')


def branch_func(**context):
    if random.random() < 0.5:
        return 'say_hi'
    return 'say_hello'


run_this_task = PythonOperator(task_id='run_this',
                               python_callable=push_to_xcom,
                               provide_context=True,
                               retries=10,
                               retry_delay=timedelta(seconds=1),
                               dag=dag
                               )

run_this_task_2 = PythonOperator(task_id='say_hi',
                                 python_callable=print_hi,
                                 provide_context=True,
                                 dag=dag
                                 )

run_this_task_3  = PythonOperator(task_id='say_hello',
                                  python_callable=print_hello,
                                  provide_context=True,
                                  dag=dag
                                  )

branch_op = BranchPythonOperator(task_id='branch_task',
                                 python_callable=branch_func,
                                 provide_context=True,
                                 dag=dag)

run_this_task >> branch_op >> [run_this_task_2, run_this_task_3]
