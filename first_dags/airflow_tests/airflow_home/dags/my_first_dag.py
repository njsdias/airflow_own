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

dag = DAG(dag_id='my_first_dag',
          default_args=args,
          schedule_interval=None)


def run_this_func(**context):
    print('hi')


def randomly_fail(**context):
    if random.random() > 0.7:
        raise Exception('Exception')
    print('Im ok!!')


run_this_task = PythonOperator(task_id='run_this',
                               python_callable=randomly_fail,
                               provide_context=True,
                               retries=10,
                               retry_delay=timedelta(seconds=1),
                               dag=dag
                               )


run_this_task2 = PythonOperator(task_id='run_this2',
                                python_callable=run_this_func,
                                provide_context=True,
                                dag=dag
                                )


run_this_task >> run_this_task2
