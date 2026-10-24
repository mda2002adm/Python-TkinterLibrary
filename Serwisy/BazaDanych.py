import json
import os
from Serwisy.Dekoratory import wykonywanie_operacji
from models import Movie, Book, Series


class Database:
    @staticmethod
    def get_file_path():
        return "Serwisy/library_storage.json"

    @staticmethod
    @wykonywanie_operacji
    def save_to_file(manager):
        data = {
            "items": [item.to_dict() for item in manager.items],
            "studios": list(manager.studios),
            "authors": list(manager.authors)
        }
        with open(Database.get_file_path(), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    @wykonywanie_operacji
    def load_from_file(manager):
        path = Database.get_file_path()
        if not os.path.exists(path):
            return

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        manager.studios = set(data.get("studios", manager.studios))
        manager.authors = set(data.get("authors", manager.authors))

        for d in data.get("items", []):
            t = d["type"]
            if t == "Film":
                manager.add_item(
                    Movie(d["name"], d["year"], d["studio"], d["duration"], d["genre"], d["status"], d["image_path"]))
            elif t == "Książka":
                manager.add_item(Book(d["name"], d["author"], d["pages"], d["genre"], d["status"], d["image_path"]))
            elif t == "Serial":
                manager.add_item(
                    Series(d["name"], d["year"], d["studio"], d["episodes"], d["genre"], d["status"], d["image_path"]))