import pymysql

print("Content-Type: text/html\n")
print("<html><head><title>products</title></hesd>")
print("<body>")
print("<h1>products</h1>")
print("<ul>")

connection = pymysql.connect(user='user', passwd='pwd', db='product_db')
cursor = connection.cursor()
cursor.execute("SELECT name FROM products OPDER BY create_date DESC LIMIT 10")

for row in cursor.fetchall():
    print("<li>%s</li>" % row[0])

print("</ul>")
print("<p>https://www.baidu.com</p>")

connection.close()
























