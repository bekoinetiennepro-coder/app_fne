import customtkinter as ctk

from services.fne_service import (
    total_factures,
    total_factures_certifiees,
    total_factures_non_certifiees,
    total_avoirs_certifies
)


class DashboardPage:

    def __init__(self, parent):

        # ==================================================
        # FRAME PRINCIPAL
        # ==================================================

        frame = ctk.CTkFrame(parent)

        frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # ==================================================
        # TITRE
        # ==================================================

        titre = ctk.CTkLabel(
            frame,
            text="TABLEAU DE BORD FNE",
            font=("Arial", 32, "bold")
        )

        titre.pack(
            pady=30
        )

        # ==================================================
        # DONNEES
        # ==================================================

        nb_total = total_factures()

        nb_certifiees = total_factures_certifiees()

        nb_non_certifiees = total_factures_non_certifiees()

        nb_avoirs = total_avoirs_certifies()

        # ==================================================
        # CONTAINER CARDS
        # ==================================================

        cards = ctk.CTkFrame(frame)

        cards.pack(
            pady=20
        )

        # ==================================================
        # CARD TOTAL FACTURES
        # ==================================================

        card_total = ctk.CTkLabel(
            cards,
            text=f"🧾 TOTAL FACTURES\n{nb_total}",
            width=260,
            height=170,
            fg_color="#1f6aa5",
            corner_radius=20,
            font=("Arial", 24, "bold")
        )

        card_total.grid(
            row=0,
            column=0,
            padx=20,
            pady=20
        )

        # ==================================================
        # CARD FACTURES CERTIFIEES
        # ==================================================

        card_certifiees = ctk.CTkLabel(
            cards,
            text=f"✅ FACTURES CERTIFIÉES\n{nb_certifiees}",
            width=260,
            height=170,
            fg_color="green",
            corner_radius=20,
            font=("Arial", 24, "bold")
        )

        card_certifiees.grid(
            row=0,
            column=1,
            padx=20,
            pady=20
        )

        # ==================================================
        # CARD NON CERTIFIEES
        # ==================================================

        card_non = ctk.CTkLabel(
            cards,
            text=f"⚠ NON CERTIFIÉES\n{nb_non_certifiees}",
            width=260,
            height=170,
            fg_color="red",
            corner_radius=20,
            font=("Arial", 24, "bold")
        )

        card_non.grid(
            row=0,
            column=2,
            padx=20,
            pady=20
        )

        # ==================================================
        # CARD AVOIRS
        # ==================================================

        card_avoirs = ctk.CTkLabel(
            cards,
            text=f"↩️ AVOIRS CERTIFIÉS\n{nb_avoirs}",
            width=260,
            height=170,
            fg_color="orange",
            corner_radius=20,
            font=("Arial", 24, "bold")
        )

        card_avoirs.grid(
            row=1,
            column=1,
            padx=20,
            pady=20
        )