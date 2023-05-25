# @@@SNIPSTART python-money-transfer-project-template-withdraw
from temporalio import activity

from shared import PaymentDetails
from banking_service import BankingService, InvalidAccountError, InsufficientFundsError

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
    bank: BankingService = BankingService("bank-api.example.com")
    try:
        confirmation: str = bank.withdraw(data.source_account, data.amount, reference_id)
        return confirmation
    except InsufficientFundsError as error:
        raise error
    except InvalidAccountError as error:
        raise error
    except Exception as error:
        raise WithdrawFailedError(error) from error

# @@@SNIPEND

# @@@SNIPSTART python-money-transfer-project-template-deposit
@activity.defn
async def deposit(data: PaymentDetails) -> str:
    reference_id: str = f"{data.reference_id}-deposit"
    bank: BankingService = BankingService("bank-api.example.com")
    try:
        confirmation: str = bank.deposit(data.target_account, data.amount, reference_id)
        #confirmation: str = bank.deposit_that_fails(data.target_account, data.amount, reference_id)
        return confirmation
    except InvalidAccountError as error:
        raise error
    except Exception as error:
        raise DepositFailedError(error) from error

# @@@SNIPEND

# @@@SNIPSTART python-money-transfer-project-template-refund
@activity.defn
async def refund(data: PaymentDetails) -> str:
    reference_id: str = f"{data.reference_id}-refund"
    try:
        bank: BankingService = BankingService("bank-api.example.com")
        confirmation: str = bank.deposit(data.source_account, data.amount, reference_id)
        return confirmation
    except InvalidAccountError as error:
        raise error
    except Exception as error:
        raise RefundFailedError(error) from error

# @@@SNIPEND
