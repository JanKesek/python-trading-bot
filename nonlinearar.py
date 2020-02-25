import jsonpreprocess as jp
import pandas
from datetime import datetime
from fireTS.models import NARX
from sklearn.linear_model import LinearRegression

if __name__ == "__main__":
    data=jp.getJSONObjectCP("link-chainlink","2019-02-20","2020-02-08")
    df=jp.convertJSONToDataFrame(data,datetime(2019,2,20),datetime(2020,2,8))
    xtrain=pandas.concat([df["Today"][0:300],df["Volume"][0:300]],axis=1,keys=["Today","Volume","Lag1"])
    ytrain=df["Today"][0:300]
    xtest=pandas.concat([df["Today"][300:],df["Volume"][300:]],axis=1,keys=["Today","Volume","Lag1"])
    ytest=df["Today"][300:]
    print(xtrain)
    narx_mdl = NARX(LinearRegression(), auto_order=6, exog_order=[2, 2], exog_delay=[0, 0])
    narx_mdl.fit(xtrain,ytrain)
    ypred=narx_mdl.predict(xtest,ytest, step=3)
    print(ypred)
