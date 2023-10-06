import json

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from utils import LOG

class TranslationChain:
    def __init__(self, model_name: str = "gpt-3.5-turbo", verbose: bool = True):
        
        # 翻译任务指令始终由 System 角色承担
        template = (
            """
            Task Title: Parsing SQL Query Strings and Extracting Key Component Information \n
            Purpose: To parse and extract key component information from a given SQL query string for further analysis or processing of SQL queries.\n
            Input: A valid SQL query string that needs to be parsed and analyzed. \n
            Output: A json object that contains the following possible attributes:
                Query type (such as SELECT, Insert, UPDATE, DELETE, CREATE, ALT, DROP, etc.)
                Database username (if it can be extracted from the query)
                Database name involved
                Schema Name involved (if applicable)
                Table names involved
                Column names involved
                Other SQL components that you consider important. \n
            Compatibility requirement: The parser needs to be able to handle multiple SQL dialects (such as MySQL, PostgreSQL, SQL Server, Oracle, etc.). \n
            Error handling: The parser needs to be able to elegantly handle parsing errors or illegal query inputs, rather than crashing or producing unpredictable output. \n
            Example 1:
            Input: SELECT customers.name, COUNT (orders. id) AS order_ Count From customers
            JOIN orders ON customers. id=orders. customer_ ID
            GROUP BY customers.name
            HAVING COUNT (orders. id)>5
            ORDER BY COUNT (orders. id) DESC;
            Output:
            {
                "operation_type" : "SELECT",
                "databases" : "",
                "username" : "",
                "schema" : "",
                "tables" : ["customers"],
                "columns" : ["name","order_count"]
            }
            Example 2:
            Input: WITH RECURSIVE ancestors AS (
                SELECT id, name, parent_id 
                FROM categories
                WHERE name = 'Electronics'
                UNION
                SELECT c.id, c.name, c.parent_id 
                FROM categories c
                JOIN ancestors a ON a.parent_id = c.id
            )
            SELECT id, name FROM ancestors;
            Output:
            {
                "operation_type" : "SELECT",
                "databases" : "",
                "username" : "",
                "schema" : "",
                "tables" : ["categories"],
                "columns" : ["name","id"]
            }
            Example 3:
            Input: SELECT customers.name, orders.order_date, SUM(order_details.quantity * products.price) AS total_price
            FROM customers
            JOIN orders ON customers.id = orders.customer_id
            JOIN order_details ON orders.id = order_details.order_id
            JOIN products ON order_details.product_id = products.id
            WHERE orders.order_date BETWEEN '2022-01-01' AND '2022-12-31'
            GROUP BY customers.id, orders.order_date
            HAVING total_price > 1000
            ORDER BY total_price DESC
            LIMIT 10;
            Output:
            {
                "operation_type" : "SELECT",
                "databases" : "",
                "username" : "",
                "schema" : "",
                "tables" : ["customers","orders"],
                "columns" : ["name","order_date","total_price"]
            }
            Example 4:
            Input: SELECT employees.name, employees.salary,AVG(salary) OVER(PARTITION BY department_id) AS avg_department_salary
            FROM employees
            WHERE EXISTS (
                SELECT 1 
                FROM managers
                WHERE employees.id = managers.employee_id
                AND end_date IS NULL
            );
            Output:
            {
                "operation_type" : "SELECT",
                "databases" : "",
                "username" : "",
                "schema" : "",
                "tables" : ["employees"],
                "columns" : ["name","salary","avg_department_salary"]
            }
            Example 5:
            Input: CHANGE USER 'newuser'@'localhost' IDENTIFIED BY 'newpassword';
            Output:
            {
                "operation_type" : "CHANGE USER",
                "databases" : "",
                "username" : "newuser",
                "schema" : "",
                "tables" : [],
                "columns" : []
            }
            Example 6:
            Input: SET ROLE 'newuser';
            Output:
            {
                "operation_type" : "SET ROLE",
                "databases" : "",
                "username" : "newuser",
                "schema" : "",
                "tables" : [],
                "columns" : []
            }
            Example 7:
            Input: EXECUTE AS USER = 'newuser';
            Output:
            {
                "operation_type" : "EXECUTE",
                "databases" : "",
                "username" : "newuser",
                "schema" : "",
                "tables" : [],
                "columns" : []
            }
            Example 8:
            Input: An invalid SQL query string
            Output:
            {
                "operation_type" : "",
                "databases" : "",
                "username" : "",
                "schema" : "",
                "tables" : [],
                "columns" : []
            }
            """
        )
        system_message_prompt = SystemMessagePromptTemplate.from_template(template,template_format="jinja2")

        # 待翻译文本由 Human 角色输入
        human_template = "{sql}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        # 使用 System 和 Human 角色的提示模板构造 ChatPromptTemplate
        chat_prompt_template = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        # 为了翻译结果的稳定性，将 temperature 设置为 0
        chat = ChatOpenAI(model_name=model_name, temperature =0, verbose=verbose)

        self.chain = LLMChain(llm=chat, prompt=chat_prompt_template, verbose=verbose)

    def run(self, sql: str) -> (str, bool):
        result = {}
        try:
            result = self.chain.run({
                "sql": sql
            })

        except Exception as e:
            LOG.error(f"An error occurred during translation: {e}")
            return "", False

        return result, True