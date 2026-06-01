# 💊 Wholesale Medicine Database System

A complete **Database Management System (DBMS)** project developed for a real-world wholesale medicine business. This project focuses on medicine inventory management, supplier tracking, customer order processing, and database design using normalization principles and SQL implementation.

---

## 📌 Project Overview

The Wholesale Medicine Database System is designed to manage daily operations of a medicine wholesale business efficiently. The system stores and manages information related to medicines, suppliers, inventory, customers, and orders while maintaining data integrity through proper normalization and relational database design.

This project was developed as part of the Database Systems course and follows all required milestones including ERD design, normalization, dataset generation, DDL implementation, DML operations, and validation testing.

---

## 🎯 Objectives

- Manage medicine inventory efficiently
- Track supplier information
- Maintain customer records
- Process medicine orders
- Reduce data redundancy through normalization
- Ensure data integrity using relational database concepts
- Generate meaningful reports and statistics

---

# 🏗️ Database Design

## Entities

### Supplier
Stores supplier information.

### Medicines
Stores medicine details including category, batch number, expiry date, and supplier.

### Inventory
Tracks stock quantity and minimum stock levels.

### Customer
Stores pharmacy/customer information.

### Orders
Stores order transactions.

### OrderDetails
Stores medicines included in each order.

---

# 📊 Entity Relationship Diagram (ERD)

The ERD diagram is available in the ERD folder.

```
ERD/
└── ERD_Diagram.png
```

---

# 🔑 Database Relationships

| Parent Table | Child Table | Relationship |
|-------------|------------|-------------|
| Supplier | Medicines | One-to-Many |
| Medicines | Inventory | One-to-One |
| Customer | Orders | One-to-Many |
| Orders | OrderDetails | One-to-Many |
| Medicines | OrderDetails | One-to-Many |

---

# ✅ Normalization

The database schema has been normalized up to Third Normal Form (3NF).

### First Normal Form (1NF)
- Removed repeating groups
- Ensured atomic attributes
- Eliminated multi-valued fields

### Second Normal Form (2NF)
- Removed partial dependencies
- Separated attributes dependent on only part of a composite key

### Third Normal Form (3NF)
- Removed transitive dependencies
- Ensured non-key attributes depend only on the primary key

Detailed normalization documentation is available in:

```
Documentation/NORMALIZATION.md
```

---

# 📁 Synthetic Dataset

Synthetic data was generated to populate all core tables.

### Dataset Tables

| Table | Rows |
|---------|---------|
| Suppliers | 50+ |
| Medicines | 60+ |
| Customers | 60+ |
| Orders | 100+ |
| OrderDetails | 100+ |
| Inventory | 60+ |

CSV files are available in:

```
CSV/
```

---

# 🔄 Data Flow

### Input Sources
- Supplier Information
- Medicine Records
- Customer Records
- Order Transactions

### Processing
- Inventory Updates
- Order Processing
- Stock Monitoring
- Revenue Calculation

### Outputs
- Inventory Reports
- Customer Purchase Records
- Supplier Statistics
- Revenue Analysis

Detailed documentation:

```
Documentation/DATAFLOW.md
```

---

# 🗄️ Database Implementation

## DDL Scripts

Contains all CREATE TABLE statements including:

- Primary Keys
- Foreign Keys
- Constraints
- Indexes

Location:

```
SQL/schema.sql
```

---

## DML Scripts

Contains:

- INSERT Queries
- UPDATE Queries
- DELETE Queries
- Validation Queries

Location:

```
SQL/dml_queries.sql
```

---

# ✔ Validation Performed

The following validation checks were executed:

### Row Count Verification

```sql
SELECT COUNT(*) FROM Supplier;
SELECT COUNT(*) FROM Medicines;
SELECT COUNT(*) FROM Customer;
SELECT COUNT(*) FROM Orders;
SELECT COUNT(*) FROM OrderDetails;
SELECT COUNT(*) FROM Inventory;
```

### NULL Checks

```sql
SELECT * FROM Medicines
WHERE MedicineName IS NULL;
```

### Foreign Key Integrity Checks

```sql
SELECT *
FROM Orders o
JOIN Customer c
ON o.CustomerID = c.CustomerID;
```

---

# 🖥️ Frontend Dashboard

A Flask-based dashboard was developed to visualize database records.

### Features

- Dashboard Overview
- Revenue Analytics
- Medicine Management
- Inventory Monitoring
- Customer Directory
- Order Tracking
- Supplier Management
- Search & Filtering
- Interactive Charts

Frontend files are available in:

```
Frontend/
```

---

# 🛠️ Technologies Used

- MySQL
- MySQL Workbench
- Draw.io
- SQL
- Python
- Flask
- Pandas
- HTML
- CSS
- JavaScript
- Chart.js
- GitHub

---

# 📂 Repository Structure

```text
Wholesale-Medicine-Database-System
│
├── ERD
├── Documentation
├── CSV
├── SQL
├── Frontend
└── README.md
```

---

# 👥 Contributors

### Database Design & Documentation
**Syed Soban Ahmed Shah**

- ERD Design
- Relational Schema
- Normalization
- Dataset Preparation
- DDL & DML Scripts
- Documentation
- GitHub Repository Management

### Frontend Development
**Project Collaborator**

- Flask Application
- Dashboard Design
- API Integration
- Data Visualization

---

# 📚 Course Information

**Course:** Database Systems Lab

**Project Title:** Wholesale Medicine Database System

**Semester Project**

---

## ⭐ Project Status

✔ Milestone 1 Completed  
✔ Milestone 2 Completed  
✔ Milestone 3 Completed  
✔ Milestone 4 Completed  
✔ Milestone 5 Completed

---
