import pandas as pd
import math
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import CSVLogger

scaler = MinMaxScaler(feature_range=(0,1))

previous_ts=3

def prepare_data(data):
    data['timestamp'] = pd.to_datetime(data['timestamp']).dt.date
    dataframe = pd.DataFrame(data=data, index=[data.timestamp], columns=['close'])
    close_data = data.filter(['close'])
    close_dataset = close_data.values
    close_dataset = close_dataset.astype('float32')
    #normalizing to scale input data
    #scaler = MinMaxScaler(feature_range=(0,1))
    close_dataset = scaler.fit_transform(close_dataset)
    return close_dataset

def split(close_dataset):
    #splitting data into 80% of train data and 20% of test data
    Training_size = math.ceil(len(close_dataset)*0.8)
    Testing_size = len(close_dataset) - Training_size
    train = close_dataset[0:Training_size,:]
    test = close_dataset[Training_size:len(close_dataset),:]
    return train, test


def model_data(train,test):
    Xtrain = []
    Ytrain = []
    Xtest = []
    Ytest = []

    #Training data
    for i in range(len(train)-previous_ts-1):
        x = train[i:(i+previous_ts),0]
        Xtrain.append(x)
        Ytrain.append(train[i+previous_ts, 0])

    #Testing data
    for i in range(len(test)-previous_ts-1):
        x = test[i:(i+previous_ts),0]
        Xtest.append(x)
        Ytest.append(test[i+previous_ts, 0])

    Xtrain = np.array(Xtrain)
    Xtest= np.array(Xtest)
    Ytrain = np.array(Ytrain)
    Ytest = np.array(Ytest)

    Xtrain = np.reshape(Xtrain, (Xtrain.shape[0], 1, Xtrain.shape[1]))
    Xtest = np.reshape(Xtest, (Xtest.shape[0], 1, Xtest.shape[1]))

    return Xtrain, Ytrain, Xtest, Ytest

def fit_model(Xtrain, Ytrain, Xtest, Ytest, dropdownNeurons, dropdownSteps):
    #LSTM Network
    model = Sequential()
    model.add(LSTM(dropdownNeurons, return_sequences=True, input_shape=(1, previous_ts)))
    model.add(Dropout(rate=0.2))
    model.add(LSTM(dropdownNeurons, return_sequences=True))
    model.add(Dropout(rate=0.2))
    model.add(LSTM(dropdownNeurons, return_sequences=False))
    model.add(Dropout(rate=0.2))
    model.add(Dense(1))
    model.compile(loss="mse", optimizer="adam", metrics=['mae'])

    csv_logger = CSVLogger('run.csv', append=True, separator=',')
    model.fit(Xtrain, Ytrain, validation_data=(Xtest,Ytest), epochs=dropdownSteps, batch_size=16, verbose=2, callbacks=[csv_logger])
    return model

def predict_values(model, Xtrain, Ytrain, Xtest, Ytest, close_dataset):  
    TrainPrediction = model.predict(Xtrain)
    TestPrediction = model.predict(Xtest)
    TrainPrediction = scaler.inverse_transform(TrainPrediction)
    Ytrain = scaler.inverse_transform([Ytrain])
    TestPrediction = scaler.inverse_transform(TestPrediction)
    Ytest = scaler.inverse_transform([Ytest])
    TrainScore = math.sqrt(mean_squared_error(Ytrain[0], TrainPrediction[:,0]))
    TestScore = math.sqrt(mean_squared_error(Ytest[0], TestPrediction[:,0]))
    return TrainPrediction, Ytrain, TestPrediction, Ytest, TrainScore, TestScore

def plot_data(close_dataset, TrainPrediction, TestPrediction):
    trainPredictPlot = np.empty_like(close_dataset)
    trainPredictPlot[:, :] = np.nan
    trainPredictPlot[previous_ts:len(TrainPrediction)+previous_ts, :] = TrainPrediction
    testPredictPlot = np.empty_like(close_dataset)
    testPredictPlot[:, :] = np.nan
    testPredictPlot[len(TrainPrediction)+(previous_ts*2)+1:len(close_dataset)-1, :] = TestPrediction
    inverted_dataset = scaler.inverse_transform(close_dataset)
    return inverted_dataset, trainPredictPlot, testPredictPlot


def predict(num_prediction, model, close_dataset):
    prediction_list = close_dataset[-previous_ts:]
    
    for _ in range(num_prediction):
        x = prediction_list[-previous_ts:]
        x = x.reshape(1, 1, previous_ts)
        out = model.predict(x)
        inversed_data = scaler.inverse_transform(out)
        prediction_list = np.append(prediction_list, inversed_data)
    prediction_list = prediction_list[previous_ts-1:]
        
    return prediction_list[1]