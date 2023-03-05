# Sentiment Analysis on IMDb Movie Reviews  
This project is a sentiment analysis task on the IMDb movie reviews dataset. The goal is to classify movie reviews as either positive or negative based on their text content.  

## Table of Contents  
1. Overview  
2. Dataset  
3. Model Architecture  
4. Dependencies  
5. Usage  
6. License  

## Overview  
The project is implemented using TensorFlow and Keras libraries in Python. The code includes data preprocessing, model training, and evaluation on the test set. The trained model can be used to make predictions on new movie reviews.

## Dataset  
The IMDb movie reviews dataset contains 50,000 reviews split into 35,000 training and 7500 testing, 7500 validation sets. Each review is labeled as either positive or negative. The dataset can be found on the Kaggle website.

## Model Architecture  
The model architecture is a Convolutional Neural Network (CNN) with the following layers:

* A custom text vectorization layer using TextVectorization from Keras 
* A custom text embedding layer using Embedding from Keras  
* A Conv1D layer with 128 filters, kernel size of 12, and ReLU activation  
* A MaxPool1D layer  
* Another Conv1D layer with 128 filters, kernel size of 12, and ReLU activation  
* A GlobalMaxPool1D layer  
* A Dense output layer with sigmoid activation  
* The model is compiled with binary cross-entropy loss and Adam optimizer.  

## Dependencies
The following libraries are required to run the code:

`TensorFlow 2.x  
pandas  
numpy  
scikit-learn`  

## Usage
To use the code, follow these steps:

1. Download the IMDb dataset from the Kaggle website.
2. Install the required libraries using pip or conda.
3. Clone the repository to your local machine.  
  `git clone https://github.com/r-zeeshan/imdb-review-classifier.git`  

4. Run `main.py` file.
5. Alternatively, you can just open the colab notebook, and walkthrough each cell to train this model.  
This project is licensed under the MIT License - see the LICENSE.md file for details.

## Acknowledgments
The dataset used in this project is from the Kaggle website.  
