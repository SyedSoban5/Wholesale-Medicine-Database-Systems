SELECT COUNT(*) AS Supplier_Count FROM Supplier;

SELECT COUNT(*) AS Customers_Count FROM Customers;

SELECT COUNT(*) AS Medicines_Count FROM Medicines;

SELECT COUNT(*) AS Orders_Count FROM Orders;

SELECT COUNT(*) AS OrderDetails_Count FROM OrderDetails;

SELECT COUNT(*) AS Inventory_Count FROM Inventory;

SELECT *
FROM Medicines
WHERE MedicineName IS NULL
   OR Price IS NULL;
   
   SELECT Orders.OrderID,
       Customers.PharmacyName,
       Orders.TotalAmount
FROM Orders
JOIN Customers
ON Orders.CustomerID = Customers.CustomerID;

SET SQL_SAFE_UPDATES = 0;

UPDATE Medicines
SET Price = Price + 100
WHERE Category = 'Tablet';

DELETE FROM Customers
WHERE CustomerID = 59
AND CustomerID NOT IN (
    SELECT CustomerID FROM Orders
);
