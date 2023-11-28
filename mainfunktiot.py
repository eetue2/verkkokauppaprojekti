import csv
from collections import defaultdict

from orders import tilaus, tilaukset_csv_file, kayttajan_tilaukset
from users import rektun, rekpos, kirjaudu, load_user_data_from_csv, user_csv_file_path

widgets_to_clear = []
from PIL import Image, ImageTk
import tkinter as tk


def teksti_saato(window, font=("Arial", 16), text_color="green", bg_color="black", active_fg="yellow",
                 active_bg="white"):
    for widget in window.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(font=font, fg=text_color, bg=bg_color, activeforeground=active_fg, activebackground=active_bg)


def clear_screen(widgets_to_clear):
    for widget in widgets_to_clear:
        if widget is not None:
            widget.destroy()


# NAPIT
button_width = 10


def nappivari(button, text_color="green"):
    button.config(fg=text_color, bg="black", activeforeground="green", activebackground="black", font=("Arial", 12))


# TAUSTA

bg_photo_image = None
bg_image = None


def set_background_image(main_window):
    global bg_image

    original_image = Image.open("2563.jpg")
    bg_image = ImageTk.PhotoImage(original_image)

    bg_label = tk.Label(main_window, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)


# REKISTERÖITYMINEN
def register_user(main_window, right_sidebar):
    from adminfunktiot import hide_admin_buttons
    hide_admin_buttons(right_sidebar)
    clear_screen(widgets_to_clear)
    content_label = tk.Label(main_window, text="Rekisteröidy")
    content_label.pack()

    kayttaja = tk.StringVar()
    sposti = tk.StringVar()
    salasana = tk.StringVar()

    # Load user data from CSV
    tunnukset, postit, salasanat = load_user_data_from_csv(user_csv_file_path)

    def check_and_register():
        nonlocal tunnukset, postit, salasanat
        username = kayttaja.get()
        email = sposti.get()
        password = salasana.get()

        if not all([username, email, password]):
            error_label = tk.Label(main_window, text="Kaikki kentät ovat pakollisia.")
            error_label.pack(pady=5)
            widgets_to_clear.extend([error_label])
            teksti_saato(main_window)
        elif not rektun(username, tunnukset):
            error_label = tk.Label(main_window, text="Käyttäjänimi on jo käytössä")
            error_label.pack(pady=5)
            widgets_to_clear.extend([error_label])
            teksti_saato(main_window)
        elif not rekpos(email, postit):
            error_label = tk.Label(main_window, text="Sähköpostiosoite jo käytössä tai väärässä muodossa")
            error_label.pack(pady=5)
            widgets_to_clear.extend([error_label])
            teksti_saato(main_window)
        else:
            tunnukset.append(username)
            postit.append(email)
            salasanat.append(password)

            # Save only the new user data
            with open(user_csv_file_path, 'a', newline='') as user_file:
                user_writer = csv.writer(user_file)
                user_writer.writerow([username, email, password])

            clear_screen(widgets_to_clear)

            success_label = tk.Label(main_window, text=f"""Rekisteröinti onnistui
    Tervetuloa asiakkaaksi 
    {username}!""")
            success_label.pack(pady=5)
            teksti_saato(main_window)
            widgets_to_clear.append(success_label)

    labels = ["Käyttäjätunnus", "Sähköposti", "Salasana"]
    entries = [kayttaja, sposti, salasana]

    label_widgets = []
    entry_widgets = []
    for i, label in enumerate(labels):
        label_widget = tk.Label(main_window, text=label + ":", pady=5, bg="black")
        label_widget.pack(pady=5)
        label_widgets.append(label_widget)

        if label == "Salasana":
            entry_widget = tk.Entry(main_window, textvariable=entries[i], show='*')
        else:
            entry_widget = tk.Entry(main_window, textvariable=entries[i])

        entry_widget.pack(pady=5)
        entry_widgets.append(entry_widget)

    def submit_handler():
        if all(entries):
            check_and_register()

    submit_button = tk.Button(main_window, text="Rekisteröidy", command=submit_handler)
    nappivari(submit_button)
    submit_button.pack(pady=5)

    main_window.bind('<Return>', lambda event=None: submit_handler())
    teksti_saato(main_window)

    widgets_to_clear.extend(
        [content_label, submit_button] + label_widgets + entry_widgets)


# KIRJAUTUMINEN
def login_user(main_window, right_sidebar):
    from adminfunktiot import hide_admin_buttons
    hide_admin_buttons(right_sidebar)
    clear_screen(widgets_to_clear)
    content_label = tk.Label(main_window, text="Kirjaudu")
    content_label.pack()

    username_label = tk.Label(main_window, text="Käyttäjätunnus:")
    username_label.pack(pady=5)

    kayttaja_entry = tk.Entry(main_window)
    kayttaja_entry.pack(pady=5)

    salasana_label = tk.Label(main_window, text="Salasana:")
    salasana_label.pack(pady=5)
    salasana_entry = tk.Entry(main_window, show="*")
    salasana_entry.pack(pady=5)

    def submit():
        tunnukset, _, salasanat = load_user_data_from_csv(user_csv_file_path)
        kayttaja = kayttaja_entry.get()
        if kirjaudu(kayttaja, salasana_entry.get(), tunnukset, salasanat):
            viikonloppukauppa(main_window, kayttaja)
        else:
            error_label_kayttaja = tk.Label(main_window, text="Virheellinen käyttäjätunnus tai salasana", bg="black",
                                            fg="red")
            error_label_kayttaja.pack(pady=5)
            widgets_to_clear.extend([error_label_kayttaja])

    submit_button = tk.Button(main_window, text="Kirjaudu", command=submit, width=button_width)
    nappivari(submit_button)
    submit_button.pack(pady=5)
    main_window.bind('<Return>', lambda event=None: submit_button.invoke())
    teksti_saato(main_window)
    widgets_to_clear.extend(
        [content_label, username_label, kayttaja_entry, salasana_label, salasana_entry, submit_button])


# KAUPPAIKKUNA
def get_next_tilausnumero():
    with open(tilaukset_csv_file, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    if not rows:
        return 1

    latest_tilausnumero = max(int(row['tilausnumero']) for row in rows)
    return latest_tilausnumero + 1


def viikonloppukauppa(main_window, kayttaja):
    clear_screen(widgets_to_clear)

    counter = defaultdict(int)
    count_labels = {}

    otsikko = tk.Label(main_window, text="Tervetuloa viikonloppukauppaan", font=("Arial", 24))
    otsikko.pack(pady=20)

    selected_products = []

    product_column_names = ['product', 'price', 'product_id']
    from csv_commands import read_data_from_csv
    tuotteet_data = read_data_from_csv('tuotteet.csv', column_names=product_column_names)

    def nappi1(product, price):
        if product not in selected_products:
            selected_products.append(product)
        counter[product] += 1
        count_labels[product].config(text=f"{counter[product]}")

    # Iterate over products and create buttons
    for product, values_list in tuotteet_data.items():
        # Check if values_list has at least 1 element
        if values_list:
            values = values_list[0]
            price = float(values['price'])
            button = tk.Button(main_window, text=f"{product} - {price:.2f} €",
                               command=lambda p=product, pr=price: nappi1(p, pr),
                               width=15)
            nappivari(button)
            button.pack(side="top", anchor="s", pady=2)
            count_labels[product] = tk.Label(main_window, text=f"{counter[product]}", fg="black")
            count_labels[product].pack(side="right", anchor="n", padx=10)
            widgets_to_clear.extend([button, count_labels[product], otsikko])
        else:
            print(f"Skipping product {product} due to insufficient data. Values: {values_list}")

    def tilaa_command(kayttaja=kayttaja, main_window=main_window):
        orders_button.config(state="disabled")
        tilausnumero = get_next_tilausnumero()  # Get the next tilausnumero
        for tuote in selected_products:
            tilaus(kayttaja, tuote, counter, tilausnumero)
        tilaus_message(main_window, kayttaja)

    orders_button = tk.Button(main_window, text="Tilaa", command=tilaa_command, width=button_width)
    nappivari(orders_button)
    teksti_saato(main_window)
    orders_button.pack(side="right", pady=1, anchor="e")  # Use pack layout
    widgets_to_clear.append(orders_button)



def tilaus_message(main_window, kayttaja):
    clear_screen(widgets_to_clear)

    clear_screen(widgets_to_clear)

    # Load the background image
    image = Image.open('tiltausta.jpg')
    background_image = ImageTk.PhotoImage(image)
    background_label = tk.Label(main_window, image=background_image)
    background_label.image = background_image
    background_label.place(x=110, y=0, relwidth=0.8, relheight=1)
    widgets_to_clear.append(background_label)

    kiitos_label = tk.Label(main_window, text="Kiitos tilauksesta!")
    kiitos_label.place(x=120, y=15)
    widgets_to_clear.append(kiitos_label)

    reminder_label = tk.Label(main_window, text="""Ystävälliset
    velanperijämme,
    Boris & Igor
    ottavat yhteyttä
    ellei maksua
    suoriteta
    viikon sisällä""")
    reminder_label.place(x=95, y=130)
    teksti_saato(main_window)
    widgets_to_clear.append(reminder_label)
    paluu_button = tk.Button(main_window, text="Takaisin", command=lambda: viikonloppukauppa(main_window, kayttaja),
                             width=button_width)

    def nayta_tilaukset(kayttaja):
        orders = kayttajan_tilaukset(kayttaja)
        if orders:
            orders_by_number = defaultdict(list)
            for order in orders:
                orders_by_number[order[3]].append(f"{order[1]} {order[2]} kpl")
            orders_text = "".join([f"Tilausnumerolla {order_number}:\n{', '.join(items)}\n" for order_number, items in
                                     orders_by_number.items()])
            reminder_label.config(text=f"""Sinun tilaukset ovat:\n{orders_text}""")
            reminder_label.place(x=108, y=0)
        else:
            reminder_label.config(text="Sinulla ei ole tilauksia")

    nappivari(paluu_button)
    paluu_button.place(x=4, y=360)
    widgets_to_clear.append(paluu_button)
    tilaukset_button = tk.Button(main_window, text="Omat tilaukset", command=lambda: nayta_tilaukset(kayttaja),
                                 width=button_width)
    nappivari(tilaukset_button)
    tilaukset_button.place(x=4, y=300)
    widgets_to_clear.append(tilaukset_button)

