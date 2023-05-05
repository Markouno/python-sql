import psycopg2

def create_table(conn): # Функция, создающая структуру БД (таблицы).
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Client (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(40) NOT NULL,
            last_name VARCHAR(60) NOT NULL,
            email VARCHAR(60) NOT NULL
        );
        """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Phone_book (
            id SERIAL PRIMARY KEY,
            client_id INTEGER NOT NULL REFERENCES Client(id),
            phone VARCHAR(60)
        );
        """)

def insert_data(conn, first_name, last_name, email, phone_number=None): # Функция, позволяющая добавить нового клиента.
    cur.execute("""
        INSERT INTO Client (first_name, last_name, email)
        VALUES (%s, %s, %s) RETURNING id;
        """, (first_name, last_name, email))
    client_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO Phone_book (client_id, phone)
        VALUES (%s, %s);
        """, (client_id, phone_number))

def insert_phone(conn, client_id, phone_number): # Функция, позволяющая добавить телефон для существующего клиента
    cur.execute("""
        INSERT INTO Phone_book (client_id, phone)
        VALUES (%s, %s);
        """, (client_id, phone_number))

def info_update(conn, client_id, first_name, last_name, email, phone_number): # Функция, позволяющая изменить данные о клиенте.
    cur.execute("""
        UPDATE Client
        SET first_name = %s,
            last_name = %s,
            email = %s
        WHERE id = %s;
        """, (first_name, last_name, email, client_id))

    cur.execute("""
        UPDATE Phone_book
        SET phone = %s
        WHERE client_id = %s;
        """, (phone_number, client_id))

def remove_phone(conn, phone_number): # Функция, позволяющая удалить телефон для существующего клиента.
    cur.execute("""
        DELETE FROM Phone_book
        WHERE phone = %s;
        """, (phone_number,))

def remove_client(conn, client_id): # Функция, позволяющая удалить существующего клиента.
    cur.execute("""
        DELETE FROM Phone_book
        WHERE client_id = %s;
        """, (client_id,))

    cur.execute("""
        DELETE FROM Client
        WHERE id = %s;
        """, (client_id,))

def search_client(conn, searching_info): # Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
    cur.execute("""
        SELECT first_name, last_name from Client
        LEFT JOIN Phone_book ON client.id = phone_book.client_id
        WHERE first_name ILIKE %s OR last_name ILIKE %s OR email ILIKE %s OR phone ILIKE %s;
        """, (searching_info, searching_info, searching_info, searching_info))
    print(cur.fetchone())

with psycopg2.connect(database="Ваша база", user="Аккаунт", password="Пароль") as conn:
    with conn.cursor() as cur:
        conn.autocommit = True
        # create_table(conn)
        # insert_data(conn, 'Егорджан', 'Павлусио', 'pupochek@mail.ky', '88005553535')
        # insert_data(conn, 'Ало', 'Малё', 'tudam-syudam@odin.kilogram')
        # insert_phone(conn, '1', '41241244124')
        # info_update(conn, '1', 'Егор', 'Павлычев', 'surokk02@mail,ru', '12345454545123')
        # remove_phone(conn, '12345454545123')
        # remove_client(conn, '2')
        # search_client(conn, '41241244124')


