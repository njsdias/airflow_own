# https://www.youtube.com/watch?v=uCGuSt_yXkU&list=PLjMBCjnfVRHSsPO4sQoS1JdYpnjDFLBMc&index=3&t=1018s&ab_channel=PiterPy

from datetime import datetime
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from my_operators import MyFirstOperator, MyFirstSensor

dag = DAG(dag_id='my_test_dag',
          description='Another tutorial Dag',
          schedule_interval='0 12 * * *',
          start_date=datetime(2017, 3, 20),
          catchup=False)

dummy_task = DummyOperator(task_id='dummy_operator',
                           dag=dag)

sensor_task = MyFirstSensor(task_id='my_sensor_task', poke_interval=30, dag=dag)

operator_task = MyFirstOperator(my_operator_param='This is a test',
                                task_id='my_first_operator_tasks', dag=dag)

dummy_task >> sensor_task >> operator_task

