import os
import time
import requests
from bs4 import BeautifulSoup
import urllib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary

class ImageScraper:
    def __init__(self):
        self.name = "a"

    def scrape_images(self, search_image, num_of_images):

        link = ""
        title = ""
        nameCounter = 0
        deeplink = ""
        image = search_image
        image_list = []

        # for img in soup.select("div a img"):
        #     link = img['src']
        #     nameCounter = nameCounter + 1
        #     image_url = link
        #     image_name = "Tzuyu_" + str(nameCounter)
        #     self.save_image(image_name, image_url)




        # ブラウザのオプションを格納する変数をもらってきます。
        options = Options()

        # Headlessモードを有効にする（コメントアウトするとブラウザが実際に立ち上がります）
        options.headless = True

        # ブラウザを起動する
        driver = webdriver.Chrome(options=options, excutable_path="/usr/local/lib/python3.6/dist-packages/chromedriver_binary/__init__.py")

        # ブラウザでアクセスする
        driver.get("https://www.google.com/search?q=" + image + "&tbm=isch")

        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #driver.execute_script("window.scrollTo(document.body.scrollHeight, document.body.scrollHeight + document.body.scrollHeight);")



        # HTMLを文字コードをUTF-8に変換してから取得します。
        html = driver.page_source.encode('utf-8')

        soup = BeautifulSoup(html, 'html.parser')


        print("selecting")
        print(image)
        selectedSoup = soup.select("#search a")

        for img in selectedSoup:
            if nameCounter >= num_of_images:
                driver.quit()
                break
            try:
                link = img["href"]
            except Exception as e:
                print(e)
                try:
                    link = img["src"]
                except Exception as e:
                    print(e)
                    continue

            if "imgurl" in link:

                print("\nYES\n")

                # ブラウザのオプションを格納する変数をもらってきます。
                options2 = Options()

                # Headlessモードを有効にする（コメントアウトするとブラウザが実際に立ち上がります）
                options2.headless = True

                # ブラウザを起動する
                driver2 = webdriver.Chrome(options=options2)

                # ブラウザでアクセスする
                driver2.get("https://www.google.com" + link)

                # HTMLを文字コードをUTF-8に変換してから取得します。
                html2 = driver2.page_source.encode('utf-8')

                soup2 = BeautifulSoup(html2, 'html.parser')


                deepimage = soup2.find("meta",  property="og:image")
                print("The img tag found. The url for the image is :\n")
                try:
                    deeplink = deepimage["content"]
                except Exception as e:
                    print(e)

                print(deeplink)

                nameCounter = nameCounter + 1
                image_url = deeplink
                #image_name = image + "_" + str(nameCounter)
                #self.save_image(image_name, image_url)

                image_list.append(image_url)

                driver2.quit()
                #END of if statement in for selectSoup loop
            #END of for selectSoup loop

        driver.quit()
        print("driver quit")

        return image_list


    # def save_image(self, file_name, item_link):
    #     with open(self.download_path + file_name + r".png", 'wb+') as image_file:
    #         req = urllib.request.Request(item_link, headers={'User-Agent': 'Mozilla/5.0'})
    #
    #         try:
    #             response = urllib.request.urlopen(req)
    #         except urllib.error.URLError as e:
    #             if hasattr(e, 'reason'):
    #                 print('We failed to reach a server.')
    #                 print('Reason: ', e.reason)
    #             elif hasattr(e, 'code'):
    #                 print('The server couldn\'t fulfill the request.')
    #                 print('Error code: ', e.code)
    #         else:
    #             #response = urllib.request.urlopen(item_link)
    #             image_file.write(response.read())
    #
    #
    #
    #     print(file_name)
    #     print(item_link)
    #
    #     time.sleep(0.01)


    # def take_input_from_user(self):
    #     searchKeyword = []
    #     numOfKeywordLoop = 0
    #     numOfKeywordLoop = int(input("How many kinds of images do you want(different search keyword)? : "))
    #     for i in range(numOfKeywordLoop):
    #         searchKeyword.append(input("What images do you want?" + "\n" + str(i) + " : "))
    #     print(searchKeyword)
    #     num_of_images = int(input("how many images do you want for each search? : "))
    #     return searchKeyword, num_of_images


if __name__ == '__main__':
    scraper = ImageScraper()
    searchKeyword, num_of_images = scraper.take_input_from_user()
    for keyword in searchKeyword:
        scraper.scrape_images(search_image = keyword, num_of_images = num_of_images)
