from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt

class StockSentiment():
    
    def __init__(self, stock):
        self.finurl= 'https://finviz.com/quote.ashx?t='
        self.stock = stock
        
    def get_sentiment(self):
        ticker=self.stock
        news_tables = {}
        url = self.finurl + ticker
        req = Request(url=url, headers={'user-agent':'my-app'})
        response = urlopen(req)
        html  = BeautifulSoup(response, 'html')
        news_table = html.find(id='news-table')
        news_tables[ticker] = news_table
        
        parsed_data = []
        
        for ticker, news_table in news_tables.items():
            
            for row in news_table.findAll('tr'):
                if row.a == None:
                    continue
                else:
                    title = row.a.text
                    source = row.span.text
                    date_data = row.td.text.split(' ')
                    
                    if len(date_data) == 1:
                        time = date_data[0]
                    else:
                        date = date_data[0]
                        time = date_data[1]
                        
                parsed_data.append([ticker, date, time, title, source])
        
        df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title', 'source'])
        
        vader = SentimentIntensityAnalyzer()
        
        f = lambda title: vader.polarity_scores(title)['compound']
        df['vader_compound'] = df['title'].apply(f)
        
        df['date'] = pd.to_datetime(df.date).dt.date
        
        mean_df = df[['date', 'vader_compound']].copy()
        mean_df = mean_df.groupby(['date']).mean()
        val = mean_df['vader_compound'].mean()
        return val