from flask import Flask, jsonify, render_template, request
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
DATA = os.path.join(os.path.dirname(__file__), "static", "data")

def load_data():
    customers = pd.read_csv(f"{DATA}/customers.csv")
    medicines = pd.read_csv(f"{DATA}/medicines.csv")
    inventory = pd.read_csv(f"{DATA}/inventory.csv")
    orders = pd.read_csv(f"{DATA}/orders.csv")
    order_details = pd.read_csv(f"{DATA}/order_details.csv")
    suppliers = pd.read_csv(f"{DATA}/suppliers.csv")
    return customers, medicines, inventory, orders, order_details, suppliers

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/stats")
def stats():
    customers, medicines, inventory, orders, order_details, suppliers = load_data()
    total_revenue = orders["TotalAmount"].sum()
    low_stock = inventory[inventory["StockQuantity"] <= inventory["MinimumStockLevel"]]
    medicines["ExpiryDate"] = pd.to_datetime(medicines["ExpiryDate"], errors="coerce")
    expired = medicines[medicines["ExpiryDate"] < pd.Timestamp.now()]
    return jsonify({
        "total_customers": int(len(customers)),
        "total_medicines": int(len(medicines)),
        "total_orders": int(len(orders)),
        "total_suppliers": int(len(suppliers)),
        "total_revenue": round(float(total_revenue), 2),
        "low_stock_count": int(len(low_stock)),
        "expired_count": int(len(expired)),
        "avg_order_value": round(float(orders["TotalAmount"].mean()), 2),
    })

@app.route("/api/medicines")
def get_medicines():
    _, medicines, inventory, _, _, suppliers = load_data()
    merged = medicines.merge(suppliers[["SupplierID","SupplierName"]], on="SupplierID", how="left")
    merged = merged.merge(inventory[["MedicineID","StockQuantity","MinimumStockLevel"]], on="MedicineID", how="left")
    merged["ExpiryDate"] = pd.to_datetime(merged["ExpiryDate"], errors="coerce")
    merged["ExpiryDate"] = merged["ExpiryDate"].dt.strftime("%Y-%m-%d")
    page = int(request.args.get("page", 1))
    per_page = 15
    search = request.args.get("search", "").lower()
    cat = request.args.get("category", "")
    if search:
        merged = merged[merged["MedicineName"].str.lower().str.contains(search, na=False) |
                        merged["Brand"].str.lower().str.contains(search, na=False)]
    if cat:
        merged = merged[merged["Category"] == cat]
    total = len(merged)
    subset = merged.iloc[(page-1)*per_page : page*per_page]
    return jsonify({"total": total, "page": page, "per_page": per_page,
                    "data": subset.fillna("").to_dict(orient="records")})

@app.route("/api/medicines/categories")
def medicine_categories():
    _, medicines, _, _, _, _ = load_data()
    cats = medicines["Category"].dropna().unique().tolist()
    # Filter to clean categories only
    clean = [c for c in cats if len(c) < 30 and not any(x in c for x in ['"', "'"])]
    return jsonify(sorted(clean))

@app.route("/api/customers")
def get_customers():
    customers, _, _, orders, _, _ = load_data()
    order_counts = orders.groupby("CustomerID").agg(
        order_count=("OrderID","count"),
        total_spent=("TotalAmount","sum")
    ).reset_index()
    merged = customers.merge(order_counts, on="CustomerID", how="left")
    merged["order_count"] = merged["order_count"].fillna(0).astype(int)
    merged["total_spent"] = merged["total_spent"].fillna(0).round(2)
    page = int(request.args.get("page", 1))
    per_page = 15
    search = request.args.get("search", "").lower()
    if search:
        merged = merged[merged["PharmacyName"].str.lower().str.contains(search, na=False) |
                        merged["OwnerName"].str.lower().str.contains(search, na=False)]
    total = len(merged)
    subset = merged.iloc[(page-1)*per_page : page*per_page]
    return jsonify({"total": total, "page": page, "per_page": per_page,
                    "data": subset.fillna("").to_dict(orient="records")})

@app.route("/api/orders")
def get_orders():
    customers, _, _, orders, order_details, _ = load_data()
    detail_counts = order_details.groupby("OrderID").agg(item_count=("MedicineID","count")).reset_index()
    merged = orders.merge(customers[["CustomerID","PharmacyName"]], on="CustomerID", how="left")
    merged = merged.merge(detail_counts, on="OrderID", how="left")
    merged["item_count"] = merged["item_count"].fillna(0).astype(int)
    merged["OrderDate"] = pd.to_datetime(merged["OrderDate"], errors="coerce")
    merged["OrderDate"] = merged["OrderDate"].dt.strftime("%Y-%m-%d")
    page = int(request.args.get("page", 1))
    per_page = 15
    search = request.args.get("search", "").lower()
    if search:
        merged = merged[merged["PharmacyName"].str.lower().str.contains(search, na=False)]
    total = len(merged)
    merged = merged.sort_values("OrderID", ascending=False)
    subset = merged.iloc[(page-1)*per_page : page*per_page]
    return jsonify({"total": total, "page": page, "per_page": per_page,
                    "data": subset.fillna("").to_dict(orient="records")})

@app.route("/api/inventory")
def get_inventory():
    _, medicines, inventory, _, _, _ = load_data()
    merged = inventory.merge(medicines[["MedicineID","MedicineName","Brand","Category","Price","ExpiryDate"]], on="MedicineID", how="left")
    merged["status"] = merged.apply(
        lambda r: "critical" if r["StockQuantity"] <= r["MinimumStockLevel"] else
                  ("low" if r["StockQuantity"] <= r["MinimumStockLevel"] * 1.5 else "ok"), axis=1)
    merged["ExpiryDate"] = pd.to_datetime(merged["ExpiryDate"], errors="coerce").dt.strftime("%Y-%m-%d")
    filter_status = request.args.get("status", "")
    if filter_status:
        merged = merged[merged["status"] == filter_status]
    return jsonify(merged.fillna("").to_dict(orient="records"))

@app.route("/api/suppliers")
def get_suppliers():
    _, medicines, _, _, _, suppliers = load_data()
    med_counts = medicines.groupby("SupplierID").size().reset_index(name="medicine_count")
    merged = suppliers.merge(med_counts, on="SupplierID", how="left")
    merged["medicine_count"] = merged["medicine_count"].fillna(0).astype(int)
    return jsonify(merged.fillna("").to_dict(orient="records"))

@app.route("/api/revenue_trend")
def revenue_trend():
    _, _, _, orders, _, _ = load_data()
    orders["OrderDate"] = pd.to_datetime(orders["OrderDate"], errors="coerce")
    orders["month"] = orders["OrderDate"].dt.to_period("M").astype(str)
    trend = orders.groupby("month")["TotalAmount"].sum().reset_index()
    trend = trend.sort_values("month")
    return jsonify(trend.to_dict(orient="records"))

@app.route("/api/category_breakdown")
def category_breakdown():
    _, medicines, inventory, _, order_details, _ = load_data()
    merged = medicines.merge(inventory[["MedicineID","StockQuantity"]], on="MedicineID", how="left")
    merged["Category"] = merged["Category"].apply(lambda c: c if isinstance(c,str) and len(c)<20 and '"' not in c else "Other")
    breakdown = merged.groupby("Category").agg(count=("MedicineID","count"), stock=("StockQuantity","sum")).reset_index()
    return jsonify(breakdown.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True, port=5050)
