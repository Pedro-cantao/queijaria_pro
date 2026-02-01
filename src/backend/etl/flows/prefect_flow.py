from prefect import flow, task
import logging

# import do orquestrador (usa o pacote)
from ..etl import run_etl

logger = logging.getLogger("prefect.flow")

@task(retries=1, retry_delay_seconds=60)
def task_run_etl():
    logger.info("Iniciando task ETL via Prefect")
    run_etl()
    logger.info("Task ETL finalizada")

@flow(name="ETL-PCP-Flow")
def etl_flow():
    task_run_etl()

if __name__ == "__main__":
    # executar localmente: python -m src.backend.etl.flows.prefect_flow
    etl_flow()
