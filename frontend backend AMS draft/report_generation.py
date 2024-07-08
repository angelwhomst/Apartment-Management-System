import asyncio
from threading import Thread
from tkinter import messagebox
from customtkinter import CTkFrame, CTkButton, CTkLabel
from report_generator import create_pdf_report
import draft_backend

# Start an asyncio event loop in a separate thread
class AsyncioLoopThread(Thread):
    def __init__(self):
        super().__init__()
        self.loop = asyncio.new_event_loop()
        self._stop_event = asyncio.Event()

    def run(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._stop_event.wait())

    def stop(self):
        self.loop.call_soon_threadsafe(self._stop_event.set)

# Create an instance of the asyncio event loop thread
loop_thread = AsyncioLoopThread()
loop_thread.start()

class ReportGenerationFrame(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        label = CTkLabel(self, text="Generate Tenant Report")
        label.grid(pady=10)

        generate_button = CTkButton(self, text="Generate Report")
        generate_button.grid(pady=10)

        # Configure the button command to call handle_generate_report properly
        generate_button.configure(command=self.handle_generate_report)

    def handle_generate_report(self):
        asyncio.run_coroutine_threadsafe(self.generate_report(), loop_thread.loop)

    async def generate_report(self):
        conn = draft_backend.get_db_connection()
        tenant_data = draft_backend.for_testing(conn)
        conn.close()

        if tenant_data:
            output_filename = "tenant_information_report.pdf"
            await create_pdf_report(tenant_data, output_filename)
            messagebox.showinfo("Success", "PDF report generated successfully! Please close the browser manually.")
        else:
            messagebox.showwarning("Warning", "No data available to generate report.")
