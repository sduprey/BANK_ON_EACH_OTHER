import numpy as np

class Registree:
    def __init__(self, fullName, age, creditCard, history):
        self.fullName = fullName
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
             self.creditCard = Registree.drawRandomCreditCard(self.continuous_rating)
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
        if self.getRating() >= 150 :
            return 2000
        elif self.getRating() >= 100:
            return 1000
        else :
            return 500

    def getRating(self):
        #@todo : propagate warranter rating
        return self.continuous_rating+self.age+self.number_neighbours*10

    @staticmethod
    def drawRandomAge():
        s = np.random.uniform(18, 60, 1)
        return s

    @staticmethod
    def drawRandomCreditCard(continuous_rating):
        if continuous_rating <= 25 :
            return "Debit"
        elif continuous_rating <= 45:
            return "Credit"
        else :
            return "Credit Gold"