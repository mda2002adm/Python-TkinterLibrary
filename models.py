import re
from abc import ABC, abstractmethod
from tkinter import messagebox


class MediaItem(ABC):#KLASA ABSTRAKTNA DLA WSZYSTKICH TYPÓW MEDIA

    def __init__(self, name, genre, status, image_path=""):
        self.name = name
        self.genre = genre
        self.status = status
        self.image_path = image_path

    @abstractmethod
    def to_dict(self):
        pass


class Movie(MediaItem): #KLASA DLA FILMÓW
    def __init__(self, name, year, studio, duration, genre, status, image_path=""):
        super().__init__(name, genre, status, image_path)
        self.year = year
        self.studio = studio
        self.duration = duration

    def to_dict(self):
        return {
            "type": "Film",
            "name": self.name,
            "year": self.year,
            "studio": self.studio,
            "duration": self.duration,
            "genre": self.genre,
            "status": self.status,
            "image_path": self.image_path
        }


class Book(MediaItem): #KLASA DLA KSIĄŻEK
    def __init__(self, name, author, pages, genre, status, image_path=""):
        super().__init__(name, genre, status, image_path)
        self.author = author
        self.pages = pages

    def to_dict(self):
        return {
            "type": "Książka",
            "name": self.name,
            "author": self.author,
            "pages": self.pages,
            "genre": self.genre,
            "status": self.status,
            "image_path": self.image_path
        }


class Series(MediaItem): #KLASA DLA SERIAŁÓW
    def __init__(self, name, year, studio, episodes, genre, status, image_path=""):
        super().__init__(name, genre, status, image_path)
        self.year = year
        self.studio = studio
        self.episodes = episodes

    def to_dict(self):
        return {
            "type": "Serial",
            "name": self.name,
            "year": self.year,
            "studio": self.studio,
            "episodes": self.episodes,
            "genre": self.genre,
            "status": self.status,
            "image_path": self.image_path
        }


class LibraryManager:

    def __init__(self):
        self.items = []
        self.studios = {"Universal", "Warner Bros", "Netflix", "HBO"}
        self.authors = {"Stephen King", "J.K. Rowling", "Andrzej Sapkowski"}

    def add_item(self, item):
        self.items.append(item)
        if isinstance(item, Book):
            self.authors.add(item.author)
        elif isinstance(item, (Movie, Series)):
            self.studios.add(item.studio)


    def get_filtered_items(self, media_type, status_filter, search_query):
        #Filter ComboBox
        base_list = [
            item for item in self.items
            if ((media_type == "Film" and isinstance(item, Movie)) or
                (media_type == "Książka" and isinstance(item, Book)) or
                (media_type == "Serial" and isinstance(item, Series)))
               and item.status == status_filter
        ]

        if not search_query:
            return base_list

        #Wyszukiwarka (Regex)
        try:
            p = re.compile(search_query, re.IGNORECASE)
            return [item for item in base_list if p.search(item.name)]
        except re.error:
            return []