from flask import Flask, jsonify, render_template, request
import mysql.connector
import os
from datetime import datetime

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="wholesalemedicinedb",
	port=3307
    )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/stats")
def stats():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) as total FROM customers")
    total_customers = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as total FROM medicines")
    total_medicines = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as total FROM orders")
    total_orders = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as total FROM supplier")
    total_suppliers = cursor.fetchone()["total"]

    cursor.execute("SELECT SUM(TotalAmount) as total FROM orders")
    total_revenue = cursor.fetchone()["total"] or 0

    cursor.execute("SELECT COUNT(*) as total FROM inventory WHERE StockQuantity <= MinimumStockLevel")
    low_stock = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as total FROM medicines WHERE ExpiryDate < NOW()")
    expired = cursor.fetchone()["total"]

    cursor.execute("SELECT AVG(TotalAmount) as avg FROM orders")
    avg_order = cursor.fetchone()["avg"] or 0

    cursor.close()
    db.close()

    return jsonify({
        "total_customers": total_customers,
        "total_medicines": total_medicines,
        "total_orders": total_orders,
        "total_suppliers": total_suppliers,
        "total_revenue": round(float(total_revenue), 2),
        "low_stock_count": low_stock,
        "expired_count": expired,
        "avg_order_value": round(float(avg_order), 2),
    })

@app.route("/api/medicines")
def get_medicines():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    page = int(request.args.get("page", 1))
    per_page = 15
    search = request.args.get("search", "")
    cat = request.args.get("category", "")
    offset = (page - 1) * per_page

    where = "WHERE 1=1"
    params = []

    if search:
        where += " AND (m.MedicineName LIKE %s OR m.Brand LIKE %s)"
        params.extend([f"%{search}%", f"%{search}%"])
    if cat:
        where += " AND m.Category = %s"
        params.append(cat)

    cursor.execute(f"SELECT COUNT(*) as total FROM medicines m {where}", params)
    total = cursor.fetchone()["total"]

    query = f"""
        SELECT m.*, s.SupplierName, i.StockQuantity, i.MinimumStockLevel
        FROM medicines m
        LEFT JOIN supplier s ON m.SupplierID = s.SupplierID
        LEFT JOIN inventory i ON m.MedicineID = i.MedicineID
        {where}
        LIMIT %s OFFSET %s
    """
    params.extend([per_page, offset])
    cursor.execute(query, params)
    data = cursor.fetchall()

    for row in data:
        if row.get("ExpiryDate"):
            row["ExpiryDate"] = str(row["ExpiryDate"])

    cursor.close()
    db.close()

    return jsonify({"total": total, "page": page, "per_page": per_page, "data": data})

@app.route("/api/medicines/categories")
def medicine_categories():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT DISTINCT Category FROM medicines WHERE Category IS NOT NULL ORDER BY Category")
    cats = [row[0] for row in cursor.fetchall()]
    cursor.close()
    db.close()
    return jsonify(cats)

@app.route("/api/customers")
def get_customers():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    page = int(request.args.get("page", 1))
    per_page = 15
    search = request.args.get("search", "")
    offset = (page - 1) * per_page

    where = "WHERE 1=1"
    params = []

    if search:
        where += " AND (c.PharmacyName LIKE %s OR c.OwnerName LIKE %s)"
        params.extend([f"%{search}%", f"%{search}%"])

    cursor.execute(f"SELECT COUNT(*) as total FROM customers c {where}", params)
    total = cursor.fetchone()["total"]

    query = f"""
        SELECT c.*, 
               COUNT(o.OrderID) as order_count,
               COALESCE(SUM(o.TotalAmount), 0) as total_spent
        FROM customers c
        LEFT JOIN orders o ON c.CustomerID = o.CustomerID
        {where}
        GROUP BY c.CustomerID
        LIMIT %s OFFSET %s
    """
    params.extend([per_page, offset])
    cursor.execute(query, params)
    data = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify({"total": total, "page": page, "per_page": per_page, "data": data})

@app.route("/api/orders")
def get_orders():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    page = int(request.args.get("page", 1))
    per_page = 15
    search = request.args.get("search", "")
    offset = (page - 1) * per_page

    where = "WHERE 1=1"
    params = []

    if search:
        where += " AND c.PharmacyName LIKE %s"
        params.append(f"%{search}%")

    cursor.execute(f"""
        SELECT COUNT(*) as total FROM orders o
        LEFT JOIN customers c ON o.CustomerID = c.CustomerID
        {where}
    """, params)
    total = cursor.fetchone()["total"]

    query = f"""
        SELECT o.*, c.PharmacyName,
               COUNT(od.MedicineID) as item_count
        FROM orders o
        LEFT JOIN customers c ON o.CustomerID = c.CustomerID
        LEFT JOIN orderdetails od ON o.OrderID = od.OrderID
        {where}
        GROUP BY o.OrderID
        ORDER BY o.OrderID DESC
        LIMIT %s OFFSET %s
    """
    params.extend([per_page, offset])
    cursor.execute(query, params)
    data = cursor.fetchall()

    for row in data:
        if row.get("OrderDate"):
            row["OrderDate"] = str(row["OrderDate"])

    cursor.close()
    db.close()

    return jsonify({"total": total, "page": page, "per_page": per_page, "data": data})

@app.route("/api/inventory")
def get_inventory():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    filter_status = request.args.get("status", "")

    query = """
        SELECT i.*, m.MedicineName, m.Brand, m.Category, m.Price, m.ExpiryDate,
               CASE
                   WHEN i.StockQuantity <= i.MinimumStockLevel THEN 'critical'
                   WHEN i.StockQuantity <= i.MinimumStockLevel * 1.5 THEN 'low'
                   ELSE 'ok'
               END as status
        FROM inventory i
        LEFT JOIN medicines m ON i.MedicineID = m.MedicineID
    """

    cursor.execute(query)
    data = cursor.fetchall()

    if filter_status:
        data = [row for row in data if row["status"] == filter_status]

    for row in data:
        if row.get("ExpiryDate"):
            row["ExpiryDate"] = str(row["ExpiryDate"])

    cursor.close()
    db.close()

    return jsonify(data)

@app.route("/api/suppliers")
def get_suppliers():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT s.*, COUNT(m.MedicineID) as medicine_count
        FROM supplier s
        LEFT JOIN medicines m ON s.SupplierID = m.SupplierID
        GROUP BY s.SupplierID
    """
    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(data)

@app.route("/api/revenue_trend")
def revenue_trend():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT DATE_FORMAT(OrderDate, '%Y-%m') as month,
               SUM(TotalAmount) as TotalAmount
        FROM orders
        GROUP BY month
        ORDER BY month
    """)
    data = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(data)

@app.route("/api/category_breakdown")
def category_breakdown():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT m.Category,
               COUNT(m.MedicineID) as count,
               SUM(i.StockQuantity) as stock
        FROM medicines m
        LEFT JOIN inventory i ON m.MedicineID = i.MedicineID
        WHERE m.Category IS NOT NULL
        GROUP BY m.Category
    """)
    data = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=5050)
