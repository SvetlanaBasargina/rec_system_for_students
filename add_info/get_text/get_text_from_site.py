import urllib.request
from bs4 import BeautifulSoup
import re
import nltk
from pymystem3 import Mystem


def no_puctuation(text):
    return re.sub(r'[^\w\s]', '', text)


def no_stopwords(text):
    token_no_stopwords = []
    for word in text:
        if not word in nltk.corpus.stopwords.words('russian'):
            token_no_stopwords.append(word)
    return token_no_stopwords


def use_mystem(text):
    text = ' '.join(text)
    m = Mystem()
    text = m.lemmatize(text)
    return ''.join(text)


def text_fields_processing(text):
    text = text.lower()
    all_words = no_puctuation(text).split()
    all_words_no_stopwords = no_stopwords(all_words)
    text = use_mystem(all_words_no_stopwords).split()
    return text


def get_text(url = "https://online-olimpiada.ru/itogi/"):
    with urllib.request.urlopen(url) as url:
        html = url.read()
    soup = BeautifulSoup(html)

    for script in soup(["script", "style"]):
        script.extract()

    title = soup.title.get_text()
    text = soup.get_text()

    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text