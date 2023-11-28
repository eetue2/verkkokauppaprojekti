import tkinter as tk
from csv_commands import read_data_from_csv
from mainfunktiot import teksti_saato, widgets_to_clear, nappivari, button_width, clear_screen
from orders import tilaushaku
from users import admin, load_user_data_from_csv
from products import lisays, poista, tuotehaku, paivitys

user_csv_file_path = 'kayttajat.csv'


def create_admin_button(right_sidebar, main_window, text, command_function, *args):
    button = tk.Button(right_sidebar, text=text, command=lambda: command_function(main_window, *args),
                       width=button_width)
    nappivari(button)
    button.pack(pady=5)


def show_admin_buttons(right_sidebar, main_window, user_csv_file_path):
    clear_screen(widgets_to_clear)
    create_admin_button(right_sidebar, main_window, "Tilauslista", avaa_listaus)
    create_admin_button(right_sidebar, main_window, "Näytä tuotteet", avaa_tuotelista)
    create_admin_button(right_sidebar, main_window, "Lisää tuote", avaa_lisays)
    create_admin_button(right_sidebar, main_window, "Poista tuote", avaa_poisto)
    create_admin_button(right_sidebar, main_window, "Päivitä tuote", avaa_paivitys)
    create_admin_button(right_sidebar, main_window, "Hae tuote", avaa_tuotehaku)
    create_admin_button(right_sidebar, main_window, "Hae tilaus", avaa_tilaushaku)
    create_admin_button(right_sidebar, main_window, "Hae käyttäjä", avaa_adminhaku, user_csv_file_path)


def hide_admin_buttons(right_sidebar):
    for widget in right_sidebar.winfo_children():
        widget.destroy()


# ADMIN LOGIN
def login_admin_callback(main_window, right_sidebar):
    hide_admin_buttons(right_sidebar)
    clear_screen(widgets_to_clear)

    otsikko = tk.Label(main_window, text="Kirjaudu sisään ylläpitäjänä")
    otsikko.pack(pady=10)

    salasana_label = tk.Label(main_window, text="Salasana:")
    salasana_label.pack(pady=5)

    adminsalasana = tk.Entry(main_window, show="*")
    adminsalasana.pack(pady=5)

    def submit():
        ad_salasana = adminsalasana.get()
        if admin(ad_salasana):
            clear_screen(widgets_to_clear)
            show_admin_buttons(right_sidebar, main_window, user_csv_file_path)
        else:
            hide_admin_buttons(right_sidebar)
            error_label_sala = tk.Label(main_window, text="", fg="red", bg="black")
            error_label_sala.pack(pady=5)
            error_label_sala.config(text="Virheellinen salasana", fg="red", bg="black")
            widgets_to_clear.extend(
                [error_label_sala])

    submit_button = tk.Button(main_window, text="Kirjaudu", command=submit, width=button_width)
    nappivari(submit_button)
    submit_button.pack(pady=5)

    main_window.bind('<Return>', lambda event=None: submit_button.invoke())
    teksti_saato(main_window)

    widgets_to_clear.extend(
        [otsikko, salasana_label, adminsalasana, submit_button])


# TUOTTEEN LISÄYS
def avaa_lisays(main_window):
    clear_screen(widgets_to_clear)

    otsikko = tk.Label(main_window, text="Tuotteen lisäys")
    otsikko.pack(pady=20)

    name_label = tk.Label(main_window, text="Tuotteen nimi:")
    name_label.pack(pady=5)

    name_entry = tk.Entry(main_window)
    name_entry.pack(pady=5)

    price_label = tk.Label(main_window, text="Tuotteen hinta:")
    price_label.pack(pady=5)

    price_entry = tk.Entry(main_window)
    price_entry.pack(pady=5)

    def submit():
        try:
            result = lisays(name_entry.get(), float(price_entry.get()))
            if result:
                message_label = tk.Label(main_window, text="Tuote lisätty, jatka tai palaa takaisin.", fg="green",
                                         bg="black")
            else:
                message_label = tk.Label(main_window, text="Tuote on jo valikoimassa", fg="red")
        except ValueError:
            message_label = tk.Label(main_window, text="Tuotteen lisääminen epäonnistui, onko hinta oikeassa muodossa?",
                                     fg="red", bg="black")
        widgets_to_clear.extend([message_label])

        message_label.pack(pady=5)

    submit_button = tk.Button(main_window, text="Lisää", command=submit, width=button_width)
    nappivari(submit_button)
    submit_button.pack(pady=5)
    main_window.bind('<Return>', lambda event=None: submit_button.invoke())
    teksti_saato(main_window)
    widgets_to_clear.extend(
        [otsikko, name_label, name_entry, price_label, price_entry, submit_button])


# POISTA TUOTE
def avaa_poisto(main_window):
    clear_screen(widgets_to_clear)

    otsikko = tk.Label(main_window, text="Tuotteen poisto", font=("Arial", 20))
    otsikko.pack(pady=20)

    name_label = tk.Label(main_window, text="Tuotteen nimi:")
    name_label.pack(pady=5)

    name_entry = tk.Entry(main_window)
    name_entry.pack(pady=5)

    def submit():
        result = poista(name_entry.get())
        if result:
            poisto_label = tk.Label(main_window, text="")
            poisto_label.pack(pady=5)
            poisto_label.config(text="Tuote poistettu, jatka tai palaa takaisin.", fg="green", bg="black")
        else:
            poisto_label = tk.Label(main_window, text="")
            poisto_label.pack(pady=5)
            poisto_label.config(text="Tuotteen poistaminen epäonnistui, onko tuote olemassa?", fg="red", bg="black")
        widgets_to_clear.extend([poisto_label])

    submit_button = tk.Button(main_window, text="Poista", command=submit, width=button_width)
    nappivari(submit_button)
    submit_button.pack(pady=5)
    main_window.bind('<Return>', lambda event=None: submit_button.invoke())
    teksti_saato(main_window)
    widgets_to_clear.extend([otsikko, name_label, name_entry, message_label, submit_button])


# TUOTELISTA
import tkinter as tk
from csv_commands import read_data_from_csv

def avaa_tuotelista(main_window):
    clear_screen(widgets_to_clear)

    otsikko = tk.Label(main_window, text="Tuotevalikoima", fg="green", bg="black", font=("Arial", 14))
    otsikko.pack(pady=20)

    tuote_column_names = ['product', 'price', 'product_id']
    tuotteet_data = read_data_from_csv('tuotteet.csv', tuote_column_names)
    poistetut_tuotteet_data = read_data_from_csv('poistetut_tuotteet.csv', tuote_column_names)

    tuotteet = tuotteet_data.keys()

    for tuote in tuotteet:
        product_info = tuotteet_data[tuote][0]
        product_label = tk.Label(main_window,
                                 text=f"{tuote} - {product_info['price']} € (ID: {product_info['product_id']})",
                                 fg="green", bg="black", font=("Arial", 9))
        product_label.pack(pady=5)
        widgets_to_clear.extend([product_label])

    poistetut_tuotteet = poistetut_tuotteet_data.keys()

    for tuote in poistetut_tuotteet:
        product_info = poistetut_tuotteet_data[tuote][0]
        product_label = tk.Label(main_window,
                                 text=f"{tuote} - {product_info['price']} € (ID: {product_info['product_id']}) - Poistettu",
                                 fg="red", bg="black", font=("Arial", 9))
        product_label.pack(pady=5)
        widgets_to_clear.extend([product_label])

    widgets_to_clear.extend([otsikko])


# TUOTEHAKU


def avaa_tuotehaku(main_window):
    clear_screen(widgets_to_clear)

    otsikko = tk.Label(main_window, text="Tuotehaku", font=("Arial", 20))
    otsikko.pack(pady=20)

    def submit(tuotehaku_tulos):
        search_term = name_entry.get()

        if tuotehaku_tulos:
            tuotehaku_tulos.destroy()

        result = tuotehaku(search_term)
        if result:
            product_text = f"Hakutulos: {search_term} - Tuote: {result['product']}, Hinta: {result['price']} €, ID: {result['tuote id']}"
            if 'status' in result and result['status'] == 'poistettu':
                updated_result_label = tk.Label(main_window, text=product_text + " - Poistettu", fg="red", bg="black")
            else:
                updated_result_label = tk.Label(main_window, text=product_text, fg="green", bg="black")

            updated_result_label.pack()
            widgets_to_clear.extend([updated_result_label])
        else:
            updated_result_label = tk.Label(main_window, text="Tuotetta ei löytynyt, tarkista hakutermi", fg="red", bg="black")
            updated_result_label.pack()
            widgets_to_clear.extend([updated_result_label])

        return updated_result_label

    name_label = tk.Label(main_window, text="Tuotteen nimi tai tuotenumero:")
    name_label.pack(pady=5)

    name_entry = tk.Entry(main_window)
    name_entry.pack(pady=5)

    tuotehaku_label = None

    def submit_handler():
        nonlocal tuotehaku_label
        tuotehaku_label = submit(tuotehaku_label)

    submit_button = tk.Button(main_window, text="Hae", command=submit_handler, width=button_width)
    nappivari(submit_button)
    submit_button.pack(pady=5)

    main_window.bind('<Return>', lambda event=None: submit_button.invoke())
    teksti_saato(main_window)
    widgets_to_clear.extend([otsikko, name_label, name_entry, submit_button])


# TUOTTEEN PÄIVITYS
def avaa_paivitys(main_window):
    clear_screen(widgets_to_clear)

    otsikko = tk.Label(main_window, text="Tuotteen päivitys", font=("Arial", 20))
    otsikko.pack(pady=20)

    name_label = tk.Label(main_window, text="Tuotteen nimi:")
    name_label.pack(pady=5)

    name_entry = tk.Entry(main_window)
    name_entry.pack(pady=5)

    price_label = tk.Label(main_window, text="Uusi hinta:")
    price_label.pack(pady=5)

    price_entry = tk.Entry(main_window)
    price_entry.pack(pady=5)

    def submit():
        try:
            paivtuot = name_entry.get()
            hinnim = float(price_entry.get())
            result = paivitys(paivtuot, hinnim)
            if result:
                message_label = tk.Label(main_window, text="", fg="black", bg="white")
                message_label.pack(pady=5)
                message_label.config(text="Tuotteen hinta päivitetty", fg="green", bg="black")
            else:
                message_label = tk.Label(main_window, text="", fg="black", bg="white")
                message_label.pack(pady=5)
                message_label.config(text="Tuotteen päivittäminen epäonnistui, tarkista tuotteen nimi", fg="red",
                                     bg="black")
        except ValueError:
            message_label = tk.Label(main_window, text="", fg="black", bg="white")
            message_label.pack(pady=5)
            message_label.config(text="Tuotteen päivitys epäonnistui, onko hinta oikeassa muodossa?", fg="red",
                                 bg="black")

    submit_button = tk.Button(main_window, text="Päivitä hinta", command=submit, width=button_width)
    submit_button.pack(pady=5)
    nappivari(submit_button)
    main_window.bind('<Return>', lambda event=None: submit_button.invoke())
    teksti_saato(main_window)
    widgets_to_clear.extend(
        [otsikko, name_label, name_entry, price_label, price_entry, message_label, submit_button])


# KÄYTTÄJÄN HAKU (ADMIN)
def avaa_adminhaku(main_window, user_csv_file_path):
    clear_screen(widgets_to_clear)

    def submit_search():
        user_name = name_entry.get()
        tunnukset, postit, _ = load_user_data_from_csv(user_csv_file_path)

        if user_name not in tunnukset:
            result_text = "Käyttäjää ei löydy"
        else:
            haku_index = tunnukset.index(user_name)
            result_text = f"""tunnus:{tunnukset[haku_index]} sähköposti:{postit[haku_index]}"""
        tulos_label = tk.Label(main_window)
        tulos_label.pack()
        tulos_label.config(text=result_text)
        teksti_saato(main_window)
        widgets_to_clear.extend([tulos_label])

    clear_screen(widgets_to_clear)

    otsikko = tk.Label(main_window, text="Käyttäjätietojen haku", font=("Arial", 20))
    otsikko.pack(pady=20)

    name_label = tk.Label(main_window, text="Käyttäjän nimi:")
    name_label.pack(pady=5)

    name_entry = tk.Entry(main_window)
    name_entry.pack(pady=5)

    submit_button = tk.Button(main_window, text="Hae", command=submit_search, width=button_width)
    nappivari(submit_button)
    submit_button.pack(pady=5)

    main_window.bind('<Return>', lambda event=None: submit_button.invoke())
    teksti_saato(main_window)
    widgets_to_clear.extend([otsikko, name_label, name_entry, submit_button])


def avaa_tilaushaku(main_window):
    clear_screen(widgets_to_clear)

    otsikko = tk.Label(main_window, text="Tilaushaku", font=("Arial", 20))
    otsikko.pack(pady=20)

    def submit(tilaushaku_tulos):
        ordernumber = int(name_entry.get())

        if tilaushaku_tulos:
            tilaushaku_tulos.destroy()

        result = tilaushaku(ordernumber)
        if result:
            updated_result_label = tk.Label(
                main_window,
                text=f"Tilaustiedot: Käyttäjä: {result[0]}, Tuote: {result[1]}, Määrä: {result[2]}, Tilausnumero: {result[3]}",
                fg="green",
                bg="black"
            )
            updated_result_label.pack()
            widgets_to_clear.extend([updated_result_label])
        else:
            updated_result_label = tk.Label(main_window, text="Tilausta ei löytynyt, tarkista tilausnumero", fg="red",
                                            bg="black")
            updated_result_label.pack()
            widgets_to_clear.extend([updated_result_label])

        return updated_result_label

    name_label = tk.Label(main_window, text="Tilausnumero:")
    name_label.pack(pady=5)

    name_entry = tk.Entry(main_window)
    name_entry.pack(pady=5)

    result_label = None

    def submit_handler():
        nonlocal result_label
        result_label = submit(result_label)

    submit_button = tk.Button(main_window, text="Hae", command=submit_handler, width=button_width)
    nappivari(submit_button)
    submit_button.pack(pady=5)

    main_window.bind('<Return>', lambda event=None: submit_button.invoke())
    teksti_saato(main_window)
    widgets_to_clear.extend([otsikko, name_label, name_entry, submit_button])


# TILAUSLISTA
message_label = None


def avaa_listaus(main_window):
    clear_screen(widgets_to_clear)

    otsikko = tk.Label(main_window, text="Tilauslista", font=("Arial", 20), fg="green", bg="black")
    otsikko.pack(pady=20)

    messaging_label = None

    tilaus_column_names = ['kayttaja', 'tuote', 'counter', 'tilausnumero']
    orders_data = read_data_from_csv("tilaukset.csv", tilaus_column_names)

    if not orders_data:
        messaging_label = tk.Label(main_window, text="Tilauslista on tyhjä", fg="red", bg="black")
        messaging_label.pack(pady=1)
    else:
        for user, order_list in orders_data.items():
            user_label = tk.Label(main_window, text=f"Tilaukset käyttäjältä {user}:", bg="black", fg="yellow",
                                  font=("Arial", 12))
            user_label.pack(pady=1)
            for order in order_list:
                order_label = tk.Label(main_window,
                                       text=f"Tuote: {order['tuote']}, Määrä: {order['counter']}, Tilausnumero: {order['tilausnumero']}",
                                       fg="green", bg="black", font=("Arial", 10))
                order_label.pack(pady=1)

                widgets_to_clear.extend([otsikko, messaging_label, order_label, user_label])
