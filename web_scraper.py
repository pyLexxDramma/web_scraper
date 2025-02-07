import requests
import warnings
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import scrolledtext
from functools import partial  # Импортируем partial
import webbrowser

# Отключаем предупреждения о незащищенных запросах
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

# Список URL-адресов и их названий
urls = {
    'Разработка': 'https://netology.ru/development',
    'Маркетинг': 'https://netology.ru/marketing',
    'Управление': 'https://netology.ru/management',
    'Дизайн': 'https://netology.ru/design',
    'Наука о данных': 'https://netology.ru/data-science',
    'Управление командой': 'https://netology.ru/soft-skills',
    'Креатив': 'https://netology.ru/creative',
    'Новые курсы': 'https://netology.ru/new-courses',
    'Финансы': 'https://netology.ru/finance'
}


def open_url(url):
    webbrowser.open(url)
    show_courses()  # Возвращаемся к выбору курсов после открытия ссылки


def scrape_courses(url, title):
    output_text.delete(1.0, tk.END)  # Очищаем текстовое поле
    try:
        # Выполняем HTTP-запрос к странице
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Проверяем, успешен ли запрос

        # Создаем объект BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим все элементы, содержащие информацию о курсах
        titles = soup.select('div.programCard_title__8kC_1')  # Селектор для названий курсов

        if not titles:
            output_text.insert(tk.END, f"Курсы не найдены на странице: {url}\n")
        else:
            for title in titles:
                course_title = title.get_text(strip=True)
                course_url = title.find_parent('a')['href']  # Получаем ссылку на курс
                full_url = f"https://netology.ru{course_url}"  # Формируем полный URL
                button = tk.Button(output_text, text=course_title, command=partial(open_url, full_url), relief='raised',
                                   bd=2, bg='lightgreen')
                button.pack(anchor='center', padx=10, pady=5,
                            fill=tk.X)  # Добавляем кнопку в текстовое поле с отступами
                button.bind("<Enter>", lambda e: e.widget.config(bg='lightgray',
                                                                 cursor='hand2'))  # Изменение цвета и курсора при наведении
                button.bind("<Leave>", lambda e: e.widget.config(bg='lightgreen'))  # Возврат цвета при уходе

    except requests.exceptions.RequestException as e:
        output_text.insert(tk.END, f'Ошибка при запросе к {url}: {e}\n')


# Создаем главное окно
root = tk.Tk()
root.title("Веб-скрепер Нетологии")
root.configure(bg='lightblue')  # Устанавливаем голубой фон

# Заголовок
header = tk.Label(root, text="Образовательные курсы в Нетологии", font=("Arial", 16, "bold"), bg='lightblue',
                  fg='darkblue')
header.pack(pady=10)

# Кнопка "Выберите направление обучения"
select_button = tk.Button(root, text="Выберите направление обучения", command=lambda: show_courses(), bg='lightgray',
                          relief='raised', bd=2)
select_button.pack(pady=5)


def show_courses(selected_title=None):
    # Очищаем текстовое поле перед выводом направлений
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "Направления обучения:\n\n")

    # Удаляем предыдущие кнопки, если они есть
    for widget in output_text.winfo_children():
        widget.destroy()

    # Создаем фрейм для кнопок направлений
    frame = tk.Frame(output_text, bg='lightblue')
    frame.pack(fill=tk.BOTH, expand=True)

    # Создаем кнопки для каждого направления
    for title, url in urls.items():
        button = tk.Button(frame, text=title, command=partial(scrape_courses, url, title), relief='raised', bd=2)
        button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)  # Добавляем кнопку в фрейм с отступами
        button.bind("<Enter>", lambda e: e.widget.config(bg='lightgray',
                                                         cursor='hand2'))  # Изменение цвета и курсора при наведении
        button.bind("<Leave>", lambda e: e.widget.config(bg='white'))  # Возврат цвета при уходе

        # Если это выбранное направление, меняем цвет кнопки
        if title == selected_title:
            button.config(bg='green', fg='white')


# Создаем текстовое поле для вывода данных
output_text = scrolledtext.ScrolledText(root, width=80, height=20, bg='white')
output_text.pack(pady=10, fill=tk.BOTH, expand=True)

# Запускаем главный цикл приложения
root.mainloop()
