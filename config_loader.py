import yaml

def load_config(config_path='config.yaml'):
    """从配置文件中加载所有配置信息"""
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config
