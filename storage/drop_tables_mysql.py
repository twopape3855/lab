import mysql.connector

db_conn = mysql.connector.connect(host="acit3855-sba-microservices-vm-cameron-woolfries.eastus2.cloudapp.azure.com", user='events', password='password', database="events")

db_cursor = db_conn.cursor()

db_cursor.execute('''
                DROP TABLE incomes, shifts, users''')


db_conn.commit()
db_conn.close()