# Database Guide
## 1- Mysql Database
### Import connector

    import mysql.connector

### Connect to database

    mydb = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '19@mY%718',
        database = 'testdb',
    )
    
### Create an executer variable

    my_cursor = mydb.cursor()

### Create database

    my_cursor.execute("CREATE DATABASE fkdemo")
    
### Show database

    my_cursor.execute("SHOW DATABASES")

### Create a table

    my_cursor.execute("CREATE TABLE prices (symbol VARCHAR(255), "
                      "time VARCHAR(255), "
                      "close INTEGER(10), "
                      "high INTEGER(10), "
                      "low INTEGER(10), "
                      "open INTEGER(10), "
                      "value INTEGER,"
                      "id INTEGER AUTO_INCREMENT PRIMARY key) ")
    
### Show table

    my_cursor.execute("SHOW TABLES")
    

### Add a record

    sqlstuff = "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)"
    record1 = ("John", "john@codemy.com", 40)
    my_cursor.execute(sqlstuff, record1)
    mydb.commit()



### add multiple record

    sqlstuff = "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)"
    records = [
        ("tim", "tim@tim.com", 32),
        ("Mary", "Mary@mary.com", 21),
        ("Steve", "steve@steveEmail.com", 57),
        ("Tina", "tina@something", 29),]
    my_cursor.executemany(sqlstuff, records)
    mydb.commit()


### Select data

    my_cursor.execute("SELECT name FROM users")
    result = my_cursor.fetchall()

### Where clause

    my_cursor.execute("SELECT * FROM users WHERE name = 'john'")
    my_cursor.execute("SELECT * FROM users WHERE age >= 28")
    result = my_cursor.fetchall()


### Like clause and wildcard

    my_cursor.execute("SELECT * FROM users WHERE name LIKE'Ti%'")
   ti% means start with ti and something else in the rest
   
    my_cursor.execute("SELECT * FROM users WHERE name LIKE'%i%'")
   %i% means start with something and then have i and then something else in the rest or i in midlle
    
    result = my_cursor.fetchall()


### And and OR

    my_cursor.execute("SELECT * FROM users WHERE name LIKE'%i%' AND age = 29 AND user_id = 5")
    result = my_cursor.fetchall()


### Updating records

    my_sql = "UPDATE users SET age = 41 WHERE user_id = 2"
   don't use nonunique items like name ....
   
    my_cursor.execute(my_sql)
    mydb.commit()
    

### Limit and ordering

    my_cursor.execute("SELECT * FROM users LIMIT 3")
   top 3
   
    my_cursor.execute("SELECT * FROM users LIMIT 3 OFFSET 1")
   skip first
   
    my_cursor.execute("SELECT * FROM users ORDER BY user_id DESC")
   ASC and DESC
    
    result = my_cursor.fetchall()


### Delete records

    my_sql = "DELETE FROM users WHERE user_id = 6"
    my_cursor.execute(my_sql)
    mydb.commit()


### Delete table

   back up from workbench then delete
   
    my_sql = "DROP TABLE IF EXISTS users"
    my_cursor.execute(my_sql)



