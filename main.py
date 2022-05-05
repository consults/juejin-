# -*- coding: utf-8 -*-
import time
from configparser import ConfigParser

import schedule
import yagmail
from setting.setting import config_path, options, log_path, exec_time, e_user, e_password, e_host, \
    e_to, e_subject, e_contents
from loguru import logger
import requests
from wxpusher import WxPusher

logger.add(log_path, encoding='utf-8')


class Juejin(object):
    def __init__(self):
        logger.info('初始化账号配置')
        # 读取配置
        self.session_list = self._init_config()
        # 初始化邮件功能
        self.yag = yagmail.SMTP(user=e_user, password=e_password, host=e_host, encoding='utf-8')

    @staticmethod
    def _init_config():
        """
        加载配置文件，并返回session——list
        :return:
        """
        logger.info('读取session列表')
        conf = ConfigParser()
        # 读取配置文件
        conf.read(config_path, encoding='utf-8')
        # 获取节点下所有session
        session_ids = conf.options(options)
        # 加载所有session
        session_list = []
        for item_key in session_ids:
            session_list.append(conf.get(options, item_key))
        logger.success(f'读取session列表成功：{session_list}')
        return session_list

    def run(self):
        for session in self.session_list:
            # 签到
            subscribe_result = self.subscribe(session)
            if subscribe_result.get('err_no') != 0:
                logger.error(f'{session} 签到失败')
                # 签到失败，进行报警
                self.warning(session)
                continue
            # 每日抽奖
            self.day_one(session)
            # 微信推送
            self.send_msg(f"掘金 {session} 的当前积分 {subscribe_result.get('sum_point')}")

    def subscribe(self, session):
        """
        签到
        :param token:
        :return:
        """
        headers = {
            'content-type': 'application/json',
            'cookie': f'sessionid={session};'
        }
        response = requests.post('https://api.juejin.cn/growth_api/v1/check_in', headers=headers).json()
        logger.info(response.get('err_msg'))
        return response

    def day_one(self, session):
        """
        每日抽奖
        :return:
        """
        headers = {
            'content-type': 'application/json',
            'cookie': f'sessionid={session};'
        }
        response = requests.post(
            'https://api.juejin.cn/growth_api/v1/lottery/draw?aid=2608&uuid=7040994416811361792&_signature=_02B4Z6wo00901i4gWqAAAIDCriKg4MxW9SIuJF4AAOoJAN57qoImv5OEUMh2t8du1WLNEHoJyzmQdec0vcS08W18vU3yRAul8K7pBypYs4GLx7FF5p3SGdilEGnt0zTpzNM7ePG7S64cEbdgc3',
            headers=headers).json()
        return response

    def send_msg(self, msg):
        """
        发送签到结果
        :return:
        """
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

    def warning(self, session):
        """
        签到失败，报警
        :return:
        """
        self.yag.send(to=e_to, subject=e_subject, contents=e_contents.format(session))
        logger.info('签到失败，进行报警')


def run():
    c = Juejin()
    c.run()


if __name__ == '__main__':
    run()
    schedule.every().day.at(exec_time).do(run)
    logger.info(f'执行时间：{exec_time}')
    while True:
        schedule.run_pending()  # run_pending：运行所有可以运行的任务
        time.sleep(3)
