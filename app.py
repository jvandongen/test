import configparser
import logging
import os
import selenium
from steps import (
    TicketswapLogin,
    TicketPageRefresh,
    Notify
)

logger = logging.getLogger(__name__)
config = configparser.ConfigParser()
config.read(os.path.expanduser('settings.ini'))
browser = selenium.webdriver.Chrome()

path = [TicketswapLogin, TicketPageRefresh, Notify]
for step in path:
    current_step = step(config, browser)
    try:
        current_step.Execute()
    except Exception as e:
        logger.exception(e)
