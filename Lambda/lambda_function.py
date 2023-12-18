### Required Libraries ###
import json
import numpy as np
import pandas as pd
import yfinance as yf

import random
import requests
import os

### Dialog Actions Helper Functions ###
def get_slots(intent_request):
    """
    Fetch all the slots and their values from the current intent.
    """
    return intent_request["currentIntent"]["slots"]

def delegate(session_attributes, slots):
    """
    Defines a delegate slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {"type": "Delegate", "slots": slots},
    }


def close(session_attributes, fulfillment_state, message):
    """
    Defines a close slot type response.
    """

    response = {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": message,
        },
    }

    return response
    
### Business Login Function ###
def calculate_portfolio_metrics(stock_ticker, short_window=20, long_window=100, initial_capital=100000, share_size=500):
    # Data Preparation
    getStockData = yf.Ticker(stock_ticker)
    df = pd.DataFrame(data=getStockData.history(period="max"))
    signals_df = df.copy()

    # Generate moving averages
    signals_df['SMA50'] = signals_df['Close'].rolling(window=short_window).mean()
    signals_df['SMA100'] = signals_df['Close'].rolling(window=long_window).mean()

    # Generate trading signals
    signals_df['Signal'] = 0.0
    signals_df['Signal'][short_window:] = np.where(
        signals_df['SMA50'][short_window:] > signals_df['SMA100'][short_window:], 1.0, 0.0
    )

    # Entry/Exit signals
    signals_df['Entry/Exit'] = signals_df['Signal'].diff()

    # Set initial capital
    signals_df['Position'] = share_size * signals_df['Signal']
    signals_df['Entry/Exit Position'] = signals_df['Position'].diff()
    signals_df['Portfolio Holdings'] = signals_df['Close'] * signals_df['Position']
    signals_df['Portfolio Cash'] = initial_capital - (signals_df['Close'] * signals_df['Entry/Exit Position']).cumsum()
    signals_df['Portfolio Total'] = signals_df['Portfolio Cash'] + signals_df['Portfolio Holdings']
    signals_df['Portfolio Daily Returns'] = signals_df['Portfolio Total'].pct_change()
    signals_df['Portfolio Cumulative Returns'] = (1 + signals_df['Portfolio Daily Returns']).cumprod() - 1

    # Portfolio-Level Risk/Reward Evaluation Metrics
    portfolio_evaluation_df = pd.DataFrame(index=["Annualized Return", "Cumulative Returns", "Annual Volatility", "Sharpe Ratio", "Sortino Ratio"],
                                           columns=["Backtest"])

    portfolio_evaluation_df.loc["Annualized Return"] = signals_df["Portfolio Daily Returns"].mean() * 252
    portfolio_evaluation_df.loc["Cumulative Returns"] = signals_df["Portfolio Cumulative Returns"][-1]
    portfolio_evaluation_df.loc["Annual Volatility"] = signals_df["Portfolio Daily Returns"].std() * np.sqrt(252)
    portfolio_evaluation_df.loc["Sharpe Ratio"] = (signals_df["Portfolio Daily Returns"].mean() * 252) / (signals_df["Portfolio Daily Returns"].std() * np.sqrt(252))

    # Sortino Ratio Calculation
    sortino_ratio_df = signals_df[["Portfolio Daily Returns"]].copy()
    sortino_ratio_df.loc[:, "Downside Returns"] = 0
    sortino_ratio_df.loc[sortino_ratio_df["Portfolio Daily Returns"] < 0, "Downside Returns"] = sortino_ratio_df["Portfolio Daily Returns"] ** 2

    annualized_return = sortino_ratio_df["Portfolio Daily Returns"].mean() * 252
    downside_standard_deviation = np.sqrt(sortino_ratio_df["Downside Returns"].mean()) * np.sqrt(252)
    sortino_ratio = annualized_return / downside_standard_deviation

    portfolio_evaluation_df.loc["Sortino Ratio"] = sortino_ratio

    return signals_df, portfolio_evaluation_df  

### Intents Handlers ###

def get_stock_quote(intent_request):
    # Gets slots' values
    stock_name = get_slots(intent_request)["stock_name"]

    try:
        # Use Alpha Vantage API to get stock information
        api_url = f'https://www.alphavantage.co/query'
        api_key = os.environ.get('ALPHA_VANTAGE_API_KEY')
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': stock_name,
            'apikey': api_key,
        }

        response = requests.get(api_url, params=params)
        data = response.json()

        # Extract relevant information (you may customize this based on your needs)
        stock_symbol = data.get('Global Quote', {}).get('01. symbol', '')
        stock_price = data.get('Global Quote', {}).get('05. price', 'N/A')

        # Return a message with the stock information
        return close(
            intent_request["sessionAttributes"],
            "Fulfilled",
            {
                "contentType": "PlainText",
                "content": f"The current price of {stock_symbol} is {stock_price}.",
            },
        )

    except Exception as e:
        # Handle errors, such as invalid stock symbol or network issues
        return close(
            intent_request["sessionAttributes"],
            "Fulfilled",
            {
                "contentType": "PlainText",
                "content": f"An error occurred while fetching stock information: {str(e)}",
            },
        )



def get_market_trends(intent_request):
    # Gets slots' values
    stock_name = get_slots(intent_request)["stock_name"]
    
    # Return a message with the result (for now, a simple message is returned)
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": "get_market_trends! (Market Trends Logic to be implemented)",
        },
    )

def get_stock_performance(intent_request):
    try:
        # Extract slot values
        slots = get_slots(intent_request)
        stock_name = slots["stock_ticker"]
        short_window = slots["short_window"]
        long_window = slots["long_window"]
        initial_capital = slots["initial_capital"]
        share_size = slots["share_size"]

        # Retrieve stock data and calculate portfolio metrics
        stock_data, portfolio_metrics = calculate_portfolio_metrics(stock_name, short_window, long_window, initial_capital, share_size)
        
        # Format the results as a JSON response
        response_body = format_response_body(stock_name, portfolio_metrics)

        # Return the formatted result
        return create_successful_response(intent_request, response_body)

    except Exception as e:
        # Handle errors, such as invalid stock symbol or network issues
        error_message = f"An error occurred while fetching stock performance: {str(e)}"
        return create_error_response(intent_request, error_message)

def format_response_body(stock_name, portfolio_metrics):
    """
    Format the response body as a JSON.
    """
    return {
        "stock_name": stock_name,
        "portfolio_metrics": portfolio_metrics.to_dict(orient='columns')
    }

def create_successful_response(intent_request, response_body):
    """
    Create a successful response with JSON content.
    """
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "statusCode": 200,
            "body": json.dumps(response_body)
        },
    )

def create_error_response(intent_request, error_message):
    """
    Create an error response with plain text content.
    """
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": error_message,
        },
    )

    
def get_news_updates(intent_request):
    # Gets slots' values
    ticker = get_slots(intent_request)["stock_ticker"]
    
    # Logic for retrieving news updates based on the provided slots can be added here
    try:
        stock = yf.Ticker(ticker)

        # Return a message with the result (for now, a simple message is returned)
        return close(
            intent_request["sessionAttributes"],
            "Fulfilled",
            {
                "contentType": "PlainText",
                "content": f"Fetching news updates for {ticker}: {stock.news}",
            },
        )
    
    except Exception as e:
        # Handle errors, such as invalid stock symbol or network issues
        return close(
            intent_request["sessionAttributes"],
            "Fulfilled",
            {
                "contentType": "PlainText",
                "content": f"An error occurred while fetching stock news: {str(e)}",
            },
        )
        
    except Exception as ve:
        # Handle errors, such as invalid stock symbol or network issues
        return close(
            intent_request["sessionAttributes"],
            "Fulfilled",
            {
                "contentType": "PlainText",
                "content":  f"ValueError:{str(ve)}",
            },
        )    
        
def get_investment_recommendation(intent_request):
    # Extracting slot values from the intent request
    income_objective = intent_request["currentIntent"]["slots"]["income_objective"]
    investment_amount = intent_request["currentIntent"]["slots"]["investment_amount"]
    investment_horizon = intent_request["currentIntent"]["slots"]["investment_horizon"]
    risk_tolerance = intent_request["currentIntent"]["slots"]["risk_tolerance"]
    sector_preference = intent_request["currentIntent"]["slots"]["sector_preference"]

    # Generating investment recommendation based on slots or using a random recommendation
    recommendation = generate_investment_recommendation(income_objective, investment_amount, investment_horizon, risk_tolerance, sector_preference)

    # Return a message with the recommendation
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": f"Here is your investment recommendation: {recommendation}",
        },
    )        

# Function to generate investment recommendation based on slots
def generate_investment_recommendation(income_objective=None, investment_amount=None, investment_horizon=None, risk_tolerance=None, sector_preference=None):
    # Check if all slots are provided
    if all((income_objective, investment_amount, investment_horizon, risk_tolerance, sector_preference)):
        recommendations = [
            "Consider diversifying your portfolio with a mix of technology and healthcare stocks.",
            "For long-term growth, you may want to explore established companies in the renewable energy sector.",
            "Investing in a combination of large-cap and mid-cap stocks can provide a balanced risk-return profile.",
            "Explore opportunities in emerging markets for potential high returns, but be mindful of the associated risks.",
            "Consider adding blue-chip stocks with a history of consistent dividends for a stable income stream.",
        ]
        selected_recommendation = random.choice(recommendations)
        return f"Considering your preferences - Income Objective: {income_objective}, Investment Amount: {investment_amount}, Investment Horizon: {investment_horizon}, Risk Tolerance: {risk_tolerance}, Sector Preference: {sector_preference} - here is a specific recommendation - {selected_recommendation}"
   
### Intents Dispatcher ###
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    # Get the name of the current intent
    intent_name = intent_request["currentIntent"]["name"]

    # Dispatch to bot's intent handlers
    if intent_name == "GetStockQuote":
        return get_stock_quote(intent_request)
    elif intent_name == "GetMarketTrends":
        return get_market_trends(intent_request)
    elif intent_name == "StockPerformance":
        return get_stock_performance(intent_request)       
    elif intent_name == "NewsUpdates":
        return get_news_updates(intent_request) 
    elif intent_name == "GetInvestmentRecommendation":
        return get_investment_recommendation(intent_request)     
        
    raise Exception("Intent with name " + intent_name + " not supported")


### Main Handler ###
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    return dispatch(event)
