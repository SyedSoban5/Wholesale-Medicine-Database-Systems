Wholesale Medicine Database System — Normalization
First Normal Form (1NF)
Rule of 1NF

A table must:

Have atomic values
Have no repeating groups
Have unique rows
Supplier Table
Issue

No repeating groups or multivalued attributes were found.

Justification

Each supplier record contains atomic values such as SupplierName, ContactNumber, and Address. Every row is uniquely identified using SupplierID.

Result

The table already satisfies 1NF. No changes were required.

Medicines Table
Issue

The table already stores atomic values. Each medicine attribute contains only one value.

Justification

Attributes such as MedicineName, Brand, Category, and Price contain single values only. No repeating groups exist.

Result

The table satisfies 1NF without modification.

Customers Table
Issue

No multivalued or repeating attributes were present.

Justification

Each customer has unique and atomic details such as PharmacyName, OwnerName, and Phone.

Result

The table already satisfies 1NF.

Orders Table
Issue

The table contains atomic attributes only.

Justification

OrderDate and TotalAmount store single values for each order.

Result

The table satisfies 1NF.

OrderDetails Table
Issue

No repeating groups exist.

Justification

Each row stores one medicine entry per order using Quantity and Price attributes.

Result

The table already satisfies 1NF.

Inventory Table
Issue

No repeating groups or multivalued attributes were found.

Justification

StockQuantity and MinimumStockLevel contain atomic values.

Result

The table satisfies 1NF.

Second Normal Form (2NF)
Rule of 2NF

A table must:

Already be in 1NF
Have no partial dependency
Supplier Table
Issue

No partial dependency exists because the table uses a single-column primary key.

Justification

All attributes depend completely on SupplierID.

Result

The table satisfies 2NF.

Medicines Table
Issue

No partial dependency exists.

Justification

All medicine attributes depend entirely on MedicineID.

Result

The table already satisfies 2NF.

Customers Table
Issue

No partial dependency exists.

Justification

All customer attributes depend fully on CustomerID.

Result

The table satisfies 2NF.

Orders Table
Issue:

No partial dependency exists.

Justification:

All order attributes depend on OrderID.

Result:

The table satisfies 2NF.

OrderDetails Table
Issue:

Potential duplication between Orders and Medicines needed to be resolved.

Change Made:

A separate OrderDetails table was created to manage the many-to-many relationship between Orders and Medicines.

Justification:

This prevents partial dependency and stores order-specific medicine data efficiently.

Result:

The table satisfies 2NF after normalization.

Inventory Table
Issue:

No partial dependency exists.

Justification:

All attributes depend fully on InventoryID.

Result:

The table satisfies 2NF.

Third Normal Form (3NF)
Rule of 3NF:

A table must:

Already be in 2NF
Have no transitive dependency
Supplier Table
Issue

No transitive dependency exists.

Justification

All non-key attributes depend only on SupplierID.

Result

The table satisfies 3NF.

Medicines Table
Issue

Supplier information was not duplicated inside the table.

Justification

Supplier details are stored separately in the Supplier table and linked using SupplierID.

Result

The table satisfies 3NF.

Customers Table
Issue

No transitive dependency exists.

Justification

All attributes depend directly on CustomerID.

Result

The table satisfies 3NF.

Orders Table
Issue

Customer information was separated from order information.

Justification

Customer details are stored in the Customers table and linked using CustomerID.

Result

The table satisfies 3NF.

OrderDetails Table
Issue

Medicine and order data were properly separated.

Justification

The table only stores relationship-specific attributes such as Quantity and Price.

Result

The table satisfies 3NF.

Inventory Table
Issue

No transitive dependency exists.

Justification

Inventory-related attributes depend directly on InventoryID.

Result

The table satisfies 3NF.

Duplicate Removal and Schema Improvements
Changes Performed
Removed duplication between Orders and Medicines using OrderDetails
Separated supplier information from Medicines
Separated customer information from Orders
Maintained inventory in a dedicated table
Result

The database structure became more efficient, consistent, and easier to maintain.

Final Normalized Tables
Supplier
Medicines
Customers
Orders
OrderDetails
Inventory

Duplicate Removal and Redundancy Check
Medicines Table
Issue Checked

Possible duplication of supplier information inside the Medicines table.

Action Taken:

Supplier details such as SupplierName and ContactNumber were removed from the Medicines table and stored separately in the Supplier table.

Reason:

This prevents repeated supplier data for every medicine record and improves consistency.

Orders Table
Issue Checked

Possible duplication of customer information inside Orders.

Action Taken:

Customer details were separated into the Customers table and linked using CustomerID.

Reason:

This avoids repeating customer data in every order.

OrderDetails Table
Issue Checked

Direct many-to-many relationship between Orders and Medicines.

Action Taken:

The OrderDetails table was created to handle the relationship.

Reason:

This prevents duplicate medicine records inside orders and maintains normalization.

Inventory Table
Issue Checked:

Stock information stored with medicine details.

Action Taken:

Inventory was maintained in a separate table.

Reason:

This improves maintainability and allows better inventory management.

Final Result:
The schema was reviewed for duplicate and redundant data. All unnecessary repetition was removed by separating entities into dedicated tables and using foreign key relationships.
