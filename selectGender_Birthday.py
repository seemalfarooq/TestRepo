from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By



driver = webdriver.Firefox()
driver.get("https://www.facebook.com/")

day = Select(driver.find_element_by_id('day'))
day.select_by_visible_text("14")
print "Day Selected"

month = Select(driver.find_element_by_id('month'))
month.select_by_visible_text("Nov")
print "Month Selected"

year = Select(driver.find_element_by_id('year'))
year.select_by_visible_text("1985")
print "year Selected"


# Radio Button Selection for Gender
radio = driver.find_element_by_xpath("//input[@id='u_0_h']")
radio.click()
print "gender female selected"

# Click Create An Account
account = driver.find_element_by_xpath("//button[@id='u_0_e']")
account.click()
print "create account clicked"



# Click Login
login = driver.find_element_by_xpath("//input[@value='Log In']")
login.click()
print "Login clicked"




