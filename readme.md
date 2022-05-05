# 掘金签到脚本
## 配置账号
使用google浏览器无痕模式进行登录，然后进入签到页面，查看请求中的session

在配置文件config.ini文件里面session节点下面新添加一行sessionx

```ini
[session]
sessionid1=xxx
sessionid2=xxx
sessionid3=xxx
```

## 配置邮件

email节点下配置，发送邮件账号，授权码，邮件类型，发送人，发送主题，发送内容

```ini
[email]
e_user=xxx@qq.com
e_password=xxx
e_host=smtp.xxx.com
e_to=xxx@xx.com
e_subject=xx subscribe failure
e_contents=failing id {}
```

## 配置运行每天运行时间

```ini
[time]
exec_time=09:00
```

## 运行

```dockerfile
# 编译docker镜像
docker build -t juejin .
# 运行镜像
docker run -itd --name juejin -v /home/juejin:/app juejin
```

