import tkinter as tk
from tkinter import messagebox

from services.db_manager import (db_init,
                                 get_all_users,
                                 create_user,
                                 delete_user)
from constants.ui_constants import (PACK_PANEL_PADX,
                                    PACK_PANEL_PADY,
                                    BUTTON_WIDTH,
                                    BUTTON_HEIGHT)


db_init()

main_window = tk.Tk()
main_window.title('Smart Key')
main_window.geometry('600x900')

#region Funkcije
def doorbell():
    lbl_message_var.set('Zvono je aktivirano\nUskoro ce netko otvoriti vrata.')
    # ili
    messagebox.showinfo('Info', 'Zvono je aktivirano\nUskoro ce netko otvoriti vrata.')


def unlock():
    print('Gumb Otkljucaj je kliknut!')
    frm_pin.pack(padx=PACK_PANEL_PADX, pady=PACK_PANEL_PADY)
    frm_admin.pack(padx=PACK_PANEL_PADX, pady=PACK_PANEL_PADY)


def pin_button_1():
    pin(number='1')

def pin_button_2():
    pin(number='2')

def pin_button_3():
    pin(number='3')

def pin_button_4():
    pin(number='4')

def pin_button_5():
    pin(number='5')

def pin_button_6():
    pin(number='6')

def pin_button_7():
    pin(number='7')

def pin_button_8():
    pin(number='8')

def pin_button_9():
    pin(number='9')

def pin_button_0():
    pin(number='0')

def pin_button_c():
    pin(reset=True)

def pin_button_ce():
    lbl_pin_var.set('')
    update_pin_display_board(lbl_pin_var.get())

def pin(number: str = '', reset: bool = False):
    pin_value = lbl_pin_var.get()

    if reset:
        if len(pin_value) == 0:
            # Provjeri PIN, ako je OK, onda idi dalje, ako nije prikazi porku
            print(f'{number} {reset}')
            return
        pin_value = pin_value[ : -1]
        lbl_pin_var.set(pin_value)
        print(lbl_pin_var.get())
        update_pin_display_board(lbl_pin_var.get())
        return

    if len(pin_value) == 4:
        print(lbl_pin_var.get())
        return

    pin_value += number
    lbl_pin_var.set(pin_value)
    print(lbl_pin_var.get())
    update_pin_display_board(lbl_pin_var.get())

    if len(pin_value) == 4:
        # Provjeri PIN, ako je OK, onda idi dalje, ako nije prikazi porku
        print(f'{number} {reset}')

def update_pin_display_board(pin: str = ''):
    pin_lenght = len(pin)
    match pin_lenght:
        case 0:
            lbl_pin_1_var.set('')
            lbl_pin_2_var.set('')
            lbl_pin_3_var.set('')
            lbl_pin_4_var.set('')
        case 1:
            lbl_pin_1_var.set(pin[0])
            lbl_pin_2_var.set('')
            lbl_pin_3_var.set('')
            lbl_pin_4_var.set('')
        case 2:
            lbl_pin_1_var.set(pin[0])
            lbl_pin_2_var.set(pin[1])
            lbl_pin_3_var.set('')
            lbl_pin_4_var.set('')
        case 3:
            lbl_pin_1_var.set(pin[0])
            lbl_pin_2_var.set(pin[1])
            lbl_pin_3_var.set(pin[2])
            lbl_pin_4_var.set('')
        case 4:
            lbl_pin_1_var.set(pin[0])
            lbl_pin_2_var.set(pin[1])
            lbl_pin_3_var.set(pin[2])
            lbl_pin_4_var.set(pin[3])


def fill_listbox():
    users = get_all_users()
    lb_users.delete(0, tk.END)

    for user in users:
        lb_users.insert(tk.END, user)


def on_user_select(event):
    users = get_all_users()
    selection = lb_users.curselection()
    if selection:
        selected_index = selection[0]
        selected_user = users[selected_index]

        user_id_var.set(selected_user[0])
        user_first_name_var.set(selected_user[1])
        user_last_name_var.set(selected_user[2])
        user_pin_var.set(selected_user[3])
        user_is_active_var.set(selected_user[4])


def on_save_user():
    id = user_id_var.get()

    if id != 0:
        create_user(user_first_name_var.get(),
                    user_last_name_var.get(),
                    user_pin_var.get(),
                    user_is_active_var.get(),
                    id)
    else:
        create_user(user_first_name_var.get(),
                    user_last_name_var.get(),
                    user_pin_var.get(),
                    user_is_active_var.get())
    on_cancel()


def on_delete_user():
    id = user_id_var.get()

    if id != 0:
        delete_user(id)
    on_cancel()


def on_cancel():
    lb_users.selection_clear(0, tk.END)
    user_id_var.set(0)
    user_first_name_var.set('')
    user_last_name_var.set('')
    user_pin_var.set('')
    user_is_active_var.set(False)
    fill_listbox()

#endregion


#region Frame s gumbima
frm_buttons = tk.Frame(main_window,
                       borderwidth=2,
                       relief=tk.RAISED)
frm_buttons.pack(padx=PACK_PANEL_PADX, pady=PACK_PANEL_PADY)
frm_buttons.columnconfigure(0, minsize=200)
frm_buttons.columnconfigure(1, minsize=200)

# Labela
lbl_message_var = tk.StringVar()
lbl_message_var.set('')
lbl_message = tk.Label(frm_buttons,
                       textvariable=lbl_message_var)
lbl_message.grid(row=0, column=0, columnspan=2, sticky='ew')
# Gumbi
btn_doorbell = tk.Button(frm_buttons,
                         text='Pozvoni',
                         command=doorbell)
btn_doorbell.grid(row=1, column=0,
                  sticky='w',
                  padx=PACK_PANEL_PADX, pady=PACK_PANEL_PADY)

btn_unlock = tk.Button(frm_buttons,
                       text='Otkljucaj',
                       command=unlock)
btn_unlock.grid(row=1, column=1,
                sticky='e',
                padx=PACK_PANEL_PADX, pady=PACK_PANEL_PADY)

#endregion

#region Frame s gumbima
frm_pin = tk.Frame(main_window,
                   borderwidth=2,
                   relief=tk.RAISED)
frm_pin.columnconfigure(0, weight=1)
frm_pin.columnconfigure(1, weight=2)

#region PIN display board
frm_pin_board = tk.Frame(frm_pin)
frm_pin_board.grid(row=0, column=0, sticky='w')

lbl_pin_var = tk.StringVar()
lbl_pin_var.set('')
lbl_pin_1_var = tk.StringVar()
lbl_pin_1 = tk.Label(frm_pin_board, textvariable=lbl_pin_1_var, width=10, height=10)
lbl_pin_1.grid(row=0, column=0)
lbl_pin_2_var = tk.StringVar()
lbl_pin_2 = tk.Label(frm_pin_board, textvariable=lbl_pin_2_var, width=10, height=10)
lbl_pin_2.grid(row=0, column=1)
lbl_pin_3_var = tk.StringVar()
lbl_pin_3 = tk.Label(frm_pin_board, textvariable=lbl_pin_3_var, width=10, height=10)
lbl_pin_3.grid(row=0, column=2)
lbl_pin_4_var = tk.StringVar()
lbl_pin_4 = tk.Label(frm_pin_board, textvariable=lbl_pin_4_var, width=10, height=10)
lbl_pin_4.grid(row=0, column=3)

#region PIN buttons
btn_pin_1 = tk.Button(frm_pin_board,
                      text='1', width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                      command=pin_button_1)
btn_pin_1.grid(row=1, column=0)
btn_pin_2 = tk.Button(frm_pin_board,
                      text='2', width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                      command=pin_button_2)
btn_pin_2.grid(row=1, column=1)
btn_pin_3 = tk.Button(frm_pin_board,
                      text='3', width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                      command=pin_button_3)
btn_pin_3.grid(row=1, column=2)
btn_pin_4 = tk.Button(frm_pin_board,
                      text='4', width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                      command=pin_button_4)
btn_pin_4.grid(row=2, column=0)
btn_pin_5 = tk.Button(frm_pin_board,
                      text='5', width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                      command=pin_button_5)
btn_pin_5.grid(row=2, column=1)
btn_pin_6 = tk.Button(frm_pin_board,
                      text='6', width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                      command=pin_button_6)
btn_pin_6.grid(row=2, column=2)
btn_pin_7 = tk.Button(frm_pin_board,
                      text='7', width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                      command=pin_button_7)
btn_pin_7.grid(row=3, column=0)
btn_pin_8 = tk.Button(frm_pin_board,
                      text='8', width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                      command=pin_button_8)
btn_pin_8.grid(row=3, column=1)
btn_pin_9 = tk.Button(frm_pin_board,
                      text='9', width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                      command=pin_button_9)
btn_pin_9.grid(row=3, column=2)
btn_pin_ce = tk.Button(frm_pin_board,
                      text='CE', width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                      command=pin_button_ce)
btn_pin_ce.grid(row=4, column=0)
btn_pin_0 = tk.Button(frm_pin_board,
                      text='0', width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                      command=pin_button_0)
btn_pin_0.grid(row=4, column=1)
btn_pin_c = tk.Button(frm_pin_board,
                      text='C', width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                      command=pin_button_c)
btn_pin_c.grid(row=4, column=2)

#endregion

#endregion

frm_status_display = tk.Frame(frm_pin)
frm_status_display.grid(row=0, column=1, sticky='ew')

lbl_status_display_var = tk.StringVar()
lbl_status_display_var.set('Lorem ipsum')
lbl_status_display = tk.Label(frm_status_display,
                              textvariable=lbl_status_display_var)
lbl_status_display.grid(row=0, column=0,
                        sticky='eswn',
                        padx=PACK_PANEL_PADX, pady=PACK_PANEL_PADY)

#endregion

#region Admin Frame
frm_admin = tk.Frame(main_window,
                     borderwidth=2,
                     relief=tk.RAISED)
# frm_admin.pack(padx=PACK_PANEL_PADX, pady=PACK_PANEL_PADY)
frm_admin.columnconfigure(0, weight=1)
frm_admin.columnconfigure(1, weight=2)

# Listbox
frm_listbox = tk.Frame(frm_admin,
                       borderwidth=2,
                       relief=tk.RAISED)
frm_listbox.grid(row=0, column=0, padx=PACK_PANEL_PADX, pady=PACK_PANEL_PADY)

lb_users = tk.Listbox(frm_listbox)
lb_users.grid(row=0, column=0, padx=PACK_PANEL_PADX, pady=PACK_PANEL_PADY)

scrollbar = tk.Scrollbar(frm_listbox,
                         orient=tk.VERTICAL,
                         command=lb_users.yview)
scrollbar.grid(row=0, column=1, sticky='ns')
lb_users.config(yscrollcommand=scrollbar.set)
users = get_all_users()
fill_listbox()
lb_users.bind("<<ListboxSelect>>", on_user_select)

# Form
frm_form = tk.Frame(frm_admin,
                     borderwidth=2,
                     relief=tk.RAISED)
frm_form.columnconfigure(0, weight=1)
frm_form.columnconfigure(1, weight=1)
frm_form.columnconfigure(2, weight=1)
frm_form.grid(row=0, column=1, padx=PACK_PANEL_PADX, pady=PACK_PANEL_PADY)


user_id_var = tk.IntVar()
user_id_var.set(0)
user_first_name_var = tk.StringVar()
lbl_first_name = tk.Label(frm_form,
                            text="First Name:")
lbl_first_name.grid(row=0, column=0, sticky="e", padx=PACK_PANEL_PADX, pady=PACK_PANEL_PADY)
entry_first_name = tk.Entry(frm_form,
                            textvariable=user_first_name_var)
entry_first_name.grid(row=0, column=1, columnspan=2, padx=PACK_PANEL_PADX, pady=PACK_PANEL_PADY)

user_last_name_var = tk.StringVar()
lbl_last_name = tk.Label(frm_form, text="Last Name:")
lbl_last_name.grid(row=2, column=0, sticky="e", padx=PACK_PANEL_PADX, pady=PACK_PANEL_PADY)
entry_last_name = tk.Entry(frm_form, textvariable=user_last_name_var)
entry_last_name.grid(row=2, column=1, columnspan=2, padx=PACK_PANEL_PADX, pady=PACK_PANEL_PADY)

user_pin_var = tk.StringVar()
lbl_pin = tk.Label(frm_form, text="PIN:")
lbl_pin.grid(row=3, column=0, sticky="e", padx=PACK_PANEL_PADX, pady=PACK_PANEL_PADY)
entry_pin = tk.Entry(frm_form, textvariable=user_pin_var)
entry_pin.grid(row=3, column=1, columnspan=2, padx=PACK_PANEL_PADX, pady=PACK_PANEL_PADY)


user_is_active_var = tk.BooleanVar()
is_active_label = tk.Label(frm_form, text="Active:")
is_active_label.grid(row=4, column=0, sticky="e", padx=PACK_PANEL_PADX, pady=PACK_PANEL_PADY)
is_active_entry = tk.Checkbutton(frm_form, variable=user_is_active_var)
is_active_entry.grid(row=4, column=1, columnspan=2, padx=PACK_PANEL_PADX, pady=PACK_PANEL_PADY)



btn_save = tk.Button(frm_form,
                     text='Spremi',
                     command=on_save_user)
btn_save.grid(row=5, column=0, padx=PACK_PANEL_PADX, pady=PACK_PANEL_PADY)

btn_cancel = tk.Button(frm_form,
                     text='Odustani',
                     command=on_cancel)
btn_cancel.grid(row=5, column=1, padx=PACK_PANEL_PADX, pady=PACK_PANEL_PADY)

btn_delete = tk.Button(frm_form,
                     text='Izbrisi',
                     command=on_delete_user)
btn_delete.grid(row=5, column=2, padx=PACK_PANEL_PADX, pady=PACK_PANEL_PADY)

#endregion





if __name__ == '__main__':
    db_init()
    main_window.mainloop()