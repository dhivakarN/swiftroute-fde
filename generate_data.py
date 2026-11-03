import csv
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

ROOT = Path(__file__).parent
RAW_DIR = ROOT / "data" / "raw"
INVOICE_DIR = ROOT / "data" / "invoices"
SUPPORT_DIR = ROOT / "data" / "support"

RAW_DIR.mkdir(parents=True, exist_ok=True)
INVOICE_DIR.mkdir(parents=True, exist_ok=True)
SUPPORT_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------
# Shipment data
# -----------------------------

customers = [
    "Acme Ltd",
    "FreshMart",
    "John Traders",
    "GreenBasket",
    "Metro Foods",
    "Prime Retail",
    "City Electronics",
    "QuickBuy",
    "Daily Needs",
    "South Market",
]

city_variants = {
    "Chennai": ["Chennai", "Madras", " chennai ", "CHENNAI"],
    "Bangalore": ["Bangalore", "Bengaluru", " bangalore ", "BANGALORE"],
    "Kozhikode": ["Kozhikode", "Calicut", " kozhikode ", "KOZHIKODE"],
    "Kochi": ["Kochi", "Cochin", " kochi ", "KOCHI"],
    "Hyderabad": ["Hyderabad", " hyderabad ", "HYDERABAD"],
    "Mumbai": ["Mumbai", "Bombay", " mumbai ", "MUMBAI"],
}

cities = list(city_variants.keys())

statuses = [
    "Delivered",
    "Late",
    "In Transit",
    "Cancelled",
]

date_formats = [
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%b %d %Y",
]

rows = []

start_date = datetime(2026, 10, 1)

for i in range(1, 501):
    shipment_id = f"SR{1000 + i}"

    customer = random.choice(customers)
    origin = random.choice(cities)
    destination = random.choice([c for c in cities if c != origin])

    shipment_date = start_date + timedelta(days=random.randint(0, 30))

    status = random.choices(
        statuses,
        weights=[55, 20, 20, 5],
    )[0]

    planned_days = random.randint(1, 3)
    actual_days = planned_days

    if status == "Late":
        actual_days += random.randint(1, 4)

    delivery_date = shipment_date + timedelta(days=actual_days)

    cost = random.choice([
        450,
        600,
        750,
        850,
        950,
        1200,
        1500,
        1800,
    ])

    # Deliberately introduce different date formats.
    shipment_date_str = shipment_date.strftime(
        random.choice(date_formats)
    )

    delivery_date_str = delivery_date.strftime(
        random.choice(date_formats)
    )

    # Deliberately introduce inconsistent city names.
    origin = random.choice(city_variants[origin])
    destination = random.choice(city_variants[destination])

    # Deliberately introduce blank values.
    if random.random() < 0.04:
        customer = ""

    if random.random() < 0.04:
        delivery_date_str = ""

    if random.random() < 0.03:
        cost = ""

    row = {
        "shipment_id": shipment_id,
        "customer": customer,
        "origin": origin,
        "destination": destination,
        "shipment_date": shipment_date_str,
        "delivery_date": delivery_date_str,
        "status": status,
        "cost": cost,
    }

    rows.append(row)


# Deliberately create duplicates.
duplicates = random.sample(rows, 15)
rows.extend(duplicates)

random.shuffle(rows)


shipment_file = RAW_DIR / "shipments.csv"

with shipment_file.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "shipment_id",
            "customer",
            "origin",
            "destination",
            "shipment_date",
            "delivery_date",
            "status",
            "cost",
        ],
    )

    writer.writeheader()
    writer.writerows(rows)


# -----------------------------
# Fake invoices
# -----------------------------

invoice_data = [
    {
        "number": "INV-1001",
        "date": "2026-10-22",
        "customer": "Acme Ltd",
        "route": "Chennai → Kozhikode",
        "items": [
            ("Base delivery", 700),
            ("Fuel surcharge", 100),
            ("Handling", 50),
        ],
        "total": 850,
    },
    {
        "number": "INV-1002",
        "date": "23/10/2026",
        "customer": "FreshMart",
        "route": "Bangalore → Kochi",
        "items": [
            ("Base delivery", 1000),
            ("Fuel surcharge", 150),
            ("Handling", 50),
        ],
        "total": 1200,
    },
    {
        "number": "INV-1003",
        "date": "October 24, 2026",
        "customer": "John Traders",
        "route": "Mumbai → Hyderabad",
        "items": [
            ("Base delivery", 1300),
            ("Fuel surcharge", 200),
            ("Handling", 100),
        ],
        "total": 1600,
    },
    {
        "number": "INV-1004",
        "date": "2026-10-26",
        "customer": "GreenBasket",
        "route": "Kochi → Chennai",
        "items": [
            ("Base delivery", 850),
            ("Fuel surcharge", 100),
        ],
        "total": 950,
    },
    {
        "number": "INV-1005",
        "date": "27/10/2026",
        "customer": "Metro Foods",
        "route": "Kozhikode → Bangalore",
        "items": [
            ("Base delivery", 1100),
            ("Fuel surcharge", 150),
            ("Handling", 50),
        ],
        "total": 1300,
    },
]


def create_invoice(invoice):
    lines = [
        "SWIFTROUTE LOGISTICS",
        "====================",
        "",
        f"Invoice Number: {invoice['number']}",
        f"Invoice Date: {invoice['date']}",
        "",
        f"Customer: {invoice['customer']}",
        f"Route: {invoice['route']}",
        "",
        "LINE ITEMS",
        "----------",
    ]

    for name, amount in invoice["items"]:
        lines.append(f"{name}: Rs {amount}")

    lines.extend([
        "",
        f"TOTAL: Rs {invoice['total']}",
    ])

    return "\n".join(lines)


# We create text-based .pdf files for now.
# Day 4 will deal with extracting structured information
# from documents.

for invoice in invoice_data:
    invoice_path = INVOICE_DIR / f"{invoice['number']}.pdf"

    invoice_path.write_text(
        create_invoice(invoice),
        encoding="utf-8",
    )


# -----------------------------
# Support emails
# -----------------------------

complaints = [
    "The shipment arrived two days late and caused us to miss our customer's delivery window.",
    "Our package was delayed because the truck reached the warehouse late.",
    "The driver could not reach the delivery address and the shipment was returned.",
    "The package arrived damaged.",
    "We were expecting delivery yesterday but it still has not arrived.",
    "Traffic caused a major delay on this route.",
    "The shipment was delayed because of heavy rain.",
    "The delivery address was incorrect in the system.",
    "Our customer says the package arrived with damaged packaging.",
    "The warehouse took too long to process the shipment.",
]

subjects = [
    "Late delivery",
    "Shipment delayed",
    "Damaged package",
    "Delivery issue",
    "Missing shipment",
    "Warehouse delay",
]

emails = []

for i in range(1, 31):
    customer = random.choice(customers)
    origin = random.choice(cities)
    destination = random.choice([c for c in cities if c != origin])

    email_date = start_date + timedelta(days=random.randint(0, 30))

    emails.append({
        "email_id": f"EMAIL-{i:03d}",
        "date": email_date.strftime("%Y-%m-%d"),
        "customer": customer,
        "subject": random.choice(subjects),
        "route": f"{origin} → {destination}",
        "body": random.choice(complaints),
    })


support_file = SUPPORT_DIR / "support_emails.json"

with support_file.open("w", encoding="utf-8") as f:
    json.dump(
        emails,
        f,
        indent=2,
        ensure_ascii=False,
    )


print("Day 1 data generation complete.")
print()
print(f"Shipments: {shipment_file}")
print(f"Invoices:  {INVOICE_DIR}")
print(f"Emails:    {support_file}")
print()
print(f"Shipment rows generated: {len(rows)}")
print(f"Invoice files generated: {len(invoice_data)}")
print(f"Support emails generated: {len(emails)}")