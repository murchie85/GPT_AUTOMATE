import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# Connect to Mongo DB
client = MongoClient('localhost', 27017)
db = client.forex_db
forex_collection = db.forex_collection


def get_forex_prices():
    """
    Retrieves forex prices from various sources and stores them in the database
    """
    forex_sources = {
        'EUR/USD': 'https://www.investing.com/currencies/eur-usd',
        'GBP/USD': 'https://www.investing.com/currencies/gbp-usd',
        'USD/JPY': 'https://www.investing.com/currencies/usd-jpy',
        'AUD/USD': 'https://www.investing.com/currencies/aud-usd'
    }

    # Scrape the forex prices from the sources
    for currency_pair, url in forex_sources.items():
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the forex price from the scraped data
        forex_price = soup.find('span', {'id': 'last_last'}).text

        # Add the forex price to the database
        forex_collection.insert_one({
            'currency_pair': currency_pair,
            'price': forex_price
        })


def predict_next_prices():
    """
    Implements a basic prediction algorithm using historical data to predict next prices for the next five days
    """
    # Retrieve historical forex prices from the database
    forex_prices = forex_collection.find()

    # Convert the forex prices to a list
    forex_prices_list = [price for price in forex_prices]

    # Predict the next forex prices for the next five days using a naive algorithm
    predicted_prices = []
    for i in range(1, 6):
        next_price = float(forex_prices_list[-1]['price']) + ((i/100) * float(forex_prices_list[-1]['price']))
        predicted_prices.append(next_price)

    return predicted_prices


def store_predicted_prices(predicted_prices):
    """
    Stores the predicted forex prices in the database
    """
    for i, price in enumerate(predicted_prices):
        forex_collection.insert_one({
            'currency_pair': f'Predicted_{i+1}_day',
            'price': price
        })


def main():
    """
    Main function for scraping forex prices and predicting next prices
    """
    get_forex_prices()
    predicted_prices = predict_next_prices()
    store_predicted_prices(predicted_prices)


if __name__ == '__main__':
    main()##JOB_COMPLETE##