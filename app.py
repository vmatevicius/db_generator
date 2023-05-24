from tqdm import tqdm
from typing import Dict, List, Optional, Union, Any
from pymongo import MongoClient
import utilities as utils

class DbGenerator:
    def __init__(
        self, host: str, port: int, db_name: str, collection_name: str
    ) -> None:
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def create_document(self, document: Dict[str, Any]) -> str:
        result = self.collection.insert_one(document)
        return str(result.inserted_id)

    @classmethod
    def create_db(cls, db_name: str, collection_name: str) -> "DbGenerator":
        return cls(
            host="localhost",
            port=27017,
            db_name=db_name,
            collection_name=collection_name,
        )

    @staticmethod
    def launch_generator() -> None:
        db_name = utils.get_database_name()
        collection_name = utils.get_collection_name()
        db = DbGenerator.create_db(db_name, collection_name)
        template = utils.create_empty_document()
        number_of_documents = utils.get_number_of_docs_to_create()
        pbar = tqdm(total=number_of_documents)
        while number_of_documents != 0:
            document = {}
            for name, value in template.items():
                if value[0] == "string":
                    document[name] = utils.generate_value(type=value[0])
                elif value[0] == "list":
                    loops = 0
                    values = []
                    if value[1] == "string":
                        while value[2] != loops:
                            values.append(utils.generate_value(type=value[1]))
                            loops += 1
                        document[name] = values
                    if value[1] in ["int", "float"]:
                        while value[4] != loops:
                            values.append(
                                utils.generate_value(
                                    type=value[1], min=value[2], max=value[3]
                                )
                            )
                            loops += 1
                        document[name] = values
                elif value[0] == "date":
                    document[name] = utils.generate_value(type=value[0])
                else:
                    document[name] = utils.generate_value(
                        type=value[0], min=value[1], max=value[2]
                    )
            db.create_document(document)
            number_of_documents -= 1
            pbar.update(1)
        pbar.close()

if __name__ == "__main__":
    DbGenerator.launch_generator()