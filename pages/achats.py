import customtkinter as ctk
from tkinter import ttk

class AchatPage:

    def __init__(self, parent):

        frame = ctk.CTkFrame(parent)
        frame.pack(fill="both", expand=True)

        titre = ctk.CTkLabel(
            frame,
            text="CERTIFICATION DES ACHATS",
            font=("Arial", 28, "bold")
        )
        titre.pack(pady=20)

        table = ttk.Treeview(
            frame,
            columns=("FOURNISSEUR", "DATE", "MONTANT"),
            show="headings"
        )

        table.heading("FOURNISSEUR", text="FOURNISSEUR")
        table.heading("DATE", text="DATE")
        table.heading("MONTANT", text="MONTANT")

        table.pack(fill="both", expand=True, padx=20, pady=20)