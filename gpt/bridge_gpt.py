from toolbox import is_openai_api_key
from config import API_KEY

import logging
import requests

from toolbox import get_conf

proxies, TIMEOUT_SECONDS, MAX_RETRY = get_conf('proxies', 'TIMEOUT_SECONDS', 'MAX_RETRY')

def predict(inputs, llm_kwargs, plugin_kwargs, chatbot, history=[], system_prompt='', stream=True):
    user_input = inputs

    raw_input = inputs
    logging.info(f'[raw_input] {raw_input}')

    try:
        headers, payload, api_key = generate_payload(inputs, llm_kwargs, history, system_prompt)
    except RuntimeError as e:
        logging.error(
            f"您提供的api-key不满足要求，不包含任何可用于{llm_kwargs['llm_model']}的api-key。您可能选择了错误的模型或请求源。")
        return

    try:
        from model_info import model_info, verify_endpoint
        endpoint = verify_endpoint(model_info[llm_kwargs['llm_model']]['endpoint'])
    except:
        logging.error(f"Endpoint不满足要求")
        return

    history.append(inputs)
    history.append("")

    retry = 0

    while True:
        try:
            # make a POST request to the API endpoint, stream=True
            response = requests.post(endpoint, headers=headers, proxies=proxies,
                                     json=payload, stream=True, timeout=TIMEOUT_SECONDS);
            break
        except:
            retry += 1
            logging.log(f"，正在重试 ({retry}/{MAX_RETRY}) ……" if MAX_RETRY > 0 else "")

            if retry > MAX_RETRY: raise TimeoutError

    gpt_replying_buffer = ""

    is_head_of_the_stream = True

    if stream:
        stream_response = response.iter_lines()
        while True:

            chunk = next(stream_response)

            # 提前读取一些信息 （用于判断异常）
            chunk_decoded, chunkjson, has_choices, choice_valid, has_content, has_role = decode_chunk(chunk)

            if is_head_of_the_stream and (r'"object":"error"' not in chunk_decoded) and (
                    r"content" not in chunk_decoded):
                # 数据流的第一帧不携带content
                is_head_of_the_stream = False;
                continue

            if chunk:
                try:
                    if has_choices and not choice_valid:
                        # 一些垃圾第三方接口的出现这样的错误
                        continue
                    # 前者是API2D的结束条件，后者是OPENAI的结束条件
                    if ('data: [DONE]' in chunk_decoded) or (len(chunkjson['choices'][0]["delta"]) == 0):
                        # 判定为数据流的结束，gpt_replying_buffer也写完了
                        lastmsg = chatbot[-1][
                                      -1] + f"\n\n\n\n「{llm_kwargs['llm_model']}调用结束，该模型不具备上下文对话能力，如需追问，请及时切换模型。」"
                        yield from update_ui_lastest_msg(lastmsg, chatbot, history, delay=1)
                        logging.info(f'[response] {gpt_replying_buffer}')
                        break
                    # 处理数据流的主体
                    status_text = f"finish_reason: {chunkjson['choices'][0].get('finish_reason', 'null')}"
                    # 如果这里抛出异常，一般是文本过长，详情见get_full_error的输出
                    if has_content:
                        # 正常情况
                        gpt_replying_buffer = gpt_replying_buffer + chunkjson['choices'][0]["delta"]["content"]
                    elif has_role:
                        # 一些第三方接口的出现这样的错误，兼容一下吧
                        continue
                    else:
                        # 一些垃圾第三方接口的出现这样的错误
                        gpt_replying_buffer = gpt_replying_buffer + chunkjson['choices'][0]["delta"]["content"]

                    history[-1] = gpt_replying_buffer
                    chatbot[-1] = (history[-2], history[-1])
                    yield from update_ui(chatbot=chatbot, history=history, msg=status_text)  # 刷新界面
                except Exception as e:
                    yield from update_ui(chatbot=chatbot, history=history, msg="Json解析不合常规")  # 刷新界面
                    chunk = get_full_error(chunk, stream_response)
                    chunk_decoded = chunk.decode()
                    error_msg = chunk_decoded
                    chatbot, history = handle_error(inputs, llm_kwargs, chatbot, history, chunk_decoded, error_msg,
                                                    api_key)
                    yield from update_ui(chatbot=chatbot, history=history, msg="Json异常" + error_msg)  # 刷新界面
                    print(error_msg)
                    return


def generate_payload(inputs, llm_kwargs, history, system_prompt):
    """
    整合所有信息，选择LLM模型，生成http请求，为发送请求做准备
    """
    if not is_openai_api_key(llm_kwargs['api_key']):
        raise AssertionError(
            "你提供了错误的API_KEY。\n\n1. 临时解决方案：直接在输入区键入api_key，然后回车提交。\n\n2. 长效解决方案：在config.py中配置。")

    api_key = API_KEY

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    messages = []
    what_i_ask_now = {}
    what_i_ask_now["role"] = "user"
    what_i_ask_now["content"] = []
    what_i_ask_now["content"].append({
        "type": "text",
        "text": inputs
    })

    messages.append(what_i_ask_now)
    model = llm_kwargs['llm_model']

    payload = {
        "model": model,
        "messages": messages,
        "temperature": llm_kwargs['temperature'],  # 1.0,
        "top_p": llm_kwargs['top_p'],  # 1.0,
        "n": 1,
        "stream": True,
        "max_tokens": get_max_token(llm_kwargs),
        "presence_penalty": 0,
        "frequency_penalty": 0,
    }
    try:
        print(f" {llm_kwargs['llm_model']} : {inputs[:100]} ..........")
    except:
        print('输入中可能存在乱码。')
    return headers, payload, api_key


def get_max_token(llm_kwargs):
    from model_info import model_info
    return model_info[llm_kwargs['llm_model']]['max_token']
