from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import sqlite3


def generate_pdf_report():
    conn = sqlite3.connect("clinic_records.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, full_name, gender, status, contact
        FROM records
    """)

    records = cursor.fetchall()
    conn.close()

    pdf = SimpleDocTemplate("clinic_report.pdf")

    data = [
        ["ID", "Full Name", "Gender", "Status", "Contact"]
    ]

    for row in records:
        data.append(list(row))

    table = Table(data)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
    ]))

    pdf.build([table])

    print("PDF Report Generated Successfully")