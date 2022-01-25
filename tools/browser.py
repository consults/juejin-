import io
from PIL import ImageFont, ImageDraw, Image
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import requests
from selenium import webdriver
from loguru import logger
import numpy as np
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import cv2
from tools.chaojiying import Chaojiying

logger.add('juejin.log')


class Browser(object):
    USERNAME = '打码平台账号'
    PASSWORD = '打码平台密码'
    JUEJIN = '掘金账号'
    JUEJINPASSWORD = '掘金密码'
    SOFT_ID = '923718'
    CAPTCHA_KIND = '9101'
    FILE_NAME = 'juejinCaptcha.jpeg'

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        # 初始化浏览器
        self.browser = webdriver.Chrome(options=options)
        self.browser.maximize_window()

    def run(self):
        url = 'https://juejin.cn/'
        self.browser.get(url)
        self.browser.implicitly_wait(10)
        loginButton = self.browser.find_element(By.XPATH, '//button[@class="login-button"]')
        self.wait('//button[@class="login-button"]')
        loginButton.click()
        self.browser.implicitly_wait(10)
        outherButton = self.browser.find_element(By.XPATH, '//div[@class="prompt-box"]/span')
        self.wait('//div[@class="prompt-box"]/span')
        outherButton.click()
        self.browser.implicitly_wait(10)
        self.input_access()
        self.browser.implicitly_wait(10)
        retryCount = 0
        responseCookies = []
        while True:
            imgSrc = self.get_captcha()
            self.downloadImg(imgSrc)
            logger.info(f'验证码地址：{imgSrc}')
            coorDinate = self.getCaptchaCoordinate()
            x = int(coorDinate['x']) / 2
            distance = self.gen_track(x + 17)
            self.moveCaptcha(distance)
            # 是否退款
            try:
                self.browser.find_element(By.XPATH, '//img[@class="lazy avatar avatar immediate"]')
                logger.success('登录成功')
                logger.success(f'{self.browser.get_cookies()}')
                responseCookies = self.browser.get_cookies()
                break
            except:
                retryCount += 1
                logger.error(f'登录失败:{retryCount} 次，重试中')

                self.refund(coorDinate['id'])
                time.sleep(1)
                if retryCount == 10:
                    break
        return responseCookies

    def refund(self, id):
        client = Chaojiying(self.USERNAME, self.PASSWORD, self.SOFT_ID)
        errRepoert = client.report_error(id)
        logger.success(f'退款信息：{errRepoert}')


    def wait(self, value):
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, value))
        )


    def input_access(self):
        inputAccount = self.browser.find_element(By.XPATH, '//input[@name="loginPhoneOrEmail"]')
        self.wait('//input[@name="loginPhoneOrEmail"]')
        inputAccount.send_keys(self.JUEJIN)
        password = self.browser.find_element(By.XPATH, '//input[@name="loginPassword"]')
        self.wait('//input[@name="loginPassword"]')
        password.send_keys(self.JUEJINPASSWORD)
        self.browser.implicitly_wait(10)
        loginButton = self.browser.find_element(By.XPATH, '//div[@class="panel"]/button[@class="btn"]')
        self.wait('//div[@class="panel"]/button[@class="btn"]')
        loginButton.click()


    def get_captcha(self):
        src = self.browser.find_element(By.XPATH, '//img[@id="captcha-verify-image"]').get_attribute('src')
        return src


    def downloadImg(self, src):
        headers = {
            'authority': 'p6-catpcha.byteimg.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'zh-CN,zh;q=0.9',
        }
        response = requests.get(src, headers=headers)
        with open(self.FILE_NAME, 'wb') as f:
            f.write(response.content)
        logger.success('图片下载完成')


    def getCaptchaCoordinate(self):
        image = cv2.imread(self.FILE_NAME)
        image = self.cv2_add_text(image, '请点击凹槽左上角', int(
            image.shape[1] / 10), int(image.shape[0] * 4 / 5), (255, 0, 0), 40)
        client = Chaojiying(self.USERNAME, self.PASSWORD, self.SOFT_ID)
        data = {}
        while True:
            result = client.post_pic(io.BytesIO(cv2.imencode(
                '.png', image)[1]).getvalue(), self.CAPTCHA_KIND)
            logger.info(f'请求超级鹰：{result}')
            if result.get('err_str') == "系统超时":
                pass
            else:
                x = result.get('pic_str').split(',')[0]
                y = result.get('pic_str').split(',')[1]
                id = result.get('pic_id')
                # 添加点
                image = cv2.circle(image, (int(x), int(y)), radius=10,
                                   color=(0, 0, 255), thickness=-1)
                cv2.imwrite(self.FILE_NAME, image)
                data = {'x': x, 'id': id}
                break
        return data


    def moveCaptcha(self, x):
        button = self.browser.find_element(By.XPATH, '//div[@class="secsdk-captcha-drag-icon sc-kEYyzF fiQtnm"]')
        # 按下鼠标左键
        ActionChains(self.browser).click_and_hold(button).perform()
        time.sleep(0.5)
        # 移动鼠标
        for i in x:
            ActionChains(self.browser).move_by_offset(xoffset=int(i), yoffset=0).perform()
            time.sleep(0.005)
        self.browser.get_screenshot_as_file('cur.png')
        time.sleep(0.5)
        ActionChains(self.browser).release(on_element=button).perform()
        time.sleep(3)


    @staticmethod
    def cv2_add_text(image, text, left, top, textColor=(255, 0, 0), text_size=20):
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('/app/tools/simsun.ttc', text_size, encoding="utf-8")
        draw.text((left, top), text, textColor, font=font)
        return cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)


    @staticmethod
    def gen_track(distance):  # distance为传入的总距离
        # 移动轨迹
        result = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 1

        while current < distance:
            if current < mid:
                # 加速度为2
                a = 4
            else:
                # 加速度为-2
                a = -3
            v0 = v
            # 当前速度
            v = v0 + a * t
            # 移动距离
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            result.append(round(move))
        return result


    def __del__(self):
        self.browser.close()
        pass


    @classmethod
    def start(cls):
        c = Browser()
        c.run()


if __name__ == '__main__':
    Browser.start()
