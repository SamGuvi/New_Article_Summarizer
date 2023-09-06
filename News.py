from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from newspaper import Article
import nltk
import streamlit as st
import openai
import time

from newspaper import Config

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent

def Summarize(news_data):
    openai.api_key = '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'
    summarize = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f'Summarize in 5 lines "{news_data}"',
        max_tokens=1000,
        temperature=0.7,
    )
    return summarize.choices[0].text


Topic=st.selectbox('Topic',('Sports','Science','Politics','Business','Entertainment','Technology','Health'))

number=st.slider('Number of news',min_value=1,max_value=15,value=1)

if st.button('Summarize'):
    site = 'https://news.google.com/rss/search?q={}'.format(Topic)
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    
    for newses in range(0,number):  # printing news
        news=news_list[newses]
        Title=news.title.text
        Link=news.link.text
        news_data = Article(news.link.text,config=config)
        news_data.download()
        news_data.parse()
        summary=news_data.text.split('\n')
        summary="".join(summary).replace('\n','')
        #summary=Summarize(summary)
        
        image=news_data.top_image
        date=news.pubDate.text 
        st.image(image)   
        with st.expander(Title):
            
            st.write(summary)
            st.write(date)
            st.markdown(['[Read More]({})'.format(Link)])
        #time.sleep(20)
            
        
    
