import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, send_file, jsonify
from utils import ArgumentParser, LOG
from parser import TranslationConfig, SQLTranslator

app = Flask(__name__)

TEMP_FILE_DIR = "flask_temps/"

@app.route('/translation', methods=['POST'])
def translation():
    data = request.get_data()
    json_data = json.loads(data.decode('utf-8'))
    result = {}
    if 'sql' in json_data:
        LOG.debug(f"\n[input sql]\n{json_data['sql']}")
        sql = json_data['sql']
        result['result_data'] = Translator.translate_sql(sql)
        LOG.debug(f"\n[output sql]\n{result}")
    else:
        result['error'] = "input data error"
    return result
if __name__ == "__main__":
    # 解析命令行
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()

    # 初始化配置单例
    config = TranslationConfig()
    config.initialize(args)

    LOG.debug("""
                        _ooOoo_
                       o8888888o
                       88" . "88
                      (|  -_-  |)
                       0\  =  /0
                 _____/`-------`\____
                .   ~ \\\\|     |// ~  .
    """)

    # 实例化 SQLTranslator 类
    # sql ="""SELECT Customers.name, Orders.order_date FROM Database1.Customers JOIN Database2.Orders ON Customers.id = Orders.customer_id WHERE Orders.order_date >= '2023-01-01'"""
    global Translator
    Translator = SQLTranslator(config.model_name)

    LOG.debug(f"Running on local URL:  http://{config.listen_addr}:{config.listen_port}")
    # 启动 Flask Web Server
    app.run(host=config.listen_addr, port=config.listen_port, debug=True)
