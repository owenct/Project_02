## Project_2


# Trading Strategy README

This repository contains the code for implementing a trading strategy using historical market data. The strategy involves generating buy/sell signals based on moving average features and evaluating the performance using machine learning models.

## Features

The main features of this repository include:

### Data Processing

Raw market data is processed to extract relevant features, including moving averages, which are used as input for the trading strategy.

### Baseline Algorithm

A baseline algorithm is implemented to generate buy/sell signals based on moving average crossovers.

## Modeling

Three machine learning models are applied to predict buy/sell signals based on historical data:

### Support Vector Machine (SVM)

A Support Vector Machine classifier is trained using the moving average features to predict buy/sell signals.

### Logistic Regression

A Logistic Regression model is trained using the same features to predict buy/sell signals.

### Multilayer Perceptron (MLP)

A Multilayer Perceptron (MLP) neural network is implemented for predicting buy/sell signals. The model architecture and hyperparameters can be adjusted for further experimentation.

## Strategy Evaluation

The performance of the trading strategy is evaluated using the predicted signals from the baseline algorithm and the machine learning models, including SVM, Logistic Regression, and MLP. Strategy returns are calculated and compared to actual returns to assess the effectiveness of the strategy.

