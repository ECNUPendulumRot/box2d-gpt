# OPENAI API KEY
API_KEY = "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"

# 设置代理
USE_PROXY = True
if USE_PROXY:
    proxies = {
        "http": "socks5h://localhost:1080",
        "https": "socks5h://localhost:1080",
    }
else:
    proxies = None

CUSTOM_API_KEY_PATTERN = ""

TIMEOUT_SECONDS = 30

MAX_RETRY = 2