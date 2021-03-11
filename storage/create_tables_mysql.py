import mysql.connector


db_conn = mysql.connector.connect(host="acit3855-sba-microservices-vm-cameron-woolfries.eastus2.cloudapp.azure.com", user='events', password='password', database="events")

db_cursor = db_conn.cursor()

db_cursor.execute('''CREATE TABLE users
                (id INT NOT NULL AUTO_INCREMENT,
                user_id VARCHAR(250) NOT NULL,
                user_name VARCHAR(250) NOT NULL,
                password VARCHAR(100) NOT NULL,
                date_created VARCHAR(100) NOT NULL,
                CONSTRAINT user_pk PRIMARY KEY (id))
                ''')

    
db_cursor.execute('''CREATE TABLE shifts
                (id INT NOT NULL AUTO_INCREMENT,
                shift_id VARCHAR(250) NOT NULL,
                shift_name VARCHAR(250) NOT NULL,
                start_time VARCHAR(100) NOT NULL,
                end_time VARCHAR(100) NOT NULL,
                date_created VARCHAR(100) NOT NULL,
                user_id INT NOT NULL,
                CONSTRAINT shift_pk PRIMARY KEY (id),
                CONSTRAINT user_shift_fk FOREIGN KEY (user_id)
                REFERENCES users(id))
                ''')


db_cursor.execute('''CREATE TABLE incomes
                (id INT NOT NULL AUTO_INCREMENT,
                income_id VARCHAR(250) NOT NULL,
                income_amount INT NOT NULL,
                date_created VARCHAR(100) NOT NULL,
                shift_id INT NOT NULL,
                CONSTRAINT shift_pk PRIMARY KEY (id),
                CONSTRAINT shift_income_fk FOREIGN KEY (shift_id)
                REFERENCES shifts(id))
                ''')


db_conn.commit()
db_conn.close()