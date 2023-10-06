import argparse

class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='A translation tool that supports translations in any language pair.')
        self.parser.add_argument('--config_file', type=str, default='config.yaml', help='Configuration file with model and API settings.')
        self.parser.add_argument('--model_name', type=str, default='gpt-3.5-turbo', help='Name of the Large Language Model.')
        self.parser.add_argument('--listen_addr', type=str, default='0.0.0.0',help='The Api server listening address.')
        self.parser.add_argument('--listen_port', type=int, default=8123,help='The Api server listening port.')

    def parse_arguments(self):
        args = self.parser.parse_args()
        return args
