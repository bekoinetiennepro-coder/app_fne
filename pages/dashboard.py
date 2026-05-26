import customtkinter as ctk

from services.fne_service import (
    total_factures,
    total_factures_certifiees,
    total_factures_non_certifiees,
    total_avoirs_certifies,
    total_achats,
    total_achats_certifies
)


class DashboardPage:

    def __init__(self, parent):
        

        # ==================================================
        # FRAME PRINCIPAL
        # ==================================================

        self.frame = ctk.CTkFrame(parent)

        self.frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )
        self.auto_refresh()
        # ==================================================
        # TITRE
        # ==================================================

        titre = ctk.CTkLabel(
            self.frame,
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

        nb_achats = total_achats()

        nb_achats_certifies = total_achats_certifies()

        # ==================================================
        # CONTAINER CARDS
        # ==================================================

        cards = ctk.CTkFrame(self.frame)

        cards.pack(
            pady=20
        )

        # ==================================================
        # CARD TOTAL FACTURES
        # ==================================================

        self.card_total = ctk.CTkLabel(
            cards,
            text=f"🧾 TOTAL FACTURES VENTE\n{nb_total}",
            width=280,
            height=180,
            fg_color="#1f6aa5",
            corner_radius=20,
            font=("Arial", 24, "bold")
        )

        self.card_total.grid(
            row=0,
            column=0,
            padx=20,
            pady=20
        )

        # ==================================================
        # CARD FACTURES CERTIFIEES
        # ==================================================

        self.card_certifiees = ctk.CTkLabel(
            cards,
            text=f"✅ FACTURES VENTE CERTIFIÉES\n{nb_certifiees}",
            width=280,
            height=180,
            fg_color="green",
            corner_radius=20,
            font=("Arial", 24, "bold")
        )

        self.card_certifiees.grid(
            row=0,
            column=1,
            padx=20,
            pady=20
        )

        # ==================================================
        # CARD NON CERTIFIEES
        # ==================================================

        self.card_non_certifiees = ctk.CTkLabel(
            cards,
            text=f"⚠ VENTE NON CERTIFIÉES\n{nb_non_certifiees}",
            width=280,
            height=180,
            fg_color="red",
            corner_radius=20,
            font=("Arial", 24, "bold")
        )

        self.card_non_certifiees.grid(
            row=0,
            column=2,
            padx=20,
            pady=20
        )

        # ==================================================
        # CARD AVOIRS
        # ==================================================

        self.card_avoirs = ctk.CTkLabel(
            cards,
            text=f"↩️ AVOIRS CERTIFIÉS\n{nb_avoirs}",
            width=280,
            height=180,
            fg_color="orange",
            corner_radius=20,
            font=("Arial", 24, "bold")
        )

        self.card_avoirs.grid(
            row=1,
            column=0,
            padx=20,
            pady=20
        )

        # ==================================================
        # CARD TOTAL ACHATS
        # ==================================================

        self.card_achats = ctk.CTkLabel(
            cards,
            text=f"🛒 TOTAL ACHATS\n{nb_achats}",
            width=280,
            height=180,
            fg_color="#6f42c1",
            corner_radius=20,
            font=("Arial", 24, "bold")
        )

        self.card_achats.grid(
            row=1,
            column=1,
            padx=20,
            pady=20
        )

        # ==================================================
        # CARD ACHATS CERTIFIES
        # ==================================================

        self.card_achats_certifies = ctk.CTkLabel(
            cards,
            text=f"🏷️ ACHATS CERTIFIÉS\n{nb_achats_certifies}",
            width=280,
            height=180,
            fg_color="#198754",
            corner_radius=20,
            font=("Arial", 24, "bold")
        )

        self.card_achats_certifies.grid(
            row=1,
            column=2,
            padx=20,
            pady=20
        )
        
    def auto_refresh(self):
    
        try:

            nb_total = total_factures()

            nb_certifiees = total_factures_certifiees()

            nb_non = total_factures_non_certifiees()

            nb_avoirs = total_avoirs_certifies()

            nb_achats = total_achats()

            nb_achats_certifies = total_achats_certifies()

            self.card_total.configure(
                text=f"🧾 TOTAL FACTURES VENTE\n{nb_total}"
            )

            self.card_certifiees.configure(
                text=f"✅ FACTURES VENTE CERTIFIÉES\n{nb_certifiees}"
            )

            self.card_non_certifiees.configure(
                text=f"⚠ VENTE NON CERTIFIÉES\n{nb_non}"
            )

            self.card_avoirs.configure(
                text=f"↩️ AVOIRS CERTIFIÉS\n{nb_avoirs}"
            )

            self.card_achats.configure(
                text=f"🛒 TOTAL ACHATS\n{nb_achats}"
            )

            self.card_achats_certifies.configure(
                text=f"🏷️ ACHATS CERTIFIÉS\n{nb_achats_certifies}"
            )

        except:
            pass

        self.frame.after(
            5000,
            self.auto_refresh
        )