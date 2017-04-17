# Python Version Used 3.5
# Naive-Bayes-Classifier
This projects attempts to demostrate a simple Naive Bayes Classifier using Multinomial method. In this project we take ".txt" files as Input and split 50% of the data as Training and the rest 50% of it as Testing. This step of seperating files has already been done so we don't have to worry about it. Follwing are the list of files included in the Project and their respective descriptions.

## 1. BayesianClassifier.py
This is the main Python file which you would need to run from your CMD or Terminal or any other IDE which supports Python. The command to execute this from CMD or Terminal is :
**python BayesianClassifier.py**
The code takes approximately 1 Min 30 Sec to execute, howerver the runtimes may differ depending on your Machine. During the run process we read 900 files, out of which 450 of them we treat as Training Data and the rest as Testing Data.

**NOTE: Running this code on an older version of Python i.e 2.7 may lead to errors, "Divide by zero" to be more specific, as Python 2.7 coverts really small decimal values like 1/200000 to 0, which is very weird as it may lead to bigger computational mistakes**

## 2. articles.zip
This files needs to be unzipped for the code to run. It contains the Training and Testing data. Once you unizp this file you would notice that it has 3 Folders, which for some reason have names which may look like typed by playing a piano on the keyboard, this is not true, well to some extent might be, but them have some significance and it is as follows.

* PLoS Computational Biology (PLOS)
* The machine learning repository on arXiv (ARXIV)
* The psychology journal Judgment and Decision Making (JDM)

## 3. stoplist.txt
This file contains all the words which are of little significance when predicting the actual class of an Article. Some examples of such  wors are "a", "an", "the", "but" etc. These words are removed while constructing a vocabulary for a particular class of articles.

## 4. About-BayesianClassifier.pdf
This document explains in details what we are trying to achieve and what every single function is doing in the ".py" file. Some of the functions may not have been explained in this file as they don't have a significant effect on the predictions.

## 5. arxivOutputFile.txt, jdmOutputFile.txt & plosOutputFile.txt
This file consists the actual predictions of the articles. When the code computes its prediction on the testing data. It dumps its prediction in these files. For example all the predictions of "arxiv" folder would be in "arxivOutputFile.txt" an so forth.
