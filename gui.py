import tkinter as tk
from tkinter import ttk, messagebox
import requests

# Базовый URL
BASE_URL = "http://localhost:8000"

def create_mushroom():
    name = entry_name.get()
    edible = var_edible.get()
    weight = int(entry_weight.get())
    freshness = int(entry_freshness.get())

    if freshness < 0 or freshness > 10:
        messagebox.showerror("Ошибка", "Свежесть должна быть от 0 до 10")
        return

    data = {
        "name": name,
        "edible": edible,
        "weight": weight,
        "freshness": freshness
    }
    response = requests.post(f"{BASE_URL}/mushrooms/", json=data)
    if response.status_code == 200:
        messagebox.showinfo("Успех", "Гриб создан!")
        refresh_mushrooms()
    else:
        messagebox.showerror("Ошибка", response.json().get("detail", "Ошибка при создании гриба"))

def create_basket():
    owner = entry_owner.get()
    capacity = int(entry_capacity.get())

    data = {
        "owner": owner,
        "capacity": capacity
    }
    response = requests.post(f"{BASE_URL}/baskets/", json=data)
    if response.status_code == 200:
        messagebox.showinfo("Успех", "Корзинка создана!")
        refresh_baskets()
    else:
        messagebox.showerror("Ошибка", response.json().get("detail", "Ошибка при создании корзинки"))

def add_mushroom_to_basket():
    basket_id = int(entry_basket_id.get())
    mushroom_id = int(entry_mushroom_id.get())

    response = requests.post(f"{BASE_URL}/baskets/{basket_id}/add?mushroom_id={mushroom_id}")
    if response.status_code == 200:
        messagebox.showinfo("Успех", "Гриб добавлен в корзинку!")
        refresh_baskets()
    else:
        messagebox.showerror("Ошибка", response.json().get("detail", "Ошибка при добавлении гриба"))

def remove_mushroom_from_basket():
    basket_id = int(entry_basket_id_remove.get())
    mushroom_id = int(entry_mushroom_id_remove.get())

    response = requests.delete(f"{BASE_URL}/baskets/{basket_id}/remove?mushroom_id={mushroom_id}")
    if response.status_code == 200:
        messagebox.showinfo("Успех", "Гриб удален из корзинки!")
        refresh_baskets()
    else:
        messagebox.showerror("Ошибка", response.json().get("detail", "Ошибка при удалении гриба"))

def refresh_mushrooms():
    response = requests.get(f"{BASE_URL}/mushrooms/")
    if response.status_code == 200:
        mushrooms = response.json()
        for row in tree_mushrooms.get_children():
            tree_mushrooms.delete(row)
        for mushroom in mushrooms:
            tree_mushrooms.insert("", "end", values=(
                mushroom["id"], mushroom["name"], mushroom["edible"], mushroom["weight"], mushroom["freshness"]
            ))

def refresh_baskets():
    response = requests.get(f"{BASE_URL}/baskets/")
    if response.status_code == 200:
        baskets = response.json()
        for row in tree_baskets.get_children():
            tree_baskets.delete(row)
        for basket in baskets:
            tree_baskets.insert("", "end", values=(
                basket["id"], basket["owner"], basket["capacity"], basket["mushrooms"]
            ))

# Создание основного окна
root = tk.Tk()
root.title("Управление грибами и корзинками")

# Вкладки
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Вкладка для грибов
tab_mushrooms = ttk.Frame(notebook)
notebook.add(tab_mushrooms, text="Грибы")

# Поля для создания гриба
tk.Label(tab_mushrooms, text="Название:").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(tab_mushrooms)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(tab_mushrooms, text="Съедобный:").grid(row=1, column=0, padx=5, pady=5)
var_edible = tk.BooleanVar()
tk.Checkbutton(tab_mushrooms, variable=var_edible).grid(row=1, column=1, padx=5, pady=5)

tk.Label(tab_mushrooms, text="Вес:").grid(row=2, column=0, padx=5, pady=5)
entry_weight = tk.Entry(tab_mushrooms)
entry_weight.grid(row=2, column=1, padx=5, pady=5)

tk.Label(tab_mushrooms, text="Свежесть (0-10):").grid(row=3, column=0, padx=5, pady=5)
entry_freshness = tk.Entry(tab_mushrooms)
entry_freshness.grid(row=3, column=1, padx=5, pady=5)

tk.Button(tab_mushrooms, text="Создать гриб", command=create_mushroom).grid(row=4, column=0, columnspan=2, pady=10)

# Таблица для грибов
columns = ("id", "name", "edible", "weight", "freshness")
tree_mushrooms = ttk.Treeview(tab_mushrooms, columns=columns, show="headings")
for col in columns:
    tree_mushrooms.heading(col, text=col)
tree_mushrooms.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Вкладка для корзинок
tab_baskets = ttk.Frame(notebook)
notebook.add(tab_baskets, text="Корзинки")

# Поля для создания корзинки
tk.Label(tab_baskets, text="Владелец:").grid(row=0, column=0, padx=5, pady=5)
entry_owner = tk.Entry(tab_baskets)
entry_owner.grid(row=0, column=1, padx=5, pady=5)

tk.Label(tab_baskets, text="Вместимость:").grid(row=1, column=0, padx=5, pady=5)
entry_capacity = tk.Entry(tab_baskets)
entry_capacity.grid(row=1, column=1, padx=5, pady=5)

tk.Button(tab_baskets, text="Создать корзинку", command=create_basket).grid(row=2, column=0, columnspan=2, pady=10)

# Поля для добавления гриба в корзинку
tk.Label(tab_baskets, text="ID корзинки:").grid(row=3, column=0, padx=5, pady=5)
entry_basket_id = tk.Entry(tab_baskets)
entry_basket_id.grid(row=3, column=1, padx=5, pady=5)

tk.Label(tab_baskets, text="ID гриба:").grid(row=4, column=0, padx=5, pady=5)
entry_mushroom_id = tk.Entry(tab_baskets)
entry_mushroom_id.grid(row=4, column=1, padx=5, pady=5)

tk.Button(tab_baskets, text="Добавить гриб в корзинку", command=add_mushroom_to_basket).grid(row=5, column=0, columnspan=2, pady=10)

# Поля для удаления гриба из корзинки
tk.Label(tab_baskets, text="ID корзинки:").grid(row=6, column=0, padx=5, pady=5)
entry_basket_id_remove = tk.Entry(tab_baskets)
entry_basket_id_remove.grid(row=6, column=1, padx=5, pady=5)

tk.Label(tab_baskets, text="ID гриба:").grid(row=7, column=0, padx=5, pady=5)
entry_mushroom_id_remove = tk.Entry(tab_baskets)
entry_mushroom_id_remove.grid(row=7, column=1, padx=5, pady=5)

tk.Button(tab_baskets, text="Удалить гриб из корзинки", command=remove_mushroom_from_basket).grid(row=8, column=0, columnspan=2, pady=10)

# Таблица для корзинок
columns = ("id", "owner", "capacity", "mushrooms")
tree_baskets = ttk.Treeview(tab_baskets, columns=columns, show="headings")
for col in columns:
    tree_baskets.heading(col, text=col)
tree_baskets.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

# Обновление данных при запуске
refresh_mushrooms()
refresh_baskets()

# Запуск цикла
root.mainloop()