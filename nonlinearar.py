import jsonpreprocess as jp
from datetime import datetime
from fireTS.models import NARX
from sklearn.linear_model import LinearRegression

if __name__ == "__main__":
    data=jp.getJSONObjectCP("link-chainlink","2019-02-20","2020-02-08")
    df=jp.convertJSONToDataFrame(data,datetime(2019,2,20),datetime(2020,2,8))
    xtrain=df["Today"][0:300]+df["Volume"][0:300]+df["Lag1"][0:300]
    ytrain=df["Volume"][0:300]
    xtest=df["Today"][300:]+df["Volume"][300:]+df["Lag1"][300:]
    ytest=df["Volume"][300:]
    print(xtrain)
    narx_mdl = NARX(LinearRegression(), auto_order=6, exog_order=[3, 3], exog_delay=[0, 0])
    narx_mdl.fit(xtrain,ytrain)
    ypred=narx_mdl.predict(xtest,ytest, step=3)
