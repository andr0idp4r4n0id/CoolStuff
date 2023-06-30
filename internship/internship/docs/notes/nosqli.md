# NoSQL

## What is it?

It's a non relational database, created to manage massive collections of unstructured data. Instead of tables, it has collections.

There are 4 types of NoSQL databases:

---------------------------------------------------
1. **Key-Value Pair based**
2. **Column Oriented Graph**
3. **Graphs Based**
4. **Document Oriented**
---------------------------------------------------


1. Data is stored in key value pairs, it handles lots of data and a heavy load. Each key is unique, and is stored in a hash table, where the value can be JSON, BLOB, string..etc.  It is the most basic NoSQL databse example.
2. It's a dynamic schema, and are not fixed within the table. Each column is stored seperately, similiar columns are joined into column families. Each is stored separetely. Inside a column family there are rows, and inside those rows there are columns that don't need to adhere to a standard. There's also a Row-Key which identifies that row, it is always unique.
3. Just as the name implies, it is composed of nodes and edges. That gives relationship between nodes. They all have unique identifiers.
4. It stores values as key:value pairs but the value is a document in JSON or XML. It is understood by the db and can be queried.

##MongoDB

###SELECT

Select is used with the function find in MongoDB.

**Example**:

`db.inventory.find( { status: "D" } )`


There are operators you can use in these contexts, which, from an attacker perspective can do a lot of things.

**Attacker Perspective Example**

__bypass login__

`db.accounts.find({username: "admin", password: {$ne:null});)`

__code execution__

`db.collection.find({$where:function(){return(this.name == 'a'; sleep(10))}});`

