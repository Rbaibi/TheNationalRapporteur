from selenium.webdriver import Chrome
import pandas as pd
import requests

# Please download chromedriver for windows to this directory (scrape_data)
path = 'chromedriver.exe'

data_dir = "../data/"
browser = Chrome(path)
browser.get('https://www.nationaalrapporteur.nl/publicaties/index.aspx?select=5&q=&df=01-01-0001&dt=31-12-9999&dctermsType=&kw=&dl=False&SortBy=Datum')


excep = 0
try:
    results = browser.find_element_by_css_selector('#content > div.common.results')
    links = results.find_elements_by_tag_name("a")


    print('Link: ', 10)

    element = browser.find_element_by_css_selector('#content > div.common.results').find_elements_by_tag_name("a")[9]
    element.click()
    browser.implicitly_wait(3)
    browser.switch_to.window(browser.window_handles[0])


    news = browser.find_elements_by_css_selector("#content > div > h1")[0].text
    meta = browser.find_elements_by_css_selector("#content > div > p")[0].text

    block = browser.find_element_by_css_selector('#content > div')
    divs = block.find_elements_by_tag_name("div")

    paras = []
    downloads = []
    pdfs = []
    intro = []
    misc = []
    downloaded_data = []
    for i in range(len(divs)):
        tex = divs[i]
        if tex.get_attribute("class") == "intro":
            try:
                intro.append(tex.text)
            except:
                empty_list = []
                intro.append(empty_list)
        elif tex.get_attribute("class") == "paragraph":
            try:
                paras.append(tex.text)
            except:
                empty_list = []
                paras.append(empty_list)
        elif tex.get_attribute("class") == "download":
            try:
                downloads.append(tex.text)
                link = tex.find_element_by_css_selector('a').get_attribute('href')
                print(link)
                filename = link.split("binaries/")[1]

                pdfs.append(filename)
                r = requests.get(link)
                with open(data_dir + filename, "wb") as code:
                    code.write(r.content)
                print(link)
            except:
                print("Download error")
                empty_list = []
                downloads.append(empty_list)
                pdfs.append(empty_list)
        else:
            try:
                misc.append(tex.text)
            except:
                empty_list = []
                misc.append(empty_list)
    downloaded_data.append([news, meta, intro, paras, downloads, pdfs, misc])

except:
    excep = 1
    print("Exception")
    browser.close()


if excep == 0:
    browser.close()

# Save data in a pandas dataframe
df = pd.DataFrame(downloaded_data, columns=['News', 'Meta', 'Intro', 'Article', 'Downloads', 'PDFs', 'Misc'])
print(df)