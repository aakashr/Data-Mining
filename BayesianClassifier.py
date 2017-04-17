import glob
import re
import ast
import sys
import os
import datetime

def displayProgressBar(initialCount,finalCount):
    if (initialCount == 1):
        sys.stdout.write('0% ')
    if (initialCount % 5 == 0):
        sys.stdout.write('+')
    if initialCount == finalCount:
        sys.stdout.write(' 100%\n')
    sys.stdout.flush()
def calculateWordFrequencyinClass(folderPath):
    listOfFiles = glob.glob(folderPath+'/*.txt')
    progressCount = 0
    with open("stoplist.txt", "r") as f_stopList:
        stopListWords = f_stopList.read()
        stopListWords = set(stopListWords.split("\n"))
        f_stopList.close()
    wordFrequency = {}
    tempCount = 0
    className = folderPath.split("/")[2]
    sys.stdout.write('Generating Word Frequency Document for Class '+className+"\n")
    for file in listOfFiles:
        progressCount += 1
        percentProgress = round((progressCount/150)*100,2)
        with open(file, "rb") as f:
            articleText= f.read().decode('utf-8','ignore')
            f.close()
        currentArtcileWords = re.findall(r"[\w']+", articleText)
        for word in currentArtcileWords :
            word = word.lower()
            if word in stopListWords:
                continue
            if word in wordFrequency.copy().keys():
                wordFrequency[word] += 1
            else:
                wordFrequency[word] = 1
        tempCount += 1
        displayProgressBar(tempCount,150)
    return wordFrequency
def writeToFile(dataForFile,fileName):
    with open(fileName+'.txt','w') as writeFileHandle:
        writeFileHandle.write(dataForFile)
        writeFileHandle.close()
def mergeDictionaries():
    print ('Merging dictionaries...')
    arxivDictionary = {}
    jdmDictionary = {}
    plosDictionary = {}
    with open("arxivWordDictionary.txt","r") as arxivHandle:
        arxivDictionary = ast.literal_eval(arxivHandle.read())
        arxivHandle.close()
    with open("jdmWordDictionary.txt","r") as jdmHandle:
        jdmDictionary = ast.literal_eval(jdmHandle.read())
        jdmHandle.close()
    with open("plosWordDictionary.txt", "r") as plosHandle:
        plosDictionary = ast.literal_eval(plosHandle.read())
        plosHandle.close()
    for word in plosDictionary:
        if word in jdmDictionary.copy().keys():
           jdmDictionary[word] = jdmDictionary[word] + plosDictionary[word]
        else:
            jdmDictionary[word] = plosDictionary[word]
    for word in arxivDictionary:
        if word in jdmDictionary.copy().keys():
           jdmDictionary[word] = jdmDictionary[word] + arxivDictionary[word]
        else:
            jdmDictionary[word] = arxivDictionary[word]
    writeToFile(str(jdmDictionary),'finalWordDictionary')
def countTotalWordsInAClass(className):
    with open(className+"WordDictionary.txt","r") as fHandle:
        classDictionary = ast.literal_eval(fHandle.read())
        fHandle.close()
    wordCount = 0
    for key in classDictionary.copy().keys():
        wordCount = wordCount + classDictionary[key]
    return (wordCount)
def generateProbOfClassGiveAWord(className):
    with open("probabilityOfWords.txt","r") as probOfWordsFileHandle:
        probabilityOfWords = ast.literal_eval(probOfWordsFileHandle.read())
        probOfWordsFileHandle.close()
    with open("arxivProbabilityOfWordGivenAClass.txt","r") as arxivFileHandle:
        arxivProbabilityOfWordsGivenAClass= ast.literal_eval(arxivFileHandle.read())
        arxivFileHandle.close()
    with open("jdmProbabilityOfWordGivenAClass.txt","r") as jdmFileHandle:
        jdmProbabilityOfWordsGivenAClass= ast.literal_eval(jdmFileHandle.read())
        jdmFileHandle.close()
    with open("plosProbabilityOfWordGivenAClass.txt","r") as plosFileHandle:
        plosProbabilityOfWordsGivenAClass= ast.literal_eval(plosFileHandle.read())
        plosFileHandle.close()
    with open("finalWordDictionary.txt","r") as finalDictFileHandle:
        finalWordDict= ast.literal_eval(finalDictFileHandle.read())
        finalDictFileHandle.close()
    porbabilityOfClassGivenAWord = {}
    if className == 'arxiv':
        classProbabilityOfWordsGivenClass = arxivProbabilityOfWordsGivenAClass
    elif className == 'jdm':
        classProbabilityOfWordsGivenClass = jdmProbabilityOfWordsGivenAClass
    else:
        classProbabilityOfWordsGivenClass = plosProbabilityOfWordsGivenAClass
    for word in finalWordDict:
        if word not in classProbabilityOfWordsGivenClass.keys():
            porbabilityOfClassGivenAWord[word] = 0
        else:
            porbabilityOfClassGivenAWord[word] = classProbabilityOfWordsGivenClass[word]*(1/3)/probabilityOfWords[word]
    writeToFile(str(porbabilityOfClassGivenAWord),className+'ProbabilityOfClassGivenAWord')
def probabilityOfClassForAnArticle(folderPath):
    listOfFiles = glob.glob(folderPath+'/*.txt')
    className = folderPath.split("/")[2]
    with open("arxivProbabilityOfClassGivenAWord.txt","r") as arxivFileHandle:
        arxivProbClassGivenWord = ast.literal_eval(arxivFileHandle.read())
        arxivFileHandle.close()
    with open("jdmProbabilityOfClassGivenAWord.txt","r") as jdmFileHandle:
        jdmProbClassGivenWord = ast.literal_eval(jdmFileHandle.read())
        jdmFileHandle.close()
    with open("plosProbabilityOfClassGivenAWord.txt","r") as plosFileHandle:
        plosProbClassGivenWord = ast.literal_eval(plosFileHandle.read())
        plosFileHandle.close()
    with open("probabilityOfWords.txt","r") as finalProbFileHandle:
        probOfWords = ast.literal_eval(finalProbFileHandle.read())
        finalProbFileHandle.close()
    correctClassIdentifiedCount = 0
    classOutput = ""
    for file in listOfFiles:
        with open(file,"rb") as fileHandle:
            articleText = fileHandle.read().decode('utf-8','ignore')
            articleWords = re.findall(r"[\w']+",articleText)
            fileHandle.close()
        sumOfARXIVProbabilities = 0
        sumOfJDMProbabilities = 0
        sumOfPLOSProbabilities = 0

        for word in articleWords:
            if (word not in probOfWords):
                sumOfARXIVProbabilities += 0
                sumOfJDMProbabilities += 0
                sumOfPLOSProbabilities += 0
            elif (word not in arxivProbClassGivenWord.keys()):
                sumOfARXIVProbabilities += 0
            elif (word not in jdmProbClassGivenWord.keys()):
                sumOfJDMProbabilities += 0
            elif  (word not in plosProbClassGivenWord.keys()):
                sumOfPLOSProbabilities += 0
            else:
                sumOfARXIVProbabilities += arxivProbClassGivenWord[word]*probOfWords[word]
                sumOfJDMProbabilities += jdmProbClassGivenWord[word]*probOfWords[word]
                sumOfPLOSProbabilities += plosProbClassGivenWord[word]*probOfWords[word]
        classDicitonary = {sumOfARXIVProbabilities:'arxiv',
                       sumOfJDMProbabilities:'jdm',
                       sumOfPLOSProbabilities:'plos'}
        classOutput += "-"*24 + '\nActual Class: '+className.upper()+"\nClassified Class: "+str(classDicitonary[max(classDicitonary.copy().keys())]).upper() + "\n" + "-"*24+"\n"

        if (classDicitonary[max(classDicitonary.copy().keys())] == className):
            correctClassIdentifiedCount += 1
    writeToFile(classOutput,className+"OutputFile")
    accuracyPercentage = round((correctClassIdentifiedCount/150)*100,2)
    print (className+' Accuracy = '+str(accuracyPercentage))
def generateProbabilityOfWords(totalWordCount):
    probabilityOfWords = {}
    with open("finalWordDictionary.txt","r") as finalDictHandle:
        finalWordDicitionary = ast.literal_eval(finalDictHandle.read())
        finalDictHandle.close()
    for word in finalWordDicitionary.copy().keys():
        probabilityOfWords[word] = finalWordDicitionary[word]/totalWordCount
    writeToFile(str(probabilityOfWords),'probabilityOfWords')
def generateProbabilityOfWordGivenAClass(className):
    probailityOfWordGivenAClass = {}
    with open(className+'WordDictionary.txt',"r") as classFileHandle:
        classWordDictionary = ast.literal_eval(classFileHandle.read())
        classFileHandle.close()
    totalWordsInClass = countTotalWordsInAClass(className)
    for word in classWordDictionary.copy().keys():
        probailityOfWordGivenAClass[word] = classWordDictionary[word]/totalWordsInClass
    writeToFile(str(probailityOfWordGivenAClass),className+'ProbabilityOfWordGivenAClass')
def removeUnwantedFiles():
    os.remove('arxivWordDictionary.txt')
    os.remove('jdmWordDictionary.txt')
    os.remove('plosWordDictionary.txt')
    os.remove('finalWordDictionary.txt')
    os.remove('probabilityOfWords.txt')
    os.remove('arxivProbabilityOfWordGivenAClass.txt')
    os.remove('plosProbabilityOfWordGivenAClass.txt')
    os.remove('jdmProbabilityOfWordGivenAClass.txt')
    os.remove('arxivProbabilityOfClassGivenAWord.txt')
    os.remove('jdmProbabilityOfClassGivenAWord.txt')
    os.remove('plosProbabilityOfClassGivenAWord.txt')

def main():
    startTime = datetime.datetime.now()
    arxivWordDictionary = calculateWordFrequencyinClass('articles/Training/arxiv/')
    writeToFile(str(arxivWordDictionary), 'arxivWordDictionary')
    jdmWordDictionary = calculateWordFrequencyinClass('articles/Training/jdm/')
    writeToFile(str(jdmWordDictionary), 'jdmWordDictionary')
    plosWordDictionary = calculateWordFrequencyinClass('articles/Training/plos/')
    writeToFile(str(plosWordDictionary), 'plosWordDictionary')
    mergeDictionaries()
    arxivWordCount = countTotalWordsInAClass('arxiv')
    jdmWordCount = countTotalWordsInAClass('jdm')
    plosWordCount = countTotalWordsInAClass('plos')
    totalWordCount = arxivWordCount + jdmWordCount + plosWordCount
    generateProbabilityOfWords(totalWordCount)
    generateProbabilityOfWordGivenAClass('arxiv')
    generateProbabilityOfWordGivenAClass('jdm')
    generateProbabilityOfWordGivenAClass('plos')
    generateProbOfClassGiveAWord('arxiv')
    generateProbOfClassGiveAWord('plos')
    generateProbOfClassGiveAWord('jdm')
    probabilityOfClassForAnArticle('articles/Testing/arxiv')
    probabilityOfClassForAnArticle('articles/Testing/jdm')
    probabilityOfClassForAnArticle('articles/Testing/plos')
    removeUnwantedFiles()
    endTime = datetime.datetime.now()
    print ('Time Difference '+str(endTime-startTime))
if __name__ == '__main__':
    main()