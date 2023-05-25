# @@@SNIPSTART python-project-template-run-workflow
import asyncio

from temporalio.client import Client, WorkflowFailureError

from shared import MONEY_TRANSFER_TASK_QUEUE_NAME, PaymentDetails
from workflows import MoneyTransfer

async def main() -> None:
    # Create client connected to server at the given address
    client: Client = await Client.connect("localhost:7233")

    data: PaymentDetails =  PaymentDetails(
        source_account= "85-150",
        target_account= "43-812",
        amount=        250,
        reference_id=   "12345"
    )

    try:
        result: str = await client.execute_workflow(
            MoneyTransfer.run, data, id="pay-invoice-701", task_queue=MONEY_TRANSFER_TASK_QUEUE_NAME
        )

        print(f"Result: {result}")

    except WorkflowFailureError as err:
        activity_error = err.cause
        error = activity_error.cause
        print(f"Unable to transfer money.{error}")

if __name__ == "__main__":
    asyncio.run(main())
# @@@SNIPEND
