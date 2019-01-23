from selenium import webdriver


driver = webdriver.Firefox()
driver.implicitly_wait(10)
driver.get("http://stackoverflow.com/")
Search = driver.find_element_by_xpath("//h1[contains(@id,'h-top-questions')]").text
print Search
driver.quit()
