import pickle, re, sys
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

lm = WordNetLemmatizer()
ps = PorterStemmer()

with open("results/bm25result", "rb") as bm25result_file:
    bm25 = pickle.load(bm25result_file)

with open("results/urlresult", "rb") as urlresult_file:
    url = pickle.load(urlresult_file)

with open("results/titlesresult", "rb") as titlesresult_file:
    titles = pickle.load(titlesresult_file)

with open("results/corpusresult", "rb") as corpusresult_file:
    corpus = pickle.load(corpusresult_file)

with open("results/stopwordsresult", "rb") as stopwordsresult_file:
    stopwords = pickle.load(stopwordsresult_file)


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


query = str(sys.argv[1]).lower()
query = re.sub("[^a-zA-Z]", " ", query)
query = query.split(" ")
query = stopwords_removal(query)
query = lemmatize_words(query)
query = stemming_words(query)

n = len(titles)
docs = bm25.get_top_n(query, range(1, n + 1), 5)

ans = []
for i in docs:
    print(titles[i - 1])
    print(url[i - 1])
    print(corpus[i - 1])


# sum of the maximum elements of the resultant array
