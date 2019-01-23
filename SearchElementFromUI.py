from selenium import webdriver
from selenium.webdriver.common.keys import Keys


driver = webdriver.Firefox()
driver.get("http://stackoverflow.com/")
html_source = driver.page_source
Search = driver.find_element_by_xpath("//h1[contains(@id,'h-top-questions')]").text
print Search
driver.find_element_by_xpath("//input[contains(@name,'q')]").send_keys(Search , Keys.RETURN)
delay = 5
print "Enter pressed"
if "results" and "Search" in html_source:
    print "results and Search Found"
else:
    print "results and Search not Found"
#result = driver.find_element_by_xpath("//span[@class='results-label']").text
driver.quit()

