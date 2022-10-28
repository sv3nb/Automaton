# Create object to represent our database

database = "technique_db.json"

class TechniqueDatabase(object):
    def __init__(self, name):
        self._db = {}
        if name is not None:
            self.load(name)

    def __iter__(self):
        return iter(self._db)

    def load(self, name):
        with open(name) as tech_db:
            self._db = json.load(tech_db)

    def find(self, id):
        return next(filter(lambda x: x["id"] == id, self), {})

    # following functions allow us to retrieve properties from the DB
    def get_name(self, id):
        return self.find(id).get("name")

    def get_traffic(self, id):
        return self.find(id).get("traffic")

    def get_proto(self, id):
        return self.find(id).get("protocols")

    def get_desc(self, id):
        return self.find(id).get("description")

    def get_mitigation(self, id):
        return self.find(id).get("mitigation")
    
    # instantiate the TechniqueDatabase object
    DB = TechniqueDatabase(database)
    
    # You can pass the technique id's into the class methods to retrieve data from the database
    id = "T1548"
    name = DB.get_name(id)
    traffic = DB.get_traffic(id)
    protocol = DB.get_proto(id)
