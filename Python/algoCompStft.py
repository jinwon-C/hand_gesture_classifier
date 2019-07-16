
# coding: utf-8

# In[1]:
# edit JW

from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn import svm
from sklearn import tree
from getSetData import Classifier_Accuracy
from getSetData import Classifier_Precision
from getSetData import Classifier_Recall
from getSetData import Classifier_F1score
from getSetData import Classifier_Allscore
from getSetData import Classifier_Confusionmatrix
from getSetData import plot_confusion_matrix
from getSetData import load_data
from getSetData import load_data_test
import itertools
import matplotlib.pyplot as plt
import numpy as np
import csv

import loadcsvData as ld
# In[2]:

#clf = svm.SVC(decision_function_shape='ovo')
#dirName = "../../Data_csv/Each/TrainLED/"
#dirName1 = "../../Data_csv/Each/TrainBULB/"
#dirName2 = "../../Data_csv/Raw/Set_test_1/"
#Kind=["salt","sugar","cream","flour","bean","corn","rice","potato"]
#Kind=["flour","bean","corn","rice","potato"]

dirName = "/home/cjw/data/wintest/win5000/"

#Kind = ["raw","left-right","updown","circle"]
#Kind=["raw","left-right","updown","circle","block","right-left","downup","triangle"]
Kind = ["nothing","left-right","up-down","circle","block","right-left","triangle","down-up"]

# In[3]:

#X,Y = load_data(dirName,Kind)
#X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)


# In[4]:

#X,Y = load_data(dirName2,Kind)
#testdirName = "../../Data_csv/Each/LED/"
#testdirName1 = "../../Data_csv/Each/BULB/"
#testdirName2 = "../../Data_csv/Raw/FrameAverage_test/"
#X_train,y_train = load_data(dirName2,Kind)
#X_test,y_test = load_data_test(testdirName2,"0405",Kind)

X_train, y_train, X_test, y_test = ld.load_data(dirName,Kind,0.8)
print(len(X_train[1]), len(X_train), len(y_train), len(X_test), len(y_test))

accuracy = [0,0,0,0,0]
recall = [0,0,0,0,0]
precision = [0,0,0,0,0]
f1_score = [0,0,0,0,0]


# In[5]:

for i in range(5):
    #X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
    clfDT = DecisionTreeClassifier(max_depth=4)
    accuracy[0]+=Classifier_Accuracy(clfDT,X_train,y_train,X_test,y_test)
    precision[0] += Classifier_Precision(clfDT,X_train,y_train,X_test,y_test)
    recall[0] += Classifier_Recall(clfDT,X_train,y_train,X_test,y_test)
    f1_score[0] += Classifier_F1score(clfDT,X_train,y_train,X_test,y_test)

    clfKNN = KNeighborsClassifier(n_neighbors=1,algorithm='auto')
    accuracy[1]+=Classifier_Accuracy(clfKNN,X_train,y_train,X_test,y_test)
    precision[1] += Classifier_Precision(clfKNN,X_train,y_train,X_test,y_test)
    recall[1] += Classifier_Recall(clfKNN,X_train,y_train,X_test,y_test)
    f1_score[1] += Classifier_F1score(clfKNN,X_train,y_train,X_test,y_test)
    
    
    #clfSVM = svm.SVC(kernel='rbf', probability=True,C=10,gamma=0.0001)
    clfSVM = svm.SVC(kernel='linear', probability=True,C=100)
    accuracy[2]+=Classifier_Accuracy(clfSVM,X_train,y_train,X_test,y_test)
    precision[2] += Classifier_Precision(clfSVM,X_train,y_train,X_test,y_test)
    recall[2] += Classifier_Recall(clfSVM,X_train,y_train,X_test,y_test)
    f1_score[2] += Classifier_F1score(clfSVM,X_train,y_train,X_test,y_test)


    clfRF = RandomForestClassifier(n_estimators=200)
    accuracy[3]+=Classifier_Accuracy(clfRF,X_train,y_train,X_test,y_test)
    precision[3] += Classifier_Precision(clfRF,X_train,y_train,X_test,y_test)
    recall[3] += Classifier_Recall(clfRF,X_train,y_train,X_test,y_test)
    f1_score[3] += Classifier_F1score(clfRF,X_train,y_train,X_test,y_test)
    
    #eclf = VotingClassifier(estimators=[('DT', clfDT), ('KNN', clfKNN), ('SVM', clfSVM),('RF',clfRF,)], voting='soft',weights=[1,1,3,1])
    eclf = VotingClassifier(estimators=[('DT', clfDT), ('KNN', clfKNN), ('RF',clfRF,)], voting='soft',weights=[1,2,1])
    #eclf = VotingClassifier(estimators=[ ('KNN', clfKNN), ('SVM', clfSVM),('RF',clfRF,)], voting='soft',weights=[1,3,1])
    accuracy[4]+=Classifier_Accuracy(eclf,X_train,y_train,X_test,y_test)
    precision[4] += Classifier_Precision(eclf,X_train,y_train,X_test,y_test)
    recall[4] += Classifier_Recall(eclf,X_train,y_train,X_test,y_test)
    f1_score[4] += Classifier_F1score(eclf,X_train,y_train,X_test,y_test)
    
    print(i,"calculation end")
    

print("accuracy")    
print("DecisionTree : ",str(accuracy[0]/5))
print("KNN : ",str(accuracy[1]/5))
print("SVM : ",str(accuracy[2]/5))
print("RandomForest : ",str(accuracy[3]/5))
print("Ensemble : ",str(accuracy[4]/5))

print("precision")    
print("DecisionTree : ",str(precision[0]/5))
print("KNN : ",str(precision[1]/5))
print("SVM : ",str(precision[2]/5))
print("RandomForest : ",str(precision[3]/5))
print("Ensemble : ",str(precision[4]/5))

print("recall")    
print("DecisionTree : ",str(recall[0]/5))
print("KNN : ",str(recall[1]/5))
print("SVM : ",str(recall[2]/5))
print("RandomForest : ",str(recall[3]/5))
print("Ensemble : ",str(recall[4]/5))

print("f1_score")    
print("DecisionTree : ",str(f1_score[0]/5))
print("KNN : ",str(f1_score[1]/5))
print("SVM : ",str(f1_score[2]/5))
print("RandomForest : ",str(f1_score[3]/5))
print("Ensemble : ",str(f1_score[4]/5))

print("end")

val_result_ALL = open('8stft_val_result_ALL_20190527.txt','w')
pre_result_DT = open('8stft_pre_result_DT_20190527.txt','w')
pre_result_KNN= open('8stft_pre_result_KNN_20190527.txt','w')
pre_result_SVM = open('8stft_pre_result_SVM_20190527.txt','w')
pre_result_RF = open('8stft_pre_result_RF_20190527.txt','w')

clfDT.fit(X_train,y_train)
y_pred_DT = clfDT.predict(X_test)

clfKNN.fit(X_train,y_train)
y_pred_KNN = clfKNN.predict(X_test)

clfSVM.fit(X_train,y_train)
y_pred_SVM = clfSVM.predict(X_test)

clfRF.fit(X_train,y_train)
y_pred_RF = clfRF.predict(X_test)

for i in range(160):
	val_result_ALL.write(str(y_test[i]))
	val_result_ALL.write('\n')
	pre_result_DT.write(str(y_pred_DT[i]))
	pre_result_DT.write('\n')
	pre_result_KNN.write(str(y_pred_KNN[i]))
	pre_result_KNN.write('\n')
	pre_result_SVM.write(str(y_pred_SVM[i]))
	pre_result_SVM.write('\n')
	pre_result_RF.write(str(y_pred_RF[i]))
	pre_result_RF.write('\n')
	print(i,'/160')

print(len(y_pred_RF))


#print("DecisionTree : ")
#clfDT = DecisionTreeClassifier(max_depth=4)
#y_pred_DT = clfDT.fit(X_train,y_train).predict(X_test)
#cnf_matrix = confusion_matrix(y_test, y_pred_DT)
#plot_confusion_matrix(cnf_matrix, classes=Kind, normalize=True,
#                      title='Normalized confusion matrix')

