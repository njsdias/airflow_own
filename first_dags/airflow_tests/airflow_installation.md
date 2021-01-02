## How to install locally Airflow

**To have more Information**

[How to install Apache Airflow on local machine?: Airflow Tutorial](https://www.youtube.com/watch?v=lKL7DMIfMyc&list=PL5_c35Deekdm6N1OBHdQm7JZECTdm7zl-&index=5&ab_channel=Qubole)

[Get started developing workflows with Apache Airflow](https://michal.karzynski.pl/blog/2017/03/19/developing-workflows-with-apache-airflow/)


**Instructions and Tips**
1. Create a folder to work with Airflow

		mkdir airflow_projects

2. Create venv environment inside of folder created previously

		python3 -m venv env_airflow

3. Activate virtualenv

		source env_airflow/bin/activate

4. Install the latest version

		pip install apache-airflow==2.0.0

- set the AIRFLOW_HOME environment variable. For that run the command outside of
airflow_projects folder

        your_pc:~/airflow_projects$
        your_pc:~/airflow_projects$ cd ..
        your_pc:~$ export AIRFLOW_HOME='airflow_home'

- inside of airflow_projects folder runs:

		your_pc:~/airflow_projects$ airflow version

- Now we have the follow structure:

		airflow_projects
		  __ env_airflow
		  __ airflow_home
				___ logs
				___ airflow.cfg
				___ unittests.cfg
				___ webserver_config.py


5 Initialize the database. Outside of *airflow_home* folder run the next command

			your_pc:~/airflow_projects$ airflow db init

after this we can see *airflow.db* inside of *airflow_home*

5.1 Create users. It is essential to access the Airflow WebServer 

		airflow users create \
		         --username your_username \
		         --firstname your_firstname \
		         --lastname your_lastname \
		         --role Admin \
		         --email your_mail@service.com

	airflow users create -u your_username -f your_firstname -l our_lastnam -r Admin -e your_mail@service.com		

6 Creates a folder named as dags inside of airflow_home folder. 
Each DAG file needs to be save in Dags folder

    your_pc:~/airflow_projects/airflow_home$ mkdir dags


7 After write a dag run you need to configure the scheduler. For that open a nre Terminal windows in your Ubuntu.
  
		your_pc:~/airflow_projects$ export AIRFLOW_HOME='airflow_home'
		your_pc:~/airflow_projects$ source env_airflow/bin/activate
		(env_airflow) your_pc:~/airflow_projects$ airflow scheduler

8 Run Webserver in another Terminal window:

        (env_airflow) our_pc:~/airflow_projects$ airflow webserver

9 To see the Airflow WebServer open a new Web Browser folder (for instance in Chrome) and type:

        localhost:8080 

## Important Note

To see your Dags, Tasks and Tests, execute in this sequence:

- Open a Terminal and execute the scheduler
        
        (env_airflow) our_pc:~/airflow_projects$ airflow scheduler
        
- Open a new Terminal and execute the websever
        
        (env_airflow) our_pc:~/airflow_projects$ airflow webserver

- Open a new Web browser (for instance: Google Chrome) and type:

        localhost:8080
        
To end your work follow this sequence:

- Close your Webserver session on Web Browser

- Close the Web Browser Window

- Close Web Server. Go to Terminal where your Web Server is running and do: Ctrl + c

- Close Scheduler. Go to Terminal where you start the Scheduler and do: Ctrl + c

## Additional Information

1. To access to database. go to airflow directory

	1. enter into airflow folder:  our_pc:~/airflow_projects/airflow_home$
	2. type: sqlite3 aiflow.db
	3. see database tables: .table

2. Folder structure

[Testing Airflow workflows - ensuring your DAGs work before going into production](https://www.youtube.com/watch?v=ANJnYbLwLjE&ab_channel=ApacheAirflow)
See minute: 27:21

    dags                     Dags
    src                      Custom Library
    tests                    Tests
        ----dags
        ----conftest.py      conftest.py

Name your tests like: test_<name_of_test>
