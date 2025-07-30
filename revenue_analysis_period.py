import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# --- Функции и соответствия, связанные с GUI ---
month_to_num = {
    "январь": 1, "февраль": 2, "март": 3, "апрель": 4,
    "май": 5, "июнь": 6, "июль": 7, "август": 8,
    "сентябрь": 9, "октябрь": 10, "ноябрь": 11, "декабрь": 12
}
num_to_month = {v: k for k, v in month_to_num.items()}


def period_value(month_name, year_str):
    """
    Возвращает уникальный числовой индекс для каждого месяца.
    """
    return int(year_str) * 12 + month_to_num[month_name.lower()]


def clear_frame(frame):
    """Очищает все виджеты из фрейма."""
    for widget in frame.winfo_children():
        widget.destroy()


def show_input_form(master_root, on_submit_callback, on_exit_callback):
    """
    Отображает форму ввода данных на главном окне.
    """
    clear_frame(master_root)  # Очищаем предыдущее содержимое

    # Создаем фрейм для формы ввода
    input_frame = ttk.Frame(master_root)
    input_frame.pack(fill='both', expand=True, padx=20, pady=20)

    project_name_entry = tk.Entry(input_frame, width=40)

    # Выпадающие списки (ComboBoxes)
    months_ru = list(month_to_num.keys())
    years = [str(y) for y in range(2022, 2027)]

    # Переменные для хранения выбранных значений
    cur_start_month_var = tk.StringVar(input_frame)
    cur_start_year_var = tk.StringVar(input_frame)
    cur_end_month_var = tk.StringVar(input_frame)
    cur_end_year_var = tk.StringVar(input_frame)
    base_start_month_var = tk.StringVar(input_frame)
    base_start_year_var = tk.StringVar(input_frame)
    base_end_month_var = tk.StringVar(input_frame)
    base_end_year_var = tk.StringVar(input_frame)

    # Настройка сетки (grid layout)
    tk.Label(input_frame, text="").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(input_frame, text="начало периода\n(месяц / год)").grid(row=0, column=1, padx=10, pady=5)
    tk.Label(input_frame, text="конец периода\n(месяц / год)").grid(row=0, column=2, padx=10, pady=5)

    tk.Label(input_frame, text="текущий период").grid(row=1, column=0, padx=10, pady=5)
    cb_cur_start_month = ttk.Combobox(input_frame, values=months_ru, width=10, state="readonly",
                                      textvariable=cur_start_month_var)
    cb_cur_start_month.grid(row=1, column=1, sticky='W', padx=(10, 0))
    cb_cur_start_year = ttk.Combobox(input_frame, values=years, width=5, state="readonly",
                                     textvariable=cur_start_year_var)
    cb_cur_start_year.grid(row=1, column=1, sticky='E', padx=(0, 10))
    cb_cur_end_month = ttk.Combobox(input_frame, values=months_ru, width=10, state="readonly",
                                    textvariable=cur_end_month_var)
    cb_cur_end_month.grid(row=1, column=2, sticky='W', padx=(10, 0))
    cb_cur_end_year = ttk.Combobox(input_frame, values=years, width=5, state="readonly", textvariable=cur_end_year_var)
    cb_cur_end_year.grid(row=1, column=2, sticky='E', padx=(0, 10))

    tk.Label(input_frame, text="базисный период").grid(row=2, column=0, padx=10, pady=5)
    cb_base_start_month = ttk.Combobox(input_frame, values=months_ru, width=10, state="readonly",
                                       textvariable=base_start_month_var)
    cb_base_start_month.grid(row=2, column=1, sticky='W', padx=(10, 0))
    cb_base_start_year = ttk.Combobox(input_frame, values=years, width=5, state="readonly",
                                      textvariable=base_start_year_var)
    cb_base_start_year.grid(row=2, column=1, sticky='E', padx=(0, 10))
    cb_base_end_month = ttk.Combobox(input_frame, values=months_ru, width=10, state="readonly",
                                     textvariable=base_end_month_var)
    cb_base_end_month.grid(row=2, column=2, sticky='W', padx=(10, 0))
    cb_base_end_year = ttk.Combobox(input_frame, values=years, width=5, state="readonly",
                                    textvariable=base_end_year_var)
    cb_base_end_year.grid(row=2, column=2, sticky='E', padx=(0, 10))

    tk.Label(input_frame, text="Название проекта:").grid(row=3, column=0, padx=10, pady=(15, 5), sticky='e')
    project_name_entry.grid(row=3, column=1, columnspan=2, padx=10, pady=(15, 5), sticky='w')

    def validate_and_submit():
        p_name = project_name_entry.get().strip()
        values = {
            "cur_start_month": cur_start_month_var.get(),
            "cur_start_year": cur_start_year_var.get(),
            "cur_end_month": cur_end_month_var.get(),
            "cur_end_year": cur_end_year_var.get(),
            "base_start_month": base_start_month_var.get(),
            "base_start_year": base_start_year_var.get(),
            "base_end_month": base_end_month_var.get(),
            "base_end_year": base_end_year_var.get()
        }

        if not p_name or any(v == '' for v in values.values()):
            messagebox.showerror("Ошибка", "Заполните все поля и введите название проекта.")
            return

        try:
            cur_start_idx = period_value(values["cur_start_month"], values["cur_start_year"])
            cur_end_idx = period_value(values["cur_end_month"], values["cur_end_year"])
            base_start_idx = period_value(values["base_start_month"], values["base_start_year"])
            base_end_idx = period_value(values["base_end_month"], values["base_end_year"])
        except KeyError:
            messagebox.showerror("Ошибка", "Неверно выбран месяц. Пожалуйста, выберите из списка.")
            return
        except ValueError:
            messagebox.showerror("Ошибка", "Неверно выбран год. Пожалуйста, выберите из списка.")
            return

        if base_start_idx > base_end_idx:
            messagebox.showerror("Ошибка", "Начало базисного периода не может быть позже его конца.")
            return
        if cur_start_idx > cur_end_idx:
            messagebox.showerror("Ошибка", "Начало текущего периода не может быть позже его конца.")
            return

        # Если валидация пройдена, вызываем callback с данными
        on_submit_callback(
            p_name,
            (values['base_start_month'], int(values['base_start_year'])),
            (values['base_end_month'], int(values['base_end_year'])),
            (values['cur_start_month'], int(values['cur_start_year'])),
            (values['cur_end_month'], int(values['cur_end_year']))
        )

    btn_submit = tk.Button(input_frame, text="Подтвердить", command=validate_and_submit)
    btn_submit.grid(row=4, column=0, columnspan=3, pady=15)

    master_root.protocol("WM_DELETE_WINDOW", on_exit_callback)  # Обработка кнопки закрытия окна


def index_to_period(index):
    """
    Преобразует числовой индекс месяца в формат "месяц год".
    """
    year = index // 12
    month_num = index % 12
    if month_num == 0:  # Корректировка для декабря (месяц 12)
        month_num = 12
        year -= 1
    return f"{num_to_month[month_num]} {year}"


def get_month_indices_in_range(start_month_name, start_year_val, end_month_name, end_year_val):
    """
    Возвращает список числовых индексов месяцев в заданном диапазоне.
    """
    start_idx = period_value(start_month_name, str(start_year_val))
    end_idx = period_value(end_month_name, str(end_year_val))
    return [start_idx + i for i in range(end_idx - start_idx + 1)]


def build_weighted_deltas(cur_period, base_period):
    """
    Строит словарь весов для дельт (аналогично V_m = V_min + D_min+1 + ... + D_m).
    """
    weights = defaultdict(int)

    cur_month_indices = get_month_indices_in_range(*cur_period[0], *cur_period[1])
    base_month_indices = get_month_indices_in_range(*base_period[0], *base_period[1])

    all_involved_months = set(cur_month_indices + base_month_indices)
    if not all_involved_months:
        return weights

    min_month_index = min(all_involved_months) - 1

    month_value_weights = defaultdict(int)
    for month_idx in cur_month_indices:
        month_value_weights[month_idx] += 1
    for month_idx in base_month_indices:
        month_value_weights[month_idx] -= 1

    for current_month_idx, vm_weight in month_value_weights.items():
        if vm_weight == 0:
            continue
        for delta_month_idx in range(min_month_index + 1, current_month_idx + 1):
            weights[delta_month_idx] += vm_weight

    return weights


def build_simple_weights(cur_period, base_period):
    """
    Строит словарь весов: +1 для месяцев текущего периода, -1 для месяцев базисного.
    """
    weights = defaultdict(int)

    cur_month_indices = get_month_indices_in_range(*cur_period[0], *cur_period[1])
    base_month_indices = get_month_indices_in_range(*base_period[0], *base_period[1])

    for month_idx in cur_month_indices:
        weights[month_idx] += 1
    for month_idx in base_month_indices:
        weights[month_idx] -= 1

    return {k: v for k, v in weights.items() if v != 0}


# --- Функции, связанные с обработкой данных (pandas) ---
def process_excel_to_pivot(excel_file_path: str, sheet_name_to_process: str,
                           project_to_filter: str, status_callback=None) -> pd.DataFrame:
    """
    Обрабатывает Excel-файл для создания сводной таблицы (агрегируя все столбцы после 'Project').
    Добавлен status_callback для обновления статуса в GUI.
    """
    status_message = ""
    try:
        # --- Шаг 1: Находим строку, где находится заголовок 'Project' для определения начала таблицы ---
        header_row_index = -1
        df_temp = pd.read_excel(excel_file_path, sheet_name=sheet_name_to_process, header=None, nrows=100)
        for index, row in df_temp.iterrows():
            if 'Project' in row.astype(str).values:
                header_row_index = index
                break
        if header_row_index == -1:
            status_message = f"Ошибка: 'Project' не найден на листе '{sheet_name_to_process}'."
            if status_callback: status_callback(status_message)
            return pd.DataFrame()

        # --- Шаг 2: Читаем основную таблицу, используя найденный индекс строки как заголовки ---
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name_to_process, header=header_row_index)

        # --- Шаг 3: Заполняем пропуски нулями в столбцах после 'Y' ---
        if 'Y' in df.columns:
            y_column_index = df.columns.get_loc('Y')
            columns_after_y = df.columns[y_column_index + 1:]
            df[columns_after_y] = df[columns_after_y].fillna(0)

        # --- Шаг 4: Фильтруем DataFrame по значению в столбце 'Project' ---
        df_filtered = pd.DataFrame()
        if 'Project' in df.columns:
            df_filtered = df[df['Project'] == project_to_filter]
            if df_filtered.empty:
                status_message = f"Внимание: Проект '{project_to_filter}' не найден на листе '{sheet_name_to_process}'. Возвращаю пустой DataFrame."
                if status_callback: status_callback(status_message)
                return pd.DataFrame()
        else:
            status_message = f"Ошибка: Столбец 'Project' не найден на листе '{sheet_name_to_process}'. Возвращаю пустой DataFrame."
            if status_callback: status_callback(status_message)
            return pd.DataFrame()

        # --- Шаг 5: Создаем сводную таблицу/сводку, исключая столбцы до и включая 'Project' ---
        pivot_data = {}
        if 'Project' in df_filtered.columns:
            project_col_index = df_filtered.columns.get_loc('Project')
            start_col_index_for_pivot = project_col_index + 1
        else:
            status_message = f"Ошибка: 'Project' не найден в отфильтрованном DataFrame для листа '{sheet_name_to_process}'. Возвращаю пустой DataFrame."
            if status_callback: status_callback(status_message)
            return pd.DataFrame()

        for i in range(start_col_index_for_pivot, len(df_filtered.columns)):
            column_name = df_filtered.columns[i]
            if pd.api.types.is_numeric_dtype(df_filtered[column_name]):
                pivot_data[column_name] = df_filtered[column_name].sum()
            else:
                unique_values = df_filtered[column_name].unique()
                if len(unique_values) == 1:
                    pivot_data[column_name] = unique_values[0]
                elif len(unique_values) > 1:
                    pivot_data[column_name] = ", ".join(map(str, unique_values))
                else:
                    pivot_data[column_name] = None

        df_pivot = pd.DataFrame.from_dict(pivot_data, orient='index', columns=['Value'])
        df_pivot.index = df_pivot.index.astype(str).str.replace('\n', ' ').str.strip()

        # --- Шаг 7: Удаляем указанные строки из сводной таблицы ---
        rows_to_remove = [
            'NET DIFF to be explained', 'PREV NOISE to be explained', 'CURR NOISE to be explained',
            'NET DIFF explained', 'PREV NOISE explained', 'CURR NOISE explained',
            'NET DIFF deviation', 'PREV NOISE deviation', 'CURR NOISE deviation',
            'Support Analyst', 'G/L Account', 'G/L Account Name', 'Project'
        ]
        existing_rows_to_remove = [row for row in rows_to_remove if row in df_pivot.index]
        if existing_rows_to_remove:
            df_pivot = df_pivot.drop(existing_rows_to_remove)

        status_message = f"Успешно обработан."
        if status_callback: status_callback(status_message)
        return df_pivot

    except FileNotFoundError:
        status_message = f"Ошибка: Файл Excel не найден по пути: {excel_file_path}"
        if status_callback: status_callback(status_message)
        return pd.DataFrame()
    except KeyError as e:
        status_message = f"Ошибка: Лист '{sheet_name_to_process}' не найден или проблема с колонкой: {e}"
        if status_callback: status_callback(status_message)
        return pd.DataFrame()
    except Exception as e:
        status_message = f"Произошла непредвиденная ошибка при обработке файла '{excel_file_path}' (лист '{sheet_name_to_process}') за Y.1+N.1: {e}"
        if status_callback: status_callback(status_message)
        return pd.DataFrame()


def get_yn_sum_for_month(excel_file_path: str, sheet_name_to_process: str, project_to_filter: str,
                         status_callback=None) -> float:
    """
    Извлекает сумму (Y.1 + N.1) для указанного листа и проекта из Excel файла.
    Возвращает 0.0, если столбцы не найдены или произошла ошибка.
    Добавлен status_callback для обновления статуса в GUI.
    """
    sum_yn = 0.0
    status_message = ""
    try:
        header_row_index = -1
        df_temp = pd.read_excel(excel_file_path, sheet_name=sheet_name_to_process, header=None, nrows=100)
        for index, row in df_temp.iterrows():
            if 'Project' in row.astype(str).values:
                header_row_index = index
                break
        if header_row_index == -1:
            status_message = f"Ошибка: 'Project' не найден на листе '{sheet_name_to_process}' для Y.1+N.1."
            if status_callback: status_callback(status_message)
            return 0.0

        df = pd.read_excel(excel_file_path, sheet_name=sheet_name_to_process, header=header_row_index)

        df_filtered = pd.DataFrame()
        if 'Project' in df.columns:
            df_filtered = df[df['Project'] == project_to_filter]
            if df_filtered.empty:
                status_message = f"Внимание: Проект '{project_to_filter}' не найден на листе '{sheet_name_to_process}' для Y.1+N.1. Возвращаю 0."
                if status_callback: status_callback(status_message)
                return 0.0
        else:
            status_message = f"Ошибка: Столбец 'Project' не найден на листе '{sheet_name_to_process}'. Возвращаю 0."
            if status_callback: status_callback(status_message)
            return 0.0

        if 'Y.1' in df_filtered.columns:
            if pd.api.types.is_numeric_dtype(df_filtered['Y.1']):
                sum_yn += df_filtered['Y.1'].sum()
            else:
                status_message = f"Внимание: Столбец 'Y.1' на листе '{sheet_name_to_process}' нечисловой. Пропускаю."
                if status_callback: status_callback(status_message)

        if 'N.1' in df_filtered.columns:
            if pd.api.types.is_numeric_dtype(df_filtered['N.1']):
                sum_yn += df_filtered['N.1'].sum()
            else:
                status_message = f"Внимание: Столбец 'N.1' на листе '{sheet_name_to_process}' нечисловой. Пропускаю."
                if status_callback: status_callback(status_message)

        status_message = f"Успешно обработан."
        if status_callback: status_callback(status_message)
        return sum_yn

    except FileNotFoundError:
        status_message = f"Ошибка: Файл Excel не найден по пути: {excel_file_path}"
        if status_callback: status_callback(status_message)
        return 0.0
    except KeyError as e:
        status_message = f"Ошибка: Лист '{sheet_name_to_process}' не найден или проблема с колонкой для Y.1+N.1: {e}"
        if status_callback: status_callback(status_message)
        return 0.0
    except Exception as e:
        status_message = f"Произошла непредвиденная ошибка при обработке файла '{excel_file_path}' (лист '{sheet_name_to_process}') для Y.1+N.1: {e}"
        if status_callback: status_callback(status_message)
        return 0.0


def show_results_form(master_root, project_name, base_start_period_tuple, base_end_period_tuple,
                      cur_start_period_tuple, cur_end_period_tuple, status_messages,
                      revenue_change, pivot_deltas_df, on_restart_callback, on_exit_callback):
    """
    Создает форму результатов на главном окне.
    """
    clear_frame(master_root)  # Очищаем предыдущее содержимое

    results_frame = ttk.Frame(master_root)
    results_frame.pack(fill='both', expand=True, padx=10, pady=5)

    # Конфигурируем сетку для results_frame: две колонки
    results_frame.grid_columnconfigure(0, weight=1)  # Левая колонка
    results_frame.grid_columnconfigure(1, weight=2)  # Правая колонка (больше места для графиков)
    results_frame.grid_rowconfigure(0, weight=1)  # Основная строка для содержимого
    results_frame.grid_rowconfigure(1, weight=0)  # Строка для кнопок (не растягивается)

    # --- Левая панель для параметров, статуса и общей выручки ---
    left_info_pane = ttk.Frame(results_frame)
    left_info_pane.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    left_info_pane.grid_rowconfigure(0, weight=0)  # Параметры не растягиваются
    left_info_pane.grid_rowconfigure(1, weight=1)  # Статус растягивается
    left_info_pane.grid_rowconfigure(2, weight=0)  # Выручка не растягивается
    left_info_pane.grid_columnconfigure(0, weight=1)

    # --- Параметры от пользователя ---
    params_frame = tk.Frame(left_info_pane)
    params_frame.grid(row=0, column=0, sticky='nw', padx=5, pady=5)
    tk.Label(params_frame, text="--- Параметры от пользователя ---", font=("Arial", 10, "bold")).pack(anchor='w')
    tk.Label(params_frame, text=f"📁 Проект: {project_name}").pack(anchor='w')
    tk.Label(params_frame,
             text=f"📊 Базисный период: {base_start_period_tuple[0]} {base_start_period_tuple[1]} — {base_end_period_tuple[0]} {base_end_period_tuple[1]}").pack(
        anchor='w')
    tk.Label(params_frame,
             text=f"📈 Текущий период: {cur_start_period_tuple[0]} {cur_start_period_tuple[1]} — {cur_end_period_tuple[0]} {cur_end_period_tuple[1]}").pack(
        anchor='w')

    # --- Статус по прочтению данных из Excel ---
    status_frame = tk.Frame(left_info_pane)
    status_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
    tk.Label(status_frame, text="\n--- Статус загрузки данных ---", font=("Arial", 10, "bold")).pack(anchor='w')
    status_text_area = tk.Text(status_frame, height=7, width=40, wrap='word', bg="#f0f0f0")
    status_text_area.pack(padx=0, pady=0, fill='both', expand=True)
    for msg in status_messages:
        status_text_area.insert(tk.END, msg + "\n")
    status_text_area.config(state=tk.DISABLED)

    # --- Общее изменение выручки (Второй запрос) ---
    revenue_frame = tk.Frame(left_info_pane)
    revenue_frame.grid(row=2, column=0, sticky='sw', padx=5, pady=5)
    tk.Label(revenue_frame, text="\n--- Общее изменение выручки ---", font=("Arial", 10, "bold")).pack(anchor='w')
    tk.Label(revenue_frame, text=f"Общее изменение выручки: {revenue_change:,.2f}").pack(anchor='w')

    # --- Правая панель для анализа изменений и визуализации ---
    right_analysis_pane = ttk.Frame(results_frame)
    right_analysis_pane.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
    right_analysis_pane.grid_rowconfigure(0, weight=0)  # Заголовок не растягивается
    right_analysis_pane.grid_rowconfigure(1, weight=1)  # PanedWindow растягивается
    right_analysis_pane.grid_columnconfigure(0, weight=1)

    analysis_label = tk.Label(right_analysis_pane, text="--- Анализ изменений (Дельты) и Визуализация ---",
                              font=("Arial", 10, "bold"))
    analysis_label.grid(row=0, column=0, sticky='nw', padx=5, pady=5)

    main_pane = ttk.PanedWindow(right_analysis_pane, orient='horizontal')
    main_pane.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

    # Фильтрация данных для отображения
    filtered_pivot_deltas_df = pivot_deltas_df[~pivot_deltas_df.index.isin(['Y', 'N', 'Y.1', 'N.1'])]
    filtered_pivot_deltas_df = filtered_pivot_deltas_df[filtered_pivot_deltas_df['Value'] != 0]

    # --- Левая часть PanedWindow для таблицы ---
    left_frame = ttk.Frame(main_pane)
    main_pane.add(left_frame, weight=1)

    if not filtered_pivot_deltas_df.empty:
        tree_frame = tk.Frame(left_frame)
        tree_frame.pack(fill='both', expand=True)

        tree = ttk.Treeview(tree_frame, columns=('Название', 'Дельта'), show='headings')

        tree.heading('Название', text='Название')
        tree.heading('Дельта', text='Дельта')

        tree.column('Название', width=120, anchor='w')
        tree.column('Дельта', width=80, anchor='e')

        for index, row in filtered_pivot_deltas_df.iterrows():
            tree.insert("", "end", values=(index, f"{row['Value']:,.2f}"))

        tree.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
    else:
        tk.Label(left_frame, text="Нет значимых изменений для отображения.").pack(padx=10, pady=5)

    # --- Правая часть PanedWindow для визуализации ---
    right_frame = ttk.Frame(main_pane)
    main_pane.add(right_frame, weight=2)

    if not filtered_pivot_deltas_df.empty:
        top_10_deltas = filtered_pivot_deltas_df.reindex(
            filtered_pivot_deltas_df['Value'].abs().sort_values(ascending=False).index).head(10)

        fig, ax = plt.subplots(figsize=(6, 4))

        ax.bar(top_10_deltas.index, top_10_deltas['Value'], color='skyblue')

        ax.set_title('Топ изменений по модулю', fontsize=10)
        ax.set_ylabel('Дельта', fontsize=9)

        ax.tick_params(axis='x', labelrotation=45)
        ax.set_xticklabels(top_10_deltas.index, ha='right', fontsize=7)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=right_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, right_frame)
        toolbar.update()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    else:
        tk.Label(right_frame, text="Недостаточно данных для построения визуализации.").pack(padx=10, pady=10)

    # --- Кнопки для управления программой ---
    button_frame = tk.Frame(results_frame)
    button_frame.grid(row=1, column=0, columnspan=2, pady=10)  # Кнопки внизу, охватывают обе колонки

    btn_restart = tk.Button(button_frame, text="Начать заново", command=on_restart_callback)
    btn_restart.pack(side=tk.LEFT, padx=10)

    btn_exit = tk.Button(button_frame, text="Выход", command=on_exit_callback)
    btn_exit.pack(side=tk.LEFT, padx=10)


# --- Основной блок выполнения ---
if __name__ == "__main__":
    main_app_root = tk.Tk()
    main_app_root.title("Анализ проекта")
    main_app_root.geometry("1200x600")  # Увеличим начальный размер для новой компоновки

    # Переменные для хранения данных между этапами
    project_data = {}  # Для хранения данных из формы ввода


    # Определение callback-функций для навигации между формами
    def on_input_submit(project_name, base_start, base_end, cur_start, cur_end):
        """Callback-функция при отправке формы ввода."""
        project_data['project_name'] = project_name
        project_data['base_start'] = base_start
        project_data['base_end'] = base_end
        project_data['cur_start'] = cur_start
        project_data['cur_end'] = cur_end

        # Теперь обрабатываем данные и показываем результаты
        process_and_show_results()


    def on_restart_from_results():
        """Callback-функция при нажатии кнопки 'Начать заново' на форме результатов."""
        project_data.clear()  # Очищаем предыдущие данные
        main_app_root.geometry("800x600")  # Сбрасываем начальный размер для формы ввода
        show_input_form(main_app_root, on_input_submit, on_exit_app)


    def on_exit_app():
        """Callback-функция при нажатии кнопки 'Выход' или закрытии окна."""
        main_app_root.quit()  # Останавливаем главный цикл Tkinter
        main_app_root.destroy()  # Уничтожаем окно


    def process_and_show_results():
        """Обрабатывает данные и отображает форму результатов."""
        project_name_from_gui = project_data.get('project_name')
        base_start_period = project_data.get('base_start')
        base_end_period = project_data.get('base_end')
        cur_start_period = project_data.get('cur_start')
        cur_end_period = project_data.get('cur_end')

        if not all([project_name_from_gui, base_start_period, base_end_period, cur_start_period, cur_end_period]):
            messagebox.showinfo("Отмена", "Не все данные были введены для обработки.")
            show_input_form(main_app_root, on_input_submit, on_exit_app)  # Возвращаемся к форме ввода
            return

        status_messages_list = []

        def update_status(msg):
            status_messages_list.append(msg)

        weights_deltas = build_weighted_deltas(
            (cur_start_period, cur_end_period),
            (base_start_period, base_end_period)
        )
        simple_weights = build_simple_weights(
            (cur_start_period, cur_end_period),
            (base_start_period, base_end_period)
        )

        month_name_mapping = {
            "январь": "January", "февраль": "February", "март": "March", "апрель": "April",
            "май": "May", "июнь": "June", "июль": "July", "август": "August",
            "сентябрь": "September", "октябрь": "October", "ноябрь": "November", "декабрь": "December"
        }

        # --- ИЗМЕНЕННЫЙ ПУТЬ К ФАЙЛУ (с включением папки года) ---
        BASE_WORKING_DIR = r"C:\Users\Kiryl_Batko\xxx\xxxxx"
        EXCEL_FILE_NAME_TEMPLATE = r"\xx {year_val}\xx auto {year_val}.xlsx"  # Теперь включает  {year_val}
        # --- КОНЕЦ ИЗМЕНЕНИЯ ---

        final_sum_pivot_deltas = None

        months_to_process_deltas = sorted([idx for idx, weight in weights_deltas.items() if weight != 0])

        for month_idx_weighted in months_to_process_deltas:
            weight_value = weights_deltas[month_idx_weighted]

            year_val = month_idx_weighted // 12
            month_num_val = month_idx_weighted % 12
            if month_num_val == 0:
                month_num_val = 12
                year_val -= 1
            month_ru = num_to_month[month_num_val]

            # --- ФОРМИРОВАНИЕ ПОЛНОГО ПУТИ К ФАЙЛУ ---
            current_excel_file_path = BASE_WORKING_DIR + EXCEL_FILE_NAME_TEMPLATE.format(year_val=year_val)
            # --- КОНЕЦ ИЗМЕНЕНИЯ ---

            month_en = month_name_mapping.get(month_ru.lower())
            if not month_en:
                update_status(
                    f"Предупреждение: Неизвестное русское название месяца '{month_ru}'. Пропускаю Δ({index_to_period(month_idx_weighted)}).")
                continue
            sheet_name_excel = f"{month_en} {year_val} TM"

            update_status(f"Загрузка данных для Δ({index_to_period(month_idx_weighted)})...")

            monthly_pivot_df = process_excel_to_pivot(current_excel_file_path, sheet_name_excel, project_name_from_gui,
                                                      status_callback=update_status)

            if not monthly_pivot_df.empty:
                if pd.api.types.is_numeric_dtype(monthly_pivot_df['Value']):
                    weighted_monthly_pivot = monthly_pivot_df['Value'] * weight_value
                    weighted_monthly_pivot_df = weighted_monthly_pivot.to_frame(name='Value')

                    if final_sum_pivot_deltas is None:
                        final_sum_pivot_deltas = weighted_monthly_pivot_df
                    else:
                        final_sum_pivot_deltas = final_sum_pivot_deltas.add(weighted_monthly_pivot_df, fill_value=0)

        final_sum_yn = 0.0

        months_to_process_simple = sorted([idx for idx, weight in simple_weights.items() if weight != 0])

        for month_idx_weighted in months_to_process_simple:
            weight_value = simple_weights[month_idx_weighted]

            year_val = month_idx_weighted // 12
            month_num_val = month_idx_weighted % 12
            if month_num_val == 0:
                month_num_val = 12
                year_val -= 1
            month_ru = num_to_month[month_num_val]

            # --- ФОРМИРОВАНИЕ ПОЛНОГО ПУТИ К ФАЙЛУ ---
            current_excel_file_path = BASE_WORKING_DIR + EXCEL_FILE_NAME_TEMPLATE.format(year_val=year_val)
            # --- КОНЕЦ ИЗМЕНЕНИЯ ---

            month_en = month_name_mapping.get(month_ru.lower())
            if not month_en:
                update_status(
                    f"Предупреждение: Неизвестное русское название месяца '{month_ru}'. Пропускаю ({index_to_period(month_idx_weighted)}).")
                continue
            sheet_name_excel = f"{month_en} {year_val} TM"

            update_status(f"Загрузка данных для ({index_to_period(month_idx_weighted)}) (Y.1+N.1)...")

            monthly_yn_sum = get_yn_sum_for_month(current_excel_file_path, sheet_name_excel, project_name_from_gui,
                                                  status_callback=update_status)

            if monthly_yn_sum is not None:
                weighted_sum = monthly_yn_sum * weight_value
                final_sum_yn += weighted_sum

        if final_sum_pivot_deltas is None:
            final_sum_pivot_deltas = pd.DataFrame(columns=['Value'])

        main_app_root.geometry("1200x600")  # Настраиваем размер для окна результатов
        show_results_form(
            main_app_root,
            project_name_from_gui,
            base_start_period,
            base_end_period,
            cur_start_period,
            cur_end_period,
            status_messages_list,
            -final_sum_yn,
            final_sum_pivot_deltas,
            on_restart_from_results,  # Передаем callback для перезапуска
            on_exit_app  # Передаем callback для выхода
        )


    # Начинаем с формы ввода
    show_input_form(main_app_root, on_input_submit, on_exit_app)
    main_app_root.mainloop()  # Запускаем основной цикл событий Tkinter
