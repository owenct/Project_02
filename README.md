## Project_2


# Machine Learning Trading Strategy

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

# Amazon Lex Integration with Lambda and S3 for Stock Information

## Overview

Amazon Lex is a service that facilitates the creation of conversational interfaces or chatbots. In this integration, Amazon Lex is connected to a Lambda function to provide details about individual stocks. The solution is embedded into a static website hosted on Amazon S3.

## Integration Steps

### 1. Amazon Lex Configuration

- Create an Amazon Lex bot with defined intents, sample utterances, and slots to capture user queries related to stock details.

### 2. Lambda Function Integration

- Develop a Lambda function that serves as the fulfillment for the Amazon Lex bot.
- Implement logic within the Lambda function to handle different intents, query stock details from a data source, and generate responses.

### 3. Fulfillment Logic

- Implement the fulfillment logic in the Lambda function, fetching relevant stock information and formulating responses based on user queries.

### 4. AWS SDK Integration

- Use the AWS SDK within the Lambda function to interact with other AWS services or external APIs for retrieving up-to-date stock details.

### 5. Amazon S3 Website Hosting

- Host static website files (HTML, CSS, and JavaScript) on Amazon S3.
- Ensure the website files include the necessary JavaScript SDK or code snippets for interacting with the Amazon Lex chatbot.

### 6. Website Integration

- Embed the Amazon Lex chatbot into the website by adding a chat window or interface.
- Utilize the Amazon Lex runtime API to send user queries from the website to the Amazon Lex bot.

### 7. User Interaction

- Users can interact with the chatbot on the website by typing or speaking stock-related queries.
- The Amazon Lex bot processes user input, triggers the Lambda function, retrieves stock information, and sends a response back to the user.

### 8. TradeTitan Demo

- Visit the [demo website](https://tradetitanweb.s3.us-west-2.amazonaws.com/index.html) to experience the integrated solution.
- Engage with the chatbot on the website to obtain information about individual stocks.

This integration provides a seamless conversational experience on the website, allowing users to inquire about stock details using natural language. The combination of Amazon Lex, Lambda functions, and S3 hosting offers a scalable solution for building interactive and intelligent chatbot applications.

