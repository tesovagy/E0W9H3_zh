import tkinter as tk
from tkinter import messagebox, ttk
from file_io_ob import load_data_ob, save_data_ob, export_report_ob
from warehouse_core_ob import WarehouseOB


def create_main_window_ob():

    warehouse = WarehouseOB()
    data = load_data_ob()
    warehouse.products = data.get('products', {})
    warehouse.thresholds_ob = data.get('thresholds', {})

    root = tk.Tk()
    root.title("Raktárkezelő Alkalmazás - OB")
    root.geometry("850x700")

    selected_product = None

    COLORS = {
        "low": "#ffcccc",
        "medium": "#fff4cc",
        "high": "#ccffcc",
        "default": "#ffffff"
    }


    def save_all_data():
        data_to_save = {
            'products': warehouse.products,
            'thresholds': warehouse.thresholds_ob
        }
        save_data_ob(data_to_save)

    def add_product_handler():
        nonlocal selected_product
        name = entry_name.get()
        try:
            quantity = int(entry_quantity.get())
            threshold = int(entry_threshold.get())

            if name and quantity >= 0 and threshold >= 0:
                if selected_product:
                    if selected_product != name:
                        warehouse.remove_product_ob(selected_product)
                    warehouse.add_product_ob(name, quantity, threshold)
                    save_all_data()
                    update_product_list()
                    reset_edit_mode()
                    messagebox.showinfo("Siker", f"{name} módosítva\nMennyiség: {quantity} db\nKüszöb: {threshold} db")
                else:
                    warehouse.add_product_ob(name, quantity, threshold)
                    save_all_data()
                    update_product_list()
                    reset_input_fields()
                    messagebox.showinfo("Siker", f"{name} hozzáadva\nMennyiség: {quantity} db\nKüszöb: {threshold} db")
            else:
                messagebox.showwarning("Hiba", "Érvénytelen adatok!")
        except ValueError:
            messagebox.showwarning("Hiba", "Mennyiség és küszöb szám legyen!")

    def remove_product_handler():
        nonlocal selected_product
        selected = listbox.curselection()
        if selected:
            product = listbox.get(selected[0]).split(":")[0]
            if warehouse.remove_product_ob(product):
                save_all_data()
                update_product_list()
                if selected_product == product:
                    reset_edit_mode()
                messagebox.showinfo("Siker", f"{product} teljesen törölve")
            else:
                messagebox.showwarning("Hiba", "Nem sikerült törölni!")

    def update_product_list():
        listbox.delete(0, tk.END)

        keyword = entry_search.get()

        products_to_show = warehouse.list_products_ob()
        if keyword:
            products_to_show = warehouse.search_product_ob(keyword)

        for product, quantity in products_to_show.items():
            status = warehouse.get_stock_status_ob(product, quantity)
            color = COLORS.get(status, COLORS["default"])

            threshold = warehouse.get_threshold_ob(product)

            listbox.insert(tk.END, f"{product}: {quantity} db (küszöb: {threshold} db)")
            listbox.itemconfig(tk.END, {'bg': color})

    def auto_search_handler(*args):
        update_product_list()

    def listbox_click_handler(event):
        nonlocal selected_product
        selected = listbox.curselection()
        if selected:
            product_text = listbox.get(selected[0])
            product_name = product_text.split(":")[0]
            product_quantity = product_text.split(":")[1].strip().split(" ")[0]
            product_threshold = warehouse.get_threshold_ob(product_name)

            entry_name.delete(0, tk.END)
            entry_name.insert(0, product_name)
            entry_quantity.delete(0, tk.END)
            entry_quantity.insert(0, product_quantity)
            entry_threshold.delete(0, tk.END)
            entry_threshold.insert(0, str(product_threshold))

            selected_product = product_name
            add_button.config(text="Módosítás")
            cancel_button.pack(side='left', padx=5)
            remove_button.config(text=f"Törlés: {product_name}")

    def reset_edit_mode():
        nonlocal selected_product
        selected_product = None
        add_button.config(text="Hozzáadás")
        remove_button.config(text="Törlés")
        reset_input_fields()
        cancel_button.pack_forget()

    def reset_input_fields():
        entry_name.delete(0, tk.END)
        entry_quantity.delete(0, tk.END)
        entry_threshold.delete(0, tk.END)
        entry_threshold.insert(0, "10")  # Alapértelmezett küszöb

    def cancel_edit_handler():
        reset_edit_mode()

    def export_handler():
        export_report_ob(warehouse.products)
        messagebox.showinfo("Siker", "Jelentés exportálva!")

    def show_legend_handler():
        legend_window = tk.Toplevel(root)
        legend_window.title("Színjelmagyarázat - Készletállapotok")
        legend_window.geometry("450x200")
        legend_window.resizable(False, False)

        ttk.Label(legend_window, text="Készlet állapotok (termékenkénti küszöb):",
                  font=('Arial', 12, 'bold')).pack(pady=10)

        frame_low = ttk.Frame(legend_window)
        frame_low.pack(fill='x', padx=20, pady=3)
        tk.Label(frame_low, bg=COLORS["low"], width=8, height=2).pack(side='left', padx=5)
        ttk.Label(frame_low, text="≤ küszöb - Kevés készlet").pack(side='left')

        frame_medium = ttk.Frame(legend_window)
        frame_medium.pack(fill='x', padx=20, pady=3)
        tk.Label(frame_medium, bg=COLORS["medium"], width=8, height=2).pack(side='left', padx=5)
        ttk.Label(frame_medium, text="küszöb+1 - küszöb 1.5x - Fogyó készlet").pack(side='left')

        frame_high = ttk.Frame(legend_window)
        frame_high.pack(fill='x', padx=20, pady=3)
        tk.Label(frame_high, bg=COLORS["high"], width=8, height=2).pack(side='left', padx=5)
        ttk.Label(frame_high, text="> küszöb×4 - Sok készlet").pack(side='left')

        ttk.Button(legend_window, text="Bezárás", command=legend_window.destroy).pack(pady=15)

    frame = ttk.Frame(root, padding="10")
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text="Termék neve:").grid(row=0, column=0, sticky=tk.W, pady=2)
    entry_name = ttk.Entry(frame, width=25)
    entry_name.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)

    ttk.Label(frame, text="Mennyiség:").grid(row=1, column=0, sticky=tk.W, pady=2)
    entry_quantity = ttk.Entry(frame, width=25)
    entry_quantity.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)

    ttk.Label(frame, text="Küszöbérték:").grid(row=2, column=0, sticky=tk.W, pady=2)
    entry_threshold = ttk.Entry(frame, width=25)
    entry_threshold.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2)
    entry_threshold.insert(0, "10")

    button_frame_top = ttk.Frame(frame)
    button_frame_top.grid(row=3, column=0, columnspan=2, pady=10, sticky='w')

    add_button = ttk.Button(button_frame_top, text="Hozzáadás", command=add_product_handler)
    add_button.pack(side='left', padx=(0, 10))

    cancel_button = ttk.Button(button_frame_top, text="Mégsem", command=cancel_edit_handler)

    listbox = tk.Listbox(frame, height=18)
    listbox.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

    listbox.bind('<<ListboxSelect>>', listbox_click_handler)
    ttk.Label(frame, text="Keresés:").grid(row=5, column=0, sticky=tk.W, pady=2)
    entry_search = ttk.Entry(frame, width=25)
    entry_search.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=2)
    entry_search.bind('<KeyRelease>', auto_search_handler)
    button_frame_bottom = ttk.Frame(frame)
    button_frame_bottom.grid(row=6, column=0, columnspan=3, pady=10)

    remove_button = ttk.Button(button_frame_bottom, text="Törlés", command=remove_product_handler)
    remove_button.pack(side=tk.LEFT, padx=5)

    ttk.Button(button_frame_bottom, text="Export", command=export_handler).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame_bottom, text="Színjelmagyarázat", command=show_legend_handler).pack(side=tk.LEFT, padx=5)

    update_product_list()

    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(4, weight=1)

    root.mainloop()