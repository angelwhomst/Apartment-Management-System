import sqlite3
import hashlib
from sqlite3 import Error


def get_db_connection():
    conn = sqlite3.connect('apartment_management_system_DB.db')
    return conn


def create_tables(conn):
    cursor = conn.cursor()

    # creates table for admin
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Admin (
    admin_id    INTEGER      PRIMARY KEY AUTOINCREMENT,
    admin_name  VARCHAR (50),
    admin_email VARCHAR (50),
    admin_phone CHAR (12),
    admin_role  VARCHAR (50),
    username    VARCHAR (50) NOT NULL,
    password    VARCHAR (50) NOT NULL
);
    ''')
    # creates table for apartment building
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Apartment_Building (
    building_id     INTEGER      PRIMARY KEY AUTOINCREMENT,
    admin_id        INTEGER,
    building_name   VARCHAR (50) NOT NULL
                               UNIQUE ON CONFLICT ROLLBACK,
    number_of_units INTEGER,
    amenities       TEXT,
    country         VARCHAR (50),
    province        VARCHAR (50),
    city            VARCHAR (50),
    street          VARCHAR (50),
    lot_number      VARCHAR (50),
    zip_code        VARCHAR (10),
    is_deleted      INTEGER      DEFAULT (0),
    FOREIGN KEY (
        admin_id
    )
    REFERENCES ADMIN (admin_id) 
);
    ''')
    # creates table for apartment unit
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Apartment_Unit (
    unit_id             INTEGER       PRIMARY KEY AUTOINCREMENT,
    building_id         INTEGER,
    admin_id            INTEGER,
    unit_number         VARCHAR (100) NOT NULL,
    num_bedrooms        INTEGER,
    num_bathrooms       INTEGER,
    unit_size_square_m  INTEGER,
    rental_rate         FLOAT,
    availability_status INTEGER       NOT NULL, -- 1='available', 2='occupied' 3='under maintenance'
    maintenance_request INTEGER       DEFAULT (0),
    is_deleted          INTEGER       DEFAULT (0),
    FOREIGN KEY (
        building_id
    )
    REFERENCES Apartment_building (building_id),
    FOREIGN KEY (
        admin_id
    )
    REFERENCES Admin (admin_id) 
);
    ''')
    # creates table for tenant
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Tenant (
    tenant_id                      INTEGER       PRIMARY KEY AUTOINCREMENT,
    admin_id                       INTEGER,
    lastName                       VARCHAR (50)  NOT NULL,
    firstName                      VARCHAR (50)  NOT NULL,
    middleName                     VARCHAR (50),
    suffix                         VARCHAR (50),
    email                          VARCHAR (50)  NOT NULL,
    contact_number                 CHAR (12),
    move_in_date                   DATE,
    lease_start_date               DATE,
    lease_end_date                 DATE,
    Emergency_contact_name         VARCHAR (50),
    Emergency_contact_number       CHAR (12),
    Emergency_contact_relationship VARCHAR (50),
    tenant_photo                   BLOB,
    tenant_dob                     DATE,
    sex                            INTEGER,
    nationality                    VARCHAR (100),
    income                         DOUBLE,
    FOREIGN KEY (
        admin_id
    )
    REFERENCES Admin (admin_id) 
);
    ''')
    # creates table for payment
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Payment (
    payment_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id      INTEGER,
    unit_id        INTEGER,
    amount         FLOAT   NOT NULL,
    payment_date   DATE    NOT NULL,
    payment_method INTEGER NOT NULL,
    FOREIGN KEY (
        tenant_id
    )
    REFERENCES Tenant (tenant_id),
    FOREIGN KEY (
        unit_id
    )
    REFERENCES Apartment_Unit (unit_id) 
);
    ''')
    # creates table for expenses
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Expenses (
    expense_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_id       INTEGER,
    expense_date   DATE    NOT NULL,
    expense_amount DOUBLE  NOT NULL,
    expense_type   INTEGER,
    description    TEXT,
    FOREIGN KEY (
        admin_id
    )
    REFERENCES Admin (admin_id) 
);
    ''')
    # creates table for report
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Report (
    report_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_id,
    start_date     DATE,
    end_date       DATE,
    report_comment TEXT,
    FOREIGN KEY (
        admin_id
    )
    REFERENCES Admin (admin_id) 
);
    ''')


# ============================================================


# needed function for the tables that need admin_id
def get_admin_id(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT admin_id FROM Admin LIMIT 1")
    result = cursor.fetchone()
    if result:
        admin_id = result[0]
        print(f'admin_id is {admin_id}')
        return admin_id
    else:
        print("No admin found in the database")  # debug statement
        return None


# ================ LOGIN PAGE FUNCTIONS =======================
def hash_password(password):  # hashes the password using SHA-256
    return hashlib.sha256(password.encode()).hexdigest()


def check_username_exists(conn, username):
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM Admin WHERE username = ?', (username,))
    result = cursor.fetchone()
    return result is not None


def insert_admin(conn, username, password):
    if check_username_exists(conn, username):
        print('username already exists')  # debug statement
        return

    hashed_password = hash_password(password)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Admin (username, password) VALUES (?, ?)",
                   (username, hashed_password))
    conn.commit()
    print('insert admin successful')  # debug statement
    return cursor.lastrowid  # return the ID of the inserted admin


# Function to verify admin login with hashed password
def verify_login(conn, username, password):
    hashed_password = hash_password(password)
    cursor = conn.cursor()
    cursor.execute("SELECT admin_id, username FROM Admin WHERE username = ? AND password = ?",
                   (username, hashed_password))
    row = cursor.fetchone()
    if row:
        return {'admin_id': row[0], 'username': row[1]}
    else:
        return None


# function to check if there are any apartment units in the database
# used for disabling the tenant view button
def check_apartment_units_exist(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Apartment_Unit")
    count = cursor.fetchone()[0]
    return count > 0


# ================ Add Building PAGE FUNCTIONS =======================

def check_building_exists(conn, building_name):
    cursor = conn.cursor()
    cursor.execute("SELECT building_id FROM Apartment_Building WHERE building_name = ?", (building_name,))
    if cursor.fetchone():
        return True  # building exists
    else:
        return False  # building does not exist


def insert_building(conn, building_name, country, province, city, street, lot_number, zip_code, amenities):
    admin_id = get_admin_id(conn)
    if not admin_id:
        return

    if check_building_exists(conn, building_name):
        return  # building already exists, so return without inserting

    try:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO Apartment_Building (admin_id, building_name, country, province, city, street, 
                       lot_number, zip_code, amenities)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);''', (admin_id, building_name, country, province, city,
                                                                 street, lot_number, zip_code, amenities))
        conn.commit()
    except Exception as e:
        print(f"Error adding apartment unit: {str(e)}")
        conn.rollback()


def fetch_latest_building_id(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT max(building_id) from apartment_building;')
    return cursor.fetchone()[0]


# ================ Display Building PAGE FUNCTIONS =======================
def fetch_new_building_info(conn, building_id):
    # fetch building information from the database based on building_id
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Apartment_Building WHERE building_id = ?", (building_id,))
    building_info = cursor.fetchone()  # one row is fetched
    return building_info


# ================ Edit Building PAGE FUNCTIONS =======================

def edit_last_inserted_building_id(conn, building_name, country, province, city, street, lot_number,
                                   zip_code, amenities):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            update Apartment_Building 
        set building_name = ?,
        building_name =?, 
        country =?,
        province= ?,
        city = ?,
        street = ?, 
        lot_number =?,
         zip_code = ?, 
         amenities = ?
        where last_insert_rowid();
            ''', (building_name, country, province, city, street, lot_number, zip_code, amenities))
        conn.commit()
    except Exception as e:
        print(str(e))


# ================ Add Unit PAGE FUNCTIONS =======================
def fetch_building_names(conn):  # function to populate combobox
    cursor = conn.cursor()
    cursor.execute('SELECT building_name FROM Apartment_Building')
    buildings = cursor.fetchall()
    return [building[0] for building in buildings]


# function to get the building id based on the building name chosen by the user
def get_building_id(conn, building_name):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT building_id FROM Apartment_Building WHERE building_name = ?", (building_name,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            print("Building not found.")
            return None
    except Exception as e:
        print(f"Error fetching building ID: {str(e)}")
        return None


def insert_unit(conn, building_id, unit_number, rental_rate, number_of_bedrooms, number_of_bathrooms, unit_size,
                maintenance_request, availability_status):
    admin_id = get_admin_id(conn)
    if not admin_id:
        return

    try:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO Apartment_Unit (admin_id, building_id, unit_number, rental_rate, num_bedrooms, 
                          num_bathrooms, unit_size_square_m, maintenance_request, availability_status)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                       (admin_id, building_id, unit_number, rental_rate, number_of_bedrooms, number_of_bathrooms,
                        unit_size,
                        maintenance_request, availability_status))
        conn.commit()
        print("Unit information saved successfully.")
    except Exception as e:
        print(f"Error saving unit information: {str(e)}")
        conn.rollback()


# ================ Display Unit PAGE FUNCTIONS =======================

def fetch_building_id_from_latest_unit(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT max(building_id) FROM apartment_unit;')
    return cursor.fetchone()[0]


def fetch_latest_unit_id(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT max(unit_id) FROM apartment_unit;')
    return cursor.fetchone()[0]


def fetch_building_id_by_name(conn, building_name):
    cursor = conn.cursor()
    cursor.execute("SELECT building_id FROM Apartment_Building WHERE building_name = ?", (building_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        print(f"No building found with the name {building_name}")
        return None


def fetch_new_unit_info(conn, unit_id):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT unit_id, building_id, unit_number, num_bedrooms, num_bathrooms,
               unit_size_square_m, rental_rate,
               CASE
                   WHEN availability_status = 1 THEN 'Available'
                   WHEN availability_status = 2 THEN 'Occupied'
                   WHEN availability_status = 3 THEN 'Under Maintenance'
                   ELSE 'Unknown'
               END AS availability_status,
               maintenance_request
        FROM Apartment_Unit 
        WHERE unit_id = ?
    ''', (unit_id,))
    unit_info = cursor.fetchone()  # fetch one row
    return unit_info
