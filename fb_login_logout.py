from selenium import webdriver
import time


driver = webdriver.Firefox()
driver.get("https://www.facebook.com/")

#Login
driver.find_element_by_id("email").send_keys("fbtestaccount_88@yahoo.com")
driver.find_element_by_id("pass").send_keys("1q2w3e4r5t6y")
login = driver.find_element_by_xpath("//input[@value='Log In']")
login.click()
print "login clicked"
assert 'Facebook' in driver.title
print "Facebook found in title"
time.sleep (5)

#logout
click_on_down_arrow  = driver.find_element_by_xpath("//div[@id='userNavigationLabel']")
click_on_down_arrow.click()
print "click_on_down_arrow "
time.sleep (5)

logout = driver.find_element_by_link_text('Log out')
#logout = driver.find_element_by_xpath("//span[contains(.,'Log out')]")
print "element found"
logout.click()
print "logout clicked"


pop_up = driver.find_element_by_xpath("//button[contains(.,'OK')]")
print "OK located"

pop_up.click()
print "completely logged out"

driver.quit()