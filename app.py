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

if os.name == 'nt':
    config.read(os.path.expanduser('C:\\settings.ini'))
else:
    config.read(os.path.expanduser('~/.config/settings.ini'))

browser = selenium.webdriver.Chrome()

path = [TicketswapLogin, TicketPageRefresh, Notify]
for step in path:
    current_step = step(config, browser)
    try:
        current_step.Execute()
    except Exception as e:
        logger.exception(e)
