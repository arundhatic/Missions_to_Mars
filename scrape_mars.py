from splinter import Browser
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time


def scrape():
    
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # NASA Mars News
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    time.sleep(3)

    html = browser.html
    nsoup = bs(html, 'html.parser')
    lists = nsoup.find_all('li', class_='slide')
    
    html = browser.html
    nsoup = bs(html, "html.parser")
    
    content_title = lists[0].find('div', class_='content_title')
    news_title = content_title.text.strip()
    #print (news_title)
    
    article_teaser_body = lists[0].find('div', class_='article_teaser_body')
    news_p = article_teaser_body.text.strip()
    #print(news_p)
    
    # JPL Mars Space Images
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    jpl_html = browser.html
    jsoup = bs(jpl_html, 'html.parser')
    img_link = jsoup.find(
        'div', class_='carousel_container').article.footer.a['data-fancybox-href']
    base_link = jsoup.find('div', class_='jpl_logo').a['href'].rstrip('/')
    featured_image_title = jsoup.find(
        'h1', class_="media_feature_title").text.strip()
    featured_image_url = base_link + img_link
    
    # Mars Weather
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    result = requests.get(weather_url)
    # make it text
    html = result.text
    # create BeautifulSoup object and parse
    wsoup = bs(html, 'html.parser')
    # get the weather from the newest tweet
    weather_tweet = wsoup.find(class_='tweet-text').get_text()
    
    # to remove the extra substring at the end of the tweet text
    if (weather_tweet.find('pic.twitter.com/UeOmoDjhf3') == -1): 
        mars_weather = weather_tweet
    else: 
        mars_weather = weather_tweet.replace('pic.twitter.com/UeOmoDjhf3', '.'); 
     
    #print(mars_weather) 
    
    
     # Mars Facts
    fact_url = "http://space-facts.com/mars/"
    fact_table = pd.read_html(fact_url)
    mars_fact_table = fact_table[0]
    mars_fact_table_html = mars_fact_table.to_html(header=False, index=False)
    mars_fact_table_html = mars_fact_table_html.replace('\n', '')
    #print(mars_fact_table_html + '\n')
    
     # Mars Hemispheres
    hem_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hem_url)
    urls = [(a.text, a['href']) for a in browser
            .find_by_css('div[class="description"] a')]
    hemisphere_image_urls = []
    for title, url in urls:
        hemisphere_dict = {}
        hemisphere_dict['title'] = title
        browser.visit(url)
        img_url = browser.find_by_css('img[class="wide-image"]')['src']
        hemisphere_dict['img_url'] = img_url
        hemisphere_image_urls.append(hemisphere_dict)
    
    #print(hemisphere_image_urls)

    browser.quit()
    
    # organising the data in a dictionary
    mars_data = {}
    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p
    mars_data["featured_image_url"] = featured_image_url
    mars_data["mars_weather"] = mars_weather
    mars_data["mars_fact_table_html"] = mars_fact_table_html
    mars_data["hemisphere_image_urls"] = hemisphere_image_urls
    
    return mars_data

# for debugging
#def main():
    #scrape()
    
#if __name__ == "__main__":
    #main()


