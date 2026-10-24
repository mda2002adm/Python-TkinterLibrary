import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from models import Movie, Book, Series
from Serwisy.BazaDanych import Database
from Serwisy.Wyjątek import WlasnyError
from Serwisy.Zmienne import STATUS_LIST, GENRE_POOL


class AddTitleWindowForm:
    def __init__(self, parent, category, manager, sync_callback):
        self.sub_win = tk.Toplevel(parent)
        self.sub_win.title("Dodaj")
        self.sub_win.geometry("400x650")
        self.sub_win.grab_set()

        self.category = category
        self.manager = manager
        self.sync_callback = sync_callback

        self.build_interactive_form()

    def build_interactive_form(self):
        tk.Label(self.sub_win, text="Add", font=("Arial", 18, "bold"), pady=10).pack()

        tk.Label(self.sub_win, text="Nazwa *", font=("Arial", 9, "bold")).pack(anchor="w", padx=30)
        self.in_name = tk.Entry(self.sub_win, width=45)
        self.in_name.pack(padx=30, pady=2)

        if self.category in ("Film", "Serial"):
            tk.Label(self.sub_win, text="Rok *", font=("Arial", 9, "bold")).pack(anchor="w", padx=30)
            self.in_year = ttk.Combobox(self.sub_win, values=[str(r) for r in range(2026, 1960, -1)], state="readonly",
                                        width=42)
            self.in_year.set("2025")
            self.in_year.pack(padx=30, pady=2)

            tk.Label(self.sub_win, text="Studio (Wybierz lub wpisz)", font=("Arial", 9, "bold")).pack(anchor="w",
                                                                                                      padx=30)
            self.in_studio = ttk.Combobox(self.sub_win, values=list(self.manager.studios), width=42)
            self.in_studio.pack(padx=30, pady=2)

            lbl_num = "Czas trwania (min) *" if self.category == "Film" else "Ilość odcinków *"
            tk.Label(self.sub_win, text=lbl_num, font=("Arial", 9, "bold")).pack(anchor="w", padx=30)
            self.in_numeric = tk.Entry(self.sub_win, width=45)
            self.in_numeric.pack(padx=30, pady=2)

        elif self.category == "Książka":
            tk.Label(self.sub_win, text="Autor (Wybierz lub wpisz)", font=("Arial", 9, "bold")).pack(anchor="w",
                                                                                                     padx=30)
            self.in_author = ttk.Combobox(self.sub_win, values=list(self.manager.authors), width=42)
            self.in_author.pack(padx=30, pady=2)

            tk.Label(self.sub_win, text="Ilość stron *", font=("Arial", 9, "bold")).pack(anchor="w", padx=30)
            self.in_numeric = tk.Entry(self.sub_win, width=45)
            self.in_numeric.pack(padx=30, pady=2)

        tk.Label(self.sub_win, text="Zdjęcie okładki", font=("Arial", 9, "bold")).pack(anchor="w", padx=30)
        img_row = tk.Frame(self.sub_win)
        img_row.pack(fill="x", padx=30, pady=2)
        self.img_path_label = tk.Label(img_row, text="Brak wybranego pliku", fg="grey", anchor="w", width=25)
        self.img_path_label.pack(side="left")
        tk.Button(img_row, text="...", command=self.handle_file_picker).pack(side="right")

        tk.Label(self.sub_win, text="Status *", font=("Arial", 9, "bold")).pack(anchor="w", padx=30)
        self.in_status = ttk.Combobox(self.sub_win, values=STATUS_LIST, state="readonly", width=42)
        self.in_status.set(STATUS_LIST[0])
        self.in_status.pack(padx=30, pady=2)

        tk.Label(self.sub_win, text="Gatunki (Można wybrać kilka)", font=("Arial", 9, "bold")).pack(anchor="w", padx=30,
                                                                                                    pady=(5, 0))
        g_box = tk.LabelFrame(self.sub_win, text=" Lista gatunków ", padx=10, pady=5)
        g_box.pack(fill="both", expand=True, padx=30, pady=5)

        self.checkbox_references = {}
        for genre_name in GENRE_POOL:
            boolean_var = tk.BooleanVar()
            chk = tk.Checkbutton(g_box, text=genre_name, variable=boolean_var)
            chk.pack(anchor="w")
            self.checkbox_references[genre_name] = boolean_var


        tk.Button(self.sub_win, text="➕ Utwórz", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white",
                  command=self.process_form_submission).pack(pady=10)

    def handle_file_picker(self):
        chosen_path = filedialog.askopenfilename(filetypes=[("Grafika", "*.png *.jpg *.jpeg")])
        if chosen_path:
            self.img_path_label.config(text=chosen_path, fg="black")

    def process_form_submission(self):
        try:
            extracted_name = self.in_name.get().strip()
            if not extracted_name:
                raise WlasnyError("Nazwa nie może być pusta!")

            chosen_genres = [g_key for g_key, v_obj in self.checkbox_references.items() if v_obj.get()]
            if not chosen_genres:
                raise WlasnyError("Zaznacz przynajmniej jeden gatunek!")

            status_value = self.in_status.get()
            raw_img = self.img_path_label.cget("text")
            img_cleaned = "" if "Brak" in raw_img else raw_img

            numeric_string = self.in_numeric.get().strip()
            if not numeric_string.isdigit():
                raise WlasnyError("Wartość liczbowa musi zasierać tylko cyfry")
            numeric_val = int(numeric_string)

            if self.category == "Film":
                studio_title = self.in_studio.get().strip()
                if not studio_title: raise WlasnyError("Wpisz lub wybierz Studio!")
                new_node = Movie(extracted_name, int(self.in_year.get()), studio_title, numeric_val, chosen_genres,
                                 status_value, img_cleaned)
            elif self.category == "Serial":
                studio_title = self.in_studio.get().strip()
                if not studio_title: raise WlasnyError("Wpisz lub wybierz Studio!")
                new_node = Series(extracted_name, int(self.in_year.get()), studio_title, numeric_val, chosen_genres,
                                  status_value, img_cleaned)
            elif self.category == "Książka":
                author_title = self.in_author.get().strip()
                if not author_title: raise WlasnyError("Wpisz lub wybierz Autora!")
                new_node = Book(extracted_name, author_title, numeric_val, chosen_genres, status_value, img_cleaned)

            self.manager.add_item(new_node)
            Database.save_to_file(self.manager)
            self.sync_callback()

            messagebox.showinfo("Sukces", "Pomyślnie dodano element do bazy!")
            self.sub_win.destroy()

        except WlasnyError as error_context:
            messagebox.showwarning("Błąd walidacji", str(error_context))
        except Exception as system_error:
            messagebox.showerror("Błąd fatalny", f"Nieoczekiwany błąd: {system_error}")
