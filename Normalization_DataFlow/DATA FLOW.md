Wholesale Medicine Database System — Dataflow Description
Introduction

The Wholesale Medicine Database System manages the flow of medicine-related business data from suppliers to customers through a structured relational database. The system stores, processes, and retrieves information related to medicines, suppliers, inventory, customer orders, and order details.

Data Entry Sources

Data enters the system through multiple entities involved in the wholesale medicine business.

1. Supplier Data

Supplier information is entered into the Supplier table. This includes:

Supplier Name
Contact Number
Address

Each supplier is assigned a unique SupplierID.

2. Medicine Data

Medicine details are stored in the Medicines table. Data includes:

Medicine Name
Brand
Category
Price
Expiry Date
Batch Number

Each medicine is linked to a supplier using SupplierID.

3. Customer Data

Customer information such as pharmacy names, owner names, phone numbers, and addresses is stored in the Customers table.

Each customer is uniquely identified using CustomerID.

4. Order Data

When a pharmacy places an order, the order information is inserted into the Orders table. The system stores:

Order Date
Total Amount
CustomerID
5. Order Details Data

The medicines included in each order are stored in the OrderDetails table. This table records:

Ordered medicine
Quantity
Price

This table acts as a bridge between Orders and Medicines.

6. Inventory Data

Stock information is maintained in the Inventory table. The system tracks:

Current stock quantity
Minimum stock level

Inventory helps monitor medicine availability and low-stock conditions.

Data Movement Through the Database

The system processes data through relationships between tables.

Suppliers provide medicines
Medicines are stored in inventory
Customers place orders
Orders contain multiple medicines through OrderDetails
Inventory is updated based on medicine availability

Foreign keys are used to maintain relationships and ensure data consistency throughout the system.

Output and Usage of Data

The database can generate useful outputs including:

Medicine stock reports
Supplier records
Customer order history
Low inventory alerts
Sales and order summaries
Expiry tracking reports

The processed data can also be used in future enhancements such as:

Sales analysis
Demand prediction
AI-based inventory forecasting
Conclusion

The dataflow of the Wholesale Medicine Database System ensures efficient movement of information between suppliers, inventory, and customers. The structured relational design improves data integrity, reduces redundancy, and supports smooth business operations.
