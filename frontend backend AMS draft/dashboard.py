from CTkMessagebox import CTkMessagebox
from PIL import Image
import customtkinter as ctk
import draft_backend

from base import BaseFrame
from rental_rates import MonthlyRatesComponent
from lease_expiration_alerts import LeaseExpirationAlertComponent
from total_units import TotalUnitsComponent
from recent_tenants import RecentTenantComponent
from monthly_earnings import MonthlyEarningsComponent
from maintenance_request import MaintenanceRequestComponent


class DashboardFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_widgets()
        self.update_labels()
        self.start_refresh()

    def create_widgets(self):
        # Add background image and other dashboard setup
        dashboard_bg_image = Image.open("images/dashboardbg.jpg")
        dashboard_bg = ctk.CTkImage(dashboard_bg_image, size=(1550, 800))
        dashboard_bg_lbl = ctk.CTkLabel(self, text="", image=dashboard_bg)
        dashboard_bg_lbl.place(x=0, y=0)

        container_image = Image.open("images/whitebgdash.png")
        container_img = ctk.CTkImage(container_image, size=(1170, 650))
        container_img_lbl = ctk.CTkLabel(self, text="", image=container_img, fg_color="white")
        container_img_lbl.place(x=333, y=120)

        DashboardLabel = ctk.CTkLabel(master=self, text="Dashboard", fg_color="White",
                                      text_color="#3D291F", font=("Century Gothic", 60, "bold"))
        DashboardLabel.place(relx=0.235, rely=0.18)

        self.setup_sidebar()

        self.add_admin_tool_button()

        self.add_profile_button()

        self.add_logout_button()

        self.add_labels_with_placeholders()

        button_style = {
            'corner_radius': 0,
            'fg_color': "#937A69",
            'hover_color': "#5c483f",
            'text_color': "White",
            'bg_color': "#937A69",
            'font': ('Century Gothic', 25, "bold"),
            'width': 346,
            'height': 60
        }

        # Load the icon for buttons
        next_button_icon_image = Image.open("images/seemoreButton.png")
        next_button_icon = ctk.CTkImage(next_button_icon_image, size=(50, 50))

        # See more buttons
        button1 = ctk.CTkButton(self, text="See more", **button_style, command=self.show_total_units,
                                image=next_button_icon,
                                compound="right")
        button2 = ctk.CTkButton(self, text="See more", **button_style, command=self.show_monthly_rates,
                                image=next_button_icon,
                                compound="right")
        button3 = ctk.CTkButton(self, text="See more", **button_style, command=self.show_lease_alerts,
                                image=next_button_icon,
                                compound="right")
        button4 = ctk.CTkButton(self, text="See more", **button_style, command=self.show_recent_tenants,
                                image=next_button_icon,
                                compound="right")
        button5 = ctk.CTkButton(self, text="See more", **button_style, command=self.show_monthly_earnings,
                                image=next_button_icon,
                                compound="right")
        button6 = ctk.CTkButton(self, text="See more", **button_style, command=self.show_maintenance_requests,
                                image=next_button_icon,
                                compound="right")
        # Define button positions
        button1.place(x=366, y=436)
        button2.place(x=745, y=436)
        button3.place(x=1124, y=436)
        button4.place(x=366, y=681)
        button5.place(x=745, y=681)
        button6.place(x=1124, y=681)

    def add_labels_with_placeholders(self):
        # Dictionary to store StringVar instances
        self.label_vars = {}

        labels_info = [
            ("label_total_units", 0.2905, 0.44),
            ("label_rental_rates", 0.5365, 0.44),
            ("label_expiration_Alerts", 0.7830, 0.44),
            ("label_recent_tenants", 0.2905, 0.7455),
            ("label_monthly_earnings", 0.5365, 0.7455),
            ("label_maintenance_requests", 0.7830, 0.7455)
        ]

        for label_name, relx, rely in labels_info:
            var = ctk.StringVar()
            var.set("#")
            self.label_vars[label_name] = var

            label_frame = ctk.CTkFrame(self, fg_color="#E6E1DD", width=150, height=100)
            label_frame.place(relx=relx, rely=rely, anchor="center")

            label = ctk.CTkLabel(label_frame, textvariable=var, fg_color="#E6E1DD", text_color="#3D291F",
                                 width=300, height=100, font=("Century Gothic", 30, "bold"))
            label.place(relx=0.5, rely=0.5, anchor="center")


    # method to update labels
    def update_labels(self):
        conn = draft_backend.get_db_connection()
        if not conn:
            return
        total_units = draft_backend.total_units(conn)
        self.label_vars['label_total_units'].set(f'{total_units}')

        monthly_rate = draft_backend.average_rental_rate(conn)
        if monthly_rate is not None:
            self.label_vars['label_rental_rates'].set(f'₱{monthly_rate:,.2f}')
        else:
            self.label_vars['label_rental_rates'].set('N/A')

        lease_expirations_alerts = draft_backend.count_lease_expiration_alerts(conn)
        self.label_vars['label_expiration_Alerts'].set(f'{lease_expirations_alerts}')

        recent_tenants = draft_backend.count_recent_tenants(conn)
        self.label_vars['label_recent_tenants'].set(f'{recent_tenants}')

        monthly_earnings = draft_backend.monthly_earnings(conn)
        if monthly_earnings is not None:
            self.label_vars['label_monthly_earnings'].set(f'₱{monthly_earnings:,.2f}')
        else:
            self.label_vars['label_monthly_earnings'].set('N/A')

        maintenance_requests = draft_backend.count_maintenance_requests(conn)
        self.label_vars['label_maintenance_requests'].set(f'{maintenance_requests}')

    def start_refresh(self):
        # Periodically refresh data
        self.refresh_data()
        self.after(5000, self.start_refresh)  # Refresh every 5 seconds

    def refresh_data(self):
        conn = draft_backend.get_db_connection()
        if not conn:
            return

        try:
            # Update dashboard labels
            total_units = draft_backend.total_units(conn)
            self.label_vars['label_total_units'].set(f'{total_units}')

            monthly_rate = draft_backend.average_rental_rate(conn)
            self.label_vars['label_rental_rates'].set(f'₱{monthly_rate:,.2f}')

            lease_expirations_alerts = draft_backend.count_lease_expiration_alerts(conn)
            self.label_vars['label_expiration_Alerts'].set(f'{lease_expirations_alerts}')

            recent_tenants = draft_backend.count_recent_tenants(conn)
            self.label_vars['label_recent_tenants'].set(f'{recent_tenants}')

            monthly_earnings = draft_backend.monthly_earnings(conn)
            self.label_vars['label_monthly_earnings'].set(f'₱{monthly_earnings:,.2f}')

            maintenance_requests = draft_backend.count_maintenance_requests(conn)
            self.label_vars['label_maintenance_requests'].set(f'{maintenance_requests}')

        except Exception as e:
            print(f"Error refreshing data: {str(e)}")

        finally:
            conn.close()

    def add_admin_tool_button(self):
        admin_icon_image = Image.open("images/toolIcon.png")
        admin_icon = ctk.CTkImage(admin_icon_image, size=(20, 20))

        admin_tool_btn = ctk.CTkButton(master=self, text="Admin Tool", corner_radius=0, fg_color="#CFB9A3",
                                       hover_color="#D6BC9D", text_color="#5c483f", bg_color="#5D646E",
                                       font=('Century Gothic', 20, "bold"), width=190, height=30,
                                       image=admin_icon, compound="left",
                                       command=self.open_admin_tool)
        admin_tool_btn.place(relx=0.855, rely=0.055)

    def add_profile_button(self):
        profile_btn = ctk.CTkButton(master=self, text="Profile", corner_radius=0, fg_color="#CFB9A3",
                                    hover_color="#D6BC9D", text_color="#5c483f", bg_color="#5D646E",
                                    font=('Century Gothic', 20, "bold"), width=90, height=30,
                                    command=self.open_profile)
        profile_btn.place(relx=0.855, rely=0.105)

    def add_logout_button(self):
        logout_btn = ctk.CTkButton(master=self, text="Log out", corner_radius=0, fg_color="#CFB9A3",
                                   hover_color="#D6BC9D", text_color="#5c483f", bg_color="#5D646E",
                                   font=('Century Gothic', 20, "bold"), width=90, height=30,
                                   command=self.confirm_logout)
        logout_btn.place(relx=0.920, rely=0.105)

    def confirm_logout(self):
        response = CTkMessagebox(title="Logout Confirmation",
                                 message="Are you sure you want to log out?",
                                 icon="warning",
                                 option_1="Yes",
                                 option_2="No").get()

        if response == "Yes":
            self.open_login()

    def open_login(self):
        from login import LoginFrame
        self.controller.show_frame(LoginFrame)

    def open_profile(self):
        from profile import ProfileFrame
        self.controller.show_frame(ProfileFrame)

    def open_login(self):
        from login import LoginFrame
        self.controller.show_frame(LoginFrame)

    def open_admin_tool(self):
        from admin_tool import AdminToolComponent
        admin_tool = AdminToolComponent(self)
        admin_tool.open_admin_tool()

    def show_total_units(self):
        top_level = ctk.CTkToplevel(self)
        top_level.title("Total Units")
        top_level.geometry("900x600+100+100")
        top_level.attributes("-topmost", True)

        total_units_component = TotalUnitsComponent(top_level)
        total_units_component.pack(fill="both", expand=True)

    def show_monthly_rates(self):
        top_level = ctk.CTkToplevel(self)
        top_level.title("Monthly Rates")
        top_level.geometry("900x600+100+100")
        top_level.attributes("-topmost", True)

        monthly_rates_component = MonthlyRatesComponent(top_level)
        monthly_rates_component.pack(fill="both", expand=True)

    def show_lease_alerts(self):
        top_level = ctk.CTkToplevel(self)
        top_level.title("Lease Expiration Alerts")
        top_level.geometry("900x600+100+100")
        top_level.attributes("-topmost", True)

        lease_alerts = LeaseExpirationAlertComponent(top_level)
        lease_alerts.pack(fill="both", expand=True)

    def show_recent_tenants(self):
        top_level = ctk.CTkToplevel(self)
        top_level.title("Recent Tenants")
        top_level.geometry("900x600+100+100")
        top_level.attributes("-topmost", True)

        recent_tenants_component = RecentTenantComponent(top_level)
        recent_tenants_component.pack(fill="both", expand=True)

    def show_monthly_earnings(self):
        top_level = ctk.CTkToplevel(self)
        top_level.title("Monthly Earnings")
        top_level.geometry("900x600+100+100")
        top_level.attributes("-topmost", True)

        monthly_earnings_component = MonthlyEarningsComponent(top_level)
        monthly_earnings_component.pack(fill="both", expand=True)

    def show_maintenance_requests(self):
        top_level = ctk.CTkToplevel(self)
        top_level.title("Maintenance Requests")
        top_level.geometry("900x600+100+100")
        top_level.attributes("-topmost", True)

        maintenance_request_component = MaintenanceRequestComponent(top_level)
        maintenance_request_component.pack(fill="both", expand=True)
