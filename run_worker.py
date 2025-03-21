# @@@SNIPSTART python-money-transfer-project-template-run-worker
import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from client_provider import get_temporal_client
from activities import BankingActivities
from shared import MONEY_TRANSFER_TASK_QUEUE_NAME
from workflows import MoneyTransfer


async def main() -> None:
    client = await get_temporal_client()
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
