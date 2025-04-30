from typing import List, Tuple, Set
import nltk
from nltk.stem.snowball import *
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer as wnl
from Levenshtein import distance

class Solution:
    def is_eng_lang(self, line: str) -> bool:
        english_letters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        russian_letters = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")

        english_count = sum(1 for char in line if char in english_letters)
        russian_count = sum(1 for char in line if char in russian_letters)

        if english_count > russian_count:
            return True
        else:
            return False


    def detect(self, tracks: List[Tuple[List[str], str]]) -> List[Set[Tuple[int, int]]]:
        nltk.download('punkt_tab')
        nltk.download('wordnet')

        ru_stemmer = RussianStemmer()
        eng_wnl = wnl()
        ans = []

        for track in tracks:
            normalized_track = []
            for track_line in track[0]:
                is_eng = self.is_eng_lang(track_line)
                tokens = word_tokenize(track_line, language=("english" if is_eng else "russian"))
                normalized_tokens = [(eng_wnl.lemmatize(word)) if is_eng else ru_stemmer.stem(word) for word in tokens]

                norm_line = " "
                parenth_fl = False
                for word in normalized_tokens:
                    if word == '(':
                        parenth_fl = True
                    if not parenth_fl:
                        norm_line = norm_line + word + " "
                    if word == ')':
                        parenth_fl = False

                normalized_track.append(norm_line.strip())

            dist_matrices = []

            for i in range(2, min(21, len(normalized_track))):
                dist_matrix = []
                for j in range(len(normalized_track) - i + 1):
                    candidate = ' '.join(normalized_track[j:j + i]).strip()

                    if len(candidate) == 0:
                        candidate = ' '

                    dist_row = []
                    for k in range(len(normalized_track) - i + 1):
                        current_lines = ' '.join(normalized_track[k:k + i]).strip()

                        if len(current_lines) == 0:
                            current_lines = ' '

                        dist_row.append(distance(candidate, current_lines) / max(len(candidate), len(current_lines)))
                    dist_matrix.append(dist_row)
                dist_matrices.append(dist_matrix)

            threshold = 0.076
            max_score = -1
            chorus_len = 0
            first_occurance = -1

            for i in range(len(dist_matrices)):
                for j in range(len(dist_matrices[i])):
                    cur_score = sum(1 for num in dist_matrices[i][j] if num < threshold) - 1

                    if max_score <= cur_score:
                        max_score = cur_score
                        chorus_len = i + 2
                        first_occurance = j

            track_ans = []
            for i in range(len(dist_matrices[chorus_len - 2][first_occurance])):
                if dist_matrices[chorus_len - 2][first_occurance][i] < threshold:
                    track_ans.append((i, i + chorus_len - 1))

            ans.append(set(track_ans))
        return ans
