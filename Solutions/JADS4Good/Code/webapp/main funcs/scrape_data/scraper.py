from selenium.webdriver import Chrome
import pandas as pd
import requests

# Please download chromedriver for windows to this directory (scrape_data)
path = 'chromedriver.exe'
browser = Chrome(path)

# The website to download from
browser.get('https://www.nationaalrapporteur.nl/publicaties/')

# Directory to save data
data_dir = "../data/"

# list to append data to (later converted to dataframe)
downloaded_data = []

# Keep track of page number
flag = 1

# Check if exceptions occur
excep_outer = 0

while flag <= 10:
    print("Page ", flag)

    # Check if exceptions occur
    excep_inner = 0

    # Block to navigate from one page to next
    # Check if not first page. If True, then navigate to next page.
    if flag != 1:
        try:
            result = browser.find_element_by_css_selector('#content > ul > li.next').find_element_by_tag_name("a")
            result.click()
            browser.implicitly_wait(3)
            browser.switch_to.window(browser.window_handles[0])
        except:
            excep_outer = 1
            browser.close()
            print("Exception category 1")
            break

    # Block to navigate from one link to the enxt in a single page
    try:
        results = browser.find_element_by_css_selector('#content > div.common.results')
        # Find number of articles in a page
        links = results.find_elements_by_tag_name("a")


        for i in range(len(links)):

            paras = []
            downloads = []
            pdfs = []
            intro = []
            misc = []

            # Open link 'i' in page 'flag'
            print('Link: ', i + 1)
            element = browser.find_element_by_css_selector('#content > div.common.results').find_elements_by_tag_name("a")[i]
            element.click()
            browser.implicitly_wait(3)
            browser.switch_to.window(browser.window_handles[0])

            # Get header of page (article title)
            try:
                news = browser.find_elements_by_css_selector("#content > div > h1")[0].text
            except:
                news = browser.find_elements_by_css_selector("#main > div.header > div > h1")[0].text

            # Get article meta-data
            meta = browser.find_elements_by_css_selector("#content > div > p")[0].text

            # Get actual content of page
            block = browser.find_element_by_css_selector('#content > div')
            divs = block.find_elements_by_tag_name("div")

            # Loop through content chunks and check type
            for j in range(len(divs)):
                tex = divs[j]

                # Intro paragraph
                if tex.get_attribute("class") == "intro":
                    try:
                        intro.append(tex.text)
                    except:
                        empty_list = []
                        intro.append(empty_list)

                # Content paragraph
                elif tex.get_attribute("class") == "paragraph":
                    try:
                        paras.append(tex.text)
                    except:
                        empty_list = []
                        paras.append(empty_list)

                # Download pdfs and get pdf related data
                elif tex.get_attribute("class") == "download":
                    try:
                        downloads.append(tex.text)
                        link = tex.find_element_by_css_selector('a').get_attribute('href')
                        filename = link.split("binaries/")[1]
                        pdfs.append(filename)
                        r = requests.get(link)
                        with open(data_dir + filename, "wb") as code:
                            code.write(r.content)
                    except:
                        print("Download Error")
                        empty_list = []
                        downloads.append(empty_list)
                        pdfs.append(empty_list)

                # If there's other type of content
                else:
                    try:
                        misc.append(tex.text)
                    except:
                        empty_list = []
                        misc.append(empty_list)

            # append article info to list
            downloaded_data.append([news, meta, intro, paras, downloads, pdfs, misc])
            browser.back()


    except:
        excep_inner = 1
        print("Exception category 2")
        browser.close()
        break

    flag += 1

if excep_inner == 0 or excep_outer == 0:
    browser.close()

# Save data in a pandas dataframe
df = pd.DataFrame(downloaded_data, columns=['News', 'Meta', 'Intro', 'Article', 'Downloads', 'PDFs', 'Misc'])
df.to_csv(data_dir + "data.csv", sep="\t")