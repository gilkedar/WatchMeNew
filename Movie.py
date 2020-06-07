
from Item import Item

class Movie(Item):

    def __init__(self,name):
        Item.__init__(self,name)
        self.rating = self.get_movie_rating()
