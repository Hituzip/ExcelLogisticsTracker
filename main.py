import tkinter as tk
from tkinter import filedialog

from modules.nmb import nmb_column_sum
from modules.logocenter import logocenter_column_sum
from modules.dry import dry_column_sum

data = {
    "НМБ металлопрокат": [0, 0, 0],
    "Логоцентр металлопрокат": [0, 0, 0],
    "Сухой порт слябы": [0, 0, 0],
    "Сухой порт рулоны": [0, 0, 0],
    "Сухой порт контейнеры": [0, 0, 0],
    "Сухой порт контейнеры гружёные": [0, 0, 0],
    "Сухой порт контейнеры (марганец)": [0, 0, 0]
}

recent_files = []  # Список для хранения последних 5 файлов

root = tk.Tk()
root.title("Интерфейс")

selected_type = tk.StringVar()
selected_category = tk.StringVar()


def process_file():
    """Обрабатывает выбранный файл и обновляет данные."""
    file_path = filedialog.askopenfilename(
        filetypes=[("Excel Files", "*.xlsx;*.xls")]
    )
    if not file_path:
        return

    # Обновляем список последних файлов
    recent_files.insert(0, file_path)
    if len(recent_files) > 5:
        recent_files.pop()  # оставляем только 5 последних
    update_recent_files()

    type_value = selected_type.get()
    category_value = selected_category.get()

    if type_value == "Логоцентр":
        if category_value == "Остатки":
            data["Логоцентр металлопрокат"][0] += logocenter_column_sum(
                file_path, "G"
            )
        elif category_value == "Отгрузки":
            data["Логоцентр металлопрокат"][1] += logocenter_column_sum(
                file_path, "P"
            )
        elif category_value == "Поступление":
            data["Логоцентр металлопрокат"][2] += logocenter_column_sum(
                file_path, "V"
            )
    elif type_value == "НМБ":
        new_values = nmb_column_sum(file_path)
        data["НМБ металлопрокат"] = [
            sum(x) for x in zip(data["НМБ металлопрокат"], new_values)
        ]
    elif type_value == "Сухой порт":
        dry_mapping = {
            "Остатки": "A, D",
            "Отгрузки": "B, E",
            "Поступление": "G, J"
        }
        dry_result = dry_column_sum(file_path, dry_mapping[category_value])
        dry_key_to_data = {
            "Контейнер": "Сухой порт контейнеры",
            "Рулон": "Сухой порт рулоны",
            "Слябы": "Сухой порт слябы",
            "Контейнер груженый": "Сухой порт контейнеры гружёные",
            "Контейнер (марганец)": "Сухой порт контейнеры (марганец)"
        }
        for key, value in dry_result.items():
            data_key = dry_key_to_data.get(key)
            if data_key is not None:
                idx = ["Остатки", "Отгрузки", "Поступление"].index(
                    category_value
                )
                multiplier = 1000 if "Контейнер" in key else 1  # умножаем только контейнеры
                data[data_key][idx] += round(value * multiplier, 4)

    update_table()


def update_table():
    """Обновляет таблицу на экране с текущими данными."""
    for i, (key, values) in enumerate(data.items()):
        table_labels[i][0].config(text=key, anchor="w")
        for j, value in enumerate(values):
            table_labels[i][j + 1].config(text=str(value))


def toggle_category():
    """Включает или отключает выбор категории в зависимости от типа."""
    state = tk.NORMAL if selected_type.get() != "НМБ" else tk.DISABLED
    for btn in category_buttons:
        btn.config(state=state)


def update_recent_files():
    """Обновляет виджет списка последних загруженных файлов."""
    listbox_recent.delete(0, tk.END)
    for f in recent_files:
        listbox_recent.insert(tk.END, f)


# --- Создание таблицы результатов ---
frame_table = tk.Frame(root)
frame_table.pack(pady=10)

headers = ["Объект", "Остатки", "Отгрузки", "Поступление"]
for col, text in enumerate(headers):
    tk.Label(
        frame_table,
        text=text,
        borderwidth=1,
        relief="solid",
        padx=10,
        pady=5,
        font=("Arial", 10, "bold"),
        width=9
    ).grid(row=0, column=col)

table_labels = []
for i, (key, values) in enumerate(data.items(), start=1):
    row_labels = []
    lbl_key = tk.Label(
        frame_table,
        text=key,
        borderwidth=1,
        relief="solid",
        padx=10,
        pady=5,
        anchor="w",
        width=30
    )
    lbl_key.grid(row=i, column=0, sticky="w")
    row_labels.append(lbl_key)

    for j, value in enumerate(values):
        lbl = tk.Label(
            frame_table,
            text=str(value),
            borderwidth=1,
            relief="solid",
            padx=10,
            pady=5,
            width=10
        )
        lbl.grid(row=i, column=j + 1)
        row_labels.append(lbl)

    table_labels.append(row_labels)


# --- Контейнер для выбора типа и категории ---
frame_controls = tk.Frame(root)
frame_controls.pack(pady=10)

frame_type = tk.Frame(frame_controls)
frame_type.pack(side=tk.LEFT, padx=20)

frame_category = tk.Frame(frame_controls)
frame_category.pack(side=tk.LEFT, padx=20)

# Выбор типа (слева)
tk.Label(
    frame_type,
    text="Выберите тип",
    font=("Arial", 10, "bold")
).pack(anchor="w")

types = ["Логоцентр", "НМБ", "Сухой порт"]
for t in types:
    tk.Radiobutton(
        frame_type,
        text=t,
        variable=selected_type,
        value=t,
        command=toggle_category
    ).pack(anchor="w")

# Выбор категории (справа)
tk.Label(
    frame_category,
    text="Выберите категорию",
    font=("Arial", 10, "bold")
).pack(anchor="w")

category_buttons = []
categories = ["Остатки", "Отгрузки", "Поступление"]
for c in categories:
    btn = tk.Radiobutton(
        frame_category,
        text=c,
        variable=selected_category,
        value=c
    )
    btn.pack(anchor="w")
    category_buttons.append(btn)

# --- Кнопка выбора файла ---
tk.Button(
    root,
    text="Выбрать файл",
    command=process_file,
    font=("Arial", 10, "bold"),
    padx=10,
    pady=5
).pack(pady=10)

# --- Виджет для отображения последних 5 файлов ---
frame_recent = tk.Frame(root)
frame_recent.pack(pady=10, fill=tk.X)

tk.Label(
    frame_recent,
    text="Последние загруженные файлы:",
    font=("Arial", 10, "bold")
).pack(anchor="w")

listbox_recent = tk.Listbox(frame_recent, height=5, width=80)
listbox_recent.pack(fill=tk.X)

root.mainloop()
