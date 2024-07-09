import sqlite3
import hashlib


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
    availability_status INTEGER       NOT NULL,
    maintenance_request INTEGER       DEFAULT (0),
    is_deleted          INTEGER       DEFAULT (0),
    FOREIGN KEY (
        building_id
    )
    REFERENCES Apartment_Building (building_id),
    FOREIGN KEY (
        admin_id
    )
    REFERENCES Admin (admin_id),
    UNIQUE (
        building_id,
        unit_number
    )
);
    ''')
    # creates table for tenant
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Tenant (
    tenant_id                      INTEGER      PRIMARY KEY AUTOINCREMENT,
    admin_id                       INTEGER,
    unit_id                        INTEGER      REFERENCES Apartment_Unit (unit_id),
    lastName                       VARCHAR (50) NOT NULL,
    firstName                      VARCHAR (50) NOT NULL,
    middleName                     VARCHAR (50),
    suffix                         VARCHAR (50),
    email                          VARCHAR (50),
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
    income                         DOUBLE,
    is_deleted                     INTEGER      DEFAULT (0),
    FOREIGN KEY (
        admin_id
    )
    REFERENCES Admin (admin_id) );
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
    is_deleted     INTEGER DEFAULT (0),
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


# function for tables that need admin_id
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


# ================ login PAGE FUNCTIONS =======================
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


# ================ add_building PAGE FUNCTIONS =======================

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


# ================ display_building PAGE FUNCTIONS =======================
def fetch_new_building_info(conn, building_id):
    # fetch building information from the database based on building_id
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Apartment_Building WHERE building_id = ?", (building_id,))
    building_info = cursor.fetchone()  # one row is fetched
    return building_info


# for testing only
def fetch_building_treeview(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT building_id, building_name, country, amenities FROM Apartment_Building;')
    return cursor.fetchall()


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


# ================ add_unit PAGE FUNCTIONS =======================
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
                        unit_size, maintenance_request, availability_status))
        conn.commit()
        print("Unit information saved successfully.")
    except Exception as e:
        print(f"Error saving unit information: {str(e)}")
        conn.rollback()


# ================ display_unit_info PAGE FUNCTIONS =======================

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


def fetch_unit_info(conn, unit_id):
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


# ================ add_expense PAGE FUNCTIONS =======================
def insert_expense(conn, expense_date, expense_amount, expense_type, description):
    admin_id = get_admin_id(conn)
    if not admin_id:
        return

    try:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO Expenses(admin_id, expense_date, expense_amount, expense_type, description)
                        VALUES (?, ?, ?, ?, ?);''', (admin_id, expense_date, expense_amount, expense_type, description))
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()


# ================ display_expense PAGE FUNCTIONS =======================

def fetch_latest_expense_id(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT max(expense_id) FROM Expenses;')
    return cursor.fetchone()[0]


# ================ tenant_information PAGE FUNCTIONS =======================

def fetch_tenant_treeview(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''SELECT
    AB.building_name,
    AU.unit_number,
    T.firstName || ' ' || T.middleName || ' ' || T.lastName AS tenant_name,
    T.contact_number AS contact_number,
    CASE
        WHEN P.payment_id IS NOT NULL THEN 'Paid'
        ELSE 'Not Paid'
    END AS payment_status,
    T.lease_start_date
FROM Tenant AS T
INNER JOIN Apartment_Unit AS AU
    ON T.unit_id = AU.unit_id -- correctly link tenants to apartment units
INNER JOIN Apartment_Building AS AB
    ON AU.building_id = AB.building_id -- correctly link apartment units to buildings
LEFT JOIN Payment AS P
    ON T.tenant_id = P.tenant_id
    AND P.payment_date BETWEEN T.lease_start_date AND T.lease_end_date
WHERE T.is_deleted = 0
ORDER BY T.tenant_id, P.payment_date DESC; -- Ensure tenants are shown correctly and ordered by tenant_id;
''')
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print({e})
        return []


def fetch_tenants_by_name(conn, search_name):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT
                AB.building_name,
                AU.unit_number,
                T.firstName || ' ' || T.lastName AS tenant_name,
                T.contact_number,
                CASE
                    WHEN P.payment_id IS NOT NULL THEN 'Paid'
                    ELSE 'Not Paid'
                END AS payment_status,
                T.lease_start_date
            FROM Tenant AS T
            INNER JOIN Apartment_Unit AS AU
                ON T.tenant_id = AU.tenant_id
            INNER JOIN Apartment_Building AS AB
                ON AU.building_id = AB.building_id
            LEFT JOIN Payment AS P
                ON T.tenant_id = P.tenant_id
                AND P.payment_date BETWEEN T.lease_start_date AND T.lease_end_date
            WHERE (T.firstName LIKE '%' || ? || '%' OR T.middleName LIKE '%' || ? || '%' OR T.lastName LIKE '%' || ? || '%')
        ''', (search_name, search_name, search_name))

        # Fetch all rows matching the search criteria
        tenant_data = cursor.fetchall()
        return tenant_data

    except Exception as e:
        print(f"Error executing search query: {str(e)}")
        return None


def fetch_tenants_by_filters(conn, search_name, from_date, to_date):
    cursor = conn.cursor()
    query = '''SELECT AB.building_name, AU.unit_number, 
                      T.firstName || ' ' || T.middleName || ' ' || T.lastName AS tenant_name, 
                      T.contact_number, T.move_in_date, T.lease_start_date, T.lease_end_date
               FROM Tenant AS T
               INNER JOIN Apartment_Unit AS AU ON T.Tenant_id = AU.unit_id
               INNER JOIN Apartment_Building AS AB ON AU.building_id = AB.building_id
               WHERE 1=1 '''

    params = []
    if search_name != "Search Name...":
        query += " AND (T.firstName || ' ' || T.middleName || ' ' || T.lastName LIKE ?)"
        params.append(f"%{search_name}%")

    if from_date:
        query += " AND T.lease_start_date >= ?"
        params.append(from_date.strftime('%Y-%m-%d'))

    if to_date:
        query += " AND T.lease_start_date <= ?"
        params.append(to_date.strftime('%Y-%m-%d'))

    query += " ORDER BY T.lease_start_date ASC"
    cursor.execute(query, params)
    return cursor.fetchall()


# ================ add_tenant PAGE FUNCTIONS =======================

def fetch_building_name(conn):
    cursor = conn.cursor()
    cursor.execute('select distinct building_name from apartment_building;')
    return cursor.fetchall()


def fetch_unit_numbers_by_building(conn, building_name):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT unit_number
            FROM Apartment_Unit au
            JOIN Apartment_Building ab ON au.building_id = ab.building_id
            WHERE ab.building_name = ?;
        ''', (building_name,))
        result = cursor.fetchall()
        return [row[0] for row in result]

    except Exception as e:
        print(f"Error fetching unit numbers: {str(e)}")
        return []


def get_unit_id(conn, unit_number, building_id):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT unit_id
            FROM Apartment_Unit
            WHERE unit_number = ? AND building_id = ?;
        ''', (unit_number, building_id))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    except Exception as e:
        print(f"Error fetching unit_id: {str(e)}")
        return None


def insert_tenant(conn, lastName, firstName, middleName, suffix, email, contact_number, move_in_date,
                  lease_start_date, lease_end_date, emergency_contact_name, emergency_contact_number,
                  emergency_contact_relationship, tenant_dob, sex, income, unit_id):
    admin_id = get_admin_id(conn)
    if not admin_id:
        return None  # Return None if admin_id is not available

    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Tenant (
                admin_id, 
                unit_id,
                lastName, 
                firstName, 
                middleName, 
                suffix, 
                email, 
                contact_number, 
                move_in_date, 
                lease_start_date,
                lease_end_date, 
                Emergency_contact_name, 
                Emergency_contact_number, 
                Emergency_contact_relationship, 
                tenant_dob, 
                sex,
                income
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        ''', (admin_id, unit_id, lastName, firstName, middleName, suffix, email,
              contact_number, move_in_date,
              lease_start_date, lease_end_date, emergency_contact_name,
              emergency_contact_number,
              emergency_contact_relationship, tenant_dob, sex, income))

        # Fetch the inserted tenant_id
        tenant_id = cursor.lastrowid

        conn.commit()
        return tenant_id  # Return the inserted tenant_id

    except Exception as e:
        print(f"Error saving tenant information: {str(e)}")
        conn.rollback()
        return None  # Return None on error


# ================ display_tenant_details PAGE FUNCTIONS =======================

def fetch_new_tenant_info(conn, tenant_id):
    cursor = conn.cursor()
    cursor.execute('''SELECT
                T.firstName || ' ' || T.middleName || ' ' || T.lastName AS tenant_name,
                T.contact_number,
                T.email,
                AU.unit_number,
                CASE 
                    WHEN T.sex = 1 THEN 'Male'
                    WHEN T.sex = 2 THEN 'Female'
                    ELSE 'Prefer not to say'
                END AS sex,
                T.tenant_dob AS birthdate,
                T.move_in_date,
                T.lease_start_date,
                T.lease_end_date,
                (SELECT MAX(P.payment_date)
                 FROM Payment P
                 WHERE P.tenant_id = T.tenant_id) AS last_payment_date,
                T.Emergency_contact_name,
                T.Emergency_contact_number,
                T.Emergency_contact_relationship
            FROM
                Tenant T
                LEFT JOIN Apartment_Unit AU ON T.tenant_id = AU.unit_id
            WHERE
                T.tenant_id = ?''', (tenant_id,))
    result = cursor.fetchone()
    return result


def fetch_latest_payment(conn, tenant_id):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.payment_id, p.unit_id, p.amount, p.payment_date, p.payment_method
        FROM Payment p
        WHERE p.tenant_id = ?
        ORDER BY p.payment_date DESC
        LIMIT 1
    ''', (tenant_id,))
    payment_info = cursor.fetchone()
    return payment_info


# ================ expenses PAGE FUNCTIONS =======================

def fetch_expense_treeview(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''SELECT expense_date, expense_amount,
CASE 
WHEN expense_type = 1 THEN 'Utilities'
WHEN expense_type = 2 THEN 'Maintenance and Repairs'
WHEN expense_type = 3 THEN 'Advertising'     
WHEN expense_type = 4 THEN 'Insurance'
WHEN expense_type = 5 THEN  'Administrative Costs'
WHEN expense_type = 6 THEN 'Property Management Costs'
END,
description
FROM Expenses;''')
        rows = cursor.fetchall()
        return rows

    except Exception as e:
        print({e})
        return []


# ================ dashboard PAGE FUNCTIONS =======================
def total_units(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Apartment_Unit;')
    return cursor.fetchone()[0]


def count_lease_expiration_alerts(conn):
    cursor = conn.cursor()
    cursor.execute('''SELECT COUNT(*)
FROM Tenant AS T
INNER JOIN Apartment_Unit AS AU
    ON T.Unit_id = AU.unit_id
INNER JOIN Apartment_Building AS AB
    ON AU.building_id = AB.building_id
WHERE T.lease_end_date <= DATE('now', '+30 days') AND T.lease_end_date >= DATE('now');
''')
    return cursor.fetchone()[0]


def count_recent_tenants(conn):
    cursor = conn.cursor()
    cursor.execute('''SELECT COUNT(*)
    FROM Tenant AS T
    INNER JOIN Apartment_Unit AS AU
        ON T.unit_id = AU.unit_id
    INNER JOIN Apartment_Building AS AB
        ON AU.building_id = AB.building_id
        WHERE T.move_in_date >= DATE('now', '-30 days') AND T.is_deleted = 0
    ORDER BY move_in_date DESC;''')
    return cursor.fetchone()[0]


def count_maintenance_requests(conn):
    cursor = conn.cursor()
    cursor.execute('''SELECT COUNT(*)
FROM Apartment_Unit AS AU
LEFT JOIN Tenant AS T
    ON AU.unit_id = T.tenant_id
INNER JOIN Apartment_Building AS AB
    ON AU.building_id = AB.building_id
WHERE AU.maintenance_request = 1;''')
    return cursor.fetchone()[0]


# ================ See More total_units FUNCTIONS =======================
def count_available_units(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Apartment_Unit WHERE availability_status = 1')
    return cursor.fetchone()[0]


def count_occupied_units(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Apartment_Unit WHERE availability_status = 2')
    return cursor.fetchone()[0]


def count_under_maintenance_units(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Apartment_Unit WHERE availability_status = 3')
    return cursor.fetchone()[0]


# ================ See More rental_rates FUNCTIONS =======================
def average_rental_rate(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT AVG (rental_rate) FROM Apartment_Unit')
    return cursor.fetchone()[0]


def maximum_rental_rate(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT MAX (rental_rate) FROM Apartment_Unit')
    return cursor.fetchone()[0]


def minimum_rental_rate(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT MIN (rental_rate) FROM Apartment_Unit')
    return cursor.fetchone()[0]


# ================ See More monthly_earnings FUNCTIONS =======================
def rent_collection(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(amount) FROM Payment;')
    return cursor.fetchone()[0]


def monthly_expense(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(expense_amount) FROM Expenses;')
    return cursor.fetchone()[0]


def monthly_earnings(conn):
    cursor = conn.cursor()
    cursor.execute('''SELECT (SELECT (SELECT COALESCE(SUM(amount), 0)FROM Payment) - COALESCE(SUM(expense_amount), 0) 
                        FROM Expenses)  AS earnings;
                        -- COALESCE. if there are no records to sum (resulting in NULL), it defaults to 0 
''')
    return cursor.fetchone()[0]


# ================ See More lease_expiration_alerts FUNCTIONS =======================
def fetch_lease_expiration_alerts(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''SELECT
    AB.building_name,
    AU.unit_number,
    T.firstName || ' ' || T.middleName || ' ' || T.lastName AS tenant_name,
    T.contact_number,
    T.move_in_date,
    T.lease_start_date,
    T.lease_end_date 
FROM Tenant AS T
INNER JOIN Apartment_Unit AS AU
    ON T.Unit_id = AU.unit_id
INNER JOIN Apartment_Building AS AB
    ON AU.building_id = AB.building_id
WHERE T.lease_end_date <= DATE('now', '+30 days') AND T.lease_end_date >= DATE('now')
ORDER BY T.lease_end_date ASC;''')
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print({e})
        return []


# ================ See More maintenance_requests FUNCTIONS =======================
def fetch_maintenance_requests(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''SELECT
    AB.building_name,
    AU.unit_number,
    CASE
        WHEN AU.availability_status = 1 THEN 'Available'
        WHEN AU.availability_status = 2 THEN 'Occupied'
        WHEN AU.availability_status = 3 THEN 'Under Maintenance'
    END AS availability_status,
    COALESCE(T.firstName || ' ' || T.middleName || ' ' || T.lastName, 'No Tenant') AS tenant_name,
    T.contact_number
FROM Apartment_Unit AS AU
LEFT JOIN Tenant AS T
    ON AU.unit_id = T.tenant_id
INNER JOIN Apartment_Building AS AB
    ON AU.building_id = AB.building_id
WHERE AU.maintenance_request = 1;''')
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print({e})
        return []


# ================ See More recent_tenants FUNCTIONS =======================
def fetch_recent_tenants(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''SELECT
        AB.building_name,
        AU.unit_number,
        T.firstName || ' ' || T.middleName || ' ' || T.lastName AS tenant_name,
        T.contact_number AS contact_number,
        T.move_in_date
    FROM Tenant AS T
    INNER JOIN Apartment_Unit AS AU
        ON T.unit_id = AU.unit_id
    INNER JOIN Apartment_Building AS AB
        ON AU.building_id = AB.building_id
        WHERE T.move_in_date >= DATE('now', '-30 days') AND T.is_deleted = 0
    ORDER BY move_in_date DESC;''')
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print({e})
        return []


# ================ payment_management PAGE FUNCTIONS =======================
def fetch_payment_treeview(conn):
    cursor = conn.cursor()
    cursor.execute('''SELECT AB.building_name,
                    AU.unit_number,
                    T.firstName || ' ' || T.middleName || ' ' || T.lastName AS tenant_name,
                    T.lease_end_date,
                    AU.rental_rate
                    FROM Tenant AS T
                INNER JOIN Apartment_Unit AS AU
                    ON T.tenant_id = AU.unit_id
                INNER JOIN Apartment_Building AS AB
                    ON AU.building_id = AB.building_id
                WHERE T.is_deleted = 0
                AND AU.availability_status=2
                ORDER BY T.lease_end_date ASC;
                ''')
    return cursor.fetchall()


