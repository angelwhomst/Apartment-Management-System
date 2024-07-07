import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Scrollbar
import draft_backend
from display_building_info import DisplayBuildingInformation

class TryLangBuildingTreeview(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.title("Building Info Treeview SANA GUMANA")
        self.controller = controller

        # Create the Treeview container
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Create the Treeview widget
        self.add_treeview()

        # Populate the Treeview with sample data
        self.populate_treeview()

    def add_treeview(self):
        # Create Treeview
        columns = ("Building Name", "Country", "Amenities")
        self.tree = ttk.Treeview(self.container, columns=("hidden_id", *columns), show='headings')

        # Hide the ID column
        self.tree.column("hidden_id", width=0, stretch=False)
        self.tree.heading("hidden_id", text="")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Create Scrollbar
        vsb = Scrollbar(self.container, orient=tk.VERTICAL, command=self.tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure Treeview to use Scrollbar
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def on_tree_select(self, event):
        selected_item = self.tree.selection()[0]
        building_id = self.tree.item(selected_item, 'values')[0]  # Fetch the hidden ID
        self.show_building_details(building_id)

    def show_building_details(self, building_id):
        new_frame = DisplayBuildingInformation(self, building_id)
        container = tk.Frame(self.container)
        container.pack(fill="both", expand=True)
        new_frame.pack(in_=container, fill="both", expand=True)

    def populate_treeview(self):
        conn = draft_backend.get_db_connection()
        if conn:
            building_id = draft_backend.fetch_building_treeview(conn)
            conn.close()
            for row in building_id:
                # Insert the row with the hidden ID column
                self.tree.insert("", "end", values=(row[0], *row[1:]))


if __name__ == "__main__":
    app = TryLangBuildingTreeview(controller=None)
    app.mainloop()
