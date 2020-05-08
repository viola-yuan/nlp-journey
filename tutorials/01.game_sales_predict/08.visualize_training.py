import pandas as pd
from tensorflow.keras.callbacks import *
from tensorflow.keras.layers import *
from tensorflow.keras.models import Sequential

"""
可以多次训练模型，然后在TensorBoard中查看因为参数变动导致的变动
"""

RUN_NAME = "run 3 with 500 nodes"  # 可以修改

training_data_df = pd.read_csv("dataset/sales_data_training_scaled.csv")

X = training_data_df.drop('销售总额', axis=1).values
Y = training_data_df[['销售总额']].values

# 定义模型
model = Sequential()
model.add(Dense(500, input_dim=9, activation='relu', name='layer_1'))
model.add(Dense(100, activation='relu', name='layer_2'))
model.add(Dense(50, activation='relu', name='layer_3'))
model.add(Dense(1, activation='linear', name='output_layer'))
model.compile(loss='mean_squared_error', optimizer='adam')

# 构建TensorBoard日志组件
logger = TensorBoard(
    log_dir='logs/{}'.format(RUN_NAME),
    histogram_freq=5,
    write_graph=True
)

test_data_df = pd.read_csv("dataset/sales_data_testing_scaled.csv")

X_test = test_data_df.drop('销售总额', axis=1).values
Y_test = test_data_df[['销售总额']].values

# 训练模型
model.fit(
    X,
    Y,
    epochs=50,
    shuffle=True,
    verbose=2,
    callbacks=[logger],
    validation_data=[X_test, Y_test]
)

test_error_rate = model.evaluate(X_test, Y_test, verbose=0)
print("The mean squared error (MSE) for the test data set is: {}".format(test_error_rate))
