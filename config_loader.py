import yaml
import os
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
                print('配置文件路径: {}'.format(config_path))
                print('{}编码格式: gbk'.format(config_path))
        except UnicodeDecodeError:
            with open(config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                print('配置文件路径: {}'.format(config_path))
                print('{}编码格式: utf-8'.format(config_path))
        except FileNotFoundError:
            print('配置文件不存在: {}'.format(config_path))
            exit(1)
        print(config)
        return config

    def get_config(self):
        return self._config

# 使用单例模式获取配置
if __name__ == '__main__':
    config_singleton = SingletonConfig()
    config = config_singleton.get_config()
    # 检查我的config.yaml里有多少个camera
    # for camera in config['camera']:
    # 打印每个camera的name
    # print(config['camera'][camera]['rtsp_url'])
