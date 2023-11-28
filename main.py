
import tkinter as tk

from mainfunktiot import set_background_image, login_user, register_user, nappivari, \
    widgets_to_clear
from adminfunktiot import login_admin_callback

admin_logged_in = False

def main():
    global bg_image
    main_window = tk.Tk()
    main_window.geometry("700x400+520+150")
    main_window.title("Viikonlopun verkkokauppa")

    canvas = tk.Canvas(main_window, width=700, height=400)
    canvas.pack(expand=tk.YES, fill=tk.BOTH)
    main_window.resizable(width=False, height=False)

    set_background_image(canvas)

    message_label = tk.Label(canvas, text="Tervetuloa kaupoille", fg="green", bg="black", font=("Arial", 32))
    message_label.pack(pady=0)
    widgets_to_clear.extend([message_label])


    side_menu = tk.Frame(canvas, width=200, bg="black")
    side_menu.pack(side="left", fill="y")

    right_sidebar = tk.Frame(canvas, width=120, bg="black")
    right_sidebar.pack(side="right", fill="y")
    register_button = tk.Button(side_menu, text="Rekisteröidy", command=lambda: register_user(canvas, right_sidebar))
    nappivari(register_button)
    register_button.pack(fill="x", padx=5, pady=5)

    login_button = tk.Button(side_menu, text="Kirjaudu", command=lambda: login_user(canvas, right_sidebar))
    nappivari(login_button)
    login_button.pack(fill="x", padx=5, pady=5)

    admin_button = tk.Button(side_menu, text="Admin", command=lambda: login_admin_callback(canvas, right_sidebar))
    nappivari(admin_button)
    admin_button.pack(fill="x", padx=5, pady=5)

    exit_button = tk.Button(side_menu, text="Poistu", command=main_window.destroy)
    nappivari(exit_button)
    exit_button.pack(fill="x", padx=5, pady=5)

    main_window.mainloop()

if __name__ == '__main__':
    main()
