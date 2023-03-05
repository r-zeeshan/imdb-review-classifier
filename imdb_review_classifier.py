# -*- coding: utf-8 -*-
"""imdb-review-classifier.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19YxlyhAavm0ux5PqZbi0j-0yNzkG4bOk
"""

import tensorflow as tf
import pandas as pd
import numpy as np 
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import TextVectorization, Embedding, Dense, Input, Conv1D, GlobalMaxPool1D, Dropout, MaxPool1D
from sklearn.preprocessing import LabelEncoder

!wget --no-check-certificate "https://docs.google.com/uc?export=download&id=1rxUd_7UpGz4WVGM1Bjb2uJ74ummZlfTy" -O imdb.csv

df = pd.read_csv("/content/imdb.csv")
df.head()

label_encoder = LabelEncoder()
df["sentiment"] = label_encoder.fit_transform(df["sentiment"])

df["sentiment"].value_counts()

label_encoder.classes_

data_sentences = df["review"].to_list()
data_labels = df["sentiment"].to_list()

train_sentences, X_test, train_labels, y_test = train_test_split(data_sentences, data_labels, test_size = 0.3)

test_sentences, val_sentences, test_labels, val_labels = train_test_split(X_test, y_test, test_size = 0.5)

len(train_sentences), len(test_sentences), len(val_sentences)

# Calculate the average sentence length
sent_lens = [len(sentence.split()) for sentence in train_sentences]
avg_sent_len = np.mean(sent_lens)
output_seq_len = int(np.percentile(sent_lens, 98))
output_seq_len

vocab_size = 49600 # From Kaggle Dataset page

# Creating fast loading dataset with tf.data api

train_dataset = tf.data.Dataset.from_tensor_slices((train_sentences, train_labels)).batch(128).prefetch(tf.data.AUTOTUNE)
test_dataset = tf.data.Dataset.from_tensor_slices((test_sentences, test_labels)).batch(128).prefetch(tf.data.AUTOTUNE)
val_dataset = tf.data.Dataset.from_tensor_slices((val_sentences, val_labels)).batch(128).prefetch(tf.data.AUTOTUNE)

# Creating a custom text vectorizer layer using tf.keras.layers.TextVectorizer
text_vectorizer = TextVectorization(max_tokens = vocab_size, output_mode = "int", output_sequence_length=output_seq_len)
text_vectorizer.adapt(train_sentences)

text_vocab = text_vectorizer.get_vocabulary()
print(f"No. of words in vocab: {len(text_vocab)}")
print(f"Most common words in vocab: {text_vocab[:5]}")
print(f"Least common words in data: {text_vocab[-5:]}")

# Creating a custom text embedding layer using tf.keras.layers.Embedding
text_embedding = Embedding(input_dim = len(text_vocab),
                           output_dim = 512,
                           mask_zero=True,
                           name="text_embedding")

# Creating the final model
token_input = Input(shape=(1,), dtype=tf.string)
x = text_vectorizer(token_input)
x = text_embedding(x)
x = Conv1D(128, kernel_size=12, padding="same", activation="relu")(x)
x = MaxPool1D()(x)
x = Conv1D(128, kernel_size=12, padding="same", activation="relu")(x)
x = GlobalMaxPool1D()(x)
output = Dense(1, activation="sigmoid")(x)


model = tf.keras.Model(inputs = token_input,
                       outputs = output)

model.compile(loss="binary_crossentropy",
              optimizer=tf.keras.optimizers.Adam(),
              metrics=["accuracy"])

# Setup EarlyStopping callback to stop training if model's val_loss doesn't improve for 3 epochs
early_stopping = tf.keras.callbacks.EarlyStopping(monitor="val_loss", # watch the val loss metric
                                                  patience=3) # if val loss decreases for 3 epochs in a row, stop training

# Creating learning rate reduction callback
reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor="val_loss",  
                                                 factor=0.2, # multiply the learning rate by 0.2 (reduce by 5x)
                                                 patience=2,
                                                 verbose=1, # print out when learning rate goes down 
                                                 min_lr=1e-7)

history = model.fit(train_dataset,
                    epochs=50,
                    validation_data= val_dataset,
                    callbacks=[early_stopping, reduce_lr])

model.evaluate(test_dataset)

test_sentence = """
                I wish I had enjoyed it, given the Tim Burton credential, and my moviegoer love for this director and his nightmarish visions and lovable weird characters. But this is no Tim Burton per se creation, it is a Netflix series, Netflix flows in its veins from the start, from the trailer and the "Paint it Black" cover (which somehow sounds like the cover of the Westworld cover), and the buzz around it. I was expecting "Wednesday" but watching it was like a cold shower, going back to reality, Netflix reality that is : pleasing the majority of its users, transforming the Addams girl into an obnoxious teen in school with her peers, obnoxious teens. Then there was no point in the Addams pariah basis. And no point in keeping watching the series.
                """

def make_preds(model, sentence, label_encoder):

    pred = int(model.predict([sentence])[0])

    return label_encoder.inverse_transform([pred])[0]

make_preds(model, test_sentence, label_encoder)

