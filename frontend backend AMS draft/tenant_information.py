import tkinter as tk
import tkinter.ttk as ttk

from CTkMessagebox import CTkMessagebox
from tkcalendar import DateEntry
import PIL.Image
from tkinter import Scrollbar
import customtkinter as ctk
from base import BaseFrame
from login import LoginFrame
from profile import ProfileFrame
import draft_backend
from display_tenant_details import DisplayTenantComponent  # Import the DisplayTenantComponent
from edit_tenant_info import EditTenantComponent
import datetime


class TenantInformationFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_widgets()
        self.populate_treeview()

        # Bind double-click event on Treeview
        self.tree.bind("<Double-1>", self.show_tenant_details)

        self.tree.bind("<Double-3>", self.show_edit_tenant_info)

    def create_widgets(self):
        # Add background image
        dashboard_bg_image = PIL.Image.open("images/tenantInformationbg.jpg")
        dashboard_bg = ctk.CTkImage(dashboard_bg_image, size=(1550, 800))
        dashboard_bg_lbl = ctk.CTkLabel(self, text="", image=dashboard_bg)
        dashboard_bg_lbl.place(x=0, y=0)

        # Add dashboard container image
        container_image = PIL.Image.open("images/dashcontainer.png")
        container_img = ctk.CTkImage(container_image, size=(1170, 650))
        container_img_lbl = ctk.CTkLabel(self, text="", image=container_img, fg_color="white")
        container_img_lbl.place(x=333, y=120)

        # Tenant information Label
        TenantInfoLabel = ctk.CTkLabel(master=self, text="Tenants Information", fg_color="White",
                                       text_color="#3D291F", font=("Century Gothic", 45, "bold"))
        TenantInfoLabel.place(relx=0.23, rely=0.18)

        # Ensure the sidebar is setup after the background images
        self.setup_sidebar()

        # Create Treeview
        columns = ("Building Name", "Unit Number", "Name", "Contact Number", "Status", "Start Date")
        self.tree = ttk.Treeview(self, columns=(*columns, "hidden_id"), show='headings')

        # Hide the ID column
        self.tree.column("hidden_id", width=0, stretch=False)
        self.tree.heading("hidden_id", text="")

        # Define headings with adjusted styles
        for col in columns:
            self.tree.heading(col, text=col, anchor='w')
            self.tree.column(col, anchor='w', width=190)  # Align data to the left

        # # Bind the Treeview row click event
        # self.tree.bind("<ButtonRelease-1>", self.on_row_click)

            # Add Delete Button

            delete_button = ctk.CTkButton(master=self, text="Delete", corner_radius=5, fg_color="#B8C8D3",
                                          hover_color="#9EA3AC", text_color="black", bg_color="White",
                                          font=('Century Gothic', 16,), width=100, height=30,
                                          command=self.delete_selected)
            delete_button.place(relx=0.860, rely=0.230)

        # Style Treeview
        style = ttk.Style(self)
        style.theme_use("clam")  # Use a specific theme that can be customized
        style.configure("Treeview", background="#e6e1dd", foreground="#3D291F", rowheight=25,
                        font=('Century Gothic', 12))
        style.map('Treeview', background=[('selected', '#d6cec8')])
        style.configure("Treeview.Heading", background="#d6cec8", foreground="#3D291F",
                        font=('Century Gothic', 14, 'bold'))

        # Create Scrollbar
        vsb = Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        vsb.place(x=1835, y=370, height=537)

        # Configure Treeview to use Scrollbar
        self.tree.configure(yscrollcommand=vsb.set)

        # Place Treeview inside the container
        self.tree.place(x=440, y=370, width=1415, height=538)

        profile_btn = ctk.CTkButton(master=self, text="Profile", corner_radius=0, fg_color="#CFB9A3",
                                    hover_color="#D6BC9D", text_color="#5c483f", bg_color="#5D646E",
                                    font=('Century Gothic', 20, "bold"), width=90, height=30,
                                    command=lambda: self.controller.show_frame(ProfileFrame))
        profile_btn.place(relx=0.855, rely=0.105)

        # Logout Button
        logout_btn = ctk.CTkButton(master=self, text="Log out", corner_radius=0, fg_color="#CFB9A3",
                                   hover_color="#D6BC9D", text_color="#5c483f", bg_color="#5D646E",
                                   font=('Century Gothic', 20, "bold"), width=90, height=30,
                                   command=lambda: self.controller.show_frame(LoginFrame))
        logout_btn.place(relx=0.920, rely=0.105)

        # Add To: DateEntry
        self.to_date_entry = DateEntry(self, font=('Century Gothic', 16), bg="white", fg="#5c483f", width=12)
        self.to_date_entry.place(relx=0.710, rely=0.300)

        # Add From: DateEntry
        self.from_date_entry = DateEntry(self, font=('Century Gothic', 16), bg="white", fg="#5c483f", width=12)
        self.from_date_entry.place(relx=0.610, rely=0.300)

        # Clear the DateEntry fields initially
        self.to_date_entry.set_date(self.to_date_entry._date.today())
        self.from_date_entry.set_date(self.from_date_entry._date.today())
        self.to_date_entry.delete(0, tk.END)
        self.from_date_entry.delete(0, tk.END)


        # Add Search Entry with Placeholder Text
        def on_entry_click(event):
            if self.search_entry.get() == "Search Name...":
                self.search_entry.delete(0, tk.END)
                self.search_entry.config(fg="black")

        def on_focus_out(event):
            if self.search_entry.get() == "":
                self.search_entry.insert(0, "Search Name...")
                self.search_entry.config(fg="#5c483f")

        self.search_entry = tk.Entry(self, font=('Century Gothic', 16), bg="white", fg="#5c483f", width=30)
        self.search_entry.insert(0, "Search Name...")
        self.search_entry.bind('<FocusIn>', on_entry_click)
        self.search_entry.bind('<FocusOut>', on_focus_out)
        self.search_entry.place(relx=0.400, rely=0.300)

        # Add Search Button
        search_button = ctk.CTkButton(master=self, text="Search", corner_radius=5, fg_color="#BDA588",
                                      hover_color="#D6BC9D", text_color="black", bg_color="White",
                                      font=('Century Gothic', 16,), width=100, height=30,
                                      command=self.perform_search)
        search_button.place(relx=0.820, rely=0.295)

        # Add Clear Filter Button
        clear_filter_button = ctk.CTkButton(master=self, text="Clear Filter", corner_radius=5, fg_color="#B8C8D3",
                                            hover_color="#9EA3AC", text_color="black", bg_color="White",
                                            font=('Century Gothic', 16,), width=100, height=30,
                                            command=self.clear_filters)
        clear_filter_button.place(relx=0.890, rely=0.295)

        # Start periodic refresh
        self.start_refresh()

    def start_refresh(self):
        # Periodically refresh data
        if not hasattr(self, 'refreshing_search') or not self.refreshing_search:
            self.refresh_data()
            self.after(5000, self.start_refresh)  # Refresh every 5 seconds

    def populate_treeview(self):
        conn = draft_backend.get_db_connection()
        if conn:
            tenant_data = draft_backend.fetch_tenant_treeview(conn)
            conn.close()
            for row in tenant_data:
                # Insert the row with the hidden ID column
                self.tree.insert("", "end", values=(row[1], row[2], row[3], row[4], row[5], row[0]))

    def refresh_data(self):
        conn = draft_backend.get_db_connection()
        if not conn:
            return

        try:
            # Fetch all tenants
            tenants = draft_backend.fetch_tenant_treeview(conn)

            # Clear existing items from the Treeview
            self.tree.delete(*self.tree.get_children())

            # Iterate over fetched tenants and update or insert into Treeview
            for tenant in tenants:
                # Extract relevant values
                building_name = tenant[1]
                unit_number = tenant[2]
                tenant_name = tenant[3]
                contact_number = tenant[4]
                payment_status = tenant[5]
                lease_start_date = tenant[6]
                tenant_id = tenant[0]

                # Insert or update Treeview item
                self.tree.insert("", "end", values=(building_name, unit_number, tenant_name, contact_number,
                                                    payment_status, lease_start_date, tenant_id))

        except Exception as e:
            print(f"Error fetching data: {str(e)}")

        finally:
            conn.close()

    def perform_search(self):
        # Disable auto-refresh during search
        self.refreshing_search = True

        search_name = self.search_entry.get()
        from_date = self.from_date_entry.get_date()
        to_date = self.to_date_entry.get_date()

        # Print debug information
        print(f"Search Name: {search_name}")
        print(f"From Date: {from_date}")
        print(f"To Date: {to_date}")

        # If date fields are empty, set them to None
        from_date = from_date if from_date else None
        to_date = to_date if to_date else None

        conn = draft_backend.get_db_connection()
        if conn:
            try:
                # Fetch tenant data based on name search and date range
                tenant_data = draft_backend.fetch_tenants_by_filters(conn, search_name, from_date, to_date)

                # Clear existing treeview data
                for item in self.tree.get_children():
                    self.tree.delete(item)

                # Insert new data into Treeview
                for row in tenant_data:
                    self.tree.insert("", "end", values=row)

            except Exception as e:
                print(f"Error performing search: {str(e)}")

            finally:
                conn.close()

    def update_treeview_with_search_results(self, results):
        # Clear existing data in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Insert search results
        for item in results:
            self.tree.insert('', 'end', values=item)

    def add_clear_filter_button(self):
        clear_filter_button = ctk.CTkButton(master=self, text="Clear Filter", corner_radius=5, fg_color="#B8C8D3",
                                            hover_color="#9EA3AC", text_color="black", bg_color="White",
                                            font=('Century Gothic', 16,), width=100, height=30,
                                            command=self.clear_filters)
        clear_filter_button.place(relx=0.890, rely=0.295)

    def clear_filters(self):
        self.to_date_entry.set_date(self.to_date_entry._date.today())
        self.from_date_entry.set_date(self.from_date_entry._date.today())
        self.to_date_entry.delete(0, tk.END)
        self.from_date_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, "Search Name...")
        # Re-populate treeview with all data
        self.clear_treeview()
        self.populate_treeview()

    def clear_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def show_tenant_details(self, event):
        # Get the selected item from Treeview
        item = self.tree.selection()[0]
        # Retrieve the tenant_id (the last column in the Treeview)
        tenant_id = self.tree.item(item, "values")[-1]

        # Open a new window to display tenant details
        top_level_window = tk.Toplevel(self)
        top_level_window.title("Tenant Details")
        top_level_window.geometry("1120x720")

        # Create an instance of DisplayTenantComponent and pass tenant_id
        DisplayTenantComponent(top_level_window, tenant_id)

    def show_edit_tenant_info(self, event):
        # Get the selected item from Treeview
        item = self.tree.selection()[0]
        # Retrieve the tenant_id (the last column in the Treeview)
        tenant_id = self.tree.item(item, "values")[-1]

        # Open a new window to display tenant details
        top_level_window = tk.Toplevel(self)
        top_level_window.title("Edit Tenant Details")
        top_level_window.geometry("1120x720")

        # Create an instance of EditTenantComponent and pass tenant_id
        EditTenantComponent(top_level_window, tenant_id)

    def delete_selected(self):
        selected_item = self.tree.selection()  # Get selected item(s)
        if selected_item:
            response = CTkMessagebox(title="Delete Confirmation",
                                     message="Are you sure you want to delete the selected tenant?",
                                     icon="warning",
                                     option_1="Yes",
                                     option_2="No").get()

            if response == "Yes":
                for item in selected_item:
                    # Get the tennat_id from the hidden column
                    tenant_id = self.tree.item(item, 'values')[6]

                    # Delete from Treeview
                    self.tree.delete(item)

                    # Delete from Database
                    conn = draft_backend.get_db_connection()
                    if conn:
                        try:
                            draft_backend.delete_tenant(conn, tenant_id)
                        except Exception as e:
                            CTkMessagebox(title="Error", message=f"Error deleting: {str(e)}")
                        finally:
                            conn.close()
        else:
            CTkMessagebox(title="Error", message="No item selected.")


