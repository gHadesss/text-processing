import json
import codecs
import pandas as pd
import numpy as np
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from typing import Iterable

class Solution:
    def __init__(self):
        with codecs.open("dev-dataset-task2024-04.json", "r", "utf-8") as file:
            data = json.load(file)
        self.data = data
        nltk.download('stopwords')
        self.tfidf = TfidfVectorizer(stop_words=nltk.corpus.stopwords.words("russian"))
        X_data = [entry[0] for entry in data]
        y_data = [entry[1] for entry in data]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X_data, y_data, test_size=0.01, random_state=42)
        # self.tfidf = TfidfVectorizer()
        true_unique = np.unique(self.y_train).shape[0]
        X = self.tfidf.fit_transform(self.X_train)

        self.kmeans = KMeans(n_clusters=true_unique, random_state=42, max_iter=100)
        self.kmeans.fit(X, self.y_train)


    def predict(self, text: str) -> int:
        news_vector = self.tfidf.transform([text])
        cluster = self.kmeans.predict(news_vector)
        return int(cluster[0])

    def f1_metric(self, n: int, predict: set[int], expect: set[int]) -> float:
        r, p = 0, 0
        j = predict
        i = expect

        tmp = len(i & j) ** 2
        r += tmp / len(i)
        p += tmp / len(j)

        p /= n
        r /= n
        if p == 0 or r == 0:
            return 0

        return 2 * p * r / (p + r)

    def test(self) -> None:
        predict = set([self.predict(entry) for entry in self.X_test])
        expect = set([int(entry) for entry in self.y_test])
        n = len(self.y_test)
        print(self.f1_metric(n, predict, expect))

        print(expect)
        print(predict)

if __name__ == "__main__":
    Solution().test()
