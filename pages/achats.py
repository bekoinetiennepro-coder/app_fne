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
    creer_achat_db,
    charger_lignes_achat
)

class AchatPage:

    def __init__(self, parent):

        self.frame = ctk.CTkFrame(parent)

        self.frame.pack(
            fill="both",
            expand=True
        )
         # PAGINATION
        self.page = 1
        self.page_size = 20
        self.total_pages = 1

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
            "MONTANT",
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
        
        # =================================================
        # PAGINATION UI
        # =================================================

        pagination_frame = ctk.CTkFrame(self.frame)

        pagination_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        btn_prev = ctk.CTkButton(
            pagination_frame,
            text="⬅ Précédent",
            width=120,
            command=self.page_precedente
        )

        btn_prev.pack(
            side="left",
            padx=10
        )

        self.lbl_page = ctk.CTkLabel(
            pagination_frame,
            text="Page 1 / 1",
            font=("Arial", 14, "bold")
        )

        self.lbl_page.pack(
            side="left",
            padx=20
        )

        btn_next = ctk.CTkButton(
            pagination_frame,
            text="➡ Suivant",
            width=120,
            command=self.page_suivante
        )

        btn_next.pack(
            side="left",
            padx=10
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
        if values[5] == "CERTIFIÉ":

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

        # =================================================
        # TOTAL PAGES
        # =================================================

        total = len(rows)

        self.total_pages = max(
            1,
            (total + self.page_size - 1) // self.page_size
        )

        # =================================================
        # LIMITES
        # =================================================

        start = (self.page - 1) * self.page_size

        end = start + self.page_size

        rows_page = rows[start:end]

        # =================================================
        # LABEL PAGE
        # =================================================

        self.lbl_page.configure(
            text=f"Page {self.page} / {self.total_pages}"
        )

        # =================================================
        # INSERTION
        # =================================================

        for r in rows_page:

            if achat_existe(r[0]):

                statut = "CERTIFIÉ"
                tag = "DONE"

            else:

                statut = "DISPONIBLE"
                tag = "OK"

            self.tree.insert(
                "",
                "end",
                # values=(
                #     "☐",
                #     r[0],
                #     r[1],
                #     r[3].strftime("%Y-%m-%d"),
                #     statut
                # ),
                 values=(
                    "☐",
                    r[0],  # FACTURE
                    r[1],  # FOURNISSEUR
                    f"{float(r[6]):,.0f} FCFA",  # MONTANT
                    r[3].strftime("%Y-%m-%d"),   # DATE
                    statut
                ),
                tags=(tag,)
            )
    # =====================================================
    # PAGE SUIVANTE
    # =====================================================

    def page_suivante(self):

        if self.page < self.total_pages:

            self.page += 1

            self.charger_donnees()

    # =====================================================
    # PAGE PRECEDENTE
    # =====================================================

    def page_precedente(self):

        if self.page > 1:

            self.page -= 1

            self.charger_donnees()     

    
    # =====================================================
    # RECHERCHE
    # =====================================================

    def rechercher(self):
        
        self.page = 1

        date_debut = self.entry_debut.get()

        date_fin = self.entry_fin.get()

        ref = self.entry_ref.get().lower().strip()

        statut_filter = self.combo_statut.get()

        self.tree.delete(
            *self.tree.get_children()
        )

        rows = charger_achats()

        for r in rows:

            if achat_existe(r[0]):

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
                    ref not in str(r[0]).lower()
                    and
                    ref not in str(r[1]).lower()
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

            date_doc = r[3].strftime("%Y-%m-%d")

            if date_doc < date_debut:
                continue

            if date_doc > date_fin:
                continue

            # =========================================
            # INSERT
            # =========================================

            # self.tree.insert(
            #     "",
            #     "end",
            #     values=(
            #         "☐",
            #         r.DO_PIECE,
            #         r.DO_TIERS,
            #         date_doc,
                    
            #         statut
            #     ),
            #     tags=(tag,)
            # )
            self.tree.insert(
                "",
                "end",
                values=(
                    "☐",
                    r[0],  # DO_Piece
                    r[1],  # DO_Tiers
                    f"{float(r[6]):,.0f} FCFA", # DL_MontantTTC
                    r[3].strftime("%Y-%m-%d"),  # DO_Date
                    statut
                ),
                tags=(tag,)
            )

    # =====================================================
    # RESET
    # =====================================================

    def reinitialiser(self):
        
        self.page = 1

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

        # ==========================================
        # RECUPERATION LIGNE
        # ==========================================

        values = self.tree.item(
            selected[0],
            "values"
        )

        do_piece = values[1]

        fournisseur = values[2]

        # ==========================================
        # VERIFICATION DOUBLE CERTIFICATION
        # ==========================================

        if achat_existe(do_piece):

            messagebox.showerror(
                "Erreur",
                "Cet achat est déjà certifié."
            )

            return

        # ==========================================
        # CHARGER ARTICLES ACHAT
        # ==========================================

        lignes = charger_lignes_achat(
            do_piece
        )
        client_ncc = lignes[0].CT_Siret or ""
        client_phone = lignes[0].CT_Telephone or ""
        client_email = lignes[0].CT_Email or ""
        print("COLONNES DISPONIBLES :")
        print(lignes[0])
        # ==========================================
        # CONSTRUCTION ITEMS
        # ==========================================

        items = []

        for r in lignes:

            prix = float(r.DL_PrixUnitaire or 0)

            if prix <= 0:
                continue

            items.append({

                "reference": r.AR_Ref or "",

                "description": r.DL_Design or "",

                "quantity": float(r.DL_Qte or 0),

                "amount": prix,

                "discount": 0,

                "measurementUnit": "pcs",
                

            })

        # ==========================================
        # VERIFICATION ITEMS
        # ==========================================

        if not items:

            messagebox.showerror(
                "Erreur",
                "Aucun article trouvé."
            )

            return

        # ==========================================
        # PAYLOAD FNE
        # ==========================================

        payload = {

            "invoiceType": "purchase",

            "paymentMethod": "mobile-money",

            "template": "B2B",

            "clientNcc": client_ncc,

            "clientCompanyName": fournisseur,

            "clientPhone": client_phone,

            "clientEmail": client_email,

            "clientSellerName": fournisseur,

            "pointOfSale": "SODISMAF",

            "establishment": "SODISMAF",

            "commercialMessage": "Soyez les bienvenus",

            "footer": "Merci pour votre confiance",

            "items": items,

            "discount": 0
        }

        print("PAYLOAD FNE :")
        print(payload)

        # ==========================================
        # API FNE
        # ==========================================

        response = certifier_achat(
            payload
        )

        print("REPONSE API :")
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

                len(items)
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
