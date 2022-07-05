import re, sys, pickle
from rank_bm25 import *
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

lm = WordNetLemmatizer()
ps = PorterStemmer()


def spl_chars_removal(lst):
    lst1 = list()
    for element in lst:
        str = ""
        str = re.sub("[^a-zA-Z]", " ", element)
        lst1.append(str)
    return lst1


def stopwords_removal(lst):
    lst1 = list()
    for str in lst:
        text_tokens = word_tokenize(str)
        tokens_without_sw = [word for word in text_tokens if not word in stopwords]
        str_t = " ".join(tokens_without_sw)
        lst1.append(str_t)
    return lst1


def stemming_words(lst):
    lst1 = list()
    for str in lst:
        temp = ps.stem(str)
        if temp != "":
            lst1.append(temp)
    return lst1


def lemmatize_words(lst):
    lst1 = list()
    for str in lst:
        lst1.append(lm.lemmatize(str))
    return lst1


f = open("files/stopwords.txt")
stopwords = []
for word in f.readlines():
    word = word.strip()
    stopwords.append(word)
f.close()

f = open("files/problems_url.txt")
url = []
for word in f.readlines():
    word = word.strip()
    url.append(word)
f.close()

f = open("files/problems_titles.txt")
titles = []
for word in f.readlines():
    titles.append(word[:-2])
f.close()

print(len(titles))

corpus = []
n = len(titles)
for i in range(1, n + 1):
    f = open("files/problems/problem_text_" + str(i) + ".txt")
    doc = ""
    for line in f.readlines():
        doc += line
    corpus.append(line.lower())
    f.close()

tokenized_corpus = [
    stemming_words(
        lemmatize_words(stopwords_removal(spl_chars_removal(word_tokenize(doc))))
    )
    for doc in corpus
]
bm25 = BM25Okapi(tokenized_corpus)

# To save bm25 object
with open("results/bm25result", "wb") as bm25result_file:
    pickle.dump(bm25, bm25result_file)

with open("results/corpusresult", "wb") as corpusresult_file:
    pickle.dump(corpus, corpusresult_file)

with open("results/urlresult", "wb") as urlresult_file:
    pickle.dump(url, urlresult_file)

with open("results/titlesresult", "wb") as titlesresult_file:
    pickle.dump(titles, titlesresult_file)

with open("results/stopwordsresult", "wb") as stopwordsresult_file:
    pickle.dump(stopwords, stopwordsresult_file)
