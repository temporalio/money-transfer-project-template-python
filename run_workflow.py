# @@@SNIPSTART python-project-template-run-workflow
import asyncio
import os
import traceback

from temporalio.client import Client, WorkflowFailureError
from temporalio.envconfig import ClientConfigProfile

from shared import MONEY_TRANSFER_TASK_QUEUE_NAME, PaymentDetails
from workflows import MoneyTransfer


async def main() -> None:
    # Connect to Temporal Cloud using the "cloud-setup" profile from the shared
    # client config file (temporal.toml), which supplies the Cloud address,
    # namespace, and API key. Run the Temporal Cloud setup to populate it.
    profile = ClientConfigProfile.load("cloud-setup")
    client: Client = await Client.connect(**profile.to_client_connect_config())

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
            id=os.environ.get("WORKFLOW_ID", "money-transfer-demo"),
            task_queue=MONEY_TRANSFER_TASK_QUEUE_NAME,
        )

        print(f"Result: {result}")

    except WorkflowFailureError:
        print("Got expected exception: ", traceback.format_exc())


if __name__ == "__main__":
    asyncio.run(main())
# @@@SNIPEND
