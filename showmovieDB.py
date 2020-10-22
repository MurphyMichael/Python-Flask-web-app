class ShowMovieDatabase:
    #photo should be the last one but I'm not to sure how to add this into the database and the class
    def __init__(self, title, year, genre, description, _type):
        self.title = title
        self.yearReleased = year
        self.genre = genre
        self.description = description
        self._type = _type

    #set the title
    def setTitle(self, title):
        self.title = title

    #get the title    
    def getTitle(self, title):
        return self.title

    #set the year released
    def setYear(self, year):
        self.year = year
    
    #get the year released
    def getYear(self, year):
        return self.year

    #set the genre
    def setGenre(self, genre):
        self.genre = genre

    #get the genre
    def getGenre(self, genre):
        return self.genre

    #set the description
    def setDescription(self, description):
        self.description = description
    
    #get the description
    def getdescription(self, description):
        return self.description

    #set the tpye of media, ie movie or show
    def setType(self, _type):
        self._type = _type

    #get the type of media, ie movie or show
    def getType(self, _type):
        return self._type

    