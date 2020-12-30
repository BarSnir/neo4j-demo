from neo4j import GraphDatabase

class DemoExample:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def getResults(self, modelName):
        self.createReadSession()
        return self.session.read_transaction(self.getModelRelations, modelName)

    def createReadSession(self):
        self.session = self.driver.session()

    def getModelRelations(self, tx, modelName):
        entire_result = []
        results = tx.run("MATCH (primary:model)-[r:BELONG_TO_FAMILY]-(b)-[f:BELONG_TO_FAMILY]-(c) "
                        "WHERE primary.name=$name "
                        "return primary,r,b,f,c", name=modelName)
        for record in results:
          entire_result.append(record)
        return entire_result


def getModelRelations():
    examiner = DemoExample("bolt://localhost:7687", "neo4j", "BarSnir1991")
    results = examiner.getResults("Picanto")
    for record in results:
        print(record, "\n") 
    examiner.close()

getModelRelations()