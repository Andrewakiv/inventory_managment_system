from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago


with DAG(
    dag_id="etl_orders_dag",
    schedule_interval="@hourly",
    start_date=days_ago(1),
    catchup=False,
    tags=["inventory-analysis"],
) as dag:

    fetch_orders = DockerOperator(
        task_id="fetch_orders",
        image="inventory-analysis:latest",
        api_version="auto",
        auto_remove=True,
        command="python /app/app/run_fetch.py",
        mount_tmp_dir=False,
        docker_url="unix://var/run/docker.sock",
        network_mode="inventory_net"
    )

    analyze_orders = DockerOperator(
        task_id="analyze_orders",
        image="inventory-analysis:latest",
        api_version="auto",
        auto_remove=True,
        command="python /app/app/run_analyze.py",
        mount_tmp_dir=False,
        docker_url="unix://var/run/docker.sock",
        network_mode="inventory_net"
    )

    fetch_orders >> analyze_orders
