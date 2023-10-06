import json

class SQLSplitter:
    def __init__(self):
        pass

    def split_sql(self, sql_scripts: str) -> str:
        """
        Split the input string into separate SQL statements.

        Parameters:
        - sql_scripts (str): A string containing multiple SQL statements, separated by semicolons.

        Returns:
        - str: A JSON string containing a list of separate SQL statements.
        """
        # Split the input string into separate SQL statements based on the semicolon.
        sql_statements = sql_scripts.split(';')

        # Remove any empty strings or whitespace-only strings from the list.
        sql_statements = [stmt.strip() for stmt in sql_statements if stmt.strip()]

        # Convert the list of SQL statements to a JSON string.
        return json.dumps(sql_statements)
