FROM selenium/standalone-chrome:85.0-chromedriver-85.0-20200907
USER root

RUN sed -i 's#http://deb.debian.org#https://mirrors.163.com#g' /etc/apt/sources.list
RUN apt-get update && apt-get install -y libglib2.0-dev libsm6 libxrender1 libxext-dev supervisor build-essential xvfb python3-distutils && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
  python3 get-pip.py
RUN mkdir /app/
WORKDIR /app
ENV TimeZone=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TimeZone /etc/localtime && echo $TimeZone > /etc/timezone
COPY requirements.txt .
RUN python3 -m pip install -r /app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
COPY . /app/
CMD ["supervisord","-c","/app/supervisord.conf"]