import os

from langchain.chat_models import ChatOpenAI

OPENAI_API_KEY = "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"
def llm_init(model_name="gpt-4",
             temperature=0.2,
             model_kwargs={'frequency_penalty':0.2, 'presence_penalty':0}):

    llm = ChatOpenAI(model_name=model_name,
                     temperature=temperature,
                     model_kwargs=model_kwargs,
                     openai_api_key=OPENAI_API_KEY)

    return llm
