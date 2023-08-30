import re, sqlite3, sqlite3, datetime, time, platform, os, random, bcrypt

def gen_token():
    a="qwertyuiopasdfghjklzxcvbnm"
    a=a+a.upper()
    a=a+"1234567890"
    return "".join(random.choices(a, k=10))+"."+"".join(random.choices(a, k=20))+"."+str(round(time.time()))


if platform.system()=='Windows':
    database_directory="..\\rx.db"
else:
    database_directory=r"../rx.db"


def setup_db(DB_FILENAME):
    # Check if the database file exists
    if os.path.exists(DB_FILENAME):
        print("rx.db exists")
        
        # Connect to the database
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()
        
        # Check if TPU_accounts table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='TPU_accounts'")
        tpu_accounts_exists = cursor.fetchone()
        
        if not tpu_accounts_exists:
            print("TPU_accounts table does not exist, creating...")
            # Create TPU_accounts table
            cursor.execute("CREATE TABLE TPU_accounts (id INTEGER, username TEXT, email TEXT, authtoken TEXT, avatar_link TEXT)")
            
        # Rename existing accounts table to accounts_old
        cursor.execute("ALTER TABLE accounts RENAME TO accounts_old")
        
        # Create a new accounts table
        cursor.execute("CREATE TABLE accounts (email TEXT, username TEXT, token TEXT PRIMARY KEY, hashed_password TEXT, avatar BLOB)")
        
        # Fill the new accounts table with data
        cursor.execute("INSERT INTO accounts (email, username, token, hashed_password, avatar) "
                       "SELECT email, username, ?, ?, NULL FROM accounts_old",
                       (gen_token(), bcrypt.hashpw("accounts_oldpassword".encode('utf-8'), bcrypt.gensalt()).hex()))
        
        # Delete accounts_old table
        cursor.execute("DROP TABLE accounts_old")
        
        # Commit changes and close the connection
        conn.commit()
        conn.close()
        
    else:
        print("rx.db does not exist, creating...")
        # Create a new database
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()
        
        # Create TPU_accounts table
        cursor.execute("CREATE TABLE TPU_accounts (id INTEGER, username TEXT, email TEXT, authtoken TEXT, avatar_link TEXT)")
        
        # Create accounts table
        cursor.execute("CREATE TABLE accounts (email TEXT, username TEXT, token TEXT PRIMARY KEY, hashed_password TEXT, avatar BLOB)")
        
        # Create activity table
        cursor.execute("CREATE TABLE activity (timestamp INTEGER)")
        
        # Insert timestamps into activity table
        current_time = round(time.time())
        cursor.execute("INSERT INTO activity (timestamp) VALUES (?)", (current_time,))
        cursor.execute("INSERT INTO activity (timestamp) VALUES (?)", (current_time,))
        
        # Commit changes and close the connection
        conn.commit()
        conn.close()

setup_db(database_directory)



def find_sql_insertion(input_string):
    # Common SQL injection patterns
    sql_injection_patterns = [
        r"\bSELECT\b.*\bFROM\b",
        r"\bINSERT INTO\b",
        r"\bUPDATE\b.*\bSET\b",
        r"\bDELETE FROM\b",
        r"\bDROP TABLE\b",
        r"\bUNION\b.*\bSELECT\b",
        r"\bOR\b.*\b1=1\b"
    ]
    
    # Characters that might indicate SQL injection
    harmful_characters = ["'", "\"", "}", ")", "]"]
    
    # Check for harmful characters
    for char in harmful_characters:
        if char in input_string:
            return True
    
    # Check if any of the patterns match
    for pattern in sql_injection_patterns:
        if re.search(pattern, input_string, re.IGNORECASE):
            return True
    
    return False

def is_valid_email(email):
    # Regular expression pattern for validating email addresses
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Use the re.match function to check if the email matches the pattern
    if not re.match(email_pattern, email):
        return False
    elif find_sql_insertion(email):
        return False
    else:
        return True

def new_user_signup(username: str, email: str, hashed_password: str) -> None:
    try:
        connection = sqlite3.connect(database_directory)
        cursor = connection.cursor()

        # Check if the email already exists in TPU_accounts table
        cursor.execute("SELECT email FROM TPU_accounts WHERE email = ?;", (email,))
        existing_tpu_email = cursor.fetchone()
        if existing_tpu_email:
            return "Oops this account is already registered as a TPU account, login with TPU to add a password to it"

        # Check if the email already exists in accounts table
        cursor.execute("SELECT email FROM accounts WHERE email = ?;", (email,))
        existing_email = cursor.fetchone()
        if existing_email:
            return "Email id already exists"

        # Check if the username length is valid
        if len(username) < 3 or len(username) > 16:
            return "Username must be between 3 and 16 characters long"

        token = gen_token()

        cursor.execute('''INSERT INTO accounts (email, username, token, hashed_password, avatar)
                          VALUES (?, ?, ?, ?, NULL);''', (email, username, token, hashed_password))
        
        connection.commit()
        print("User signup successful.")
        return None
    except sqlite3.Error as e:
        return f"Error inserting user data: {e}"
    finally:
        if connection:
            connection.close()

def delete_account(email: str):
    try:
        connection = sqlite3.connect(database_directory)
        cursor = connection.cursor()

        # Check if the email exists in accounts table
        cursor.execute("SELECT * FROM accounts WHERE email = ?;", (email,))
        existing_accounts_entries = cursor.fetchall()

        # Check if the email exists in TPU_accounts table
        cursor.execute("SELECT * FROM TPU_accounts WHERE email = ?;", (email,))
        existing_tpu_entries = cursor.fetchall()

        if existing_accounts_entries or existing_tpu_entries:
            # Delete entries from accounts table
            cursor.execute("DELETE FROM accounts WHERE email = ?;", (email,))

            # Delete entries from TPU_accounts table
            cursor.execute("DELETE FROM TPU_accounts WHERE email = ?;", (email,))
            
            connection.commit()
            return False  # Deletion successful
        else:
            return "No matching account found"

    except sqlite3.Error as e:
        return f"Deletion error: {e}"
    finally:
        if connection:
            connection.close()

def login_user(email: str, prehashed_password: str):
    try:
        connection = sqlite3.connect(database_directory)
        cursor = connection.cursor()

        # Check if the email exists in TPU_accounts table
        cursor.execute("SELECT * FROM TPU_accounts WHERE email = ?;", (email,))
        tpu_account = cursor.fetchone()

        if tpu_account:
            # Check if the email exists in accounts table
            cursor.execute("SELECT * FROM accounts WHERE email = ?;", (email,))
            account = cursor.fetchone()

            if account:
                # Compare prehashed_password with the hashed password in the database
                stored_hashed_password = bytes.fromhex(account[3])
                if bcrypt.checkpw(prehashed_password.encode('utf-8'), stored_hashed_password):
                    account_data = {
                        "email": account[0],
                        "username": account[1],
                        "token": account[2],
                        "hashed_password": account[3],
                        "avatar": account[4]
                    }
                    return account_data
                else:
                    return "Login failed: Incorrect password"
            else:
                return "This account already exists as a TPU account, please login with TPU to add a password to your account"
        else:
            return "Account not found"

    except sqlite3.Error as e:
        return f"Login failed because: {e}"
    finally:
        if connection:
            connection.close()

def edit_username(new_username: str, email: str) -> bool:

    try:
        connection = sqlite3.connect(database_directory)
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return False
    
    cursor = connection.cursor()
    
    try:
        cursor.execute("UPDATE accounts SET username = ? WHERE email = ?;", (new_username, email))
        connection.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error updating username: {e}")
        return False
    finally:
        connection.close()

def calls_per_day(timestamps):
    days_counts = {}
    today = datetime.datetime.now().date()
    
    for ts in timestamps:
        dt = datetime.datetime.fromtimestamp(ts)
        day = dt.date()
        
        if (today - day).days <= 6:
            formatted_day = dt.strftime('%b %d')
            if formatted_day in days_counts:
                days_counts[formatted_day] += 1
            else:
                days_counts[formatted_day] = 1
    
    last_week_dates = [(today - datetime.timedelta(days=i)).strftime('%b %d') for i in range(6, -1, -1)]
    result = {date: days_counts.get(date, 0) for date in last_week_dates}
    
    return result

def get_timestamps():
    try:
        connection = sqlite3.connect(database_directory)
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return []
    
    cursor = connection.cursor()
    
    try:
        cursor.execute("SELECT timestamps FROM activity;")
        timestamps = [row[0] for row in cursor.fetchall()]
        return timestamps
    except sqlite3.Error as e:
        print(f"Error retrieving timestamps: {e}")
        return []
    finally:
        connection.close()

def insert_timestamp():
    try:
        connection = sqlite3.connect(database_directory)
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return False
    
    cursor = connection.cursor()
    
    try:
        current_timestamp = round(time.time())
        cursor.execute("INSERT INTO activity (timestamps) VALUES (?);", (current_timestamp,))
        connection.commit()
        return True
    except sqlite3.Error as e:
        return False
    finally:
        connection.close()

def TPU_signin(TPU_id: int, TPU_email: str, TPU_username: str, TPU_authtoken: str, TPU_avatar: str):
    try:
        connection = sqlite3.connect(database_directory)
        cursor = connection.cursor()

        # Check if TPU_id exists in TPU_accounts table
        cursor.execute("SELECT * FROM TPU_accounts WHERE id = ?;", (TPU_id,))
        existing_tpu = cursor.fetchone()

        if not existing_tpu:
            # Check if TPU_email already exists in accounts table
            cursor.execute("SELECT * FROM accounts WHERE email = ?;", (TPU_email,))
            existing_email_account = cursor.fetchone()

            # Check if TPU_email already exists in TPU_accounts table
            cursor.execute("SELECT * FROM TPU_accounts WHERE email = ?;", (TPU_email,))
            existing_email_tpu = cursor.fetchone()

            if existing_email_account and not existing_email_tpu:
                return "This account is already registered on anga.pro, login to it to add your TPU account"

            # Insert values into TPU_accounts table
            cursor.execute('''INSERT INTO TPU_accounts (id, username, email, authtoken, avatar_link)
                              VALUES (?, ?, ?, ?, ?);''', (TPU_id, TPU_username, TPU_email, TPU_authtoken, TPU_avatar))
            connection.commit()
            return False  # TPU signin successful
        else:
            return False  # TPU account already exists or account not found

    except sqlite3.Error as e:
        return f"TPU signin error: {e}"
    finally:
        if connection:
            connection.close()