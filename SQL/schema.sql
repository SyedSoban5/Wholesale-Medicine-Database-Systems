CREATE DATABASE WholesaleMedicineDB;

USE WholesaleMedicineDB;


-- Supplier Table


CREATE TABLE Supplier (
    SupplierID INT PRIMARY KEY,
    SupplierName VARCHAR(100) NOT NULL,
    ContactNumber VARCHAR(20) NOT NULL UNIQUE,
    Address VARCHAR(255) NOT NULL
);


-- Medicines Table


CREATE TABLE Medicines (
    MedicineID INT PRIMARY KEY,
    MedicineName VARCHAR(100) NOT NULL,
    Brand VARCHAR(100) NOT NULL,
    Category VARCHAR(50) NOT NULL,
    Price DECIMAL(10,2) NOT NULL CHECK (Price > 0),
    ExpiryDate DATE NOT NULL,
    BatchNumber VARCHAR(50) NOT NULL UNIQUE,
    SupplierID INT NOT NULL,

    CONSTRAINT fk_supplier
        FOREIGN KEY (SupplierID)
        REFERENCES Supplier(SupplierID)
);

CREATE INDEX idx_supplierid
ON Medicines(SupplierID);


-- Customers Table


CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    PharmacyName VARCHAR(100) NOT NULL,
    OwnerName VARCHAR(100) NOT NULL,
    Phone VARCHAR(20) NOT NULL UNIQUE,
    Address VARCHAR(255) NOT NULL
);


-- Orders Table


CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT NOT NULL,
    OrderDate DATE NOT NULL,
    TotalAmount DECIMAL(10,2) NOT NULL CHECK (TotalAmount >= 0),

    CONSTRAINT fk_customer
        FOREIGN KEY (CustomerID)
        REFERENCES Customers(CustomerID)
);

CREATE INDEX idx_customerid
ON Orders(CustomerID);


-- OrderDetails Table


CREATE TABLE OrderDetails (
    OrderDetailID INT PRIMARY KEY,
    OrderID INT NOT NULL,
    MedicineID INT NOT NULL,
    Quantity INT NOT NULL CHECK (Quantity > 0),
    Price DECIMAL(10,2) NOT NULL CHECK (Price > 0),

    CONSTRAINT fk_order
        FOREIGN KEY (OrderID)
        REFERENCES Orders(OrderID),

    CONSTRAINT fk_medicine
        FOREIGN KEY (MedicineID)
        REFERENCES Medicines(MedicineID)
);

CREATE INDEX idx_orderid
ON OrderDetails(OrderID);

CREATE INDEX idx_medicineid
ON OrderDetails(MedicineID);


-- Inventory Table


CREATE TABLE Inventory (
    InventoryID INT PRIMARY KEY,
    MedicineID INT NOT NULL UNIQUE,
    StockQuantity INT NOT NULL CHECK (StockQuantity >= 0),
    MinimumStockLevel INT NOT NULL CHECK (MinimumStockLevel >= 0),

    CONSTRAINT fk_inventory_medicine
        FOREIGN KEY (MedicineID)
        REFERENCES Medicines(MedicineID)
);

CREATE INDEX idx_inventory_medicine
ON Inventory(MedicineID);
