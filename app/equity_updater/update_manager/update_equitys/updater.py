from datetime import datetime
import logging
import os

from apscheduler.schedulers.background import BackgroundScheduler
from update_manager.update_equitys.equity_updater import EquityUpdater

logger = logging.getLogger(__name__)
isinFile = "update_manager/update_equitys/all_isins_trade_repulic.csv"

finnhub_key = os.getenv('FINNHUB_API_KEY')

def start():
    """
    Start the scheduler for updating the equities in the db
    """
    logger.info("Started scheduler")
    updater = EquityUpdater(isinFile, finnhub_key, logger)
    scheduler = BackgroundScheduler()

    scheduler.add_job(updater.updateStocks, 'interval', days=1)
    scheduler.start()
