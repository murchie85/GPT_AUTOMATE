from bs4 import BeautifulSoup
import requests
import psycopg2
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def scrape_forex():
    url = 'https://www.forex.com/en-uk/market-analysis/latest-research'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    prices = soup.find_all('span', class_='market-card__item__price')
    forex_prices = []
    for price in prices:
        forex_prices.append(float(price.text))
    return forex_prices

def connect_to_db():
    conn = psycopg2.connect(
        host="localhost",
        database="forex",
        user="postgres",
        password="password")
    return conn

def insert_forex_prices(prices):
    conn = connect_to_db()
    cur = conn.cursor()
    for price in prices:
        cur.execute("INSERT INTO forex_data (price) VALUES (%s)", [price])
    conn.commit()
    cur.close()
    conn.close()

def get_forex_data():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT price FROM forex_data")
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append(row[0])
    cur.close()
    conn.close()
    return data[:500]

def get_forex_dataframe():
    conn = connect_to_db()
    sql_query = "SELECT * FROM forex_data"
    df = pd.read_sql(sql_query, conn)
    return df

#################################################################

if __name__ == '__main__':
    forex_prices = scrape_forex()
    insert_forex_prices(forex_prices)
    data = get_forex_data()
    df = get_forex_dataframe()
    
    ##JOB_COMPLETE##