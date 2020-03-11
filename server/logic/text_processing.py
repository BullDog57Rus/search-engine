import re
from typing import List

import nltk as nltk

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')


def lemmatization_preprocess(text: str) -> List[str]:
    return _remove_stop_words(_lemmatize(_tokenize(_normalize(text))))


def simple_preprocess(text: str) -> List[str]:
    return _remove_stop_words(_tokenize(_normalize(text)))


def _normalize(text: str) -> str:
    text = re.sub("\\d+", " ", text.lower())
    text = re.sub("_+", " ", text)
    text = re.sub("[^\\w*]+", " ", text)
    text = re.sub(" +", " ", text)
    return text


def _tokenize(text: str) -> List[str]:
    return nltk.word_tokenize(text)


def _lemmatize(tokens: List[str]) -> List[str]:
    lemmatizer = nltk.stem.WordNetLemmatizer()
    return [lemmatizer.lemmatize(t) for t in tokens]


def _remove_stop_words(tokens: List[str]) -> List[str]:
    stop_words = set(nltk.corpus.stopwords.words("english"))
    return [t for t in tokens if t not in stop_words]
