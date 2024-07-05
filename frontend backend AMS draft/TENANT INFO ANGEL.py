from tkinter import ttk
import PIL
import customtkinter
from customtkinter import *
from CTkMessagebox import CTkMessagebox
from tkinter import *
import draft_backend

class Tenant_InformationFrameS(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

 # ================ functional na itong treeview, nakakapag-fetch na kapag clinick yung button, pakiayos na lang yung UI tnx ============
    def create_widgets(self):
        label_tenants = customtkinter.CTkLabel(master=self, text="Tenant Information")
        label_tenants.grid(pady=10)

        # Treeview Customisation (theme colors are selected)
        bg_color = self._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"])
        text_color = self._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkLabel"]["text_color"])
        selected_color = self._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkButton"]["fg_color"])

        treestyle = ttk.Style()
        treestyle.theme_use('default')
        treestyle.configure("Treeview", background=bg_color, foreground=text_color, fieldbackground=bg_color,
                            borderwidth=0)
        treestyle.map('Treeview', background=[('selected', bg_color)], foreground=[('selected', selected_color)])
        self.bind("<<TreeviewSelect>>", lambda event: self.focus_set())

        # Treeview widget to display tenants
        self.tree_tenants = ttk.Treeview(self, columns=(
            "unit_number", "tenant_name", "contactNumber",
            "lease_start_date", "building_name", "building_address", "amenities"
            ), show="headings", height=6)
        self.tree_tenants.grid(padx=10)

        for col in self.tree_tenants["columns"]:
            self.tree_tenants.heading(col, text=col.replace("_", " ").title())

        # Button to fetch and display tenants data
        fetch_tenants_button = customtkinter.CTkButton(master=self, text="Fetch Tenants",
                                                       command=self.display_tenants)
        fetch_tenants_button.grid(pady=10)

    def display_tenants(self):
        self.clear_treeview()
        conn = draft_backend.get_db_connection()
        if not conn:
            return

        rows = draft_backend.fetch_tenants(conn)
        for row in rows:
            self.tree_tenants.insert("", "end", values=row)
        conn.close()

    def clear_treeview(self):
        for row in self.tree_tenants.get_children():
            self.tree_tenants.delete(row)