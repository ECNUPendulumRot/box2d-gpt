openai_endpoint = "https://api.openai.com/v1/chat/completions"


def verify_endpoint(endpoint):
    """
        检查endpoint是否可用
    """
    return endpoint


model_info = {
    # openai
    "gpt-3.5-turbo": {
        "endpoint": openai_endpoint,
        "max_token": 4096
    },

    "gpt-3.5-turbo-16k": {
        "endpoint": openai_endpoint,
        "max_token": 16385
    },

    "gpt-3.5-turbo-0613": {
        "endpoint": openai_endpoint,
        "max_token": 4096
    },

    "gpt-3.5-turbo-16k-0613": {
        "endpoint": openai_endpoint,
        "max_token": 16385
    },

    "gpt-3.5-turbo-1106": {  # 16k
        "endpoint": openai_endpoint,
        "max_token": 16385,
    },

    "gpt-4": {
        "endpoint": openai_endpoint,
        "max_token": 8192,
    },

    "gpt-4-32k": {
        "endpoint": openai_endpoint,
        "max_token": 32768,
    },

    "gpt-4-1106-preview": {
        "endpoint": openai_endpoint,
        "max_token": 128000,
    },

    "gpt-3.5-random": {
        "endpoint": openai_endpoint,
        "max_token": 4096,
    },

    "gpt-4-vision-preview": {
        "endpoint": openai_endpoint,
        "max_token": 4096,
    }
}