import os

DEFAULT_BASE_URL = os.getenv("COT_API_BASE_URL", "https://api.cot-bias-terminal.com/v1")
DEFAULT_TIMEOUT_SEC = float(os.getenv("COT_TIMEOUT_SEC", "15.0"))
DEFAULT_MAX_RETRIES = int(os.getenv("COT_MAX_RETRIES", "3"))
