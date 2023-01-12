import os
import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)

finnhub_key = os.getenv('FINNHUB_API_KEY')
isinFile = "update_manager/update_equitys/all_isins_trade_repulic.csv"

class UpdateManagerConfig(AppConfig):
    name = 'update_manager'

    def ready(self):
        # TODO: use scheduler
        from .update_equitys import updater
        from update_manager.update_equitys.equity_updater import EquityUpdater

        # update DB once on startup
        eq_updater = EquityUpdater(isinFile, finnhub_key, logger)
        eq_updater.updateStocks()

        # start scheduler
        updater.start()
