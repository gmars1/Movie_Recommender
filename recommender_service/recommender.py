import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity

class MovieRecommender:
    def __init__(self, xlsx_path='backend/filmsDBDataFiller/top_250.xlsx'):
        self.movies = pd.read_excel(xlsx_path)
        required_cols = {'Название (русское)', 'Рейтинг', 'Жанр', 'Актеры'}
        if not required_cols.issubset(self.movies.columns):
            raise ValueError(f'В файле должны быть столбцы: {required_cols}')
        # Преобразуем жанры и актёров в списки
        self.movies['Жанр_list'] = self.movies['Жанр'].astype(str).str.split(', ')
        self.movies['Актеры_list'] = self.movies['Актеры'].astype(str).str.split(', ')
        # Векторизация жанров
        self.genre_mlb = MultiLabelBinarizer()
        self.genre_matrix = self.genre_mlb.fit_transform(self.movies['Жанр_list'])
        # Векторизация актёров
        self.actors_mlb = MultiLabelBinarizer()
        self.actors_matrix = self.actors_mlb.fit_transform(self.movies['Актеры_list'])

    def recommend(self, title, top_n=5):
        idx = self.movies[self.movies['Название (русское)'] == title].index
        if len(idx) == 0:
            return []
        idx = idx[0]
        # Схожесть по жанрам
        genre_sim = cosine_similarity(
            self.genre_matrix[idx].reshape(1, -1), self.genre_matrix
        ).flatten()
        # Схожесть по актёрам
        actors_sim = cosine_similarity(
            self.actors_matrix[idx].reshape(1, -1), self.actors_matrix
        ).flatten()
        # Нормируем рейтинг
        ratings = self.movies['Рейтинг']
        ratings_norm = (ratings - ratings.min()) / (ratings.max() - ratings.min())
        # Итоговый скор: жанры 0.6, актёры 0.3, рейтинг 0.1
        final_score = 0.6 * genre_sim + 0.3 * actors_sim + 0.1 * ratings_norm
        final_score[idx] = -1  # исключаем сам фильм
        similar_indices = final_score.argsort()[-top_n:][::-1]
        return self.movies.iloc[similar_indices]['Название (русское)'].tolist()

recommender = MovieRecommender()

# if __name__ == "__main__":
#     recommender = MovieRecommender()
#     test_title = "Бойцовский клуб"  # Подставь реальное название из твоего файла
#     recommendations = recommender.recommend(test_title, top_n=5)
#     print(f"Рекомендации для '{test_title}':")
#     for title in recommendations:
#         print(title)
