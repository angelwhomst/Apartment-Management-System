from tkinter import ttk
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image
import tkinter as tk
from base import BaseFrame
from login import LoginFrame
from profile import ProfileFrame
import draft_backend
from display_building_info import DisplayBuildingInformation


class BuildingInformationFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_widgets()
        self.populate_treeview()

    def create_widgets(self):
        # Add background image
        dashboard_bg_image = Image.open("images/buildinginfobg.jpg")
        dashboard_bg = ctk.CTkImage(dashboard_bg_image, size=(1550, 800))
        dashboard_bg_lbl = ctk.CTkLabel(self, text="", image=dashboard_bg)
        dashboard_bg_lbl.place(x=0, y=0, )

        # Add dashboard container image
        container_image = Image.open("images/dashcontainer.png")
        container_img = ctk.CTkImage(container_image, size=(1170, 650))
        container_img_lbl = ctk.CTkLabel(self, text="", image=container_img, fg_color="white")
        container_img_lbl.place(x=333, y=120)

        # Building Information Label
        BuildingInfoLabel = ctk.CTkLabel(master=self, text="Building Information", fg_color="White",
                                         text_color="#3D291F", font=("Century Gothic", 45, "bold"))
        BuildingInfoLabel.place(relx=0.23, rely=0.18)

        # Ensure the sidebar is setup after the background images
        self.setup_sidebar()

        # Profile Button
        self.add_profile_button()

        # Logout Button
        self.add_logout_button()

        # Add Treeview
        self.add_treeview()

    def add_profile_button(self):
        profile_btn = ctk.CTkButton(master=self, text="Profile", corner_radius=0, fg_color="#CFB9A3",
                                    hover_color="#D6BC9D", text_color="#5c483f", bg_color="#5D646E",
                                    font=('Century Gothic', 20, "bold"), width=90, height=30,
                                    command=lambda: self.controller.show_frame(ProfileFrame))
        profile_btn.place(relx=0.855, rely=0.105)

    def add_logout_button(self):
        logout_btn = ctk.CTkButton(master=self, text="Log out", corner_radius=0, fg_color="#CFB9A3",
                                   hover_color="#D6BC9D", text_color="#5c483f", bg_color="#5D646E",
                                   font=('Century Gothic', 20, "bold"), width=90, height=30,
                                   command=lambda: self.controller.show_frame(LoginFrame))
        logout_btn.place(relx=0.915, rely=0.105)

        # Add Search Entry with Placeholder Text
        def on_entry_click(event):
            if self.search_entry.get() == "Search building name...":
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
        self.search_entry.place(relx=0.230, rely=0.300)

    def add_treeview(self):
        # Create Treeview
        columns = ("Building Name", "Country", "Province", "City", "Street", "Lot Number", "Zip Code", "Amenities")
        self.tree = ttk.Treeview(self, columns=(*columns, "hidden_id"), show='headings')

        # Hide the ID column
        self.tree.column("hidden_id", width=0, stretch=False)
        self.tree.heading("hidden_id", text="")

        # Define headings with adjusted styles
        for col in columns:
            self.tree.heading(col, text=col, anchor='w')
            self.tree.column(col, anchor='w', width=100)  # Align data to the left

        search_button = ctk.CTkButton(master=self, text="Search", corner_radius=5, fg_color="#BDA588",
                                      hover_color="#D6BC9D", text_color="black", bg_color="White",
                                      font=('Century Gothic', 16,), width=100, height=25, command=self.perform_search)
        search_button.place(relx=0.450, rely=0.300)

        # Add Clear Filter Button
        clear_filter_button = ctk.CTkButton(master=self, text="Clear Filter", corner_radius=5, fg_color="#B8C8D3",
                                            hover_color="#9EA3AC", text_color="black", bg_color="White",
                                            font=('Century Gothic', 16,), width=100, height=30,
                                            command=self.clear_filters)
        clear_filter_button.place(relx=0.895, rely=0.295)

        # Add Delete Button

        delete_button = ctk.CTkButton(master=self, text="Delete", corner_radius=5, fg_color="#B8C8D3",
                                      hover_color="#9EA3AC", text_color="black", bg_color="White",
                                      font=('Century Gothic', 16,), width=100, height=30, command=self.delete_selected)
        delete_button.place(relx=0.825, rely=0.295)

        # Style Treeview
        style = ttk.Style(self)
        style.theme_use("clam")  # Use a specific theme that can be customized
        style.configure("Treeview", background="#e6e1dd", foreground="#3D291F", rowheight=25,
                        font=('Century Gothic', 12))
        style.map('Treeview', background=[('selected', '#d6cec8')])
        style.configure("Treeview.Heading", background="#d6cec8", foreground="#3D291F",
                        font=('Century Gothic', 14, 'bold'))

        # Create Scrollbar
        vsb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        vsb.place(x=1840, y=370, height=537)

        # Configure Treeview to use Scrollbar
        self.tree.configure(yscrollcommand=vsb.set)

        # Place Treeview inside the container
        self.tree.place(x=440, y=370, width=1415, height=538)

    def populate_treeview(self):
        conn = draft_backend.get_db_connection()
        if conn:
            building_info = draft_backend.fetch_building_information_treeview(conn)
            conn.close()
            if building_info is not None:  # Check if building_info is not None
                for row in building_info:
                    # Insert the row with the hidden ID column
                    self.tree.insert("", "end", values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                                                        row[8], row[0]))
            else:
                print("Error: No building information fetched.")
        else:
            print("Error: Failed to connect to the database.")

    def start_refresh(self):
        # Periodically refresh data
        if not hasattr(self, 'refreshing_search') or not self.refreshing_search:
            self.refresh_data()
            self.after(5000, self.start_refresh)  # Refresh every 5 seconds

    def refresh_data(self):
        conn = draft_backend.get_db_connection()
        if not conn:
            return

        try:
            # Fetch all buildings
            buildings = draft_backend.fetch_building_information_treeview(conn)

            # Clear existing items from the Treeview
            self.tree.delete(*self.tree.get_children())

            # Iterate over fetched buildings and update or insert into Treeview
            for building in buildings:
                # Debug print to check data
                print(f"Fetched building data: {building} with length {len(building)}")

                if len(building) != 9:
                    print(f"Error: Expected 9 elements, got {len(building)}")
                    continue  # Skip this row if it doesn't have the expected number of elements

                building_id = building[0]
                building_name = self.replace_none(building[1])
                country = self.replace_none(building[2])
                province = self.replace_none(building[3])
                city = self.replace_none(building[4])
                street = self.replace_none(building[5])
                lot_number = self.replace_none(building[6])
                zip_code = self.replace_none(building[7])
                amenities = self.replace_none(building[8])

                # Insert or update Treeview item
                self.tree.insert("", "end", values=(building_name, country, province, city, street,
                                                    lot_number, zip_code, amenities, building_id))

        except Exception as e:
            print(f"Error fetching data: {str(e)}")

        finally:
            conn.close()

        # Resume refreshing after processing
        self.after(5000, self.start_refresh)  # Refresh every 5 seconds

    def replace_none(self, value):
        return value if value is not None else ""

    def perform_search(self):
        # Disable auto-refresh during search
        self.refreshing_search = True

        search_term = self.search_entry.get().strip().lower()
        conn = draft_backend.get_db_connection()
        if conn:
            try:
                building_info = draft_backend.fetch_building_information_treeview(conn)
                conn.close()
                self.tree.delete(*self.tree.get_children())  # Clear current data
                for row in building_info:
                    if search_term in row[1].lower():
                        # Insert the row with the hidden ID column
                        self.tree.insert("", "end", values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                                                            row[8], row[0]))
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
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, "Search Name...")
        # Re-populate treeview with all data
        self.clear_treeview()
        self.populate_treeview()

    def clear_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def show_building_information(self, event):
        # Get the selected item from Treeview
        item = self.tree.selection()[0]
        # Retrieve the building_id (the last column in the Treeview)
        building_id = self.tree.item(item, "values")[-1]

        # Open a new window to display tenant details
        top_level_window = tk.Toplevel(self)
        top_level_window.title("Building Information")
        top_level_window.geometry("1120x750")

        # Create an instance of DisplayTenantComponent and pass tenant_id
        DisplayBuildingInformation(top_level_window, building_id)

    def delete_selected(self):
        selected_item = self.tree.selection()  # Get selected item(s)
        if selected_item:
            response = CTkMessagebox(title="Delete Confirmation",
                                     message="Are you sure you want to delete the selected building?",
                                     icon="warning",
                                     option_1="Yes",
                                     option_2="No").get()

            if response == "Yes":
                for item in selected_item:
                    # Get the building_id from the hidden column
                    building_id = self.tree.item(item, 'values')[8]

                    # Delete from Treeview
                    self.tree.delete(item)

                    # Delete from Database
                    conn = draft_backend.get_db_connection()
                    if conn:
                        try:
                            draft_backend.delete_building(conn, building_id)
                        except Exception as e:
                            CTkMessagebox(title="Error", message=f"Error deleting from database: {str(e)}")
                        finally:
                            conn.close()
        else:
            CTkMessagebox(title="Error", message="No item selected.")
