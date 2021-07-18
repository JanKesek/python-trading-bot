from json import load
from re import L
from statistics import mode
from keras.models import load_model, Sequential
from keras.layers import RNN, Dropout, TimeDistributed, LSTMCell, Dense
from keras.regularizers import l1_l2
from numpy.core.numeric import full
from backtester import getOHLCVByFilenameJSON,  getOHLCVByFilename
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TKAgg')


def predict_lstm(X, model, testLength,fullLength):
	#X = X.reshape(1, 1, len(X))
	#preds=np.array([])
	preds=[]
	i=testLength
	while i<fullLength:
		Y=model.predict(X)
		#print(Y[-1])
		#preds=np.append(preds,Y[-1])
		preds.append(Y[-1][0])
		new_tensor=np.append(X[-1][0][1:],preds[-1])
		#new_tensor=np.array([X[-1][0][1],preds[-1]])
		print(new_tensor)
		new_tensor=new_tensor.reshape((1,1,len(new_tensor)))
		X=np.concatenate((X,new_tensor))
		#X=np.append(X,preds[-1])
		print(i, ":", fullLength)
		i+=1
		if i%100==0:
			predsdf= pd.DataFrame(preds)
			predsdf.to_csv("predictedValuesLSTM.csv",index=False)	
	return pd.DataFrame(preds)
	#yhat = model.predict(X)
	#return yhat

def preprocess_df(data,mode='full',look_back = 24):
	dataset, scaler = get_scaler()
	X=create_dataset(dataset[:,:],look_back=look_back)
	print("X_shape in preprocess: {} y_shape".format(X.shape))
	X = np.reshape(X, (X.shape[0], 1, X.shape[1]))
	return X,scaler
def create_dataset(dataset, data_mode='valid',look_back=1):
	dataX = []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		#print("TENSORS OF X: ",dataX)
		#print("TENSORS OF Y: ",dataY)
		dataX.append(a)
	return np.array(dataX)

def set_up_model(weights_filename):
	model = Sequential([    
		RNN(LSTMCell(30), return_sequences=True,input_shape=[None, 8]),   
		Dropout(0.8),
		RNN(LSTMCell(30),return_sequences=True), 
		Dropout(0.8),
		TimeDistributed(Dense(1,kernel_regularizer=l1_l2(l1=0.001, l2=1e-4)))
  	])
	model.load_weights(weights_filename)
	return model
def get_scaler(data):
	dataset = data.astype('float32')
	dataset = np.reshape(dataset.values,(-1,1))
	scaler = MinMaxScaler(feature_range=(0, 1))
	dataset = scaler.fit_transform(dataset)
	return dataset, scaler
def rescale_values(original_df,df):
	_,scaler = get_scaler(original_df)
	return scaler.inverse_transform(df)
def predict_values():
	model = set_up_model("model.h5")
	#to_predict = 
	X_data= getOHLCVByFilename("BTC-USDT","1h")['close']
	data_length = len(X_data)
	X, scaler = preprocess_df(X_data[0:29500], look_back=8)
	lst=predict_lstm(X,model, len(X),data_length)
	lst.to_csv("predictedValuesLSTM.csv",index=False)
def plot_real_to_predicted(realdf, predicteddf):
	x= [i for i in range(len(realdf))]
	plt.plot(x,realdf)
	plt.plot(x,predicteddf)
	plt.show()
def get_reals(df, index, predslen):
	reals = []
	realslen =len(reals)
	while realslen<predslen and index+8<len(df):
		reals.append(df[index+8])
		index+=8
		realslen=len(reals)
	return pd.DataFrame(reals)

if __name__=='__main__':
	X_data= getOHLCVByFilename("BTC-USDT","1h")['close']
	predictedValues = pd.read_csv("predictedValuesLSTM.csv")
	predictedRescaled = pd.DataFrame(rescale_values(X_data,predictedValues))
	reals = get_reals(X_data,29500,len(predictedValues))
	preds=predictedRescaled
	print(reals, len(reals))
	print(preds, len(preds))
	plot_real_to_predicted(reals,preds)