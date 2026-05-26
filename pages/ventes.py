import customtkinter as ctk

from tkinter import ttk, messagebox

from tkcalendar import DateEntry

from datetime import datetime

from services.fne_service import (
    charger_factures,
    facture_est_certifiee,
    certifier_facture,
    sauvegarder_facture_fne,
    sauvegarder_items_fne
)


class VentePage:

    def __init__(self, parent):

        # ==================================================
        # FRAME PRINCIPAL
        # ==================================================

        self.frame = ctk.CTkFrame(parent)

        self.frame.pack(
            fill="both",
            expand=True
        )
        self.auto_refresh()

        # ==================================================
        # TITRE
        # ==================================================

        titre = ctk.CTkLabel(
            self.frame,
            text="CERTIFICATION DES VENTES",
            font=("Arial", 30, "bold")
        )

        titre.pack(pady=20)

        # ==================================================
        # FRAME ACTIONS
        # ==================================================

        actions_frame = ctk.CTkFrame(self.frame)

        actions_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        # ==================================================
        # DATE DEBUT
        # ==================================================

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

        # ==================================================
        # DATE FIN
        # ==================================================

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

        # ==================================================
        # REFERENCE FACTURE
        # ==================================================

        self.entry_ref = ctk.CTkEntry(
            actions_frame,
            placeholder_text="N° Facture",
            width=220
        )

        self.entry_ref.pack(
            side="left",
            padx=20
        )

        # ==================================================
        # BOUTON RECHERCHE
        # ==================================================

        btn_rechercher = ctk.CTkButton(
            actions_frame,
            text="🔎 Rechercher",
            command=self.rechercher
        )

        btn_rechercher.pack(
            side="left",
            padx=10
        )

        # ==================================================
        # BOUTON RESET
        # ==================================================

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

        # ==================================================
        # BOUTON CERTIFIER
        # ==================================================

        btn_certifier = ctk.CTkButton(
            actions_frame,
            text="✅ CERTIFIER",
            fg_color="green",
            command=self.certifier_selection
        )

        btn_certifier.pack(
            side="right",
            padx=10
        )

        # ==================================================
        # FRAME TABLEAU
        # ==================================================

        table_frame = ctk.CTkFrame(self.frame)

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # ==================================================
        # STYLE TREEVIEW
        # ==================================================

        style = ttk.Style()

        style.configure(
            "Treeview",
            rowheight=35,
            font=("Arial", 11)
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 12, "bold")
        )

        # ==================================================
        # COLONNES
        # ==================================================

        columns = (
            "CHECK",
            "FACTURE",
            "REFERENCE",
            "DATE",
            "CLIENT",
            "CODE_CLIENT",
            "MONTANT",
            "STATUT"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.tree.pack(
            fill="both",
            expand=True
        )

        # ==================================================
        # CONFIGURATION COLONNES
        # ==================================================

        self.tree.heading("CHECK", text="✓")

        self.tree.column(
            "CHECK",
            width=100,
            anchor="center"
        )

        for col in columns[1:]:

            self.tree.heading(
                col,
                text=col
            )

            self.tree.column(
                col,
                width=180,
                anchor="center"
            )

        # ==================================================
        # TAGS COULEURS
        # ==================================================

        self.tree.tag_configure(
            "certifiee",
            background="#d4f8d4"
        )

        self.tree.tag_configure(
            "non_certifiee",
            background="#f8d4d4"
        )

        # ==================================================
        # EVENT CHECKBOX
        # ==================================================

        self.tree.bind(
            "<Button-1>",
            self.toggle_check
        )

        # ==================================================
        # CHARGEMENT INITIAL
        # ==================================================

        self.charger_table()


    def auto_refresh(self):
    
        try:

            current_count = len(
                self.tree.get_children()
            )

            rows = charger_factures()

            if len(rows) != current_count:

                self.charger_donnees()

        except:
            pass

        self.frame.after(
            5000,
            self.auto_refresh
        )

    # ==================================================
    # CHARGER TABLE
    # ==================================================

    def charger_table(
            self,
            date_debut=None,
            date_fin=None,
            do_piece=None
    ):

        self.tree.delete(
            *self.tree.get_children()
        )

        factures = charger_factures(
            date_debut,
            date_fin,
            do_piece
        )

        for f in factures:

            est_certifie = facture_est_certifiee(
                f.DO_Piece
            )

            statut = (
                "CERTIFIÉE"
                if est_certifie
                else "NON CERTIFIÉE"
            )

            tag = (
                "certifiee"
                if est_certifie
                else "non_certifiee"
            )

            self.tree.insert(
                "",
                "end",
                values=(
                    "☐",
                    f.DO_Piece,
                    f.DO_Ref,
                    f.DO_Date.strftime("%Y-%m-%d"),
                    f.CT_Intitule,
                    f.CT_Num,
                    int(f.DL_MontantTTC),
                    statut
                ),
                tags=(tag,)
            )

    # ==================================================
    # CHECKBOX
    # ==================================================

    def toggle_check(self, event):

        col = self.tree.identify_column(event.x)

        item = self.tree.identify_row(event.y)

        if col != "#1" or not item:
            return

        values = list(
            self.tree.item(item, "values")
        )

        if values[7] == "CERTIFIÉE":

            messagebox.showwarning(
                "Bloqué",
                "Facture déjà certifiée"
            )

            return

        values[0] = (
            "☑"
            if values[0] == "☐"
            else "☐"
        )

        self.tree.item(
            item,
            values=values
        )

    # ==================================================
    # RECHERCHE
    # ==================================================

    def rechercher(self):

        d1 = self.entry_debut.get().strip()

        d2 = self.entry_fin.get().strip()

        ref = self.entry_ref.get().strip()

        self.charger_table(
            d1 or None,
            d2 or None,
            ref or None
        )

    # ==================================================
    # RESET
    # ==================================================

    def reinitialiser(self):

        self.entry_debut.set_date(
            datetime.today()
        )

        self.entry_fin.set_date(
            datetime.today()
        )

        self.entry_ref.delete(
            0,
            "end"
        )

        self.charger_table()

    # ==================================================
    # CERTIFICATION
    # ==================================================

    def certifier_selection(self):

        selection = False

        certification_ok = False

        for item in self.tree.get_children():

            values = list(
                self.tree.item(item, "values")
            )

            # ==========================================
            # FACTURE COCHÉE
            # ==========================================

            if values[0] == "☑":

                selection = True

                statut = values[7]

                # ==========================================
                # NON CERTIFIÉE
                # ==========================================

                if statut == "NON CERTIFIÉE":

                    ok, data = certifier_facture(values[1])

                    if ok:

                        print(data)

                        invoice = data.get("invoice", {})

                        print(invoice)

                        fne_invoice_id = invoice.get("id")

                        fne_reference = invoice.get("reference")

                        items = invoice.get("items", [])

                        print(items)

                        # ==========================================
                        # SAUVEGARDE FACTURE FNE
                        # ==========================================

                        sauvegarder_facture_fne(
                            values[1],
                            fne_invoice_id,
                            fne_reference
                        )

                        # ==========================================
                        # SAUVEGARDE ARTICLES
                        # ==========================================

                        sauvegarder_items_fne(
                            values[1],
                            items
                        )

                        # ==========================================
                        # UPDATE TABLE
                        # ==========================================

                        values[7] = "CERTIFIÉE"

                        values[0] = "☐"

                        self.tree.item(
                            item,
                            values=values,
                            tags=("certifiee",)
                        )

                        certification_ok = True

        # ==================================================
        # MESSAGE AUCUNE SELECTION
        # ==================================================

        if not selection:

            messagebox.showwarning(
                "Aucune sélection",
                "Veuillez sélectionner une facture."
            )

            return

        # ==================================================
        # MESSAGE SUCCÈS
        # ==================================================

        if certification_ok:

            messagebox.showinfo(
                "Succès",
                "Certification terminée."
            )

        else:

            messagebox.showwarning(
                "Information",
                "Aucune facture certifiée."
            )