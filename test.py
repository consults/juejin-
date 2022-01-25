import requests
from requests.cookies import RequestsCookieJar

headers = {
    'authority': 'api.juejin.cn',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'content-type': 'application/json',
    'accept': '*/*',
    'origin': 'https://juejin.cn',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://juejin.cn/',
    'accept-language': 'zh-CN,zh;q=0.9'
}


data = [{'domain': 'juejin.cn', 'expiry': 1674553491, 'httpOnly': False, 'name': 'tt_scid', 'path': '/', 'secure': False, 'value': 'YUo.JYTx69b8KonWq4S7u2RTWG6Ck6Lc.kv2T7wNp9ghX7lCJJJ6CWUxLEBuT.m0d675'}, {'domain': '.juejin.cn', 'expiry': 1648201488, 'httpOnly': True, 'name': 'sessionid_ss', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'a32e07127d3a3e4c990d85e368014fe0'}, {'domain': '.juejin.cn', 'expiry': 1648201488, 'httpOnly': True, 'name': 'sessionid', 'path': '/', 'secure': False, 'value': 'a32e07127d3a3e4c990d85e368014fe0'}, {'domain': '.juejin.cn', 'expiry': 1648201488, 'httpOnly': True, 'name': 'sid_tt', 'path': '/', 'secure': False, 'value': 'a32e07127d3a3e4c990d85e368014fe0'}, {'domain': '.juejin.cn', 'expiry': 1648201488, 'httpOnly': True, 'name': 'uid_tt_ss', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '98dd878fccbd4a020e1356f149f6e084'}, {'domain': '.juejin.cn', 'expiry': 1648201488, 'httpOnly': True, 'name': 'uid_tt', 'path': '/', 'secure': False, 'value': '98dd878fccbd4a020e1356f149f6e084'}, {'domain': '.juejin.cn', 'expiry': 1674121489, 'httpOnly': True, 'name': 'sid_guard', 'path': '/', 'secure': False, 'value': 'a32e07127d3a3e4c990d85e368014fe0%7C1643017489%7C5183999%7CFri%2C+25-Mar-2022+09%3A44%3A48+GMT'}, {'domain': '.juejin.cn', 'expiry': 1643622072, 'httpOnly': False, 'name': '_tea_utm_cache_2018', 'path': '/', 'secure': False, 'value': 'undefined'}, {'domain': '.juejin.cn', 'expiry': 1648201488, 'httpOnly': True, 'name': 'sid_ucp_v1', 'path': '/', 'secure': True, 'value': '1.0.0-KDY0NDkyYzBlOGFhODY1NmQzZmJkMGM2OTdhZmZhYTk3ZmMyOTFiNDUKFwiewMDA_fW5BRCR6rmPBhiwFDgCQO8HGgJsZiIgYTMyZTA3MTI3ZDNhM2U0Yzk5MGQ4NWUzNjgwMTRmZTA'}, {'domain': '.juejin.cn', 'expiry': 1648201272, 'httpOnly': False, 'name': 'passport_csrf_token_default', 'path': '/', 'secure': False, 'value': 'a70bdba54cf60220639846050294c732'}, {'domain': '.juejin.cn', 'expiry': 1648201272, 'httpOnly': False, 'name': 'passport_csrf_token', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'a70bdba54cf60220639846050294c732'}, {'domain': '.juejin.cn', 'expiry': 1648201488, 'httpOnly': True, 'name': 'ssid_ucp_v1', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '1.0.0-KDY0NDkyYzBlOGFhODY1NmQzZmJkMGM2OTdhZmZhYTk3ZmMyOTFiNDUKFwiewMDA_fW5BRCR6rmPBhiwFDgCQO8HGgJsZiIgYTMyZTA3MTI3ZDNhM2U0Yzk5MGQ4NWUzNjgwMTRmZTA'}, {'domain': 'juejin.cn', 'httpOnly': False, 'name': 's_v_web_id', 'path': '/', 'secure': False, 'value': 'verify_kysi28zc_zwCpMgzT_aN3F_4mwR_BheY_MLm9p2yH1pFK'}, {'domain': '.juejin.cn', 'expiry': 1737625272, 'httpOnly': False, 'name': '__tea_cookie_tokens_2608', 'path': '/', 'secure': False, 'value': '%257B%2522web_id%2522%253A%25227056705391330543136%2522%252C%2522ssid%2522%253A%25222adc3c31-16f8-4c78-9178-2febcca42472%2522%252C%2522user_unique_id%2522%253A%25227056705391330543136%2522%252C%2522timestamp%2522%253A1643017272196%257D'}, {'domain': '.juejin.cn', 'expiry': 1643103890, 'httpOnly': False, 'name': '_gid', 'path': '/', 'secure': False, 'value': 'GA1.2.1667279830.1643017272'}, {'domain': '.juejin.cn', 'expiry': 1653385489, 'httpOnly': True, 'name': 'n_mh', 'path': '/', 'secure': False, 'value': 'Opz34QDGOsywMwicAR82MP0F6jYNglYygX0FpMkB-js'}, {'domain': 'juejin.cn', 'expiry': 1650793272, 'httpOnly': False, 'name': 'MONITOR_DEVICE_ID', 'path': '/', 'secure': False, 'value': '310ad263-f02a-4863-a7da-a273a2ed4ec1'}, {'domain': '.juejin.cn', 'expiry': 1706089490, 'httpOnly': False, 'name': '_ga', 'path': '/', 'secure': False, 'value': 'GA1.2.228618149.1643017272'}, {'domain': '.juejin.cn', 'expiry': 1650793490, 'httpOnly': False, 'name': 'MONITOR_WEB_ID', 'path': '/', 'secure': False, 'value': 'ce0e28cc-dd93-4795-9092-76fe2baa3db8'}, {'domain': 'juejin.cn', 'expiry': 1674553271, 'httpOnly': False, 'name': 'ttcid', 'path': '/', 'secure': False, 'value': '1fc86559b2464162ac80affa381b8c3616'}]
cookies = {}
for cook in data:
    cookies[cook["name"]]=cook["value"]
# response = requests.post('https://api.juejin.cn/growth_api/v1/check_in', headers=headers,cookies=cookies)
# print(response.text)   test
print(cookies)

