@echo off
echo 使用国内镜像源安装所需的Python库...

:: 确保pip已经更新
python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple

:: 安装OpenCV用于视频处理
pip install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple

:: 安装PyYAML用于解析YAML配置文件
pip install pyyaml -i https://pypi.tuna.tsinghua.edu.cn/simple

:: 安装Paramiko用于SSH操作
pip install paramiko -i https://pypi.tuna.tsinghua.edu.cn/simple

:: 你可以在这里添加其他需要的库

echo 所有库安装完成。
pause
