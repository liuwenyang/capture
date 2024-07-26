import yaml

def load_config(config_path='config.yaml'):
    """从配置文件中加载所有配置信息并打印其内容"""
    try:
        with open(config_path, 'r', encoding='gbk') as file:
            config = yaml.safe_load(file)
            print('配置文件路径: {}'.format(config_path))
            print()
            print('{}编码格式: gbk'.format(config_path))

    except UnicodeDecodeError:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            print('配置文件路径: {}'.format(config_path))
            print()
            print('{}编码格式: utf-8'.format(config_path))

    except FileNotFoundError:
        print('配置文件不存在: {}'.format(config_path))
        exit(1)
    print(config)
    return config


if __name__ == '__main__':
    config = load_config()
    #检查我的config.yaml里有多少个camera
    #for camera in config['camera']:
        #打印每个camera的name
        #print(config['camera'][camera]['rtsp_url'])
