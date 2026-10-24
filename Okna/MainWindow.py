import tkinter as tk
from tkinter import ttk, messagebox

from Okna.AddWindow import AddTitleWindowForm
from Serwisy.BazaDanych import Database
from Serwisy.Zmienne import STATUS_LIST, THEME_COLORS
from models import LibraryManager, Movie, Book, Series
import random


class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Biblioteka")
        self.root.geometry("850x700")
        self.root.minsize(700, 300)

        self.manager = LibraryManager()
        Database.load_from_file(self.manager)

        self.active_type = "Film"
        self.active_status = STATUS_LIST[0]

        self.build_gui()
        self.apply_theme_refresh()

    def build_gui(self):

        ############# Frame na górze z wyszukiwarką #############################################################

        self.search_bar_frame = tk.Frame(self.root, pady=8, padx=15)
        self.search_bar_frame.pack(fill="x")

        self.search_input = tk.Entry(self.search_bar_frame, font=("Arial", 11))
        self.search_input.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.search_input.bind("<KeyRelease>", lambda e: self.render_content_cards())  #LAMBDA

        self.losowy = tk.Button(self.search_bar_frame, text="🔄 Losowy", font=("Arial", 9), command=self.trigger_random_view)
        self.losowy.pack(side="left", padx=3)



        ################### Status Tabs ##########################################################

        self.tabs_frame = tk.Frame(self.root, pady=2)
        self.tabs_frame.pack(fill="x", padx=10)

        self.tab_buttons = {}
        for status in STATUS_LIST:
            btn = tk.Button(self.tabs_frame, text=status, font=("Arial", 9, "bold"), command=lambda s=status: self.switch_status_tab(s), bd=2)
            btn.pack(side="left", expand=True, fill="x", padx=1)
            self.tab_buttons[status] = btn
        self.refresh_tab_headers()


        ################ Skrolling #############################################################################

        self.scroll_canvas = tk.Canvas(self.root)
        self.scroll_bar = ttk.Scrollbar(self.root, orient="vertical", command=self.scroll_canvas.yview)
        self.grid_container = tk.Frame(self.scroll_canvas)

        self.grid_container.bind(
            "<Configure>", lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))
        )
        self.scroll_canvas.create_window((0, 0), window=self.grid_container, anchor="nw")
        self.scroll_canvas.configure(yscrollcommand=self.scroll_bar.set)

        self.scroll_canvas.pack(side="left", fill="both", expand=True, padx=15, pady=10)
        self.scroll_bar.pack(side="right", fill="y")


        ################## Przyciski i ComboBox #####################################################


        self.control = tk.Frame(self.root, pady=12, padx=20, bd=1, relief="flat")
        self.control.pack(fill="x", side="bottom")

        tk.Label(self.control, text="Kategoria:", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        self.category_sel = ttk.Combobox(self.control, values=["Film", "Książka", "Serial"], state="readonly",
                                         width=12)
        self.category_sel.set(self.active_type)
        self.category_sel.pack(side="left")
        self.category_sel.bind("<<ComboboxSelected>>", self.handle_category_switch)

        self.btn_global_add = tk.Button(
            self.control, text="  +  ", font=("Arial", 16, "bold"),
            bg="#4CAF50", fg="white", relief="raised", bd=3, command=self.open_form_wizard
        )
        self.btn_global_add.pack(side="right", padx=(0, 40))

    # Zmiana kategorii
    def handle_category_switch(self, event):
        self.active_type = self.category_sel.get()
        self.apply_theme_refresh()

    # Zmiana statusu
    def switch_status_tab(self, status_title):
        self.active_status = status_title
        self.refresh_tab_headers()
        self.render_content_cards()

    def refresh_tab_headers(self):
        for stat, widget in self.tab_buttons.items():
            if stat == self.active_status:
                widget.config(bg="#4F4F4F", fg="white", relief="sunken")
            else:
                widget.config(bg="#F5F5F5", fg="black", relief="raised")

    def apply_theme_refresh(self):
        color_hex = THEME_COLORS[self.active_type]
        self.root.config(bg=color_hex)
        self.search_bar_frame.config(bg=color_hex)
        self.tabs_frame.config(bg=color_hex)
        self.grid_container.config(bg=color_hex)
        self.scroll_canvas.config(bg=color_hex)
        self.control.config(bg=color_hex)
        self.render_content_cards()

    def element_iterator(self, filtered_items):
        for single_item in filtered_items:
            yield single_item

    def render_content_cards(self):
        for child in self.grid_container.winfo_children():
            child.destroy()

        matched_data = self.manager.get_filtered_items(
            self.active_type, self.active_status, self.search_input.get()
        )

        current_row, current_col = 0, 0
        generator_stream = self.element_iterator(matched_data)


        ########################## Dodawanie filtrowanych kart ##################################

        while True:
            try:
                media_node = next(generator_stream)

                card_box = tk.Frame(self.grid_container, bd=2, relief="groove", width=140, height=170, bg="white")
                card_box.grid(row=current_row, column=current_col, padx=12, pady=12)
                card_box.grid_propagate(False)

                card_box.bind("<Button-1>", lambda e, item=media_node: self.show_info_card(item))

                symbol = "🎬" if self.active_type != "Książka" else "📖"
                img_box = tk.Label(card_box, text=f"{symbol}\n[Obraz]", font=("Arial", 12), bg="#EFEFEF", fg="#666",
                                   width=12, height=4)
                img_box.pack(pady=6)
                img_box.bind("<Button-1>", lambda e, item=media_node: self.show_info_card(item))

                title_lbl = tk.Label(card_box, text=media_node.name, font=("Arial", 9, "bold"), bg="white",
                                     wraplength=120, justify="center")
                title_lbl.pack(fill="x", side="bottom", pady=4)
                title_lbl.bind("<Button-1>", lambda e, item=media_node: self.show_info_card(item))

                current_col += 1
                if current_col > 3:
                    current_col = 0
                    current_row += 1
            except StopIteration:
                break

    def trigger_random_view(self):
        if not self.manager.items:
            messagebox.showinfo("Informacja", "Baza danych jest pusta!")
            return
        self.show_info_card(random.choice(self.manager.items))

    def show_info_card(self, item):
        info_win = tk.Toplevel(self.root)
        info_win.title("Szczegóły tytułu")
        info_win.geometry("380x300")
        info_win.grab_set()

        dataset = [
            ("Nazwa:", item.name),
            ("Gatunki:", ", ".join(item.genre)),
            ("Status:", item.status)
        ]

        if isinstance(item, Movie):
            dataset.extend([("Typ:", "Film"), ("Rok:", item.year), ("Studio:", item.studio),
                            ("Czas trwania:", f"{item.duration} min")])
        elif isinstance(item, Book):
            dataset.extend([("Typ:", "Książka"), ("Autor:", item.author), ("Stron:", item.pages)])
        elif isinstance(item, Series):
            dataset.extend(
                [("Typ:", "Serial"), ("Rok:", item.year), ("Studio:", item.studio), ("Odcinki:", item.episodes)])

        for header, content in dataset:
            row = tk.Frame(info_win, pady=3, padx=15)
            row.pack(fill="x")
            tk.Label(row, text=header, font=("Arial", 10, "bold"), width=12, anchor="w").pack(side="left")
            tk.Label(row, text=content, font=("Arial", 10), anchor="w").pack(side="left")


    def open_form_wizard(self):
        AddTitleWindowForm(self.root, self.active_type, self.manager, sync_callback=self.render_content_cards)
