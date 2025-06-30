import logging
from datetime import datetime

logging.basicConfig(
    filename="actions.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_action(user: str, action: str, target: str):
    logging.info(f"User '{user}' performed '{action}' on '{target}'")
