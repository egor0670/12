import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

# --- Основная логика приложения ---
class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("600x500")
        self.data = [] # Список для хранения расходов в памяти

        # --- Создание виджетов ---
        self.create_widgets()
        self.load_data() # Пробуем загрузить данные при запуске

    def create_widgets(self):
        # Рамка для ввода данных
        input_frame = ttk.LabelFrame(self.root, text="Добавить расход")
        input_frame.pack(pady=10, fill="x")

        # Сумма
        ttk.Label(input_frame, text="Сумма:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_sum = ttk.Entry(input_frame)
        self.entry_sum.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Категория
        ttk.Label(input_frame, text="Категория:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.combo_category = ttk.Combobox(input_frame, values=["Еда", "Транспорт", "Развлечения", "Жильё", "Здоровье"])
        self.combo_category.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.combo_category.current(0)

        # Дата
        ttk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_date = ttk.Entry(input_frame)
        self.entry_date.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        # Кнопка добавления
        ttk.Button(input_frame, text="Добавить расход", command=self.add_expense).grid(row=3, columnspan=2, pady=10)

        # Таблица расходов
        self.tree = ttk.Treeview(self.root, columns=("sum", "category", "date"), show='headings')
        self.tree.heading("sum", text="Сумма")
        self.tree.heading("category", text="Категория")
        self.tree.heading("date", text="Дата")
        
        # Добавляем скроллбар
        yscroll = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=yscroll.set)
        
        self.tree.pack(pady=10, fill="both", expand=True)
        yscroll.pack(side="right", fill="y")

        # Рамка для управления данными
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=5)

        # Кнопки сохранения и загрузки JSON
        ttk.Button(control_frame, text="Сохранить в JSON", command=self.save_to_json).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Загрузить из JSON", command=self.load_data).pack(side="left", padx=5)

    # --- Функции работы с данными ---
    def add_expense(self):
        """Добавляет новый расход после валидации."""
        try:
            sum_text = self.entry_sum.get()
            if not sum_text:
                raise ValueError("Сумма не может быть пустой.")
            sum_ = float(sum_text)
            if sum_ <= 0:
                raise ValueError("Сумма должна быть положительным числом.")
            
            category = self.combo_category.get()
            if not category:
                raise ValueError("Выберите категорию.")
            
            date_text = self.entry_date.get()
            if not date_text:
                raise ValueError("Дата не может быть пустой.")
            date_ = datetime.strptime(date_text, "%Y-%m-%d").date()
            
            # Добавляем в память и в таблицу
            expense = {"sum": sum_, "category": category, "date": date_.isoformat()}
            self.data.append(expense)
            self.update_treeview()
            
            # Очищаем поля ввода
            self.entry_sum.delete(0, tk.END)
            self.entry_date.delete(0, tk.END)
            
            messagebox.showinfo("Успех", "Расход добавлен!")

        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))

    def update_treeview(self):
        """Обновляет таблицу на экране на основе данных в памяти."""
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        for expense in self.data:
            self.tree.insert("", "end", values=(f"{expense['sum']:.2f}", expense['category'], expense['date']))

    def save_to_json(self):
        """Сохраняет данные из памяти в файл JSON."""
        try:
            with open("expenses.json", "w") as f:
                json.dump(self.data, f)
            messagebox.showinfo("Успех", "Данные сохранены в expenses.json")
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", str(e))

    def load_data(self):
        """Загружает данные из файла JSON в память."""
        try:
            with open("expenses.json", "r") as f:
                self.data = json.load(f)
            self.update_treeview()
            messagebox.showinfo("Успех", "Данные загружены из expenses.json")
        except FileNotFoundError:
            messagebox.showinfo("Информация", "Файл expenses.json не найден. Будет создан при первом сохранении.")
            self.data = []
            self.update_treeview()

# --- Запуск приложения ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
