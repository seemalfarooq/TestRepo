from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select



class Facebook:

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.get("https://www.facebook.com/")

    def log_in(self, username, password):
        self.driver.find_element_by_id("email").send_keys(username)
        self.driver.find_element_by_id("pass").send_keys(password)
        login = self.driver.find_element_by_xpath("//input[@value='Log In']")
        login.click()
        print "login clicked"
        assert 'Facebook' in self.driver.title
        print "Facebook found in title"
        time.sleep(5)

    def log_out(self):
        click_on_down_arrow = self.driver.find_element_by_xpath("//div[@id='userNavigationLabel']")
        click_on_down_arrow.click()
        print "click_on_down_arrow "
        time.sleep(5)
        logout = self.driver.find_element_by_link_text('Log out')
        print "element found"
        logout.click()
        print "logout clicked"
        pop_up = self.driver.find_element_by_xpath("//button[contains(.,'OK')]")
        print "OK located"
        pop_up.click()
        print "completely logged out"

    def createAccount(self):
        self.driver.find_element_by_xpath("//input[@id='u_0_1']").send_keys("Rose")
        print "First name found by x path and value added"
        self.driver.find_element_by_xpath("//input[@id='u_0_3']").send_keys("Petal")
        print "Sur name found"
        self.driver.find_element_by_xpath("//input[@id='u_0_5']").send_keys("fbtestaccount_88@yahoo.com")
        print "Mobile number or email address"
        self.driver.find_element_by_xpath("//input[@id='u_0_8']").send_keys("fbtestaccount_88@yahoo.com")
        print "re-enter Mobile number or email address"
        self.driver.find_element_by_xpath("//input[@id='u_0_a']").send_keys("1q2w3e4r5t6y")
        print "New Password"
        day = Select(self.driver.find_element_by_id('day'))
        day.select_by_visible_text("22")
        print "Day Selected"
        month = Select(self.driver.find_element_by_id('month'))
        month.select_by_visible_text("Dec")
        print "Month Selected"
        year = Select(self.driver.find_element_by_id('year'))
        year.select_by_visible_text("1988")
        print "year Selected"
        # Radio Button Selection for Gender
        radio = self.driver.find_element_by_xpath("//input[@id='u_0_h']")
        radio.click()
        print "gender female selected"
        # Click Create An Account
        account = self.driver.find_element_by_xpath("//button[@id='u_0_e']")
        account.click()
        print "create account clicked"

    def tearDown(self):
        self.driver.quit()


logsin = Facebook()
logsin.log_in('fbtestaccount_88@yahoo.com','1q2w3e4r5t6y')
logsin.log_out()
logsin.tearDown()