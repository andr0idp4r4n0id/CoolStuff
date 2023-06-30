# SQL - Structured Query Language

## Definition

It's a standard language for accessing and manipulating databases.

## RDBMS - Relational Database Management System

Data is stored in objects called `tables`. It's a collection of related data entries, it consists of `columns` and `rows`

A table is identifiable by its name

**Columns** is the vertical entity in the table.

**Rows** is the horizontal entity in the table.

## SQL Syntax

```
CustomerId		customerName
1				Júlio
2				Duarte
3				Pedro

```
This example has 3 rows and 2 columns.

##SQL Statements - SELECT

`SELECT * FROM Customers`

SELECT, as the name implies, selects from a database. The data returned is stored in the result table.

SELECT `customerId` FROM `Customers` - SELECT works on columns, FROM works on table name. Which means, by selecting a column, I'll also select all the rows of that column.

###First Exercise

Taking into account what I've learn't, the solution is simple. SELECT gets columns, so it's the keyword missing.

**SOLUTION**:

`SELECT`

###Second Exercise

To select columns is select, therefore to select the column City it's:

`SELECT City FROM`

##SQL Statements - DISTINCT 

`SELECT DISTINCT` removes duplicates. It only returns different values.

`SELECT DISTINCT column1, column2 FROM table_name`

##SQL Statements - WHERE

It filters rows. It extracts the records that fulfill a specified condition.

`SELECT column1, column2 FROM table_name WHERE condition`

**CAN ALSO BE USED IN UPDATE, DELETE, ETC.**

Where allows conditional operators of most of the typical language, but it also allows:

**BETWEEN** - Between a certain range

**LIKE** - Search for a pattern.

**IN** Specify multiple possible values for a column

###First Exercise

We need to use the where clause to filter. Logically speaking, this will SELECT all the rows but return only the rows which the City column has the value Berlin. (It will only select the rows that are the left of and right of the value city.

`WHERE City = 'Berlin'`

##SQL Statements - WHERE - OPERATORS.

It combines with `AND`, `OR`, `NOT`.

If all the conditions separated by AND are true, then the record/s are returned.
If one of the conditions separared by OR are true, then all the record/s are returned.
If the condition/s are not true the record/s are returned.


###Second Exercise.

We need to select where the city is not 'Berlin', meaning it will ignore all the rows that have the City column as 'Berlin'
We use the NOT operator.

`SELECT * FROM Customers WHERE NOT City = 'Berlin'`

###Third Exercise

We need to select where the customerID column has the value 32, it will only select the rows like that.

`SELECT * FROM Customers WHERE CustomerID = 32`

###Fourth Exercise.

We need to select rows with columns with value London or Berlin.

`SELECT * FROM Customers WHERE City = 'Berlin' OR City = 'London`


##SQL Statements - ORDER BY

Sorts the result-set (resulting table) in ascending or descending order.

Sorts in ascending order by default. Use DESC for descending

```
SELECT column1, column2, ...
FROM table_name
ORDER BY column1, column2, ... ASC|DESC

```

You can order multiple columns by separating them with a comma.

```
SELECT * FROM Customers
ORDER BY Country ASC, CustomerName DESC

```

###First Exercise

We need to sort on the City field, therefore:

`SELECT * FROM Customers ORDER BY City`

###Second Exercise

We need to sort on the City field in reverse order, therefore:

`SELECT * FROM Customers ORDER BY City DESC`

###Third Exercise

We need to sort on the Country field and then City field, therefore:

`SELECT * FROM Customers ORDER BY Country, City`

##SQL - Statements INSERT INTO

Inserts new records in a table.

```
INSERT INTO table_name (column1, column2, column3, ...)
VALUES (value1, value2, value3, ...)

```
or, if we add to all the table columns

```
INSERT INTO table_name
VALUES (value1, value2, value3, ...)
```

###First Exercise

```
INSERT INTO Customers(CustomerName, Address, City, PostalCode, Country) VALUES('Hekkan', 'Gatevein', 'Sandnes', '4306', 'Norway')

```

##SQL Statements - NULL.

We can only use IS NULL to test for NULL values or IS NOT NULL to test for NOT NULL Values

```
SELECT column_names
FROM table_name
WHERE column_name IS NULL

SELECT column_names
FROM table_name
WHERE column_name IS NOT NULL

```

###First Exercise

We need to test if its empty, that is, null, therefore:

`SELECT * FROM Customers WHERE PostalCode IS NULL`

###Second Exercise

We need to test if its not empty, that is, NOT NULL, therefore:

`SELECT * FROM Customers WHERE PostalCode IS NOT NULL`

##SQL Statement - UPDATE

The update statement modifies existing records in a table.

```
UPDATE table_name
SET column1 = value1, column2 = value2, ...
WHERE condition

```

It's important to use the WHERE clause. if you don't, all records will be changed.
It decides how many records are to be updated.

```
UPDATE Customers
SET ContactName='Juan'

```

###First Exercise

We need to update all records of the city column in the customer table, as such:

`UPDATE Customers SET City = 'Oslo'`

###Second Exercise

We need to update all the records of the city column in the customer table where the country is 'Norway', therefore:

`UPDATE Customers SET City = 'Oslo' WHERE Country = 'Norway'`

###Third Exercise

We need to update the City value and Country value, as such:

`UPDATE Customers SET City = 'Oslo', Country = 'Norway' WHERE CustomerID=32`

##SQL Statement - DELETE

Deletes existing records in a table.

`DELETE FROM table_name WHERE condition`

**Be careful when deleting records in a table! Notice the WHERE clause in the DELETE statement. The WHERE clause specifies which record(s) should be deleted. If you omit the WHERE clause, all records in the table will be deleted**

###First Exercise

We need to delete the column Country with row value 'Norway'. As such:

`DELETE FROM Customers WHERE Country = 'Norway'`

###Second Exercise

We need to delete all the records from the Customer table.

`DELETE FROM Customers`

##SQL Statements - Functions

It does operations on the selected column values.

**MIN** Returns the smallest value of the selected column

**MAX** Returns the biggest value of the selected column

```
SELECT MIN/MAX(column_name)
FROM table_name
WHERE condition
```
###First Exercise

We need to select the min value from the column Price:

`SELECT MIN(Price) FROM Products`

###Second Exercise

The max value:

`SELECT MAX(Price) FROM Products`

###Third Exercise

Number of records:

`SELECT COUNT(*) FROM Customers WHERE Price = 18`

###Fourth Exercise

We need to select a function that calculates the average price of all products.

`SELECT AVG(Price) FROM Products`

###Fith Exercise

We need to select a function that calculates the sum of product's price's.

`SELECT SUM(Price) FROM Products`

##SQL Statement - LIKE

The LIKE operator searches a where caluse for a pattern

**MS Access uses an asterisk (*) instead of the percent sign (%), and a question mark (?) instead of the underscore (_).**

```
SELECT column1, column2, ...
FROM table_name
WHERE columnN LIKE pattern
```
```
WHERE CustomerName LIKE 'a%' 	Finds any values that start with "a"
WHERE CustomerName LIKE '%a' 	Finds any values that end with "a"
WHERE CustomerName LIKE '%or%' 	Finds any values that have "or" in any position
WHERE CustomerName LIKE '_r%' 	Finds any values that have "r" in the second position
WHERE CustomerName LIKE 'a_%' 	Finds any values that start with "a" and are at least 2 characters in length
WHERE CustomerName LIKE 'a__%' 	Finds any values that start with "a" and are at least 3 characters in length
WHERE ContactName LIKE 'a%o' 	Finds any values that start with "a" and ends with "o"

```
###First Exercise

Has to start with letter a, therefore:

`SELECT * FROM Customers WHERE City LIKE 'a%'`

###Second Exercise

Has to end with letter a, therefore:

`SELECT * FROM Customers WHERE City LIKE '%a'`

###Third Exercise

Has to contain the letter a, therefore:

`SELECT * FROM Customers WHERE City LIKE '%a%'`

###Fourth Exercise

Has to start with a, end with b:

`SELECT * FROM Customers WHERE City LIKE 'a%b'`

###Fith Exercise

Can't start with letter a, therefore:

`SELECT * FROM Customers WHERE City NOT LIKE 'a%'`

##SQL Statements - Wildcards

**MS Access**

```

* 	Represents zero or more characters 	bl* finds bl, black, blue, and blob
? 	Represents a single character 	h?t finds hot, hat, and hit
[] 	Represents any single character within the brackets 	h[oa]t finds hot and hat, but not hit
! 	Represents any character not in the brackets 	h[!oa]t finds hit, but not hot and hat
- 	Represents any single character within the specified range 	c[a-b]t finds cat and cbt
# 	Represents any single numeric character 	2#5 finds 205, 215, 225, 235, 245, 255, 265, 275, 285, and 295

```

**SQL Server**

```
% 	Represents zero or more characters 	bl% finds bl, black, blue, and blob
_ 	Represents a single character 	h_t finds hot, hat, and hit
[] 	Represents any single character within the brackets 	h[oa]t finds hot and hat, but not hit
^ 	Represents any character not in the brackets 	h[^oa]t finds hit, but not hot and hat
- 	Represents any single character within the specified range 	c[a-b]t finds cat and cbt

```

###First Exercise

Find where city's second letter is a:

`SELECT * FROM Customers WHERE City LIKE '_a%'`

###Second Exercise

Find where city's first letter is a or c or s:

`SELECT * FROM Customers WHERE City LIKE '[acs]%'`

###Third Exercise

Starts with a to f:

`SELECT * FROM Customers WHERE City LIKE '[a-f]%'`

###Fourth Exercise

Doesn't start with acf.

`SELECT * FROM Customers WHERE City LIKE '[!acf]%'`

##SQL Statement  - IN Operator

Allows to specify multiple values in a WHERE clause

```
SELECT column_name(s)
FROM table_name
WHERE column_name IN (value1, value2, ...)

```
###First Exercise

All the records where Country is either Norway or France

`SELECT * FROM Customers WHERE Country IN('Norway','France')`

###Second Exercise

All the records where country is not Norway and France

`SELECT * FROM Customers WHERE Country NOT IN('Norway','France')`

###SQL Statement - Between

Allows to select records within a given range.

```
SELECT column_name(s)
FROM table_name
WHERE column_name BETWEEN value1 AND value2

```

###First Exercise

Select between 10 and 20.

`SELECT * FROM Products WHERE Price BETWEEN 10 AND 20`

###Second Exercise

Select not between 10 and 20

`SELECT * FROM Products WHERE Price NOT BETWEEN 10 AND 20`

###Third Exercise

Select between two words aphabetically

`SELECT * FROM Products WHERE ProductName BETWEEN 'Geitost' AND 'Pavlova'`

##SQL  Statement - Aliases

They give a table or column a temporary name.

```
SELECT column_name AS alias_name
FROM table_name

```

```
SELECT column_name(s)
FROM table_name AS alias_name

```

##SQL Statement - JOINS

(INNER) JOIN - Returns records whose values match in both tables, that is, they exist in both tables.
LEFT (OUTER) JOIN - Returns all the records selected from the left table and records that exist in both from the right table.
RIGHT (OUTER) JOIN - Returns all the records selected from the right table and records that exist in both from the left table.
FULL (OUTER) JOIN - Returns all the selected records from both tables.

###First Exercise 

Insert the missing parts in the join clause, using customerID field in both tables as the relationship.

`SELECT * FROM Orders LEFT JOIN Customers ON Orders.CustomerID=Customers.CustomerID`

###Second Exercise

Pick the right type of join, to select all the records where there is a match on both tables.

`SELECT * FROM Orders INNER JOIN Customers ON Orders.CustomerID=Customers.CustomerID`

###Third Exercise

Pick the right type of join, to select all the records where there is a match and that exists in the right table

`SELECT * FROM Orders RIGHT JOIN Customers ON Orders.CustomerID=Customers.CustomerID`

##SQL Statement - Group BY

Groups the same value rows. So, if we have, for example, two columns, CustomerID and COUNT(CostumerName) and we group by customerID, we get all the unique customerID values with the count of each customerName associated with those customerID's.
We can group by more than one column:

```
Book_1 - Francisco - Romance - 12.40€
Book_2 - Diogo - Aventura - 13.40€
Book_3 - Diogo - Terror - 14.40€

SELECT Genre, MAX(Price), Author FROM Books GROUP BY Genre, Author

Terror - Diogo - 14.40€
Romance - Francisco - 12.40€

SELECT column_name(s)
FROM table_name
WHERE condition
GROUP BY column_name(s)
ORDER BY column_name(s)

```
###First Exercise

We need to list the number of customers in each country.

`SELECT COUNT(CusomterID), Country FROM Costumers GROUP BY Country`

###Second Exercise

List the number of customers in each country, ordered by the country with the most customers first.

`SELECT COUNT(CustomerID), Country FROM Customers GROUP BY Country ORDER BY Count(CustomerID) DESC`

