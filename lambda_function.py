### Required Libraries ###
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
     # Gets slots' values
    stock_name = get_slots(intent_request)["stock_name"]
    
    # Return a message with the result (for now, a simple message is returned)
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": "get_stock_performance! (Stock Performance Logic to be implemented)",
        },
    )
    
def get_news_updates(intent_request):
    # Gets slots' values
    news_location = get_slots(intent_request)["news_location"]
    news_source = get_slots(intent_request)["news_source"]
    news_topic = get_slots(intent_request)["news_topic"]
    time_frame = get_slots(intent_request)["time_frame"]

    # Your logic for retrieving news updates based on the provided slots can be added here

    # Return a message with the result (for now, a simple message is returned)
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": f"Fetching news updates for {news_topic} in {news_location} from {news_source} {time_frame}. (News Updates Logic to be implemented)",
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
