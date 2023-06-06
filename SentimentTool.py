from langchain.tools import BaseTool
from StockSentiment import StockSentiment

class SentimentTool(BaseTool):
    name = "Stock Sentiment Analyzer"
    description = "takes an input of an individual stock ticker and return the week's aggregate stock sentiment"
    
    def _run(self, ticker:str):
        analyzer = StockSentiment(ticker)
        return analyzer.get_sentiment()
    
    def _arun(self, ticker:str):
        raise NotImplementedError("This tool currently does not support Async")