import customtkinter as ctk

from tkinter import ttk, messagebox

from tkcalendar import DateEntry

from services.fne_service import (
    charger_factures_certifiees,
    charger_articles_facture,
    certifier_avoir,
    avoir_existe,
    creer_avoir_db
)


class AvoirPage:

    def __init__(self, parent):

        self.frame = ctk.CTkFrame(parent)
       

        self.frame.pack(
            fill="both",
            expand=True
        )

        self.setup_ui()

        self.charger_factures()
        self.auto_refresh()

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(self):

        # ==================================================
        # TITRE
        # ==================================================

        titre = ctk.CTkLabel(
            self.frame,
            text="CERTIFICATION DES AVOIRS",
            font=("Arial", 28, "bold")
        )

        titre.pack(
            pady=15
        )

        # ==================================================
        # ACTIONS / RECHERCHE
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
        # REFERENCE
        # ==================================================

        self.entry_ref = ctk.CTkEntry(
            actions_frame,
            placeholder_text="N° Facture / Référence FNE",
            width=250
        )

        self.entry_ref.pack(
            side="left",
            padx=20
        )

        # ==================================================
        # FILTRE STATUT
        # ==================================================

        self.combo_statut = ctk.CTkComboBox(
            actions_frame,
            values=[
                "TOUS",
                "DISPONIBLE",
                "DEJA CERTIFIÉ"
            ],
            width=180
        )

        self.combo_statut.set("TOUS")

        self.combo_statut.pack(
            side="left",
            padx=10
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
        # BOUTON CERTIFIER AVOIR
        # ==================================================

        btn_avoir = ctk.CTkButton(
            actions_frame,
            text="↩️ CERTIFIER AVOIR",
            fg_color="orange",
            command=self.generer_avoir
        )

        btn_avoir.pack(
            side="right",
            padx=10
        )

        # ==================================================
        # TABLE FACTURES
        # ==================================================

        frame_factures = ctk.CTkFrame(self.frame)

        frame_factures.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "CHK",
            "FACTURE",
            "FNE_ID",
            "REFERENCE",
            "DATE",
            "STATUT"
        )

        self.tree_factures = ttk.Treeview(
            frame_factures,
            columns=columns,
            show="headings",
            height=8
        )
        style = ttk.Style()

        style.configure(
            "Treeview",
            rowheight=38,
            font=("Arial", 12)
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 12, "bold")
        )

        for col in columns:

            self.tree_factures.heading(
                col,
                text=col
            )

            self.tree_factures.column(
                col,
                width=280,
                anchor="center"
            )

        self.tree_factures.pack(
            fill="both",
            expand=True
        )

        # ==================================================
        # TABLE ARTICLES
        # ==================================================

        frame_articles = ctk.CTkFrame(self.frame)

        frame_articles.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns2 = (
            "ARTICLE",
            "ITEM_ID",
            "QUANTITE"
        )

        self.tree_articles = ttk.Treeview(
            frame_articles,
            columns=columns2,
            show="headings",
            height=6
        )

        for col in columns2:

            self.tree_articles.heading(
                col,
                text=col
            )

            self.tree_articles.column(
                col,
                width=250,
                anchor="center"
            )

        self.tree_articles.pack(
            fill="both",
            expand=True
        )

        # ==================================================
        # EVENTS
        # ==================================================

        self.tree_factures.bind(
            "<<TreeviewSelect>>",
            self.selection_facture
        )

        # ==================================================
        # COULEURS BADGES
        # ==================================================

        self.tree_factures.tag_configure(
            "OK",
            background="#d4edda"
        )

        self.tree_factures.tag_configure(
            "DONE",
            background="#f8d7da"
        )


    def auto_refresh(self):
    
        try:

            current_count = len(
                self.tree_factures.get_children()
            )

            rows = charger_factures_certifiees()

            if len(rows) != current_count:

                self.charger_factures()

        except:
            pass

        self.frame.after(
            5000,
            self.auto_refresh
        )

    # ==================================================
    # CHARGER FACTURES
    # ==================================================

    def charger_factures(self):

        self.tree_factures.delete(
            *self.tree_factures.get_children()
        )

        rows = charger_factures_certifiees()

        for r in rows:

            deja_avoir = avoir_existe(
                r.FNE_INVOICE_ID
            )

            if deja_avoir:

                statut = "DEJA CERTIFIÉ"

                tag = "DONE"

                chk = "☑"

            else:

                statut = "DISPONIBLE"

                tag = "OK"

                chk = "☐"

            self.tree_factures.insert(
                "",
                "end",
                values=(
                    chk,
                    r.DO_PIECE,
                    r.FNE_INVOICE_ID,
                    r.FNE_REFERENCE,
                    r.DATE_CERTIFICATION.strftime("%Y-%m-%d"),
                    statut
                ),
                tags=(tag,)
            )

    # ==================================================
    # RECHERCHE
    # ==================================================

    def rechercher(self):

        date_debut = self.entry_debut.get()

        date_fin = self.entry_fin.get()

        reference = self.entry_ref.get().lower().strip()

        statut_filter = self.combo_statut.get()

        self.tree_factures.delete(
            *self.tree_factures.get_children()
        )

        rows = charger_factures_certifiees()

        for r in rows:

            deja_avoir = avoir_existe(
                r.FNE_INVOICE_ID
            )

            if deja_avoir:

                statut = "DEJA CERTIFIÉ"

                tag = "DONE"

                chk = "☑"

            else:

                statut = "DISPONIBLE"

                tag = "OK"

                chk = "☐"

            # =====================================
            # FILTRE REFERENCE
            # =====================================

            if reference:

                if (
                    reference not in str(r.DO_PIECE).lower()
                    and
                    reference not in str(r.FNE_REFERENCE).lower()
                ):
                    continue

            # =====================================
            # FILTRE STATUT
            # =====================================

            if statut_filter != "TOUS":

                if statut != statut_filter:
                    continue

            # =====================================
            # FILTRE DATE
            # =====================================

            date_facture = r.DATE_CERTIFICATION.strftime("%Y-%m-%d")

            if date_facture < date_debut:
                continue

            if date_facture > date_fin:
                continue

            # =====================================
            # INSERTION
            # =====================================

            self.tree_factures.insert(
                "",
                "end",
                values=(
                    chk,
                    r.DO_PIECE,
                    r.FNE_INVOICE_ID,
                    r.FNE_REFERENCE,
                    date_facture,
                    statut
                ),
                tags=(tag,)
            )

    # ==================================================
    # RESET
    # ==================================================

    def reinitialiser(self):

        self.entry_ref.delete(
            0,
            "end"
        )

        self.combo_statut.set(
            "TOUS"
        )

        self.charger_factures()

    # ==================================================
    # SELECTION FACTURE
    # ==================================================

    def selection_facture(self, event):

        self.tree_articles.delete(
            *self.tree_articles.get_children()
        )

        selected = self.tree_factures.selection()

        if not selected:
            return

        values = self.tree_factures.item(
            selected[0],
            "values"
        )

        do_piece = values[1]

        articles = charger_articles_facture(
            do_piece
        )

        for a in articles:

            self.tree_articles.insert(
                "",
                "end",
                values=(
                    a.ARTICLE,
                    a.FNE_ITEM_ID,
                    a.QUANTITE
                )
            )

    # ==================================================
    # GENERER AVOIR
    # ==================================================

    def generer_avoir(self):

        selected = self.tree_factures.selection()

        if not selected:

            messagebox.showwarning(
                "Attention",
                "Sélectionnez une facture."
            )

            return

        values = self.tree_factures.item(
            selected[0],
            "values"
        )

        do_piece = values[1]

        fne_invoice_id = values[2]

        # =====================================
        # VERIFICATION DOUBLE AVOIR
        # =====================================

        if avoir_existe(fne_invoice_id):

            messagebox.showerror(
                "Erreur",
                "Cette facture possède déjà un avoir."
            )

            return

        # =====================================
        # ARTICLES
        # =====================================

        items = []

        for item in self.tree_articles.get_children():

            v = self.tree_articles.item(
                item,
                "values"
            )

            try:

                qty = float(
                    str(v[2]).replace(",", ".")
                )

            except:

                qty = 0

            if qty <= 0:
                continue

            items.append({
                "id": v[1],
                "quantity": qty
            })

        # =====================================
        # VERIFICATION ARTICLES
        # =====================================

        if not items:

            messagebox.showerror(
                "Erreur",
                "Aucun article valide."
            )

            return

        # =====================================
        # API FNE
        # =====================================

        
        print("INVOICE ID :", fne_invoice_id)

        print("ITEMS :", items)

        ok = certifier_avoir(
            fne_invoice_id,
            items
        )

        print("REPONSE API :", ok)

        # =====================================
        # SUCCES
        # =====================================

        if ok:

            creer_avoir_db(
                fne_invoice_id,
                do_piece,
                items
            )

            messagebox.showinfo(
                "Succès",
                "Avoir certifié avec succès."
            )

            self.charger_factures()

        else:

            messagebox.showerror(
                "Erreur",
                "Erreur certification avoir."
            )