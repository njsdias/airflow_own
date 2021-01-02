import unittest
from datetime import datetime
from airflow import DAG
from airflow.models import TaskInstance
from airflow_home.plugins.helloworld_sensor import HelloworldSensor


class TestHelloWorldSensor(unittest.TestCase):
    def test_poke_should_return_false_when_value_is_not_divisible_by_three(self):
        dag = DAG(dag_id='anydag',
                  start_date=datetime.now()
                  )

        sensor_task = HelloworldSensor(task_id='any_sensor_task',
                                       poke_interval=2,
                                       params={'sensor_start_time': datetime(2018, 8, 8, 10, 50)},
                                       dag=dag)

        sensor_task_instance = TaskInstance(task=sensor_task,
                                            execution_date=datetime.now())

        result = sensor_task.poke(sensor_task_instance.get_template_context())
        self.assertFalse(result)

    def test_poke_should_return_true_wen_value_is_divisible_by_three(self):
        dag = DAG(dag_id='anydag',
                  start_date=datetime.now()
                  )
        sensor_task = HelloworldSensor(task_id='any_sensor_task',
                                       poke_interval=2,
                                       params={'sensor_start_time': datetime(2018, 8, 8, 10, 9)},
                                       dag=dag)

        sensor_task_instance = TaskInstance(task=sensor_task,
                                            execution_date=datetime.now()
                                            )

        result = sensor_task.poke(sensor_task_instance.get_template_context())
        self.assertTrue(result)

    def test_execute_should_return_true(self):
        dag = DAG(dag_id='anydag', start_date=datetime.now())
        sensor_task = HelloworldSensor(task_id='any_sensor_task',
                                       poke_interval=2,
                                       params={'sensor_start_time': datetime(2018, 8, 8, 10, 10)},
                                       dag=dag
                                       )

        sensor_task_instance = TaskInstance(task=sensor_task,
                                            execution_date=datetime.now()
                                            )

        sensor_time = sensor_task.execute(sensor_task_instance.get_template_context())
        self.assertEqual(sensor_time, 12)


suite = unittest.TestLoader().loadTestsFromTestCase(TestHelloWorldSensor)
unittest.TextTestRunner(verbosity=2).run(suite)
