from datetime import datetime
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from multiplyby5_operator import MultiplyBy5Operator


def print_hello():
    return 'Hello_World'


dag = DAG(dag_id='hello_world_by_five',
          description='Hello world example',
          schedule_interval='0 12 * * *',
          start_date=datetime(2017, 3, 12),
          catchup=False)

dummy_operator = DummyOperator(task_id='dummy_task',
                               retries=3,
                               dag=dag)

hello_operator = PythonOperator(task_id='hello_task',
                                python_callable=print_hello,
                                dag=dag)

multiplyby5_operator = MultiplyBy5Operator(my_operator_param='my_operator_param',
                                           task_id='multiplyby5_task',
                                           dag=dag)

dummy_operator >> hello_operator
dummy_operator >> multiplyby5_operator

