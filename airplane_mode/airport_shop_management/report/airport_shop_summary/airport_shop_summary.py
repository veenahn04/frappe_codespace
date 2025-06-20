# Copyright (c) 2025, Karthik and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = [
        {"label": ("Airport"), "fieldname": "airport", "fieldtype": "Link", "options": "Airport", "width": 200},
        {"label": ("Total Shops"), "fieldname": "total", "fieldtype": "Int", "width": 120},
        {"label": ("Occupied Shops"), "fieldname": "occupied", "fieldtype": "Int", "width": 150},
        {"label": ("Available Shops"), "fieldname": "available", "fieldtype": "Int", "width": 150},
    ]

    data = frappe.db.sql("""
        SELECT
            airport,
            COUNT(name) AS total,
            SUM(CASE WHEN is_occupied = 1 THEN 1 ELSE 0 END) AS occupied,
            SUM(CASE WHEN is_occupied = 0 THEN 1 ELSE 0 END) AS available
        FROM `tabAirport Shop`
        GROUP BY airport
        ORDER BY airport
    """, as_dict=True)

    chart = {
        "data": {
            "labels": [row.airport for row in data],
            "datasets": [
                {
                    "name": "Available Shops",
                    "values": [row.available for row in data]
                },
                {
                    "name": "Occupied Shops",
                    "values": [row.occupied for row in data]
                }
            ]
        },
        "type": "pie",
        "colors": ["#34d399", "#6366f1"]  # green & blue
    }

    return columns, data, None, chart