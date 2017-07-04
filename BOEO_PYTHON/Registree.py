import numpy as np

class Registree:
    def __init__(self, fullName, age, creditCard, history):
        self.fullName = fullName
        self.rating = 0
        self.neighbours = []
        ##@todo store negihbourgs properties
        self.number_neighbours = 0
        self.history = history
        self.defaulting = 0
        self.defaultdate = None
        if age is None :
             self.age = Registree.drawRandomAge()
        else:
            self.age = age
        if creditCard is None :
             self.continuous_rating = np.random.uniform(0, 50, 1)
             self.creditCard = Registree.drawRandomCreditCard(self.age, self.continuous_rating)
        else:
            self.creditCard = creditCard

    def setDefaulting(self,defaulting):
        self.defaulting = defaulting

    def setDefaultDate(self,defaultdate):
        self.defaultdate = defaultdate

    def getDefaulting(self):
        return self.defaulting

    def getDefaultDate(self):
        return self.defaultdate

    def setNeighbours(self,computedNeighbours):
        self.neighbours = computedNeighbours
        self.number_neighbours = len(computedNeighbours)

    def getNeighbours(self):
        return self.neighbours

    def getBorrowableAmount(self):
        if self.getRating() >= 50:
            return 2000
        elif self.getRating() >= 10:
            return 1000
        else :
            return 500

    def getIsolatedRating(self):
        #@todo : propagate warranter rating
        return self.continuous_rating+self.age

    def getSimpleRating(self):
        #@todo : propagate warranter rating
        return self.continuous_rating+self.age+self.number_neighbours*10

    def setRating(self,computedRate):
        self.rating = computedRate

    def getRating(self):
        return self.rating

    @staticmethod
    def drawRandomAge():
        s = np.random.uniform(18, 60, 1)
        return s

    @staticmethod
    def drawRandomCreditCard(age, continuous_rating):
        if age > 40 :
            if continuous_rating >= 30 :
                return "Credit Gold"
            else :
                return "Credit"
        else :
            if continuous_rating >= 50 :
                return "Credit Gold"
            else :
                return "Credit"

