# @@@SNIPSTART python-money-transfer-project-template-workflows
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError

with workflow.unsafe.imports_passed_through():
    from activities import BankingActivities
    from shared import PaymentDetails


@workflow.defn
class MoneyTransfer:
    @workflow.run
    async def run(self, payment_details: PaymentDetails) -> str:
        activities = BankingActivities()
        retry_policy = RetryPolicy(
            maximum_attempts=3,
            maximum_interval=timedelta(seconds=2),
            non_retryable_error_types=["InvalidAccountError", "InsufficientFundsError"],
        )

        # Withdraw money
        withdraw_output = await workflow.execute_activity(
            activities.withdraw,
            payment_details,
            start_to_close_timeout=timedelta(seconds=5),
            retry_policy=retry_policy,
        )

        # Deposit money
        try:
            deposit_output = await workflow.execute_activity(
                activities.deposit,
                payment_details,
                start_to_close_timeout=timedelta(seconds=5),
                retry_policy=retry_policy,
            )
        except ActivityError as deposit_err:
            # Handle deposit error
            workflow.logger.error(f"Deposit failed: {deposit_err}")
            # Attempt to refund
            try:
                refund_output = await workflow.execute_activity(
                    activities.refund,
                    payment_details,
                    start_to_close_timeout=timedelta(seconds=5),
                    retry_policy=retry_policy,
                )
                workflow.logger.info(
                    f"Refund successful. Confirmation ID: {refund_output}"
                )
                raise deposit_err
            except ActivityError as refund_error:
                workflow.logger.error(f"Refund failed: {refund_error}")
                raise refund_error

        result = (
            f"Transfer complete (transaction IDs: {withdraw_output}, {deposit_output})"
        )
        return result


# @@@SNIPEND
