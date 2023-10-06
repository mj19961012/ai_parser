class DBObject:
    def __init__(self, query):
        self.query = query.strip()
        self.operation_type = None
        self.databases = []
        self.schemas = []
        self.tables = []
        self.columns = []
