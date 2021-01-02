
# Unit test to MultiplyBy5 Operator

import unittest
from datetime import datetime
from airflow import DAG
from airflow.models import TaskInstance
from airflow_home.plugins.multiplyby5_operator import MultiplyBy5Operator


class TestMultiplyBy5OPerator(unittest.TestCase):

    def test_execute(self):
        dag = DAG(dag_id='anydag',
                  start_date=datetime.now()
                  )
        task = MultiplyBy5Operator(my_operator_param=10,
                                   task_id='anytask',
                                   dag=dag)
        task_instance = TaskInstance(task=task,
                                     execution_date=datetime.now())
        result = task.execute(task_instance.get_template_context())
        self.assertEqual(result, 50)


suite = unittest.TestLoader().loadTestsFromTestCase(TestMultiplyBy5OPerator)
unittest.TextTestRunner(verbosity=2).run(suite)
