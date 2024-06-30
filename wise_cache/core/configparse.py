import os
import yaml


cyrillic_encodings = (
    'utf-8',
    'cp1251',
    'cp866',
    'cp855',
    'koi8_r',
    'cyrillic',
    'maccyrillic'
)


def read_yaml(filepath):
    for encoding in cyrillic_encodings:
        try:
            with open(filepath,
                      'r', encoding=encoding) as stream:
                try:
                    return yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)
        except UnicodeDecodeError:
            continue


def read_config(path):

    config_file_names = ['config.yml', 'config.yaml']

    if os.path.isfile(path):
        return read_yaml(path)

    for file_name in config_file_names:
        abs_config_path = os.path.abspath(path) + '/' + file_name
        if os.path.exists(abs_config_path):
            return read_yaml(abs_config_path)['dags']

    raise FileNotFoundError(f"No configuration file found in the specified path: {path}")
