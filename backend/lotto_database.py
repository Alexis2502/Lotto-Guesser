import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to SQLite database: {db_file}")
    except sqlite3.Error as e:
        print(e)
    return conn

def create_tables(conn, table_name):
    c = conn.cursor()
    if table_name == 'Lotto':
        c.execute('''CREATE TABLE IF NOT EXISTS lotto_results
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     number1 INTEGER, 
                     number2 INTEGER, 
                     number3 INTEGER, 
                     number4 INTEGER, 
                     number5 INTEGER, 
                     number6 INTEGER)''')
    elif table_name == 'EuroJackpot':
        c.execute('''CREATE TABLE IF NOT EXISTS eurojackpot_results
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     number1 INTEGER, 
                     number2 INTEGER, 
                     number3 INTEGER, 
                     number4 INTEGER, 
                     number5 INTEGER)''')
    elif table_name == 'MiniLotto':
        c.execute('''CREATE TABLE IF NOT EXISTS minilotto_results
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     number1 INTEGER, 
                     number2 INTEGER, 
                     number3 INTEGER, 
                     number4 INTEGER, 
                     number5 INTEGER)''')
    conn.commit()

def save_sequences_to_db(sequences, game_type):
    conn = create_connection('lotto.db')
    if conn is None:
        print("Błąd podczas tworzenia połączenia z bazą danych")
        return

    create_tables(conn, game_type)

    if game_type == 'Lotto':
        table_name = 'lotto_results'
    elif game_type == 'EuroJackpot':
        table_name = 'eurojackpot_results'
    elif game_type == 'MiniLotto':
        table_name = 'minilotto_results'
    else:
        print("Nieznany typ gry")
        return

    try:
        c = conn.cursor()
        c.execute(f"DELETE FROM {table_name}")

        for sequence in sequences:
            sequence = [int(number) for number in sequence if number.isdigit()]
            if (game_type == 'Lotto' and len(sequence) != 6) or \
               (game_type == 'EuroJackpot' and len(sequence) != 5) or \
               (game_type == 'MiniLotto' and len(sequence) != 5):
                print("Błędna sekwencja liczb:", sequence)
                continue
            if game_type == 'Lotto':
                c.execute(f"INSERT INTO {table_name} (number1, number2, number3, number4, number5, number6) VALUES (?, ?, ?, ?, ?, ?)", sequence)
            elif game_type == 'EuroJackpot':
                c.execute(f"INSERT INTO {table_name} (number1, number2, number3, number4, number5) VALUES (?, ?, ?, ?, ?)", sequence)
            elif game_type == 'MiniLotto':
                c.execute(f"INSERT INTO {table_name} (number1, number2, number3, number4, number5) VALUES (?, ?, ?, ?, ?)", sequence)
        conn.commit()

        c.execute(f"SELECT * FROM {table_name}")
        rows = c.fetchall()
    except sqlite3.Error as e:
        print("Błąd podczas wykonywania zapytań SQL:", e)
    finally:
        conn.close()