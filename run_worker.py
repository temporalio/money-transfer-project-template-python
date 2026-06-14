# @@@SNIPSTART python-money-transfer-project-template-run-worker
import asyncio

from temporalio.client import Client
from temporalio.envconfig import ClientConfigProfile
from temporalio.worker import Worker

from activities import BankingActivities
from shared import MONEY_TRANSFER_TASK_QUEUE_NAME
from workflows import MoneyTransfer


async def main() -> None:
    # Connect to Temporal Cloud using the "cloud-setup" profile from the shared
    # client config file (temporal.toml), which supplies the Cloud address,
    # namespace, and API key. Run the Temporal Cloud setup to populate it.
    profile = ClientConfigProfile.load("cloud-setup")
    client: Client = await Client.connect(**profile.to_client_connect_config())
    # Run the worker
    activities = BankingActivities()
    worker: Worker = Worker(
        client,
        task_queue=MONEY_TRANSFER_TASK_QUEUE_NAME,
        workflows=[MoneyTransfer],
        activities=[activities.withdraw, activities.deposit, activities.refund],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
# @@@SNIPEND
