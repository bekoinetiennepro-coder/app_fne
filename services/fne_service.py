import pyodbc
import requests

#=================================================
# CONFIGURATION API FNE
#=================================================

API_URL = "http://54.247.95.108/ws/external/invoices/sign"

API_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "BOYd7xHHqOz3uBYKbZyajAsffYnbUpzf"
}

# ==================================================
# CONNEXION SQL
# ==================================================

def get_connection():

    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=ETS DIALLO AMADOU;"
        "Trusted_Connection=yes;"
    )

# ==================================================
# GESTION DES FACTURES
# ==================================================

def facture_est_certifiee(do_piece):
    
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT COUNT(*)

        FROM FACTURES_FNE

        WHERE DO_PIECE = ?

    """, do_piece)

    result = cursor.fetchone()[0]

    conn.close()

    return result > 0



# ==================================================
# CHARGER FACTURES
# ==================================================

def charger_factures(
        date_debut=None,
        date_fin=None,
        do_piece=None
):

    conn = get_connection()

    cursor = conn.cursor()

    query = """
        SELECT
            DO_Piece,
            MAX(DO_Ref) AS DO_Ref,
            MAX(DO_Date) AS DO_Date,
            MAX(CT_Intitule) AS CT_Intitule,
            MAX(CT_Num) AS CT_Num,
            SUM(DL_MontantTTC) AS DL_MontantTTC
        FROM [ETS DIALLO AMADOU].[dbo].[View_FNE_RLE]
        WHERE DO_Type = 6
    """

    params = []

    if date_debut:
        query += " AND DO_Date >= ?"
        params.append(date_debut)

    if date_fin:
        query += " AND DO_Date <= ?"
        params.append(date_fin)

    if do_piece:
        query += " AND DO_Piece LIKE ?"
        params.append(f"%{do_piece}%")

    query += """
        GROUP BY DO_Piece
        ORDER BY MAX(DO_Date) DESC
    """

    cursor.execute(query, params)

    rows = cursor.fetchall()

    conn.close()

    return rows

# ==================================================
# PAYLOAD API
# ==================================================

def construire_payload(DO_Piece):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM [ETS DIALLO AMADOU].[dbo].[View_FNE_RLE]
        WHERE DO_Piece = ?
    """, DO_Piece)

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        return None

    items = []

    for r in rows:

        items.append({
            "reference": r.AR_Ref,
            "description": r.DL_Design,
            "quantity": float(r.DL_Qte),
            "amount": float(r.DL_PrixUnitaire),
            "discount": 0,
            "measurementUnit": "pcs",
            "taxes": ["TVA"]
        })

    return {
        "invoiceType": "sale",
        "paymentMethod": "mobile-money",
        "template": "B2B",
        "clientNcc": rows[0].CT_Num,
        "clientCompanyName": rows[0].CT_Intitule,
        "clientPhone": "0709331306",
        "clientEmail": "test@gmail.com",
        "pointOfSale": "SODISMAF",
        "establishment": "SODISMAF",
        "items": items,
        "customTaxes": [{"name": "DTD", "amount": 5}],
        "discount": 10
    }

# ==================================================
# CERTIFIER FACTURE
# ==================================================

def certifier_facture(DO_Piece):
    
    payload = construire_payload(DO_Piece)

    if not payload:
        return False, None

    try:

        r = requests.post(
            API_URL,
            headers=API_HEADERS,
            json=payload
        )

        print(r.text)

        if r.status_code in (200, 201):

            data = r.json()

            return True, data

        return False, None

    except Exception as e:

        print(e)

        return False, None

# ==================================================
# GESTION DES AVOIRS
# ==================================================

# ==================================================
# FACTURES CERTIFIÉES
# ==================================================

def charger_factures_certifiees():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT
            DO_PIECE,
            FNE_INVOICE_ID,
            FNE_REFERENCE,
            DATE_CERTIFICATION

        FROM FACTURES_FNE

        ORDER BY DATE_CERTIFICATION DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==================================================
# ARTICLES FACTURE
# ==================================================

def charger_articles_facture(do_piece):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT
            ARTICLE,
            FNE_ITEM_ID,
            QUANTITE

        FROM FACTURES_FNE_ITEMS

        WHERE DO_PIECE = ?

    """, do_piece)

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==================================================
# CERTIFIER AVOIR
# ==================================================

def certifier_avoir(
        fne_invoice_id,
        items
):

    url = f"http://54.247.95.108/ws/external/invoices/{fne_invoice_id}/refund"

    payload = {
        "items": items
    }

    r = requests.post(
        url,
        headers=API_HEADERS,
        json=payload
    )

    return r.status_code in (200, 201)
    


# ==================================================
# SAUVEGARDE FACTURE FNE
# ==================================================

def sauvegarder_facture_fne(
        do_piece,
        fne_invoice_id,
        fne_reference,
        statut="CERTIFIÉE",
        message="OK"
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO FACTURES_FNE
        (
            DO_PIECE,
            FNE_INVOICE_ID,
            FNE_REFERENCE,
            STATUT,
            MESSAGE_API
        )

        VALUES (?, ?, ?, ?, ?)

    """, (
        do_piece,
        fne_invoice_id,
        fne_reference,
        statut,
        message
    ))

    conn.commit()

    conn.close()


# ==================================================
# SAUVEGARDE ITEMS FNE
# ==================================================

def sauvegarder_items_fne(
        do_piece,
        items
):

    conn = get_connection()

    cursor = conn.cursor()

    for item in items:

        cursor.execute("""

            INSERT INTO FACTURES_FNE_ITEMS
            (
                DO_PIECE,
                ARTICLE,
                FNE_ITEM_ID,
                QUANTITE
            )

            VALUES (?, ?, ?, ?)

        """, (
            do_piece,
            item.get("description"),
            item.get("id"),
            item.get("quantity")
        ))

    conn.commit()

    conn.close()
    
# ==================================================
# AVOIR EXISTE
# ==================================================

def avoir_existe(fne_invoice_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*)
        FROM AVOIRS
        WHERE FNE_INVOICE_ID = ?
    """, (fne_invoice_id,))
    result = cursor.fetchone()[0] > 0
    conn.close()
    return result


def avoir_existe(fne_invoice_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*)
        FROM AVOIRS
        WHERE FNE_INVOICE_ID = ?
    """, (fne_invoice_id,))
    result = cursor.fetchone()[0] > 0
    conn.close()
    return result


# ==================================================
# CREER AVOIR DB
# ==================================================

def creer_avoir_db(fne_invoice_id, do_piece, items):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO AVOIRS (FNE_INVOICE_ID, DO_PIECE)
        OUTPUT INSERTED.ID
        VALUES (?, ?)
    """, (fne_invoice_id, do_piece))

    avoir_id = cursor.fetchone()[0]

    total_qty = 0

    for item in items:

        cursor.execute("""
            INSERT INTO AVOIR_ITEMS (AVOIR_ID, ITEM_ID, QUANTITE)
            VALUES (?, ?, ?)
        """, (avoir_id, item["id"], item["quantity"]))

        total_qty += item["quantity"]

    cursor.execute("""
        UPDATE AVOIRS
        SET TOTAL_QTY = ?
        WHERE ID = ?
    """, (total_qty, avoir_id))

    conn.commit()

    return True




# ==================================================
# GESTION DU TABLEAU DE BORD
# ==================================================


# ==================================================
# TOTAL FACTURES
# ==================================================

def total_factures():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
         SELECT COUNT(DISTINCT DO_Piece)
            DO_Piece,
            MAX(DO_Ref) AS DO_Ref,
            MAX(DO_Date) AS DO_Date,
            MAX(CT_Intitule) AS CT_Intitule,
            MAX(CT_Num) AS CT_Num,
            SUM(DL_MontantTTC) AS DL_MontantTTC
        FROM [ETS DIALLO AMADOU].[dbo].[View_FNE_RLE]
        WHERE DO_Type = 6
    """)

    return cursor.fetchone()[0]


# ==================================================
# FACTURES CERTIFIEES
# ==================================================

def total_factures_certifiees():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*)
        FROM FACTURES_FNE
    """)

    return cursor.fetchone()[0]


# ==================================================
# FACTURES NON CERTIFIEES
# ==================================================

def total_factures_non_certifiees():

    total = total_factures()

    certifiees = total_factures_certifiees()

    return total - certifiees


# ==================================================
# TOTAL AVOIRS
# ==================================================

def total_avoirs_certifies():

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*)
        FROM AVOIRS
    """)

    return cursor.fetchone()[0]