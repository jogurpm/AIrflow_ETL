**We need to have Docker installed as we will be using the Running Airflow in Docker procedure for this dag.py to Run.  **
Below are the steps install and spin up the airflow.

# Download the docker-compose.yaml file
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'

# Make expected directories and set an expected environment variable
mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env

# Initialize the database
docker-compose up airflow-init

# Start up all services
docker-compose up

**We also need to install Python,SQLAlchemy and Pandas for successful run of this Pipeline.**

**Instruction for modifying dag.py**
1. In line 10 of dag.py, Please do provide the correct path of the CSV file to be read (It is assumed that file contains a column with name "date").
2. In line 22, Please provide the username and password for the Postgres DB hosted at your localhost.
3. In line 23, Please fill replace the Table name to which data needs to be pushed.
