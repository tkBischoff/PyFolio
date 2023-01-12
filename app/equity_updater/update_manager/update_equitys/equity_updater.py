import finnhub
import time

import pandas as pd
from datetime import date, datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist

from update_manager.models import Security, SecurityPrice
from update_manager.update_equitys.isin_handler import IsinHandler 


class EquityUpdater:
    def __init__(self, equityIsins: str, finnhubApiKey: str, logger):
        """
        :param securityIsins : Path to the csv with securityIsins
        :param finnhubApiKey : API Key for finnhub.com
        :param logger        : logger instance
        """
        self.finnhub_client = finnhub.Client(api_key=finnhubApiKey)
        self.isinHandler = IsinHandler(finnhubApiKey)

        # use only US equitys as the free version of the
        # Finnhub only provides data for those
        equityIsins = pd.read_csv(equityIsins)
        self.equityIsins = equityIsins[equityIsins['ISIN'].str.startswith('US')]

        self.logger = logger

        # set begin date one year in the past as that is the 
        # allowed timeframe for the free Finnhub API
        self.beginDate = date.today() - timedelta(days=364)

    def queryHistoricalData(self, ticker: str, start: date, end: date) -> pd.DataFrame:
        """
        Queries historical data for <ticker> in the timeframe
        between <start> and <end>.
        Start can not be one year in the past when using a 
        free finnhub account.
        """
        if (date.today() - start).days > 355:
            raise ValueError("Start date is more than one year in the past")


        # convert start and end to UNIX timestamps
        start = int( time.mktime(start.timetuple()) )
        end = int( time.mktime(end.timetuple()) )

        # get historical data from finnhub
        data = self.finnhub_client.stock_candles(ticker, 'D', start, end)
        data = pd.DataFrame(data)

        # rename columns
        data = data.rename({'c':'close', 
                            'h': 'high', 
                            'l': 'low', 
                            'o': 'open', 
                            't':'date', 
                            'v': 'volume'}, axis='columns')

        # drop status
        data = data.drop('s', axis='columns')

        # unix timestamp to date
        data['date'] = data['date'].apply(lambda x: datetime.utcfromtimestamp(x).date())

        return data

    def getMostRecentEntryDate(self, ticker: str) -> date:
        """
        Returns the date of the most recent entry in the database
        for the specified ticker.

        :param ticker : ticker of the security for which to return the most
                        recent date.

        :returns      : date of the most recent entry for ticker
        """

        # get all price entries for ticker
        priceEntries = Security.objects.get(ticker=ticker).securityprice_set.all()

        # raise a ValueError if no entries exist
        if len(priceEntries) == 0:
            raise ValueError("No entries for {}".format(ticker))

        # get latest entry
        latestEntry = priceEntries.order_by('-date')[0]

        return latestEntry.date

    def queryEquityData(self, ticker: str) -> pd.DataFrame:
        """
        Returns the equity data for the specified ticker starting at
        date of the most recent entry to the current date.
        The data is queried from investing.com and contains the 
        open, close, low, high, adj_open, adj_close, adj_low, adj_high
        of the security in a daily frequency.

        :param ticker       : ticker for which to query data
        :param startingAt   : Date from which to start querying data

        :returns            : pd.DataFrame with the security data
        """
        # get the date of the latest price entry for ticker
        try:
            latestEntryDate = self.getMostRecentEntryDate(ticker)

        # TODO: Use model specific exception
        except ObjectDoesNotExist:
            # if there is not yet an entry for ticker
            self.logger.info("No entry for {}".format(ticker))
            latestEntryDate = date.today() - timedelta(days=355)

        currentDate = date.today()

        # query historical data
        data = self.queryHistoricalData(ticker, 
                                        latestEntryDate + timedelta(days=1), 
                                        currentDate)

        if len(data) == 0:
            raise ValueError(
                    "No data for {} between {} and {}".format(ticker,
                                                              latestEntryDate,
                                                              currentDate)
                    )
        else:
            return data
                                

    def insertDataInDb(self, ticker: str, currency: str, name: str, data: pd.DataFrame):
        """
        Inserts the security data for ticker into the database

        :param ticker   : Ticker for which to add the data
        :param data     : Data to add to the database
        """
        try:
            security = Security.objects.get(ticker=ticker)

        # TODO: Use model specific exception
        except ObjectDoesNotExist:
            # if there is not yet a Security entry for ticker
            # create one
            security = Security(ticker=ticker,
                                currency=currency,
                                name=name)
            security.save()

        for _, row in data.iterrows():
            sp = SecurityPrice(
                    date=row['date'],
                    open=row['open'],
                    high=row['high'],
                    low=row['low'],
                    close=row['close'],
                    volume=row['volume'],
                    security=security
                )
            sp.save()

    def updateStocks(self):
        """
        Updates all securities listed in the securityIsins csv file
        so the database contains the security price data
        for every security up to the current date, starting
        at self.beginDate.
        """
        self.logger.info("Started updating equities")

        for _, row in self.equityIsins[:10].iterrows():
            isin = row['ISIN']
            name = row['NAME']
            currency = 'USD' # TODO: currency for other countries
            
            # get ticker for ISIN
            try:
                ticker = self.isinHandler.getTickerForIsin(isin)
            except RuntimeError as e:
                self.logger.warning(e)
                continue
            
            # get missing equity data
            try:
                equityData = self.queryEquityData(ticker)
            except ValueError as e:
                self.logger.warning(e)
                continue

            # insert data in database
            self.insertDataInDb(ticker, currency, name, equityData)

            # sleep for 1s to not surpass 60 API calls per minute 
            time.sleep(1.0)
