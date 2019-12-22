from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA

def fitModel(name,model,Xtrain, ytrain, Xtest, pred):
	model.fit(Xtrain,ytrain)
	pred[name]=model.predict(Xtest)
	pred["%s_Correct"%name]=(1.0+pred[name]*pred["Actual"])/2.0
	hitRate=np.mean(pred["%s_Correct"%name])
	print(pred)
	print("%s : %.3f" % (name, hitRate))
def fitLDAQDA(ts):
	X=ts[["Lag1","Lag2"]]
	y=ts["Direction"]
	startTest=datetime(2019,12,1)
	Xtrain=X[X.index<startTest]
	Xtest=X[X.index>=startTest]
	ytrain=y[y.index<startTest]
	ytest=y[y.index>=startTest]
	pred=pd.DataFrame(index=ytest.index)
	pred["Actual"]=ytest
	models=[("LR", LogisticRegression()),("LDA",LDA()), ("QDA",QDA())]
	for m in models:
		fitModel(m[0],m[1],Xtrain, ytrain, Xtest, pred)
