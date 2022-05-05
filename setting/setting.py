from configparser import ConfigParser
import os

conf = ConfigParser()

# 选择环境
options = 'session'
# 目录位置
base_path = os.path.dirname(__file__)
# 配置文件位置
config_path = os.path.join(base_path, 'config.ini')
# 日志文件位置
log_path = os.path.join(os.path.dirname(base_path), 'log', 'juejin.log')
# 加载配置文件
conf.read(config_path)
# 邮件配置
e_user = conf.get('email', 'e_user')
e_password = conf.get('email', 'e_password')
e_host = conf.get('email', 'e_host')
e_to = conf.get('email', 'e_to')
e_subject = conf.get('email', 'e_subject')
e_contents = conf.get('email', 'e_contents')
# 执行时间
exec_time = conf.get('time', 'exec_time')
