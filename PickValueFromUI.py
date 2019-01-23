from selenium import webdriver

driver = webdriver.Firefox()
driver.get("http://selenium-python.readthedocs.io/locating-elements.html")
element_by_class_name =  driver.find_element_by_xpath("//cite[contains(.,'find_element_by_class_name')]").text
print element_by_class_name
element_by_css = driver.find_element_by_xpath("//cite[contains(.,'find_element_by_css_selector')]").text
print element_by_css
driver.quit()

