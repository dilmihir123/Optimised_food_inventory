
from google.colab import files
uploaded = files.upload()

meal_info = pd.read_csv(io.BytesIO(uploaded['meal_info.csv']))

uploaded1 = files.upload()


train=pd.read_csv(io.BytesIO(uploaded1['train.csv']))

uploaded2 = files.upload()

test=pd.read_csv(io.BytesIO(uploaded2['test.csv']))

train=pd.concat([train,test]) 

!pip install TimeSeries
!pip install time_series
!pip install statsmodels
!pip install stldecompose

#import time_series as time_series
#from time_series import TimeSeries
import seaborn as sns 
import matplotlib.pyplot as plt
import pandas as pd

# Imports for data visualization
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from matplotlib.dates import DateFormatter
from matplotlib import dates as mpld

# Seasonal Decompose
from statsmodels.tsa.seasonal import seasonal_decompose

# Holt-Winters or Triple Exponential Smoothing model
from statsmodels.tsa.holtwinters import ExponentialSmoothing

from sklearn.metrics import mean_squared_error


from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
from stldecompose import decompose, forecast
from stldecompose.forecast_funcs import (naive,
                                         drift, 
                                         mean, 
                                         seasonal_naive)
# the main library has a small set of functionality
from stldecompose import decompose, forecast
from stldecompose.forecast_funcs import (naive,
                                         drift, 
                                         mean, 
                                         seasonal_naive)
import io

NewTrain = pd.merge(left=train, right=meal_info, how='left', left_on='meal_id', right_on='meal_id')
NewTrain.head()

TrainN = pd.DataFrame(NewTrain, columns = ['meal_id', 'num_orders','week']) 
TrainN.head()

model=[]
totalMeals=TrainN['meal_id'].unique()
len(totalMeals)

def errorF(model1,model2,model3,model4,test,testlen):
    
    
    test1=test
    res1=[]
    res2=[]
    res3=[]
    res4=[]
    testlen1=testlen
    infi = float('inf')
    
    
    #print("testing model1")
    res1=model1.forecast(testlen1)
    y_pred1=[]
    #print(res1)
    for i in res1:
        y_pred1.append(i)
    y_true1=[]
    for i in test1:
        y_true1.append(i[0])
        
    
    try:
        #print(mean_squared_error(y_true1, y_pred1))
        error1=mean_squared_error(y_true1, y_pred1)
        #print(error1)
    except ValueError:
        error1=infi
        #print("Value Error")
        pass
    
    
    #print("testing model2")
    res2=model2.forecast(testlen1)
    y_pred2=[]
    #print(res2)
    for i in res2:
        y_pred2.append(i)
    y_true2=[]
    for i in test1:
        y_true2.append(i[0])
        
    
    try:
        #print(mean_squared_error(y_true2, y_pred2))
        error2=mean_squared_error(y_true2, y_pred2)
        #print(error2)
    except ValueError:
        error2=infi
        #print("Value Error")
        pass
    
    
    #print("testing model3")
    res3=model3.forecast(testlen1)
    y_pred3=[]
    #print(res3)
    for i in res3:
        y_pred3.append(i)
    y_true3=[]
    for i in test1:
        y_true3.append(i[0])
        
    
    try:
        #print(mean_squared_error(y_true3, y_pred3))
        error3=mean_squared_error(y_true3, y_pred3)
        #print(error3)
    except ValueError:
        error3=infi
        #print("Value Error")
        pass
    
    
    
    #print("testing model4")
    res4=model4.forecast(testlen1)
    y_pred4=[]
    #print(res4)
    for i in res4:
        y_pred4.append(i)
    y_true4=[]
    for i in test1:
        y_true4.append(i[0])
        
    
    try:
        #print(mean_squared_error(y_true4, y_pred4))
        error4=mean_squared_error(y_true4, y_pred4)
        #print(error4)
    except ValueError:
        error4=infi
        #print("Value Error")
        pass
    
    
    emin=0
    
    
    if(error1==infi):
        emin=min(error2,error3,error4)
        #print("Except error1")
        

    elif(error2==infi):
        emin=min(error1,error3,error4)
        #print("Except error2")
        


    elif(error3==infi):
        emin=min(error1,error2,error4)
        #print("Except error3")
        


    elif(error4==infi):
        emin=min(error1,error2,error3)
        #print("Except error4")
    
    else:
        emin=min(error1,error2,error3,error4)
        #print("No Exceptions")
        

    
        
        
    if(error1==emin):
        #print("model1")
        #print(error1)
        return model1,error1
    elif(error2==emin):
        #print("model2")
        #print(error2)
        return model2,error2
    elif(error3==emin):
        #print("Model3")
        #print(error3)
        return model3,error3
    elif(error4==emin):
        #print("Model4")
        #print(error4)
        return model4,error4
    

new_tab=TrainN.groupby([TrainN.meal_id,TrainN.week]).sum()  
new_tab.head()

def stl(k):
    from stldecompose import decompose, forecast
    ar=new_tab.loc[(k)].values
    #print(len(ar))
    a=[]
    for i in range(len(ar)):
        a.append(ar[i][0])
    
    def timeseries_df():
        index = pd.date_range(start="01-01-2017", periods=len(a), freq='W-SAT')
        ts = pd.DataFrame(a, index=index, columns=['num_orders'])
        ts['num_orders']=a
        return ts
    
    
    ts = timeseries_df()
    #print(ts)
    #print(ts.index)
    X = ts.values
    train_size = int(len(X) * 0.60)
    test_size = len(X)-train_size
    #print(test_size," ", train_size)
    #training, testing = ts[0:train_size], ts[train_size:len(X)]
    train, test = ts[0:train_size], ts[train_size:len(X)]
    #print(train)
    #print(test)
    #print('Observations: %d' % (len(X)))
    #print('Training Observations: %d' % (len(train)))
    #print('Testing Observations: %d' % (len(test)))

    trend=['add','add','mul','mul']
    seasonal=['add','mul','add','mul']
    
    
    #print(test)
    
    decomp = decompose(train, period=7)
    #print(decomp)
    #print(type(decomp))
    #s=sm.tsa.seasonal_decompose(train)
    
    #print("trend")
    #print(decomp.trend)
    #print(decomp.resid)
    
    #print("season")
    #print(decomp.seasonal)
    
    fcast = forecast(decomp, steps=test_size, fc_func=naive, seasonal=True)
    #print(fcast)
    y_pred=[]
    for i in fcast.values:
        y_pred.append(i[0])
    #print(y_pred)
    y_true=[]
    for i in test.values:
        y_true.append(i[0])
    #print(y_true)
    Ferror=mean_squared_error(y_true, y_pred)
    
    return decomp,Ferror,test_size

def ets(k):

    ar=new_tab.loc[(k)].values
    #print(len(ar))
    a=[]
    
    for i in range(len(ar)):
        a.append(ar[i][0])
    
    def timeseries_df():
        index = pd.date_range(start="01-01-2017", periods=len(a), freq='W-SAT')
        ts = pd.DataFrame(a, index=index, columns=['num_orders'])
        ts['num_orders']=a
        return ts
    
    ts = timeseries_df()
    #print(ts)
    X = ts.values
    #print(X)
    train_size = int(len(X) * 0.80)
    test_size = len(X)-train_size
    train, test = X[0:train_size], X[train_size:len(X)]
    
    
    #print('Observations: %d' % (len(X)))
    #print('Training Observations: %d' % (len(train)))
    #print('Testing Observations: %d' % (len(test)))

    #trend=['add','add','mul','mul']
    #seasonal=['add','mul','add','mul']
    
    

    
    print("ETS_training model1")
    model1 = ExponentialSmoothing(train, seasonal_periods=7, trend='add', seasonal='add',damped=True).fit(use_boxcox=True)
    print("ETS_training model2")
    model2 = ExponentialSmoothing(train, seasonal_periods=7, trend='add', seasonal='mul',damped=True).fit(use_boxcox=True)
    print("ETS_training model3")
    model3 = ExponentialSmoothing(train, seasonal_periods=7, trend='mul', seasonal='add',damped=True).fit(use_boxcox=True)
    print("ETS_training model4")
    model4 = ExponentialSmoothing(train, seasonal_periods=7, trend='mul', seasonal='mul',damped=True).fit(use_boxcox=True)
    #print(1)
    
    model,error=errorF(model1,model2,model3,model4,test,test_size)
    return model,error,test_size

dfs = []
from sklearn.externals import joblib 
for i in totalMeals:
  #df_name = 'meal_'+str(int(i))
  #dfs.append(df_name)
  print(i)
  modelSTL,errorSTL,testlenSTL=stl(i)
  print("Finished STL")
  modelETS,errorETS,testlenETS=ets(i)
  error=min(errorSTL,errorETS)
  if(error==errorSTL):
      FinalModel=modelSTL
      FModel='STL'
      print("STL")
  elif(error==errorETS):
      FinalModel=modelETS
      FModel='ETS'
      print("ETS")
    
  from stldecompose import decompose, forecast
  Pred=[]
  if(FModel=='STL'):
      forecast=forecast(FinalModel, steps=testlenSTL, fc_func=naive, seasonal=True)
      for j in forecast.values:
          Pred.append(j[0])

  elif(FModel=='ETS'):
      Pred=FinalModel.forecast(testlenETS)
      
      
  print(Pred)

  globals()['Model%s' % i] = FinalModel
  print('Model%s' % i)


  

import pickle 
from sklearn.externals import joblib 
for i in totalMeals:
  ModelName='Model%s' % i
  #print(f)
  FName="Model"+str(i)+".xml"
  mod=joblib.dump(ModelName, FName)
  files.download(FName)
  
  






