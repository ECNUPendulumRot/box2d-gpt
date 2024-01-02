import importlib
import re


def is_openai_api_key(key):
    CUSTOM_API_KEY_PATTERN = get_conf('CUSTOM_API_KEY_PATTERN')
    if len(CUSTOM_API_KEY_PATTERN) != 0:
        API_MATCH_ORIGINAL = re.match(CUSTOM_API_KEY_PATTERN, key)
    else:
        API_MATCH_ORIGINAL = re.match(r"sk-[a-zA-Z0-9]{48}$", key)
    return bool(API_MATCH_ORIGINAL)


def get_conf(*args):
    res = []
    for arg in args:
        r = read_config(arg)
        res.append(r)
    if len(res) == 1: return res[0]
    return res


def read_config(arg):
    from colorful import print亮红, print亮绿, print亮蓝

    r = getattr(importlib.import_module('config'), arg)

    if arg == 'API_KEY':
        if is_openai_api_key(r):
            print亮绿(f"[API_KEY] 您的 API_KEY 是: {r[:15]}*** API_KEY 导入成功")
        else:
            print亮红("[API_KEY] 您的 API_KEY 不是OPENAI API KEY，请在config文件中修改API密钥!")

    if arg == 'proxies':
        if not read_config('USE_PROXY'): r = None  # 检查USE_PROXY，防止proxies单独起作用
        if r is None:
            print亮红(
                '[PROXY] 网络代理状态：未配置。无代理状态下很可能无法访问OpenAI家族的模型。建议：检查USE_PROXY选项是否修改。')
        else:
            print亮绿('[PROXY] 网络代理状态：已配置。配置信息如下：', r)
            assert isinstance(r, dict), 'proxies格式错误，请注意proxies选项的格式，不要遗漏括号。'
    return r


if __name__ == '__main__':
    from check_proxy import check_proxy
    arg = 'proxies'
    proxies = get_conf(arg)
    check_proxy(proxies)
