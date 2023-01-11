import finnhub
import pandas as pd

class IsinHandler:
    def __init__(self, api_key: str):
        self.finnhub_client = finnhub.Client(api_key=api_key)

    def getInfoFromIsin(self, isin: str) -> pd.DataFrame:
        """
        Returns information corresponding to the provided
        ISIN.  
        Info contains:
        ---------------------------------------
        |description|displaySymbol|symbol|type|
        ---------------------------------------
        Raises a RuntimeError if no information on the isin is found

        :param isin     : The isin number for which to return information

        :returns        : DataFrame with information on the isin
        """
        info = self.finnhub_client.symbol_lookup(isin)

        if info['count'] < 1:
            raise RuntimeError

        return pd.DataFrame(info['result'])

    def getTickerForIsin(self, isin: str) -> str:
        """
        Returns the ticker for the provided <isin> traded in
        <currency>.

        :param isin     : Isin for which to return the ticker
        :param currency : Currency for which to return the ticker

        :returns        : Ticker for <isin> and <currency>
        """
        info_df = self.getInfoFromIsin(isin)

        # return only ticker for first result if multiple were found
        return info_df.loc[0, 'symbol']
