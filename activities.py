# @@@SNIPSTART python-money-transfer-project-template-withdraw
from temporalio import activity

from banking_service import BankingService, InvalidAccountError
from shared import PaymentDetails


# Generic errors for activity failures
class WithdrawFailedError(Exception):
    pass


class DepositFailedError(Exception):
    pass


class RefundFailedError(Exception):
    pass


@activity.defn
async def withdraw(data: PaymentDetails) -> str:
    reference_id: str = f"{data.reference_id}-withdrawal"
    bank = BankingService("bank-api.example.com")
    try:
        confirmation = bank.withdraw(data.source_account, data.amount, reference_id)
        return confirmation
    except InvalidAccountError as error:
        raise error
    except Exception as error:
        activity.logger.error(f"Withdrawal failed: {error}")
        raise WithdrawFailedError("Failed to withdraw funds") from error


# @@@SNIPEND


# @@@SNIPSTART python-money-transfer-project-template-deposit
@activity.defn
async def deposit(data: PaymentDetails) -> str:
    reference_id: str = f"{data.reference_id}-deposit"
    bank = BankingService("bank-api.example.com")
    try:
        confirmation = bank.deposit(data.target_account, data.amount, reference_id)
        # confirmation = bank.deposit_that_fails(data.target_account, data.amount, reference_id)
        return confirmation
    except InvalidAccountError as error:
        raise error
    except Exception as error:
        activity.logger.error(f"Deposit failed: {error}")
        raise DepositFailedError("Failed to deposit funds") from error


# @@@SNIPEND


# @@@SNIPSTART python-money-transfer-project-template-refund
@activity.defn
async def refund(data: PaymentDetails) -> str:
    reference_id: str = f"{data.reference_id}-refund"
    bank = BankingService("bank-api.example.com")
    try:
        confirmation = bank.deposit(data.source_account, data.amount, reference_id)
        return confirmation
    except InvalidAccountError as error:
        raise error
    except Exception as error:
        activity.logger.error(f"Refund failed: {error}")
        raise RefundFailedError("Failed to refund") from error


# @@@SNIPEND
