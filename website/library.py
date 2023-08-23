import re, sqlite3, sqlite3, datetime, time

database_directory="..\\rx.db"

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

def new_user_signup(username: str, email: str, password: str) -> bool:
    # 1) Attempt to connect to "rx.db" or create a new database if it doesn't exist
    try:
        connection = sqlite3.connect(database_directory)
    except sqlite3.Error as e:
        return f"Error connecting to database: {e}"
    
    cursor = connection.cursor()
    
    # Check if email already exists in the 'accounts' table
    cursor.execute("SELECT email FROM accounts WHERE email = ?;", (email,))
    existing_email = cursor.fetchone()
    if existing_email:
        return "Email id already exists"
    
    # Check username length
    if len(username) < 3 or len(username) > 16: 
        return "Username must be between 3 and 16 characters long"
    
    try:
        # Insert new user details into the 'accounts' table
        cursor.execute("INSERT INTO accounts (username, email, password) VALUES (?, ?, ?);",
                       (username, email, password))
        connection.commit()
        return True
    except sqlite3.Error as e:
        return f"Error inserting user data: {e}"
    finally:
        # Close the connection
        connection.close()

def delete_account(email: str) -> bool:
    try:
        connection = sqlite3.connect(database_directory)
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return False
    
    cursor = connection.cursor()
    
    try:
        cursor.execute("DELETE FROM accounts WHERE email = ?;", (email,))
        connection.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting account: {e}")
        return False
    finally:
        connection.close()

def login_user(email: str, password: str) -> list:

    # Attempt to connect to "rx.db" or create a new database if it doesn't exist
    try:
        connection = sqlite3.connect(database_directory)
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return [False, "Error connecting to the database"]
    
    cursor = connection.cursor()
    
    # Check if the email exists in the 'accounts' table
    cursor.execute("SELECT username, password FROM accounts WHERE email = ?;", (email,))
    user_info = cursor.fetchone()
    
    if not user_info:
        connection.close()
        return [False, "Email does not exist"]
    
    username, stored_password = user_info
    
    if stored_password == password:
        connection.close()
        return [True, username]
    else:
        connection.close()
        return [False, "Email and password do not match"]

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
    
    for ts in timestamps:
        dt = datetime.datetime.fromtimestamp(ts)
        day = dt.date()
        
        if day in days_counts:
            days_counts[day] += 1
        else:
            days_counts[day] = 1
    
    counts_per_day = [count for day, count in sorted(days_counts.items())]
    return counts_per_day

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
