from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

ROOT = Path(__file__).parent
INVOICE_DIR = ROOT / "data" / "invoices"

invoices = [
    {
        "number": "INV-1001",
        "date": "2026-10-22",
        "customer": "Acme Ltd",
        "route": "Chennai -> Kozhikode",
        "items": [("Base delivery", 700), ("Fuel surcharge", 100), ("Handling", 50)],
        "total": 850,
    },
    {
        "number": "INV-1002",
        "date": "23/10/2026",
        "customer": "FreshMart",
        "route": "Bangalore -> Kochi",
        "items": [("Base delivery", 1000), ("Fuel surcharge", 150), ("Handling", 50)],
        "total": 1200,
    },
    {
        "number": "INV-1003",
        "date": "October 24, 2026",
        "customer": "John Traders",
        "route": "Mumbai -> Hyderabad",
        "items": [("Base delivery", 1300), ("Fuel surcharge", 200), ("Handling", 100)],
        "total": 1600,
    },
    {
        "number": "INV-1004",
        "date": "2026-10-26",
        "customer": "GreenBasket",
        "route": "Kochi -> Chennai",
        "items": [("Base delivery", 850), ("Fuel surcharge", 100)],
        "total": 950,
    },
    {
        "number": "INV-1005",
        "date": "27/10/2026",
        "customer": "Metro Foods",
        "route": "Kozhikode -> Bangalore",
        "items": [("Base delivery", 1100), ("Fuel surcharge", 150), ("Handling", 50)],
        "total": 1300,
    },
]


def create_invoice(invoice):
    output = INVOICE_DIR / f"{invoice['number']}.pdf"

    pdf = canvas.Canvas(str(output), pagesize=A4)
    width, height = A4

    y = height - 70

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(60, y, "SWIFTROUTE LOGISTICS")

    y -= 35
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(60, y, "INVOICE")

    y -= 30
    pdf.setFont("Helvetica", 10)

    pdf.drawString(60, y, f"Invoice Number: {invoice['number']}")
    y -= 18
    pdf.drawString(60, y, f"Invoice Date: {invoice['date']}")
    y -= 30

    pdf.drawString(60, y, f"Customer: {invoice['customer']}")
    y -= 18
    pdf.drawString(60, y, f"Route: {invoice['route']}")
    y -= 30

    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(60, y, "Line Item")
    pdf.drawString(400, y, "Amount")

    y -= 20
    pdf.setFont("Helvetica", 10)

    for name, amount in invoice["items"]:
        pdf.drawString(60, y, name)
        pdf.drawRightString(450, y, f"Rs {amount}")
        y -= 18

    y -= 10

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(60, y, f"TOTAL: Rs {invoice['total']}")

    pdf.save()


for invoice in invoices:
    create_invoice(invoice)

print(f"Created {len(invoices)} valid PDF invoices in:")
print(INVOICE_DIR)