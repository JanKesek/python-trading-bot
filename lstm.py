import jsonpreprocess as jp
from datetime import datetime
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import numpy

def fit_lstm(train, batchSize, epochN, neurons):
    X, y = train[:, 0:-1], train[:, -1]
    X = X.reshape(X.shape[0], 1, X.shape[1])
    model = Sequential()
    model.add(LSTM(neurons, batch_input_shape=(batchSize, X.shape[1], X.shape[2]), stateful=True))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    for i in range(epochN):
        model.fit(X, y, epochs=1, batch_size=batchSize, verbose=0, shuffle=False)
        model.reset_states()
    return model   
def forecast_lstm(model, batch_size, X):
	X = X.reshape(1, 1, len(X))
	yhat = model.predict(X, batch_size=batch_size)
	return yhat[0,0]
def invert_scale(scaler, X, value):
	new_row = [x for x in X] + [value]
	array = numpy.array(new_row)
	array = array.reshape(1, len(array))
	inverted = scaler.inverse_transform(array)
	return inverted[0, -1]
def inverse_difference(history, yhat, interval=1):
	return yhat + history[-interval]

if __name__ == "__main__":
    data=jp.getJSONObjectCP("link-chainlink",startDate="2018-01-06", endDate="2019-01-07")+jp.getJSONObjectCP("link-chainlink",startDate="2019-01-06", endDate="2020-01-05")
    #print(data[-1])
    startDate=datetime(2018,1,6)
    endDate=datetime(2020,1,5)
    dataDF=jp.convertJSONToDataFrame(data,startD=startDate, endD=endDate)
    diffdata=jp.timeSeriesReturns(dataDF,startD=datetime(2018,1,6))
    supervised=jp.toSupervised(diffdata)
    train=pd.concat([supervised["Today"][0:-12],supervised["Tomorrow"][0:-12]],axis=1)
    test=pd.concat([supervised["Today"][-12:],supervised["Tomorrow"][-12:]],axis=1)
    print(test)
    scaler, train_scaled, test_scaled = jp.scale(train, test)
    print("TRAINSCALLED", train_scaled)
    print("TESTSCALLED", test_scaled)
    lstm_model = fit_lstm(train_scaled, 1, 500,256)
    train_reshaped = train_scaled[:, 0].reshape(len(train_scaled), 1,1)
    lstm_model.predict(train_reshaped, batch_size=1)
    predictions = []
    raw_values=dataDF["Today"].values
    for i in range(len(test_scaled)):
        print("WHICH TEST SAMPLE: ", i)
        X, y = test_scaled[i, 0:-1], test_scaled[i, -1]
        yhat = forecast_lstm(lstm_model, 1, X)
        yhat = invert_scale(scaler, X, yhat)
        # invert differencing
        yhat = inverse_difference(raw_values, yhat, len(test_scaled)+1-i)
        # store forecast
        predictions.append(yhat)
        expected = raw_values[len(train) + i + 1]
        print('Day=%d, Predicted=%f, Expected=%f' % (i+1, yhat, expected))

	# report performance
	#rmse = sqrt(mean_squared_error(raw_values[-12:], predictions))
	#print('Test RMSE: %.3f' % rmse)
	# line plot of observed vs predicted
	#pyplot.plot(raw_values[-12:])
	#pyplot.plot(predictions)
	#pyplot.show()
