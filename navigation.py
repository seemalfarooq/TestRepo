from selenium import webdriver


driver = webdriver.Firefox()
driver.get("https://www.facebook.com/")
print "Done"
driver.find_element_by_id("email")
print "email found"
element = driver.find_element_by_id("pass")
print "pass found"
driver.find_element_by_xpath("//input[@id='email']")
print "email found by xpath"
driver.find_element_by_xpath("//input[@id='pass']")
print "password found by xpath"
driver.quit()

