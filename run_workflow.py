# @@@SNIPSTART python-project-template-run-workflow
import asyncio
import traceback

from temporalio.client import Client, WorkflowFailureError

from client_provider import get_temporal_client
from shared import MONEY_TRANSFER_TASK_QUEUE_NAME, PaymentDetails
from workflows import MoneyTransfer


async def main() -> None:
    client = await get_temporal_client()

    data: PaymentDetails = PaymentDetails(
        source_account="85-150",
        target_account="43-812",
        amount=250,
        reference_id="12345",
    )

    try:
        result = await client.execute_workflow(
            MoneyTransfer.run,
            data,
            id="pay-invoice-701",
            task_queue=MONEY_TRANSFER_TASK_QUEUE_NAME,
        )

        print(f"Result: {result}")

    except WorkflowFailureError:
        print("Got expected exception: ", traceback.format_exc())


if __name__ == "__main__":
    asyncio.run(main())
# @@@SNIPEND
