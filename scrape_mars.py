from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd


#get first news headline and paragraph from Mars News URL
url = 'https://mars.nasa.gov/news/'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

results = soup.find_all("div", class_="image_and_description_container")
body_text_list = []

for result in results:
    title=result.find("div", class_="rollover_description_inner").text
    body_text_list.append(title)

first_news_headline_paragraph=body_text_list[0].strip()

news_titles = []

results = soup.find_all(class_="img-lazy")

for img in soup.find_all('img', alt=True):
    news=(img['alt'])
    print(news)
    news_titles.append(news)

revised_news_headlines = []

for x in news_titles:
    if x != "More" and x !="":
        revised_news_headlines.append(x)

first_news_headline=revised_news_headlines[0]

html = ""

executable_path = {'executable_path': 'C:/Users/Hoess/test-script/chromedriver'}

with Browser('chrome', **executable_path, headless=True) as browser:
#use Splinter to get big featured image
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

    xpath = '//div[contains(@class,"image_and_description_container")]//div[contains(@class,"img")]/img'
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()

    xpath_expand= '//a[@class="fancybox-expand"]'
    results = browser.find_by_xpath(xpath_expand)
    full_size_img = results[0]
    full_size_img.click()

    html = browser.html

soup = BeautifulSoup(html, 'html.parser')

image = soup.find("div", class_="fancybox-inner fancybox-skin fancybox-dark-skin fancybox-dark-skin-open")
full_size_image = image.find("img")
full_size_url = full_size_image["src"]

full_url_to_full_size_image = jpl_url + full_size_url

#use Pandas to scrape Space Facts

url="https://space-facts.com/mars/"
df = pd.read_html(url)[0]
df.columns = ['Category', 'Values']
df.set_index('Category', inplace=True)
html_table = df.to_html()
html_table.replace('\n', '')
df.to_html('table.html')

#get Mars Weather

mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
response = requests.get(mars_weather_url)
weather_soup = BeautifulSoup(response.text, 'html.parser')

mars_weather_tweet = weather_soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})

weather = mars_weather_tweet.find_all("div", class_="js-tweet-text-container")

for item in weather:
    mars_weather=item.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    

mars_dictionary = {"mars_news_headline" : first_news_headline, "mars_news_paragraph" : first_news_headline_paragraph, "current_mars_weather" : mars_weather}




