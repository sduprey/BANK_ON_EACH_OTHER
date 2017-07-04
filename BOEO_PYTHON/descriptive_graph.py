import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np


from Registree import Registree
from collections import defaultdict
from collections import Counter

import random
from random import randrange
from datetime import timedelta
from dateutil.relativedelta import relativedelta

import datetime as dt

import plotly
from plotly.graph_objs import Scatter, Layout

def posSum(aList):
    s = 0
    for x in aList:
        if x > 0:
            s += x
    return s

def ngSum(aList):
    s = 0
    for x in aList:
        if x < 0:
            s += x
    return s

def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

my_seed = 11181928
random.seed(my_seed)
np.random.seed(my_seed)

#show = True
show = False

df = pd.read_csv('../input/bsk.csv')

print(df.shape)

print(df.head())

G=nx.Graph()

# # adding just one node:
# G.add_node("a")
# # a list of nodes:
# G.add_nodes_from(["b","c"])

def notRegisteredYet():
     return None

properties = defaultdict(notRegisteredYet)
ratings = {}
neighbours_dictionary = defaultdict(notRegisteredYet)

for index, row in df.iterrows():
    print("affecting statistical properties")
    warranter = properties[row["warranter"]]
    if warranter is None:
        warranter = Registree(fullName=row["warranter"], age = None, creditCard = None, history = None)
        properties[row["warranter"]] = warranter

    warrantee = properties[row["warrantee"]]
    if warrantee is None:
        warrantee = Registree(fullName=row["warrantee"], age = None, creditCard = None, history = None)
        properties[row["warrantee"]] = warrantee

    G.add_nodes_from([row["warranter"],row["warrantee"]])
    G.add_edge(*row)
    first_node = neighbours_dictionary[row["warranter"]]
    second_node = neighbours_dictionary[row["warrantee"]]

    ############# beware there might be duplicates among the list
    if first_node is None :
        neighbours_dictionary[row["warranter"]] = []
    neighbours_dictionary[row["warranter"]].append(row["warrantee"])

    if second_node is None :
        neighbours_dictionary[row["warrantee"]] = []
    neighbours_dictionary[row["warrantee"]].append(row["warranter"])

print("Nodes of graph: ")
print(G.nodes())
print(len(G.nodes()))
print(len(properties))

print("Filling up the neighbours structure")
for my_node in G.nodes():
    ############# we use a set to remove the duplicates
    node_neighbours = set(neighbours_dictionary[my_node])
    properties[my_node].setNeighbours(node_neighbours)

print("computing the adjacency matrix")
#adjG = nx.adjacency_matrix(G, nodelist=None, weight='weight')
#adjG = nx.adjacency_matrix(G,weight='weight')
adjG = nx.adjacency_matrix(G)

denseAdjG = np.array(adjG.todense())
print(denseAdjG)
print("test if the matrix is symmetrical")
print((denseAdjG.transpose() == denseAdjG).all())
np.save("../input/dense_adjacency_matrix.npy", denseAdjG)



print("Initial page rank")
print(nx.pagerank(G, alpha=0.86))


print("Adding weights to the edges")
for my_node in G.nodes():
    ############# we use a set to remove the duplicates
    node_neighbours = set(neighbours_dictionary[my_node])
    for my_neighbour in node_neighbours :
        G[my_node][my_neighbour]['weight'] = properties[my_node].getIsolatedRating()

print("New page rank")
ratingsNeighbourgsAverage = nx.pagerank(G, alpha=0.86)
print(ratingsNeighbourgsAverage)


for key, value in ratingsNeighbourgsAverage.iteritems():
    rateToSet = int(value[0]*1000)
    properties[key].setRating(rateToSet)
    ratings[key] = rateToSet


print(G.is_directed())

print("Edges of graph: ")
print(G.edges())

ratingsVector = []
borrowableAmountVector = []

agesVector = []
creditcardVector = []
nodes_label = {}
nodes_label_str = []

index = 0
for node in G.nodes():
    print(node)
    print(int(ratings[node]))
    print(type(node))
    ratingsVector.append(int(ratings[node]))
    agesVector.append(properties[node].age[0])
    creditcardVector.append(properties[node].creditCard)
    borrowableAmountVector.append(properties[node].getBorrowableAmount())
    nodes_label[node]= node
    nodes_label_str.append(node)
    index=index+1
    if node == properties[node].fullName:
        print("ok")
    else:
        print("trouble")

#nodes_size = [int(ratings(node)) for node in G.nodes()]
print(len(ratingsVector))
print(len(nodes_label))

if show :
    print("Platform registree rating distribution")
    fig = plt.figure()
    fig.suptitle('Platform registree rating distribution', fontsize=14, fontweight='bold')

    n, bins, patches = plt.hist(ratingsVector, 10, normed=1, facecolor='green', alpha=0.75)

    print("Platform registree age distribution")
    fig = plt.figure()
    fig.suptitle('Platform registree age distribution', fontsize=14, fontweight='bold')

    n, bins, patches = plt.hist(agesVector, 10, normed=1, facecolor='green', alpha=0.75)

    print("Platform registree credit card distribution")
    # n, bins, patches = plt.hist(creditcardVector, 10, normed=1, facecolor='green', alpha=0.75)
    labels, values = zip(*Counter(creditcardVector).items())
    indexes = np.arange(len(labels))
    width = 1
    fig = plt.figure()
    fig.suptitle('Platform registree credit card distribution', fontsize=14, fontweight='bold')

    plt.bar(indexes, values, width)
    plt.xticks(indexes + width * 0.5-0.5, labels)
    plt.show()
############## we randomly draw 70% of our population to borrow
############## Loans are granted randomly
############## The amount one can borrow will be limited by its rating
n, p = 1, .2 # number of trials, probability of each trial
borrowerSVector = np.random.binomial(n, p, len(ratingsVector))
print("Borrower amount among registrees")
print(borrowerSVector.sum()*1.0/borrowerSVector.shape[0])

if show :
    # n, bins, patches = plt.hist(creditcardVector, 10, normed=1, facecolor='green', alpha=0.75)
    labels, values = zip(*Counter(borrowerSVector).items())
    labels = ("Not borrower", "Borrower")
    indexes = np.arange(len(labels))
    width = 1
    fig = plt.figure()
    fig.suptitle('Platform registree borrower distribution', fontsize=14, fontweight='bold')

    plt.bar(indexes, values, width)
    plt.xticks(indexes + width * 0.5 - 0.5, labels)
    plt.show()


borrowedInitialAmount = borrowerSVector * borrowableAmountVector
display_limit = 20
print(borrowedInitialAmount[:display_limit])
print(borrowerSVector[:display_limit])
print(ratingsVector[:display_limit])

if show :
    # n, bins, patches = plt.hist(creditcardVector, 10, normed=1, facecolor='green', alpha=0.75)
    labels, values = zip(*Counter(borrowedInitialAmount).items())

    indexes = np.arange(len(labels))
    width = 1
    fig = plt.figure()
    fig.suptitle('Platform registree borrowed amount distribution', fontsize=14, fontweight='bold')

    plt.bar(indexes, values, width)
    plt.xticks(indexes + width * 0.5 - 0.5, labels)
    plt.show()
    #plt.savefig("simple_path.png") # save as png

pos=nx.spring_layout(G)
nx.set_node_attributes(G, 'pos', pos)

#### plotting the graph
if show :
    fig = plt.figure()
    fig.suptitle('Platform registree graph visualization', fontsize=14, fontweight='bold')
    nx.draw(G, node_size=ratingsVector, labels=nodes_label, node_color=borrowerSVector, with_labels=True)
    plt.show()

    plt.clf()
    nx.draw(G, node_size=ratingsVector, labels=nodes_label, node_color=borrowerSVector, with_labels=True)
    plt.savefig("../input/graph_without_defaulting_node.png")

    # nx.draw_random(G, node_size=ratingsVector, labels=nodes_label, node_color=borrowerSVector, with_labels=True)
    # plt.show()
    # nx.draw_circular(G)
    # plt.show()
    # nx.draw_spectral(G)
    # plt.show()
    # nx.draw_graphviz(G)
    # plt.show()
    # nx.draw(G)
    # plt.show()
    # plt.savefig("simple_path.png") # save as png



print("Randomly assigning initial dates")

d1 = dt.datetime.strptime("01/01/2016", "%d/%m/%Y")
d2 = dt.datetime.strptime("01/01/2017", "%d/%m/%Y")
d3 = dt.datetime.strptime("01/01/2020", "%d/%m/%Y")
d4 = dt.datetime.strptime("01/01/2018", "%d/%m/%Y")

# d1 = dt.strptime('01/01/2016 0:00 PM', '%mm/%dd/%YYYY %I:%M %p')
# d2 = dt.strptime('01/01/2017 0:00 AM', '%mm/%dd/%YYYY %I:%M %p')

borrowedInitialDate = [random_date(d1, d2)  for x in borrowerSVector]
defaultingDate = [random_date(d2, d4)  for x in borrowerSVector]

#borrowedInitialAmount = [round(np.random.uniform(0, myRate*10,1))  for myRate in ratingsVector]

###### the rate should be invertedly proportional to the rating
mu, sigma = 5, 0.5 # mean and standard deviation
borrowedInitialRates = np.random.normal(mu, sigma, len(borrowerSVector))

#nodesDataframe = pd.DataFrame.from_items([('names', nodes_label), ('borrower', borrowerSVector.tolist()) , ('rates',ratingsVector),('interests',borrowedInitialRates.tolist())])

nn = pd.Series(nodes_label_str)
#nn = pd.Series(nodes_label)
bb = pd.Series(borrowerSVector.tolist())
rr = pd.Series(ratingsVector)
rara = pd.Series(borrowedInitialRates.tolist())
dada = pd.Series(borrowedInitialDate)
dede = pd.Series(defaultingDate)
amount_authorized_per_rating = 10
amam = pd.Series(borrowedInitialAmount)

my_dict = {'names' : nn,
           'borrower' : bb,
           'ratings' : rr,
           'rates' : rara,
           'dates' : dada,
           'defaultdates' : dede,
           'amount' : amam}

#nodesDataframe = pd.DataFrame(list(my_dict.iteritems()))
nodesDataframe = pd.DataFrame(my_dict)

#nodesDataframe[["names"]] = nn

print(nodesDataframe.shape)
print(nodesDataframe.head())
print(nodesDataframe.tail())

print("computing flows")

start = d1
stop = d3
def computePaymentFlows(start, stop, defaultRate = 0.02, reshuffle = False):
    if reshuffle:
        n, p = 1, .2  # number of trials, probability of each trial
        borrowerSVector = np.random.binomial(n, p, len(ratingsVector))
        print("Actual simulated borrower amount among registrees")
        print(borrowerSVector.sum() * 1.0 / borrowerSVector.shape[0])
        # we reshuffle the defaulting people and the defaulting dates
        nodesDataframe['defaultdates'] = [random_date(d2, d4) for x in range(nodesDataframe.shape(0))]
        nodesDataframe['borrower'] = pd.Series(borrowerSVector.tolist())

        defaultingVector = np.random.binomial(1, defaultRate, nodesDataframe.borrower.sum())
        print("Actual simulated default rate")
        print(defaultingVector.sum() / defaultingVector.shape[0])
        nodesDataframe['defaulting'] = 0
        nodesDataframe['defaulting'][nodesDataframe.borrower == 1] = defaultingVector

    print("updating nodes properties")
    for index, row in nodesDataframe.iterrows():
        name = row['names']
        defaultDate = row['defaultdates']
        defaultDate = dt.date(defaultDate.year, defaultDate.month, defaultDate.day)
        defaulting = row['defaulting']
        properties[name].setDefaulting(defaulting)
        properties[name].setDefaultDate(defaultDate)

    datesVector = []
    while start < stop:
        start = start + timedelta(days=1)  # increase day one by one
        datesVector.append(start)

    print("generating the flows matrix")
    flow_matrix = np.zeros((len(datesVector), len(nn)))
    flow_df = pd.DataFrame(data=flow_matrix, index=datesVector, columns=nn)
    print(flow_df.shape)
    print(flow_matrix)

    print("generating the flows operations")
    flow_operation_df = pd.DataFrame(columns=["date", "name", "amount"])
    mensuality_reimbursement = 50
    for index, row in nodesDataframe.iterrows():
        rate = row['rates']
        rating = row['ratings']
        defaulting = row['defaulting']
        initialDate = row['dates']
        initialDate = dt.date(initialDate.year, initialDate.month, initialDate.day)
        defaultDate = row['defaultdates']
        defaultDate = dt.date(defaultDate.year, defaultDate.month, defaultDate.day)

        stop = dt.date(stop.year, stop.month, stop.day)
        borrower = row['borrower']
        name = row['names']
        amount = row['amount']
        if amount > 0 :
            if amount >= 1000 :
                mensuality_reimbursement = 100
            else :
                mensuality_reimbursement = 50
            amount_to_reimburse = amount*(1+rate/100)
            flow_operation_df.loc[flow_operation_df.shape[0]] = [initialDate, name, -amount]
            total_reimbursement = 0
            loan_running = True
            while initialDate < stop and (total_reimbursement<amount_to_reimburse) and loan_running :
                if initialDate >= defaultDate:
                    if defaulting:
                        defaulting_names = []
                        notdefaulting_neighbours = []
                        defaulting_names.append(name)
                        print("checking the neighbourgs")
                        liable_neighbours = properties[name].getNeighbours()
                        print(liable_neighbours)
                        for neighbour in liable_neighbours :
                            neighbourDefaultDate = properties[neighbour].getDefaultDate()
                            neighbourDefaulting = properties[neighbour].getDefaulting()
                            if initialDate >= neighbourDefaultDate:
                                if neighbourDefaulting :
                                    defaulting_names.append(neighbour)
                                    print("a warranter is also defaulting "+neighbour)
                                else :
                                    notdefaulting_neighbours.append(neighbour)


                        defaulting_boolean = np.asarray([node in defaulting_names for node in nodes_label_str])
                        borrowerSVector[defaulting_boolean] = -1
                        notdefaulting_boolean = np.asarray([node in notdefaulting_neighbours for node in nodes_label_str])
                        oldneighbourvalues = borrowerSVector[notdefaulting_boolean]
                        #borrowerSVector[notdefaulting_boolean] = 2

                        print("displaying the defaulting node "+name)
                        plt.clf()
                        nx.draw(G, node_size=ratingsVector, labels=nodes_label, node_color=borrowerSVector, with_labels=True)
                        plt.savefig("../input/graph_with_"+name+"_defaulting_node.png")

                        borrowerSVector[defaulting_boolean] = 1
                        borrowerSVector[notdefaulting_boolean] = oldneighbourvalues
                        loan_running = False

                initialDate = initialDate + relativedelta(months = +1)  # increase day month by month
                if (total_reimbursement + mensuality_reimbursement > amount_to_reimburse):
                    last_reimbursement = amount_to_reimburse - total_reimbursement
                    total_reimbursement = total_reimbursement + last_reimbursement
                    flow_operation_df.loc[flow_operation_df.shape[0]] = [initialDate, name,last_reimbursement]
                else :
                    total_reimbursement = total_reimbursement + mensuality_reimbursement
                    flow_operation_df.loc[flow_operation_df.shape[0]] = [initialDate, name,mensuality_reimbursement]
            print("done with that node "+name)
    print("getting the flow matrix")
    print(flow_operation_df.shape)

    print("filling up with all names")
    for index, row in nodesDataframe.iterrows():
        initialDate = row['dates']
        initialDate = dt.date(initialDate.year, initialDate.month, initialDate.day)
        name = row['names']
        flow_operation_df.loc[flow_operation_df.shape[0]] = [initialDate, name, 0]

    print("filling up with all dates")
    for initialDate in datesVector :
        initialDate = dt.date(initialDate.year, initialDate.month, initialDate.day)
        flow_operation_df.loc[flow_operation_df.shape[0]] = [initialDate, name, 0]
    #daily_flow_asof_2017 <- dcast(daily_flow_asof_2017, dates ~ customer, value.var = "flows", fun.aggregate = sum)
    all_flow_operation = flow_operation_df.pivot_table(index=['date'], columns=['name'], aggfunc=sum)
    # print(len(flow_operation_df.date.dt.strftime('%dd/%mm/%yyyy').unique()))
    # print(len(flow_operation_df.date.unique()))
    # print(len(flow_operation_df.name.unique()))
    all_flow_operation.columns = all_flow_operation.columns.droplevel()

    print("filling not a number by 0")
    all_flow_operation = all_flow_operation.fillna(0)

    all_flow_operation["positiveFlows"] = all_flow_operation.apply(posSum, axis=1)
    all_flow_operation["positiveFlowsCumsum"] = all_flow_operation.positiveFlows.cumsum()


    all_flow_operation["negativeFlows"] = all_flow_operation.apply(ngSum, axis=1)
    all_flow_operation["negativeFlowsCumsum"] = all_flow_operation.negativeFlows.cumsum()

    return(all_flow_operation)

#############################
#############################
#############################
############################# Back to the main script

nb_simulation = 100
for my_simu in range(nb_simulation):
    all_flows_df = computePaymentFlows(start,stop,defaultRate = 0.05, reshuffle= True)
    print("testing the shape")
    print(all_flows_df.shape)
    print(all_flows_df.head())

    print(all_flows_df.head(50))

    writeToDisk = False
    if writeToDisk:
        print("writing flows to disk")
        all_flows_df.to_csv('../input/flows_matrix.csv')

    print("simulating defaults over time and default probability reassessment")
    print("displaying the negative flows")

    print("displaying the positive flows")
    print(all_flows_df.sum(numeric_only=True))

    plotly.offline.plot({
        "data": [Scatter(x=all_flows_df.index, y=all_flows_df.positiveFlowsCumsum),
                 Scatter(x=all_flows_df.index, y=all_flows_df.negativeFlowsCumsum)],
        "layout": Layout(title="Loan amortization")})

    print("done first plotting")








