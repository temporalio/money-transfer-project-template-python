# @@@SNIPSTART python-money-transfer-project-template-withdraw
import asyncio
import os

from temporalio import activity
from temporalio.exceptions import ApplicationError

from banking_service import BankingService, InvalidAccountError
from shared import PaymentDetails


class BankingActivities:
    def __init__(self):
        self.bank = BankingService("bank-api.example.com")

    @activity.defn
    async def withdraw(self, data: PaymentDetails) -> str:
        reference_id = f"{data.reference_id}-withdrawal"
        try:
            confirmation = await asyncio.to_thread(
                self.bank.withdraw, data.source_account, data.amount, reference_id
            )
            return confirmation
        except InvalidAccountError:
            raise
        except Exception:
            activity.logger.exception("Withdrawal failed")
            raise

    # @@@SNIPEND
    # @@@SNIPSTART python-money-transfer-project-template-deposit
    @activity.defn
    async def deposit(self, data: PaymentDetails) -> str:
        reference_id = f"{data.reference_id}-deposit"

        # Demo-only failure injection, driven by the DEMO_FAILURE env var on the
        # Worker. Unset/"off" leaves behavior unchanged.
        demo_failure = os.environ.get("DEMO_FAILURE", "").lower()
        if demo_failure == "transient" and activity.info().attempt < 3:
            # Reuse the always-failing banking path for the first two attempts.
            # The error is retryable, so Temporal retries and the activity
            # succeeds on attempt 3 -> the Workflow recovers and COMPLETEs.
            await asyncio.to_thread(
                self.bank.deposit_that_fails,
                data.target_account,
                data.amount,
                reference_id,
            )
        elif demo_failure == "permanent":
            # Reuse the always-failing banking path, but make it non-retryable so
            # the Workflow's refund compensation (saga rollback) runs instead of
            # retrying.
            try:
                await asyncio.to_thread(
                    self.bank.deposit_that_fails,
                    data.target_account,
                    data.amount,
                    reference_id,
                )
            except Exception as exc:
                raise ApplicationError(str(exc), non_retryable=True) from exc

        try:
            confirmation = await asyncio.to_thread(
                self.bank.deposit, data.target_account, data.amount, reference_id
            )
            """
            confirmation = await asyncio.to_thread(
                self.bank.deposit_that_fails,
                data.target_account,
                data.amount,
                reference_id,
            )
            """
            
            # confirmation = self.bank.deposit_that_fails(data.target_account, data.amount, reference_id)
            return confirmation
        except InvalidAccountError:
            raise
        except Exception:
            activity.logger.exception("Deposit failed")
            raise

    # @@@SNIPEND

    # @@@SNIPSTART python-money-transfer-project-template-refund
    @activity.defn
    async def refund(self, data: PaymentDetails) -> str:
        reference_id = f"{data.reference_id}-refund"
        try:
            confirmation = await asyncio.to_thread(
                self.bank.deposit, data.source_account, data.amount, reference_id
            )
            return confirmation
        except InvalidAccountError:
            raise
        except Exception:
            activity.logger.exception("Refund failed")
            raise

    # @@@SNIPEND
