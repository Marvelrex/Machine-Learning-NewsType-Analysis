# -------------------------------------------------------
# Assignment 2
# Written by Jialin Yang ID:40069006
# For COMP 472 Section KX – Summer 2020
# --------------------------------------------------------
import numpy as np
import pandas as pd


import matplotlib.pyplot as plt
import math
import sys

hackernews = pd.read_csv('Dataset\Dhns_2018_2019.csv')
trainningset = hackernews[(hackernews['Created At'] >= '2018-01-01') & (hackernews['Created At'] < '2019-01-01')]
testingset = hackernews[hackernews['Created At'] >= '2019-01-01']
Story = trainningset[trainningset['Post Type'] == 'story']
Ask = trainningset[trainningset['Post Type'] == 'ask_hn']
Show = trainningset[trainningset['Post Type'] == 'show_hn']
Poll = trainningset[trainningset['Post Type'] == 'poll']


def no_punc(str):
    punctuation = ['(', ')', '?', ':', ';', ',', '.', '!', '"', "'", '“', '‘', '”', '’']
    nopunc = ''
    for a in str:
        if a not in punctuation:
            nopunc = nopunc + a
    return nopunc


# Put all title to words and store them in a 2-d list
vocabularys = []
fakeset = []

for title in trainningset['Title']:
    title = title.lower()
    voc1 = []
    for voc in title.split():
        fakeset.append(no_punc(voc))
        voc1.append(no_punc(voc))
    vocabularys.append(voc1)
count = 0
wordcount = {}

for row in vocabularys:
    for column in row:
        if column not in wordcount:
            wordcount[column] = 1
        else:
            wordcount[column] += 1

wordcountsorted = wordcount.copy()
wordcountsorted = sorted(wordcountsorted.items(), key=lambda kv: kv[1], reverse=True)

# dicttrain record single word and its type as key and frequency as value
dicttrain = {}
for ptype in trainningset['Post Type']:
    if count < len(vocabularys):
        for b in vocabularys[count]:
            words = (b, ptype)
            if words in dicttrain:
                dicttrain[words] += 1
            else:
                dicttrain[words] = 1
    count += 1
trainkeys = list(dicttrain.keys())

storyfre = 0

askfre = 0

showfre = 0

pollfre = 0

for key in trainkeys:
    if key[1] == 'story':
        storyfre += dicttrain[key]
    elif key[1] == 'ask_hn':
        askfre += dicttrain[key]
    elif key[1] == 'show_hn':
        showfre += dicttrain[key]
    else:
        pollfre += dicttrain[key]
vocset = sorted(set(fakeset))




print("Choose the eyperiment: A: Base B:Exp1 C:Exp2 D:Exp3 ")
epnumb = input()

# User input to choose the experiments or basement test

if epnumb.upper() == "A" or epnumb.upper() == "B" or epnumb.upper() == "C" :
    removed = open("Dataset/remove_word.txt", "w", encoding="utf-8")
    for tt in vocset:
        if '#' in tt:
            removed.write(tt + "\n")
            vocset.remove(tt)
        if tt == "-" or tt == "—" or tt == "":
            removed.write(tt + "\n")
            vocset.remove(tt)

if epnumb.upper() == "A":
    modeladdress = "Dataset/model-2018.txt"
    txtvocaddress = "Dataset/vocabulary.txt"
    resultsaddress = "Dataset/baseline-result.txt"
elif epnumb.upper() == "B":
    modeladdress = "Experiments/stopword-model.txt.txt"
    txtvocaddress = "Experiments/stop-vocabulary.txt"
    resultsaddress = "Experiments/stopword-result.txt"
    Stopword = open('Dataset\stopwords.txt', 'r')
    stpwords = Stopword.read().splitlines()
    copyset = vocset.copy()
    for stp in stpwords:
        if stp in copyset:
            vocset.remove(stp)



elif epnumb.upper() == "C":
    modeladdress = "Experiments/wordlength-model.txt"
    txtvocaddress = "Experiments/wordlength-vocabulary.txt"
    resultsaddress = "Experiments/wordlength-result.txt"
    copyset = vocset.copy()
    for limitvoc in copyset:
        if len(limitvoc) >= 9 or len(limitvoc) <= 2:
            vocset.remove(limitvoc)

elif epnumb.upper() == "D":
    modeladdress = "Experiments/EP3-model.txt"
    txtvocaddress = "Experiments/EP3-vocabulary.txt"
    resultsaddress = "Experiments/EP3-result.txt"

model = open(modeladdress, "a", encoding='utf-8')
txtvoc = open(txtvocaddress, "a", encoding='utf-8')
results = open(resultsaddress, "a", encoding="utf-8")
for zz in vocset:
    txtvoc.write(zz + "\n")


# Calculate the probability for P(each word | post type)
def calculate(inputvocset):
    dictkeys = dicttrain.keys()
    counter = 0
    dictprobs = {}
    if epnumb.upper() == "D":
        model.write("_________________________________________________________________\n")
    for setkey in inputvocset:
        if (setkey, 'story') in dictkeys:
            storytimes = dicttrain[(setkey, 'story')]
        else:
            storytimes = 0
        if (setkey, 'ask_hn') in dictkeys:
            asktimes = dicttrain[(setkey, 'ask_hn')]
        else:
            asktimes = 0
        if (setkey, 'show_hn') in dictkeys:
            showtimes = dicttrain[(setkey, 'show_hn')]
        else:
            showtimes = 0
        if (setkey, 'poll') in dictkeys:
            polltimes = dicttrain[(setkey, 'poll')]
        else:
            polltimes = 0

        Pstory = round((storytimes + 0.5) / (storyfre + len(vocset) * 0.5), 5)
        Pask = round((asktimes + 0.5) / (askfre + len(vocset) * 0.5), 5)
        Pshow = round((showtimes + 0.5) / (showfre + len(vocset) * 0.5), 5)
        Ppoll = round((polltimes + 0.5) / (pollfre + len(vocset) * 0.5), 5)
        dictprobs[(setkey)] = (Pstory, Pask, Pshow, Ppoll)
        line = (str(counter) + "  " + setkey + "  " + str(storytimes) + "  " + str(Pstory) + "  " + str(
            asktimes) + "  " + str(Pask) + "  " + str(showtimes) + "  " + str(Pshow) + "  " + str(polltimes) + str(
            Ppoll) + "\n")
        model.write(line)
        counter += 1
    return dictprobs


# Calculate the probability
if epnumb.upper() == 'A' or epnumb.upper() == 'B' or epnumb.upper() == 'C':
    dictprob = calculate(vocset)

# Prepare for the filter with different conditions
if epnumb.upper() == 'D':
    freset = vocset.copy()
    freset1 = vocset.copy()
    freset2 = vocset.copy()
    freset3 = vocset.copy()
    freset4 = vocset.copy()
    for r in wordcount.keys():
        if wordcount[r] == 1:
            freset.remove(r)
        if wordcount[r] <= 5:
            freset1.remove(r)
        if wordcount[r] <= 10:
            freset2.remove(r)
        if wordcount[r] <= 15:
            freset3.remove(r)
        if wordcount[r] <= 20:
            freset4.remove(r)
    dictprobfre1 = calculate(freset)
    dictprobfre5 = calculate(freset1)
    dictprobfre10 = calculate(freset2)
    dictprobfre15 = calculate(freset3)
    dictprobfre20 = calculate(freset4)

    percset = vocset.copy()
    percset1 = vocset.copy()
    percset2 = vocset.copy()
    percset3 = vocset.copy()
    percset4 = vocset.copy()
    for index in range(int(len(wordcountsorted) * 0.25)):
        if index <= int(len(wordcountsorted) * 0.05):
            percset.remove(wordcountsorted[index][0])
        if index <= int(len(wordcountsorted) * 0.1):
            percset1.remove(wordcountsorted[index][0])
        if index <= int(len(wordcountsorted) * 0.15):
            percset2.remove(wordcountsorted[index][0])
        if index <= int(len(wordcountsorted) * 0.20):
            percset3.remove(wordcountsorted[index][0])
        percset4.remove(wordcountsorted[index][0])

    dictproperc5 = calculate(percset)
    dictproperc10 = calculate(percset1)
    dictproperc15 = calculate(percset2)
    dictproperc20 = calculate(percset3)
    dictproperc25 = calculate(percset4)

# test list 2-D list store title in words

testlist = []
faketestset = []
titlelist = []

# Clean the data for testing

for test in testingset['Title']:
    titlelist.append(test)
    test = test.lower()
    testvoc = []
    for testvoc1 in test.split():
        faketestset.append(no_punc(testvoc1))
        testvoc.append(no_punc(testvoc1))
    testlist.append(testvoc)

testset = sorted(set(faketestset))
Allscores = []


# Get the scores for each post type and return the accuracy

def scores(datanews, probabilty, inputvocset):
    scorelist = []
    for first in datanews:
        if len(Story) != 0:
            Storyscore = math.log((len(Story) / len(trainningset)), 2)
        else:
            Storyscore = 0
        if len(Ask) != 0:
            Askscore = math.log((len(Ask) / len(trainningset)), 2)
        else:
            Askscore = 0
        if len(Show) != 0:
            Showscore = math.log((len(Show) / len(trainningset)), 2)
        else:
            Showscore = 0
        if len(Poll) != 0:
            Pollscore = math.log((len(Poll) / len(trainningset)), 2)
        else:
            Pollscore = 0
        for second in first:
            if second in inputvocset:
                Storyscore += math.log(probabilty[second][0], 2)
                Askscore += math.log(probabilty[second][1], 2)
                Showscore += math.log(probabilty[second][2], 2)
                Pollscore += math.log(probabilty[second][3], 2)

        Storyscore = round(Storyscore, 5)
        Askscore = round(Askscore, 5)
        Showscore = round(Showscore, 5)
        Pollscore = round(Pollscore, 5)
        finalscore = max(Storyscore, Askscore, Storyscore, Pollscore)
        Allscores.append((Storyscore, Askscore, Showscore, Pollscore))
        if finalscore == Storyscore:
            scorelist.append("story")
        elif finalscore == Askscore:
            scorelist.append("ask_hn")
        elif finalscore == Showscore:
            scorelist.append("show_hn")
        else:
            scorelist.append("poll")
    correct = 0
    false = 0
    if epnumb.upper() == 'D':
        results.write("____________________________________________________________________________\n")
    for y in range(len(titlelist)):
        judge = (scorelist[y] == exactscorelist[y])
        if judge:
            correct += 1
        else:
            false += 1
        resultstr = str(y) + "  " + titlelist[y] + "  " + scorelist[y] + "  " + str(Allscores[y][0]) + "  " + str(
            Allscores[y][1]) + "  " + str(Allscores[y][2]) + "  " + str(Allscores[y][3]) + "  " + exactscorelist[
                        y] + "  " + str(judge) + "\n"
        results.write(resultstr)
    return correct / (correct + false)


# The post type need to be compared

exactscorelist = []
for qwe in testingset['Post Type']:
    exactscorelist.append(qwe)


def draw(x, y):
    plt.plot(x, y)

    plt.show()


# Test the results
if epnumb.upper() == 'A' or epnumb.upper() == 'B' or epnumb.upper() == 'C':
    print("Accuracy:",str(scores(testlist, dictprob, vocset)))


# Test the results and build diagram
if epnumb.upper() == 'D':
    y = [scores(testlist, dictprobfre1, freset), scores(testlist, dictprobfre5, freset1),
         scores(testlist, dictprobfre10, freset2), scores(testlist, dictprobfre15, freset3),
         scores(testlist, dictprobfre20, freset4)]

    x = [len(freset), len(freset1), len(freset2), len(freset3), len(freset4)]

    draw(x, y)

    y1 = [scores(testlist, dictproperc5, percset), scores(testlist, dictproperc10, percset1),
          scores(testlist, dictproperc15, percset2), scores(testlist, dictproperc20, percset3),
          scores(testlist, dictproperc25, percset4)]

    x1 = [len(percset), len(percset1), len(percset2), len(percset3), len(percset4)]

    draw(x1, y1)

print("Program Finished")
