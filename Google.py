from selenium import webdriver


driver = webdriver.Firefox()
driver.get("http://www.google.com/")
print "Done"
driver.close()
print "Closed and going to quit"
driver.quit()
