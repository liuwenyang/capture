import platform
import yaml
from log import Log
"""
SingletonConfig 类：这个类实现了单例模式，并负责加载配置文件。__new__ 方法确保每次实例化该类时都返回同一个实例。

_load_config 方法：这是一个静态方法，用于从指定路径加载配置文件。如果文件使用 gbk 编码读取失败，则尝试使用 utf-8 编码。文件内容加载成功后，打印出文件路径和编码格式。

get_config 方法：这个方法返回加载的配置对象，确保该对象在全局范围内唯一。

此实现方法保证了在程序的任何地方，获取配置对象时都是同一个实例，避免了多次加载配置文件，提高了程序的效率和一致性。

"""
class SingletonConfig:
    _instance = None
    _config = None

    def __new__(cls, config_path='/home/storage/capture/.config/config.yaml'):
        if cls._instance is None:
            cls._instance = super(SingletonConfig, cls).__new__(cls)
            cls._config = cls._load_config(config_path)
        return cls._instance

    @staticmethod
    def _load_config(config_path):
        try:
            with open(config_path, 'r', encoding='gbk') as file:
                config = yaml.safe_load(file)
                Log.debug(f"配置文件路径: {config_path}, 编码格式: gbk")

        except UnicodeDecodeError:
            with open(config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                Log.debug(f"配置文件路径: {config_path}, 编码格式: utf-8")
        except FileNotFoundError:
            Log.debug("配置文件不存在")
            exit(1)
        # 使用 yaml.dump 打印格式化后的配置信息
        print(yaml.dump(config, allow_unicode=True, default_flow_style=False))
        return config

    def get_config(self):
        return self._config
# 检查操作系统
current_os = platform.system()

if current_os == "Linux":
    Log.debug("当前系统是 Linux")
    # 加载配置文件
    config_singleton = SingletonConfig("/home/storage/capture/.config/config.yaml")
    config = config_singleton.get_config()

elif current_os == "Windows":
    Log.debug("当前系统是 Windows")
    # 加载配置文件
    #config_singleton = SingletonConfig("D:\开源项目\capture\config.yaml")
    #config_singleton = SingletonConfig("D:\MatrixSoftware\项目现场同步资料\补连塔\.测试记录表\config.yaml")
    config_singleton = SingletonConfig("D:\capture\config.yaml")

    config = config_singleton.get_config()

else:
    Log.debug("当前系统不是 Linux 或 Windows")

# 使用单例模式获取配置
if __name__ == '__main__':
    config_singleton = SingletonConfig('/home/storage/capture/.config/config.yaml')
    config = config_singleton.get_config()
    # 检查我的config.yaml里有多少个camera
    # for camera in config['camera']:
    # 打印每个camera的name
    # print(config['camera'][camera]['rtsp_url'])
