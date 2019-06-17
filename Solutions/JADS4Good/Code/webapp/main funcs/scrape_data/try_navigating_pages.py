from selenium.webdriver import Chrome

# Please download chromedriver for windows to this directory (scrape_data)
path = 'chromedriver.exe'
browser = Chrome(path)
browser.get('https://www.nationaalrapporteur.nl/publicaties/')

flag = 1
excep = 0
while flag <= 10:
    excep = 0
    try:
        result = browser.find_element_by_css_selector('#content > ul > li.next').find_element_by_tag_name("a")
        print(result.text)
        result.click()
        browser.implicitly_wait(3)
        browser.switch_to.window(browser.window_handles[0])
    except:
        print("Error")
        excep = 1
        browser.close()
        break
    flag += 1
    print("Switched to page ", flag, " done")

if excep == 0:
    browser.close()