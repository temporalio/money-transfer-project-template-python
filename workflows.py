# @@@SNIPSTART python-money-transfer-project-template-workflows
from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ApplicationError

from shared import PaymentDetails
from banking_service import InvalidAccountError, InsufficientFundsError
from activities import WithdrawFailedError, DepositFailedError, RefundFailedError

# Import activity, passing it through the sandbox without reloading the module
with workflow.unsafe.imports_passed_through():
    from activities import withdraw, deposit, refund

@workflow.defn
class MoneyTransfer:
    @workflow.run
    async def run(self, payment_details: PaymentDetails) -> str:
        retry_policy: RetryPolicy = RetryPolicy(
            initial_interval=timedelta(seconds=1),
            backoff_coefficient=2,
            maximum_attempts=3,
            maximum_interval=timedelta(seconds=2),
            non_retryable_error_types=["InvalidAccountError", "InsufficientFundsError"]
        )

        # Withdraw money
        try:
            withdraw_output: str = await workflow.execute_activity(
                withdraw,
                payment_details,
                start_to_close_timeout=timedelta(seconds=5),
                retry_policy=retry_policy
            )

        except (InvalidAccountError, InsufficientFundsError, WithdrawFailedError) as withdraw_err:
            raise withdraw_err

        # Captured money. Deposit.
        try:
            deposit_output: str = await workflow.execute_activity(
                deposit,
                payment_details,
                start_to_close_timeout=timedelta(seconds=5),
                retry_policy=retry_policy
            )

        except (InvalidAccountError, DepositFailedError) as deposit_err:
            # money couldn't be deposited. Return it.

            try:
                refund_output: str = await workflow.execute_activity(
                    refund,
                    payment_details,
                    start_to_close_timeout=timedelta(seconds=5),
                    retry_policy=retry_policy
                )

                print(f"""Deposit: failed to deposit money into {payment_details.target_account}.
                          Money was returned to {payment_details.source_account} with
                          confirmation ID: {refund_output}""")
                raise deposit_err

            except RefundFailedError as refund_error:
                print(f"""Deposit: failed to deposit money into {payment_details.target_account}.
                          Money could not be returned to {payment_details.source_account}""")

                # send alert for human intervention
                # ....
                raise refund_error

        result: str = f"Transfer complete (transaction IDs: {withdraw_output} {deposit_output}"
        return result
# @@@SNIPEND
