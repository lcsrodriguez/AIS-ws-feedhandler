CONFIG_FILE: str = "../config.toml"
WORK_ENV: str = "local"
API_BASE_URL: str = "wss://stream.aisstream.io/v0/stream"

API_LOGIN_URL: str = "https://aisstream.io/authenticate"
API_USAGE_URL: str = "https://aisstream.io/api/dashboard/usage"
API_ENDPOINT_AFTER_LOGIN: str = "https://aisstream.io/customer.html"

DELAY_SELENIUM: int = 2
LIMIT_ATTEMPT_AFTER_LOGIN: int = 110
USER_AGENT: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"