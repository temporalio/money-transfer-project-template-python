# @@@SNIPSTART python-money-transfer-project-template-shared
import os
from dataclasses import dataclass

# Reads TEMPORAL_TASK_QUEUE when set — e.g. a test harness isolating each run on its
# own queue — otherwise the shared default, so a copy-paste user is unaffected.
MONEY_TRANSFER_TASK_QUEUE_NAME = os.getenv("TEMPORAL_TASK_QUEUE", "TRANSFER_MONEY_TASK_QUEUE")


@dataclass
class PaymentDetails:
    source_account: str
    target_account: str
    amount: int
    reference_id: str


# @@@SNIPEND
