import time
from loguru import logger
import requests
import schedule as schedule
from dotenv import load_dotenv
import os
from wxpusher import WxPusher
from tools.browser import Browser
load_dotenv()
logger.add('juejin.log')
exec_time = os.getenv('exec_time', '09:00')
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
cookies = {'tt_scid': 'YUo.JYTx69b8KonWq4S7u2RTWG6Ck6Lc.kv2T7wNp9ghX7lCJJJ6CWUxLEBuT.m0d675', 'sessionid_ss': 'a32e07127d3a3e4c990d85e368014fe0', 'sessionid': 'a32e07127d3a3e4c990d85e368014fe0', 'sid_tt': 'a32e07127d3a3e4c990d85e368014fe0', 'uid_tt_ss': '98dd878fccbd4a020e1356f149f6e084', 'uid_tt': '98dd878fccbd4a020e1356f149f6e084', 'sid_guard': 'a32e07127d3a3e4c990d85e368014fe0%7C1643017489%7C5183999%7CFri%2C+25-Mar-2022+09%3A44%3A48+GMT', '_tea_utm_cache_2018': 'undefined', 'sid_ucp_v1': '1.0.0-KDY0NDkyYzBlOGFhODY1NmQzZmJkMGM2OTdhZmZhYTk3ZmMyOTFiNDUKFwiewMDA_fW5BRCR6rmPBhiwFDgCQO8HGgJsZiIgYTMyZTA3MTI3ZDNhM2U0Yzk5MGQ4NWUzNjgwMTRmZTA', 'passport_csrf_token_default': 'a70bdba54cf60220639846050294c732', 'passport_csrf_token': 'a70bdba54cf60220639846050294c732', 'ssid_ucp_v1': '1.0.0-KDY0NDkyYzBlOGFhODY1NmQzZmJkMGM2OTdhZmZhYTk3ZmMyOTFiNDUKFwiewMDA_fW5BRCR6rmPBhiwFDgCQO8HGgJsZiIgYTMyZTA3MTI3ZDNhM2U0Yzk5MGQ4NWUzNjgwMTRmZTA', 's_v_web_id': 'verify_kysi28zc_zwCpMgzT_aN3F_4mwR_BheY_MLm9p2yH1pFK', '__tea_cookie_tokens_2608': '%257B%2522web_id%2522%253A%25227056705391330543136%2522%252C%2522ssid%2522%253A%25222adc3c31-16f8-4c78-9178-2febcca42472%2522%252C%2522user_unique_id%2522%253A%25227056705391330543136%2522%252C%2522timestamp%2522%253A1643017272196%257D', '_gid': 'GA1.2.1667279830.1643017272', 'n_mh': 'Opz34QDGOsywMwicAR82MP0F6jYNglYygX0FpMkB-js', 'MONITOR_DEVICE_ID': '310ad263-f02a-4863-a7da-a273a2ed4ec1', '_ga': 'GA1.2.228618149.1643017272', 'MONITOR_WEB_ID': 'ce0e28cc-dd93-4795-9092-76fe2baa3db8', 'ttcid': '1fc86559b2464162ac80affa381b8c3616'}
# cookies = {}
def send_msg(msg):
    send_users = []
    token = 'AT_K91LP4X1hAl8EuzNqvB2zSZO0UJkjg4W'
    result = WxPusher.query_user(page=1, page_size=5, token=token)
    if result.get('code') == 1000:
        users = result.get('data').get('records')
        send_users = list(set([user.get('uid') for user in users]))
    else:
        logger.error(result.get('msg'))
    result = WxPusher.send_message(msg, uids=send_users, token=token)
    logger.info(result)


def sign_in():
    '''
    签到
    :return:
    '''
    global cookies
    response = requests.post('https://api.juejin.cn/growth_api/v1/check_in', headers=headers,cookies=cookies)
    if response.json().get('err_no') == 403:
        # 需要进行重新登录
        b = Browser()
        data = b.run()
        if data:
            for cook in data:
                cookies[cook["name"]] = cook["value"]
            response = requests.post('https://api.juejin.cn/growth_api/v1/check_in', headers=headers, cookies=cookies)
    return response.json().get('err_msg')


def get_cur_point():
    '''
    获取当前一共有多少积分
    :return:
    '''
    global cookies
    response = requests.get('https://api.juejin.cn/growth_api/v1/get_cur_point', headers=headers,cookies=cookies)
    logger.info(response.text)
    return response.json().get('data')


def run():
    msg = sign_in()
    time.sleep(1)
    count = get_cur_point()
    send_info = f'平台：掘金 \n 签到结果：{msg} \n 当前积分：{count}'
    send_msg(send_info)

if __name__ == '__main__':
    # run()
    schedule.every().day.at(exec_time).do(run)
    logger.info(f'执行时间：{exec_time}')
    while True:
        schedule.run_pending()  # run_pending：运行所有可以运行的任务
        time.sleep(3)
