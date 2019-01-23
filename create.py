from selenium import webdriver
from selenium.webdriver.support.ui import Select

driver = webdriver.Firefox()
driver.get("https://www.facebook.com/")
print "Done"
driver.find_element_by_xpath("//input[@id='u_0_1']").send_keys("Rose")
print "First name found by x path and value added"
print "First name found"
driver.find_element_by_xpath("//input[@id='u_0_3']").send_keys("Petal")
print "Sur name found"
driver.find_element_by_xpath("//input[@id='u_0_5']").send_keys("fbtestaccount_88@yahoo.com")
print "Mobile number or email address"
driver.find_element_by_xpath("//input[@id='u_0_8']").send_keys("fbtestaccount_88@yahoo.com")
print "re-enter Mobile number or email address"
driver.find_element_by_xpath("//input[@id='u_0_a']").send_keys("1q2w3e4r5t6y")
print "New Password"

day = Select(driver.find_element_by_id('day'))
day.select_by_visible_text("22")
print "Day Selected"

month = Select(driver.find_element_by_id('month'))
month.select_by_visible_text("Dec")
print "Month Selected"

year = Select(driver.find_element_by_id('year'))
year.select_by_visible_text("1988")
print "year Selected"


# Radio Button Selection for Gender
radio = driver.find_element_by_xpath("//input[@id='u_0_h']")
radio.click()
print "gender female selected"

# Click Create An Account
account = driver.find_element_by_xpath("//button[@id='u_0_e']")
account.click()
print "create account clicked"




