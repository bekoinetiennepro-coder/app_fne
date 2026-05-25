import customtkinter as ctk
from tkinter import PhotoImage
from pages.dashboard import DashboardPage
from pages.ventes import VentePage
from pages.avoirs import AvoirPage
from pages.achats import AchatPage

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("FNE CERTIFICATION")
        self.geometry("1400x800")
        
        # MENU LATERAL
        self.sidebar = ctk.CTkFrame(self, width=250)
        self.sidebar.pack(side="left", fill="y")

        self.content = ctk.CTkFrame(self)
        self.content.pack(side="right", fill="both", expand=True)

        titre = ctk.CTkLabel(
            self.sidebar,
            text="FNE SYSTEM",
            font=("Arial", 24, "bold")
        )
        titre.pack(pady=20)

        btn_dashboard = ctk.CTkButton(
            self.sidebar,
            text="📊 Dashboard",
            command=self.show_dashboard
        )
        btn_dashboard.pack(pady=10, padx=20)

        btn_vente = ctk.CTkButton(
            self.sidebar,
            text="🧾 Certification Vente",
            command=self.show_ventes
        )
        btn_vente.pack(pady=10, padx=20)

        btn_avoir = ctk.CTkButton(
            self.sidebar,
            text="↩️ Certification Avoir",
            command=self.show_avoirs
        )
        btn_avoir.pack(pady=10, padx=20)

        btn_achat = ctk.CTkButton(
            self.sidebar,
            text="🛒 Certification Achat",
            command=self.show_achats
        )
        btn_achat.pack(pady=10, padx=20)

        self.show_dashboard()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_content()
        DashboardPage(self.content)

    def show_ventes(self):
        self.clear_content()
        VentePage(self.content)

    def show_avoirs(self):
        self.clear_content()
        AvoirPage(self.content)

    def show_achats(self):
        self.clear_content()
        AchatPage(self.content)

app = App()
app.mainloop()