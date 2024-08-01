# 使用官方 Python 镜像作为基础镜像
FROM python:3.8-slim-buster

# 更换 Debian 源为阿里云镜像
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list

# 设置工作目录
WORKDIR /app

# 安装系统依赖项，包括编译工具
RUN apt-get update && apt-get install -y \
    gcc \
    vim-tiny \
    libopencv-dev \
    ffmpeg \
    libblas-dev \
    liblapack-dev \
    libavutil-dev \
    gfortran \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# 升级 pip 并安装 Python 依赖项，使用清华源
COPY requirements.txt ./
RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 将代码添加到容器中
COPY . .

# 运行脚本
CMD ["python3", "main.py"]
