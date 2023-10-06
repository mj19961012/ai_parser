from typing import Optional
import json
from parser.sql_splitter import SQLSplitter
from parser.translation_chain import TranslationChain
from utils import LOG


class SQLTranslator:
    def __init__(self, model_name: str):
        self.translate_chain = TranslationChain(model_name)
        self.sql_splitter = SQLSplitter()
        self.sql_scripts = []
        self.sql_results = []

    def translate_sql(self,sql: str):

        scripts = json.loads(self.sql_splitter.split_sql(sql))
        if isinstance(scripts, list):
            self.sql_scripts = scripts
        elif isinstance(scripts, str):
            self.sql_scripts.append(scripts)

        for sql_str in self.sql_scripts:
            translation, status = self.translate_chain.run(sql_str)
            if status :
                LOG.debug(f"\n[input]\n {sql_str}\n[output]\n {translation}")
                res = {}
                try:
                    res = json.loads(translation)
                    res['status'] = True
                except Exception as e:
                    res['err'] = str(e)
                    res['status'] = False
                res['sql'] = sql_str
                self.sql_results.append(res)

        return self.sql_results
