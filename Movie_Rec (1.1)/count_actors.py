import pandas as pd
from collections import Counter

def analyze_actors_frequency(filename='top_250.xlsx', column='Актеры', top_n=20):
    # Читаем Excel
    df = pd.read_excel(filename)
    
    # Проверяем, что столбец есть
    if column not in df.columns:
        print(f"Столбец '{column}' не найден в файле.")
        return
    
    # Собираем всех актёров в один список
    all_actors = []
    for actors_str in df[column].dropna():
        # Разделяем строку по запятым и убираем лишние пробелы
        actors = [actor.strip() for actor in actors_str.split(',')]
        all_actors.extend(actors)
    
    # Считаем частоту
    counter = Counter(all_actors)
    
    # Выводим топ-N
    print(f"Топ-{top_n} самых часто встречающихся актёров:")
    for actor, count in counter.most_common(top_n):
        print(f"{actor}: {count} раз(а)")
    
    # Можно сохранить результат в Excel
    result_df = pd.DataFrame(counter.most_common(), columns=['Актёр', 'Количество'])
    result_df.to_excel('count_actors.xlsx', index=False)
    print("\nРезультаты сохранены в 'count_actors.xlsx'")   

if __name__ == "__main__":
    analyze_actors_frequency()
