# Check version of TensorFlow and select 2.x
import tensorflow as tf
print(tf.__version__)

# Upgrade if neccessary
if int(tf.__version__.replace('.', '')) < 2000:
  !pip install --upgrade pip
  !pip install --upgrade tensorflow

##########################################################

# Meta Parameters
learning_rate = 0.004
training_epochs = 5000

# Network Parameters
n_input = 2 # 2 input features
n_hidden_1 = 8 # 1st layer number of features
n_classes = 1 # 1 target class

##########################################################

# Basic Neuronal Net

model = tf.keras.models.Sequential([
  tf.keras.layers.Dense(n_hidden_1, input_shape=(n_input,), activation=tf.nn.relu),
  tf.keras.layers.Dense(n_classes, activation=tf.nn.sigmoid)
])

model.compile(optimizer="adam",
                loss='binary_crossentropy', 
                metrics=['accuracy'])

hist = model.fit(X_train, y_train, epochs=training_epochs,verbose=0)
predictions = model.predict(X_test)

##########################################################

# With regularization

model = tf.keras.models.Sequential([
  tf.keras.layers.Dense(n_hidden_1,
                        input_shape=(n_input,),
                        activation=tf.nn.relu),
                        kernel_regularizer=tf.keras.regularizers.l2(0.05)

  tf.keras.layers.Dense(n_classes, activation=tf.nn.sigmoid)
])

model.compile(optimizer="adam",
                loss='binary_crossentropy', 
                metrics=['accuracy'])

hist = model.fit(X_train, y_train, epochs=training_epochs,verbose=0)
predictions = model.predict(X_test)

##########################################################

# With earlie stopping

from tensorflow.keras.callbacks import EarlyStopping
es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=20)

model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(256, activation='relu'))
model.add(tf.keras.layers.Dense(256, activation='relu'))
model.add(tf.keras.layers.Dense(1))

model.summary()

model.compile(optimizer='adam',
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['accuracy'])

hist = model.fit(train_data.shuffle(10000).batch(512),
                    epochs=num_epochs,
                    validation_data=validation_data.batch(512),
                    verbose=0,
                    callbacks=[es])


##########################################################

# Visualize Costs over Epochs 
import matplotlib.pyplot as plt

def cost_over_epochs(hist):
    f = plt.plot(hist.history['loss'],label="training loss")
    f = plt.plot(hist.history['val_loss'],label="validation loss")
    f = plt.ylabel("Cost")
    f = plt.xlabel("Epoch")
    return f