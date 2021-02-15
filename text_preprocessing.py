import re
import string

from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vectorizer = TfidfVectorizer()


# Text Processing
def cleanhtml(raw_html):
    cleanr = re.compile("<.*?>")
    raw_html = raw_html.replace("&nbsp", "")
    cleantext = re.sub(cleanr, ' ', raw_html)
    return cleantext.lower()


def remove_character_special(text):
    text = text.replace('\\t', " ").replace('\\n', " ").replace('\\u', " ").replace('\\', "")
    text = text.encode('ascii', 'replace').decode('ascii')
    text = ' '.join(re.sub("([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)", " ", text).split())
    return text.replace("http://", " ").replace("https://", " ")


def remove_number(text):
    return re.sub(r"\d+", "", text)


def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))


def remove_whitespace_LT(text):
    return text.strip()


def remove_whitespace_multiple(text):
    return re.sub('\s+', ' ', text)


def remove_singl_char(text):
    return re.sub(r"\b[a-zA-Z]\b", "", text)


def stopwords_remover(text):
    list_stopwords = stopwords.words('indonesian')
    list_stopwords.extend([
        "yg", "dg", "rt", "dgn", "ny", "d", 'klo',
        'kalo', 'amp', 'biar', 'bikin', 'bilang',
        'gak', 'ga', 'krn', 'nya', 'nih', 'sih',
        'si', 'tau', 'tdk', 'tuh', 'utk', 'ya',
        'jd', 'jgn', 'sdh', 'aja', 'n', 't',
        'nyg', 'hehe', 'pen', 'u', 'nan', 'loh', 'rt',
        '&amp', 'yah'
    ])
    words = text.split(" ")
    for word in words:
        return " ".join([word for word in words if word not in list_stopwords])


def word_stemmer(text):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    return stemmer.stem(text)


def text_processing(text):
    text = cleanhtml(text)
    text = remove_character_special(text)
    text = remove_number(text)
    text = remove_punctuation(text)
    text = stopwords_remover(text)
    text = remove_whitespace_LT(text)
    text = remove_whitespace_multiple(text)
    text = remove_singl_char(text)
    text = word_stemmer(text)
    return text


def get_processed_text(data):
    new_data = []
    for item in data:
        text = list(item.keys())[1]
        if text is not None and len(text) > 0:
            new_item_text = text_processing(item[text])
            new_data.append({"id": item['id'], text: new_item_text})
    return new_data


def get_related_text(queryset_list, keyword, number=10):
    clean_data = get_processed_text(queryset_list)
    dct = [data[list(data.keys())[1]] for data in clean_data]
    X = vectorizer.fit_transform(dct)
    keyword = text_processing(keyword)
    keyword_vec = vectorizer.transform([keyword])
    results = cosine_similarity(X, keyword_vec).reshape((-1,))
    index_list = list(results.argsort()[-number:][::-1])
    return [clean_data[i]['id'] for i in index_list]
