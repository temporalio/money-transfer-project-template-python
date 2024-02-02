# @@@SNIPSTART money-transfer-project-template-python-tests
import uuid

import pytest
from temporalio.client import WorkflowFailureError
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

from activities import BankingActivities
from shared import PaymentDetails
from workflows import MoneyTransfer


@pytest.mark.asyncio
async def test_money_transfer() -> None:
    task_queue_name: str = str(uuid.uuid4())
    async with await WorkflowEnvironment.start_time_skipping() as env:
        data: PaymentDetails = PaymentDetails(
            source_account="85-150",
            target_account="43-812",
            amount=250,
            reference_id="12345",
        )
        activities = BankingActivities()
        async with Worker(
            env.client,
            task_queue=task_queue_name,
            workflows=[MoneyTransfer],
            activities=[activities.withdraw, activities.deposit, activities.refund],
        ):
            result: str = await env.client.execute_workflow(
                MoneyTransfer.run,
                data,
                id=str(uuid.uuid4()),
                task_queue=task_queue_name,
            )
            assert result.startswith("Transfer complete")


@pytest.mark.asyncio
async def test_money_transfer_withdraw_insufficient_funds() -> None:
    task_queue_name: str = str(uuid.uuid4())
    async with await WorkflowEnvironment.start_time_skipping() as env:
        data: PaymentDetails = PaymentDetails(
            source_account="85-150",
            target_account="43-812",
            amount=25000,
            reference_id="12345",
        )

        activities = BankingActivities()
        async with Worker(
            env.client,
            task_queue=task_queue_name,
            workflows=[MoneyTransfer],
            activities=[activities.withdraw, activities.deposit, activities.refund],
        ):
            with pytest.raises(WorkflowFailureError) as excinfo:
                await env.client.execute_workflow(
                    MoneyTransfer.run,
                    data,
                    id=str(uuid.uuid4()),
                    task_queue=task_queue_name,
                )

            assert excinfo.value.__cause__.__cause__.type == "InsufficientFundsError"


# @@@SNIPEND
@pytest.mark.asyncio
async def test_money_transfer_withdraw_invalid_account() -> None:
    task_queue_name: str = str(uuid.uuid4())
    async with await WorkflowEnvironment.start_time_skipping() as env:
        data: PaymentDetails = PaymentDetails(
            source_account="85-151",
            target_account="43-812",
            amount=250,
            reference_id="12345",
        )

        activities = BankingActivities()
        async with Worker(
            env.client,
            task_queue=task_queue_name,
            workflows=[MoneyTransfer],
            activities=[activities.withdraw, activities.deposit, activities.refund],
        ):
            with pytest.raises(WorkflowFailureError) as excinfo:
                await env.client.execute_workflow(
                    MoneyTransfer.run,
                    data,
                    id=str(uuid.uuid4()),
                    task_queue=task_queue_name,
                )

            assert excinfo.value.__cause__.__cause__.type == "InvalidAccountError"
