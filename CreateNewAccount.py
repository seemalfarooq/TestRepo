from selenium import webdriver


driver = webdriver.Firefox()
driver.get("https://www.facebook.com/")
print "Done"
driver.find_element_by_xpath("//input[@id='u_0_1']").send_keys("Test Account")
print "First name found by x path and value added"
print "First name found"
driver.find_element_by_xpath("//input[@id='u_0_3']").send_keys("Test Account")
print "Sur name found"
driver.find_element_by_xpath("//input[@id='u_0_5']").send_keys("Test Account")
print "Mobile number or email address"
driver.find_element_by_xpath("//input[@id='u_0_8']").send_keys("Test Account")
print "re-enter Mobile number or email address"
driver.find_element_by_xpath("//input[@id='u_0_a']").send_keys("Test Account")
print "New Password"
driver.find_element_by_xpath("//select[@id='day']")
print "Day"
driver.find_element_by_xpath("//select[@id='month']")
print "Month"
driver.find_element_by_xpath("//select[@id='year']")
print "year"
driver.find_element_by_xpath("//input[@id='u_0_h']")
print "gender female"
driver.find_element_by_xpath("//button[@id='u_0_e']")
print "create account"




# from selenium import webdriver
# from selenium.webdriver.common.by import By
#
# driver = webdriver.Firefox()
# driver.get("https://www.facebook.com/")
# print "Done"
# element = (By.ID, 'u_0_e')
# print "create account button found"

