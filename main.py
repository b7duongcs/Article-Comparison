import streamlit as st
import pandas as pd
from newspaper import Article
from textblob import TextBlob
from googleNews import *

st.title("Article Comparison Tool")

if 'articles' not in st.session_state:
    st.session_state.articles = []
if 'can_compare' not in st.session_state:
    st.session_state.can_compare = False
if 'do_compare' not in st.session_state:
    st.session_state.do_compare = False

def genArticles():
    st.session_state.articles = getArticles(st.session_state.text_input)[0:50]
    st.session_state.can_compare = True
    st.session_state.do_compare = False

def interpretSentiment(sentiment):
    if sentiment < -0.8:
        return "Incredibly Negative"
    if sentiment < -0.6:
        return "Highly Negative"
    if sentiment < -0.4:
        return "Moderately Negative"
    if sentiment < -0.2:
        return "Somewhat Negative"
    if sentiment < 0:
        return "Slightly Negative"
    if sentiment < 0.2:
        return "Slightly Positive"
    if sentiment < 0.4:
        return "Somewhat Positive"
    if sentiment < 0.6:
        return "Moderately Positive"
    if sentiment < 0.8:
        return "Highly Positive"
    return "Incredibly Positive"

def getOverallSentiment(sentiments):
    total = 0
    numSentiments = len(sentiments)
    for sentiment in sentiments:
        total += sentiment
    return total/numSentiments

topic = st.text_input('Search for a topic', placeholder='', key="text_input", on_change=genArticles)

for article in st.session_state.articles:
    article['selected'] = st.checkbox("[{}]({})".format(article['title'], article['link']))

if st.session_state.can_compare:
    selected_articles = []
    keywords = []
    sentiments = []
    titles = []
    button = st.button("Compare Selected")
    if button:
        st.header("Summaries")
        st.session_state.do_compare = True
        for article in st.session_state.articles:
            if article['selected']:
                selected_articles.append(article)

        tab_titles = [article['publisher'] for article in selected_articles]
        tabs = st.tabs(tab_titles)
        for tab, selected_article in zip(tabs, selected_articles):
            with tab:
                titles.append(selected_article['title'])
                url = selected_article['link']
                article = Article(url)
                article.download()
                article.parse()
                article.nlp()
                
                st.header(article.title)
                st.write(article.summary)

                st.subheader("Keywords")
                key = article.keywords
                keywords.append(key)
                st.write(', '.join(key))

                blob = TextBlob(article.text)
                st.subheader("Sentiment")
                sentiment = blob.sentiment.polarity
                sentiments.append(sentiment)
                st.write(str(sentiment) + ": " + interpretSentiment(sentiment))
        
        st.header("Comparisons")

        st.subheader("Keyword Table")
        keyword_table_df = pd.DataFrame(keywords, index=titles)
        st.table(keyword_table_df.T)

        st.subheader("Sentiment Comparison")
        sentiment_df = pd.DataFrame({'Sentiment': sentiments}, index=titles)
        st.bar_chart(sentiment_df)

        st.subheader("Overall Sentiment")
        overall = getOverallSentiment(sentiments)
        interpretation = interpretSentiment(overall)
        st.write(str(overall) + ": " + interpretation)