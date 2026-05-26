# =========================================================
# pages/achats.py
# =========================================================

import customtkinter as ctk

from tkinter import ttk, messagebox

from tkcalendar import DateEntry

from services.fne_service import (
    charger_achats,
    achat_existe,
    certifier_achat,
    creer_achat_db
)


class AchatPage:

    def __init__(self, parent):

        self.frame = ctk.CTkFrame(parent)

        self.frame.pack(
            fill="both",
            expand=True
        )

        self.setup_ui()

        self.charger_donnees()
        self.auto_refresh()

    # =====================================================
    # UI
    # =====================================================

    def setup_ui(self):

        # =================================================
        # STYLE TREEVIEW
        # =================================================

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "Treeview",
            rowheight=40,
            font=("Arial", 12)
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 12, "bold")
        )

        # =================================================
        # TITRE
        # =================================================

        titre = ctk.CTkLabel(
            self.frame,
            text="GESTION DES ACHATS FNE",
            font=("Arial", 30, "bold")
        )

        titre.pack(
            pady=20
        )

        # =================================================
        # ACTIONS
        # =================================================

        actions_frame = ctk.CTkFrame(self.frame)

        actions_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        # =================================================
        # DATE DEBUT
        # =================================================

        lbl_debut = ctk.CTkLabel(
            actions_frame,
            text="Date début"
        )

        lbl_debut.pack(
            side="left",
            padx=5
        )

        self.entry_debut = DateEntry(
            actions_frame,
            width=15,
            date_pattern="yyyy-mm-dd"
        )

        self.entry_debut.pack(
            side="left",
            padx=5
        )

        # =================================================
        # DATE FIN
        # =================================================

        lbl_fin = ctk.CTkLabel(
            actions_frame,
            text="Date fin"
        )

        lbl_fin.pack(
            side="left",
            padx=10
        )

        self.entry_fin = DateEntry(
            actions_frame,
            width=15,
            date_pattern="yyyy-mm-dd"
        )

        self.entry_fin.pack(
            side="left",
            padx=5
        )

        # =================================================
        # REFERENCE
        # =================================================

        self.entry_ref = ctk.CTkEntry(
            actions_frame,
            placeholder_text="N° Facture / Fournisseur",
            width=260
        )

        self.entry_ref.pack(
            side="left",
            padx=20
        )

        # =================================================
        # FILTRE STATUT
        # =================================================

        self.combo_statut = ctk.CTkComboBox(
            actions_frame,
            values=[
                "TOUS",
                "DISPONIBLE",
                "CERTIFIÉ"
            ],
            width=180
        )

        self.combo_statut.set("TOUS")

        self.combo_statut.pack(
            side="left",
            padx=10
        )

        # =================================================
        # BOUTON RECHERCHE
        # =================================================

        btn_rechercher = ctk.CTkButton(
            actions_frame,
            text="🔎 Rechercher",
            command=self.rechercher
        )

        btn_rechercher.pack(
            side="left",
            padx=10
        )

        # =================================================
        # RESET
        # =================================================

        btn_reset = ctk.CTkButton(
            actions_frame,
            text="♻ Réinitialiser",
            fg_color="gray",
            command=self.reinitialiser
        )

        btn_reset.pack(
            side="left",
            padx=10
        )

        # =================================================
        # CERTIFIER
        # =================================================

        btn_certifier = ctk.CTkButton(
            actions_frame,
            text="✅ CERTIFIER ACHAT",
            fg_color="green",
            command=self.certifier_selection
        )

        btn_certifier.pack(
            side="right",
            padx=10
        )

        # =================================================
        # TABLE
        # =================================================

        frame_table = ctk.CTkFrame(self.frame)

        frame_table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "CHK",
            "FACTURE",
            "FOURNISSEUR",
            "DATE",
            "STATUT"
        )

        self.tree = ttk.Treeview(
            frame_table,
            columns=columns,
            show="headings",
            height=15
        )

        for col in columns:

            self.tree.heading(
                col,
                text=col
            )

            self.tree.column(
                col,
                width=240,
                anchor="center"
            )

        self.tree.pack(
            fill="both",
            expand=True
        )
        self.tree.bind(
            "<Button-1>",
            self.toggle_checkbox
        )

        # =================================================
        # TAGS
        # =================================================

        self.tree.tag_configure(
            "OK",
            background="#d4edda"
        )

        self.tree.tag_configure(
            "DONE",
            background="#cfe2ff"
        )

    # =====================================================
    # AUTO REFRESH
    # =====================================================

    def auto_refresh(self):
    
        try:

            current_count = len(
                self.tree.get_children()
            )

            rows = charger_achats()

            if len(rows) != current_count:

                self.charger_donnees()

        except:
            pass

        self.frame.after(
            5000,
            self.auto_refresh
        )

    # =====================================================
    # CHARGER DONNEES
    # =====================================================
    def toggle_checkbox(self, event):
    
        item = self.tree.identify_row(event.y)

        if not item:
            return

        column = self.tree.identify_column(event.x)

        # uniquement colonne checkbox
        if column != "#1":
            return

        values = list(
            self.tree.item(item, "values")
        )

        # bloque si déjà certifié
        if values[4] == "CERTIFIÉ":

            messagebox.showwarning(
                "Attention",
                "Cet achat est déjà certifié."
            )

            return

        # toggle
        values[0] = "☑" if values[0] == "☐" else "☐"

        self.tree.item(
            item,
            values=values
        )



    def charger_donnees(self):

        self.tree.delete(
            *self.tree.get_children()
        )

        rows = charger_achats()

        for r in rows:

            if achat_existe(r.DO_PIECE):

                statut = "CERTIFIÉ"

                tag = "DONE"

            else:

                statut = "DISPONIBLE"

                tag = "OK"

            self.tree.insert(
                "",
                "end",
                values=(
                     "☐",
                    r.DO_PIECE,
                    r.DO_TIERS,
                    r.DO_Date.strftime("%Y-%m-%d"),
                   
                    statut
                ),
                tags=(tag,)
            )

    # =====================================================
    # RECHERCHE
    # =====================================================

    def rechercher(self):

        date_debut = self.entry_debut.get()

        date_fin = self.entry_fin.get()

        ref = self.entry_ref.get().lower().strip()

        statut_filter = self.combo_statut.get()

        self.tree.delete(
            *self.tree.get_children()
        )

        rows = charger_achats()

        for r in rows:

            if achat_existe(r.DO_PIECE):

                statut = "CERTIFIÉ"

                tag = "DONE"

            else:

                statut = "DISPONIBLE"

                tag = "OK"

            # =========================================
            # FILTRE REFERENCE
            # =========================================

            if ref:

                if (
                    ref not in str(r.DO_PIECE).lower()
                    and
                    ref not in str(r.DO_TIERS).lower()
                ):
                    continue

            # =========================================
            # FILTRE STATUT
            # =========================================

            if statut_filter != "TOUS":

                if statut != statut_filter:
                    continue

            # =========================================
            # FILTRE DATE
            # =========================================

            date_doc = r.DO_Date.strftime("%Y-%m-%d")

            if date_doc < date_debut:
                continue

            if date_doc > date_fin:
                continue

            # =========================================
            # INSERT
            # =========================================

            self.tree.insert(
                "",
                "end",
                values=(
                    "☐",
                    r.DO_PIECE,
                    r.DO_TIERS,
                    date_doc,
                    
                    statut
                ),
                tags=(tag,)
            )

    # =====================================================
    # RESET
    # =====================================================

    def reinitialiser(self):

        self.entry_ref.delete(
            0,
            "end"
        )

        self.combo_statut.set(
            "TOUS"
        )

        self.charger_donnees()

    # =====================================================
    # CERTIFIER ACHAT
    # =====================================================

    def certifier_selection(self):
    
        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Attention",
                "Sélectionnez un achat."
            )

            return

        values = self.tree.item(
            selected[0],
            "values"
        )

        do_piece = values[1]

        fournisseur = values[2]

        # ==========================================
        # DOUBLE CERTIFICATION
        # ==========================================

        if achat_existe(do_piece):

            messagebox.showerror(
                "Erreur",
                "Cet achat est déjà certifié."
            )

            return

        # ==========================================
        # PAYLOAD OFFICIEL FNE ACHAT
        # ==========================================

        payload = {

            "invoiceType": "purchase",

            "paymentMethod": "mobile-money",

            "template": "B2B",
            
            "clientNcc": "",

            "clientCompanyName": fournisseur,

            "clientPhone": "0700000000",

            "clientEmail": "",

            "clientSellerName": fournisseur,

            "pointOfSale": "SODISMAF",

            "establishment": "SODISMAF",

            "commercialMessage": "Soyez les bienvenus",

            "footer": "Merci pour votre confiance",

           
            "items": [

                {
                    "reference": do_piece,

                    "description": "ACHAT FOURNISSEUR",

                    "quantity": 1,

                    "amount": 1,

                    "discount": 0,

                    "measurementUnit": "pcs"
                }

            ],

            "discount": 0
        }

        print(payload)

        # ==========================================
        # API
        # ==========================================

        response = certifier_achat(
            payload
        )

        print(response)

        # ==========================================
        # SUCCES
        # ==========================================

        if response:

            creer_achat_db(
                do_piece,
                response["invoice"]["id"],
                response["reference"],
                fournisseur,
                1
            )

            messagebox.showinfo(
                "Succès",
                "Achat certifié avec succès."
            )

            self.charger_donnees()

        else:

            messagebox.showerror(
                "Erreur",
                "Erreur certification achat."
            )

        # =============================================
        # SUCCES
        # =============================================

        if response:

            creer_achat_db(
                do_piece,
                response["invoice"]["id"],
                response["reference"],
                fournisseur,
                1
            )

            messagebox.showinfo(
                "Succès",
                "Achat certifié avec succès."
            )

            self.charger_donnees()

        else:

            messagebox.showerror(
                "Erreur",
                "Erreur certification achat."
            )
            
