import PIL
import customtkinter
from customtkinter import *
from CTkMessagebox import CTkMessagebox
from tkinter import *
import draft_backend

class Edit_AdminFrame(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        pass
    # palitan mo yung "pass" ng UI code
# ============= READ !!!!!!!!!!!!!! ============
        # initialize mo ito sa UI then saka ilagay sa entry widget as textvariable=
        #     entry_username_var = StringVar()
        #     entry_name_var = StringVar()
        #     entry_email_var = StringVar()
        #     entry_phone_var = StringVar()
        #     entry_role_var = StringVar()
        #     entry_password_var = StringVar()
        #     edited_username_var = StringVar()

    #     for example:
    #       customtkinter.CTkEntry(admin_info_frame, width=200, textvariable=entry_name_var).pack()
    # thanks

def edit_admin_info():
    conn = draft_backend.get_db_connection()
    if not conn:
        return

    try:
        entry_username = entry_username_var.get()
        entry_name = entry_name_var.get()
        entry_email = entry_email_var.get()
        entry_phone = entry_phone_var.get()
        entry_role = entry_role_var.get()
        entry_password = entry_password_var.get()
        edited_username = edited_username_var.get()

        if not all([entry_username, entry_name, entry_email, entry_phone, entry_role, entry_password, edited_username]):
            CTkMessagebox(title="Error", message="All fields must be filled out")
            return

        draft_backend.edit_admin_info(conn, entry_username, entry_name, entry_email, entry_phone, entry_role, edited_username,
                                entry_password)
        CTkMessagebox(title="Success", message="Admin information updated successfully!")

    except Exception as e:
        CTkMessagebox(title="Error", message=f"Error updating admin information: {str(e)}")

    finally:
        conn.close()
