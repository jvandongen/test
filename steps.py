import gettext
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Init:
    def __init__(self, config, browser):
        self.config = config
        self.browser = browser
        if self.config.get('ticketswap', 'language').lower() == 'dutch':
            nl = gettext.translation('steps', localedir='locale', languages=['nl'])
            nl.install()
        elif self.config.get('ticketswap', 'language').lower() == 'english':
            en = gettext.translation('steps', localedir='locale', languages=['en'])
            en.install()
        elif self.config.get('ticketswap', 'language').lower() == 'spanish':
            es = gettext.translation('steps', localedir='locale', languages=['es'])
            es.install()
        elif self.config.get('ticketswap', 'language').lower() == 'german':
            de = gettext.translation('steps', localedir='locale', languages=['de'])
            de.install()
        else:
            nl = gettext.translation('steps', localedir='locale', languages=['nl'])
            nl.install()

    def Execute(self):
        raise NotImplementedError()

class TicketswapLogin(Init):
    def Execute(self):
        self.browser.get(self.config.get('ticketswap', 'eventurl'))
        login_with_facebook = self.browser.find_element_by_link_text(_('Inloggen'))
        login_with_facebook.click()
        login_with_facebook2 = self.browser.find_element_by_class_name('login-button--facebook')
        login_with_facebook2.click()
        self.browser.switch_to_window(self.browser.window_handles[1])
        email = self.browser.find_element_by_id('email')
        email.send_keys(self.config.get('ticketswap', 'username'))
        password = self.browser.find_element_by_id('pass')
        password.send_keys(self.config.get('ticketswap', 'password'))
        login = self.browser.find_element_by_name('login')
        login.click()
        self.browser.switch_to_window(self.browser.window_handles[0])
        time.sleep(3)

class TicketPageRefresh(Init):
    def Execute(self):
        status = True
        while status == True:
            time.sleep(int(self.config.get('ticketswap', 'delay')))
            self.browser.get(self.config.get('ticketswap', 'ticketurl'))
            available = self.browser.find_element_by_class_name('counter-value').text
            print(_("Er zijn %s tickets te koop") % available)

            if available == '0':
                status == True
            else:
                count = 0
                item = self.browser.find_element_by_class_name('listings-item')
                item.click()
                status2 = True
                while status2 == True:
                    try:
                        buy = WebDriverWait(self.browser, 0.8).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-buy")))
                        buy.click()
                        status = False
                        status2 = False
                    except:

                        unavailable = self.browser.find_element_by_class_name('listing-unavailable').text
                        if _('afrekenen') not in unavailable:
                            print(_("Tickets zijn verkocht, terug naar overzicht voor %s") % self.config.get('ticketswap', 'ticketname'))
                            status = True
                            status2 = False
                        else:
                            count = count + 1
                            print(_("Iemand anders is aan het afrekenen, refreshing... (%s)") % count)
                            self.browser.refresh()
        ideal = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "button--success")))
        ideal.click()
        
class Notify(Init):
    def Execute(self):
        os.system('say "You are ready to buy your tickets"')
