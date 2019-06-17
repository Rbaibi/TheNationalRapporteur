from selenium.webdriver import Chrome

# Please download chromedriver for windows to this directory (scrape_data)
path = 'chromedriver.exe'
browser = Chrome(path)
browser.get('https://www.nationaalrapporteur.nl/Over/medewerkers/')
excep = 0
try:
    result = browser.find_element_by_class_name('common')
    elementList = result.find_elements_by_tag_name("li")
    for i in range(len(elementList)):
        element = browser.find_element_by_class_name('common').find_elements_by_tag_name("li")[i]
        print(element.text)

    # result.click()
    # browser.implicitly_wait(3)
    # browser.switch_to.window(browser.window_handles[0])
except:
    print("Error")
    excep = 1
    browser.close()

if excep == 0:
    browser.close()