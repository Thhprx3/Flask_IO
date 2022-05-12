data = historical_data('USD','bitcoin','2013-01-01','2022-01-01')
data['timestamp'] = pd.to_datetime(data['timestamp']).dt.date
dataframe = pd.DataFrame(data=data, index=[data.timestamp], columns=['close'])
close_data = data.filter(['close'])
close_dataset = close_data.values
close_dataset = close_dataset.astype('float32')

scaler = MinMaxScaler(feature_range=(0,1))

close_dataset = scaler.fit_transform(close_dataset)
Training_size = math.ceil(len(close_dataset)*0.8)
Testing_size = len(close_dataset) - Training_size

print("Trainging length: "+str(Training_size))
print("Testing length: "+str(Testing_size))

train = close_dataset[0:Training_size,:]
test = close_dataset[Training_size:len(close_dataset),:]
look_back = 3

Xtrain = []
Ytrain = []
Xtest = []
Ytest = []

#Training data
for i in range(len(train)-look_back-1):
    x = train[i:(i+look_back),0]
    Xtrain.append(x)
    Ytrain.append(train[i+look_back, 0])

#Testing data
for i in range(len(test)-look_back-1):
    x = test[i:(i+look_back),0]
    Xtest.append(x)
    Ytest.append(test[i+look_back, 0])

Xtrain = np.array(Xtrain)
Xtest= np.array(Xtest)
Ytrain = np.array(Ytrain)
Ytest = np.array(Ytest)

Xtrain = np.reshape(Xtrain, (Xtrain.shape[0], 1, Xtrain.shape[1]))
Xtest = np.reshape(Xtest, (Xtest.shape[0], 1, Xtest.shape[1]))


#LSTM Network
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(1, look_back)))
model.add(Dropout(rate=0.2))
model.add(LSTM(50, return_sequences=False))
model.add(Dropout(rate=0.2))
model.add(Dense(1))
model.compile(loss="mse", optimizer="adam", metrics=['mae'])


model.fit(Xtrain, Ytrain, epochs=100, batch_size=32, verbose=2)



from sklearn.metrics import mean_squared_error

TrainPrediction = model.predict(Xtrain)
TestPrediction = model.predict(Xtest)

TrainPrediction = scaler.inverse_transform(TrainPrediction)
Ytrain = scaler.inverse_transform([Ytrain])
TestPrediction = scaler.inverse_transform(TestPrediction)
Ytest = scaler.inverse_transform([Ytest])