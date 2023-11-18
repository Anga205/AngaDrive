import re, sqlite3, sqlite3, datetime, time, random, bcrypt, os, string

database_directory=os.path.join("rx.db")

def dbify(var):
    if var==None:
        return "NULL"
    if type(var)==type(0):
        return str(var)
    if type(var)==type(""):
        if "'" not in var:
            return "'"+var+"'"
        elif '"' not in var:
            return '"'+var+'"'
        else:
            return "'"+("".join([("''" if x=="'" else x) for x in var]))+"'"

def remove_tpu_account(token):
    try:
        con = sqlite3.connect(database_directory)
        cur = con.cursor()
        cur.execute(f"UPDATE accounts SET TPU_token = NULL WHERE token = {dbify(token)}")
        con.commit()
        con.close()
        return {200: "OK"}
    except Exception as e:
        return {"Error": e}


table_columns_cache = {}
def table_columns(table_name):
    global table_columns_cache
    if table_name in table_columns_cache:
        return table_columns_cache[table_name]
    con = sqlite3.connect("rx.db")
    cur=con.cursor()
    cur.execute(f"PRAGMA table_info({table_name})")
    table_info = cur.fetchall()
    con.close()
    columns = [x[1] for x in table_info]
    table_columns_cache[table_name]=columns
    return columns


def gen_token():
    a="qwertyuiopasdfghjklzxcvbnm"
    a=a+a.upper()
    a=a+"1234567890"
    return "".join(random.choices(a, k=10))+"."+"".join(random.choices(a, k=20))+"."+str(round(time.time()))

def change_password(token, hashed_new_password):
    try:
        con = sqlite3.connect(database_directory)
        cur = con.cursor()
        cur.execute(f"UPDATE accounts SET hashed_password = {dbify(hashed_new_password)} where token = {dbify(token)}")
        con.commit()
        con.close()
        return {200: "OK"}
    except Exception as e:
        print(f"[{time.ctime(time.time())}] Error {e} occured in change_password function in library.py")
        return {"Error": e}

def convert_to_time_value(number):
    # Check if the input number is negative
    if number < 0:
        return "Negative numbers are not supported"

    # Round off the number to the nearest integer
    number = round(number)

    # Initialize variables to store years, months, days, hours, minutes, and seconds
    years = number // (365 * 24 * 3600)
    number %= (365 * 24 * 3600)
    months = number // (30 * 24 * 3600)
    number %= (30 * 24 * 3600)
    days = number // (24 * 3600)
    number %= (24 * 3600)
    hours = number // 3600
    number %= 3600
    minutes = number // 60
    seconds = number % 60

    # Create a list to store time components
    time_components = []

    # Add years, if present
    if years > 0:
        time_components.append(f"{years}y")

    # Add months, if present
    if months > 0:
        time_components.append(f"{months}mo")

    # Add days, if present
    if days > 0:
        time_components.append(f"{days}d")

    # Add hours, if present
    if hours > 0:
        time_components.append(f"{hours}h")

    # Add minutes, if present
    if minutes > 0:
        time_components.append(f"{minutes}m")

    # Add seconds, if present or if the input is 0
    if seconds >= 0 or len(time_components) == 0:
        time_components.append(f"{seconds}s")

    # Join the time components and return as a formatted string
    return ' '.join(time_components)

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

def check_for_password(token: str) -> bool:
    try:
        con = sqlite3.connect(database_directory)
        cur = con.cursor()
        cur.execute(f"SELECT hashed_password FROM accounts WHERE token = {dbify(token)}")
        result = cur.fetchone()
        con.close()
        result = result[0]
        if result==None:
            return False
        return True
    except:
        return False
    

def new_user_signup(username: str, email: str, hashed_password: str=None, TPU_token: str=None) -> None:
    try:
        connection = sqlite3.connect(database_directory)
        cursor = connection.cursor()

        # Check if the email already exists as a TPU_account
        cursor.execute("SELECT TPU_token FROM accounts WHERE email = ?;", (email,))
        existing_tpu_email = cursor.fetchone()
        if (existing_tpu_email!=None) and (existing_tpu_email[0]==None):
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
        cursor.execute(f'''INSERT INTO accounts (email, username, token, hashed_password{', TPU_token' if TPU_token else ''}) VALUES ({dbify(email)}, {dbify(username)}, {dbify(token)}, {dbify(hashed_password)}{(', '+dbify(TPU_token)) if TPU_token else ''});''')
        
        connection.commit()
        print("User signup successful.")
        return {"token":token}
    except sqlite3.Error as e:
        return f"Error inserting user data: {e}"
    finally:
        if connection:
            connection.close()

def delete_account(token: str):
    if is_valid_email(token):
        converted_token=get_token_from_email(token)
        if converted_token == "":
            print(f"[{time.ctime(time.time())}] delete_account in library.py tried to delete {dbify(token)} but no such account was found")
            return False
        token=converted_token        
    try:
        con = sqlite3.connect(database_directory)
        cur = con.cursor()
        cur.execute(f"DELETE FROM accounts WHERE token = {dbify(token)}")
        cur.execute(f"SELECT file_name FROM file_data WHERE account_token = {dbify(token)}")
        files=cur.fetchall()
        try:
            file_names=[x[0] for x in files]
            cur.execute(f"DELETE FROM file_data WHERE account_token = {dbify(token)}")
            for file_name in file_names:
                os.remove(os.path.join("assets","i",file_name))
        except Exception as e:
            print(f"[{time.ctime(time.time())}] An error occured in delete_account while deleting files in library.py: {e}")
        con.commit()
        con.close()
        return True  # Deletion successful
    except Exception as e:
        print(f"[{time.ctime(time.time())}] Error {e} occured in delete_account function in library.py")
        return False


def login_user(email: str, prehashed_password: str):
    try:
        connection = sqlite3.connect(database_directory)
        cursor = connection.cursor()

        cursor.execute(f"SELECT email,username,token,hashed_password,TPU_token FROM accounts WHERE email = {dbify(email)}")
        account = cursor.fetchone()
        connection.close()

        if account!=None:
            if prehashed_password.startswith("TPU-OAUTH") and (prehashed_password in account):
                return get_account_info_from_token(account[2])
            if account[3]!=None:
                stored_hashed_password = bytes.fromhex(account[3]) if not type(account[3])==type(b"") else account[3]
                prehashed_password=prehashed_password.encode('utf-8') if type(prehashed_password)==type("") else prehashed_password

                if bcrypt.checkpw(prehashed_password, stored_hashed_password):
                    account_data = {
                        "email": account[0],
                        "username": account[1],
                        "token": account[2],
                        "hashed_password": account[3],
                        "TPU_token": account[4] if account[4] != None else False 
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

def TPU_signin(TPU_email: str, TPU_username: str, TPU_authtoken: str):
    try:
        con=sqlite3.connect(database_directory)
        cur=con.cursor()
        cur.execute(f"select email, username from accounts where TPU_token={dbify(TPU_authtoken)}")
        data=cur.fetchone()
        if data is None:
            cur.execute(f"select email, username from accounts where email={dbify(TPU_email)}")
            email_matching_account=cur.fetchone()
            if email_matching_account is None:
                output=new_user_signup(TPU_username, TPU_email, hashed_password=None, TPU_token=TPU_authtoken)
                return {"email":TPU_email, "username":TPU_username, "token": output.get("token")}
            else:
                return {"error":"email already registered", "email": TPU_email}
        else:
            return {"email":data[0],"username":data[1]}
    except Exception as e:
        print(f"TPU signin error: {e}")
        return {"error":f"TPU signin error: {e}"}

def obfuscate_filename(filename):
    # Get the file extension
    file_extension = os.path.splitext(filename)[1]

    # Define the allowed characters for obfuscation
    allowed_chars = string.ascii_lowercase + string.digits

    # Generate a random string of length between 10 and 15
    obfuscated_part = ''.join(random.choice(allowed_chars) for _ in range(random.randint(10, 15)))

    # Combine the obfuscated string and file extension
    obfuscated_filename = obfuscated_part + file_extension

    return obfuscated_filename

def create_sqlite_database(DB_PATH):
    # Create or connect to the SQLite database
    if os.path.isfile(DB_PATH):
        return None

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create the 'activity' table
    cursor.execute('''CREATE TABLE IF NOT EXISTS activity (
                        timestamps INTEGER
                    )''')

    # Create the 'accounts' table
    cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                        email TEXT,
                        username TEXT,
                        token TEXT PRIMARY KEY,
                        hashed_password TEXT,
                        TPU_token TEXT
                    )''')


    # Create the 'file_data' table
    cursor.execute('''CREATE TABLE IF NOT EXISTS file_data (
                        file_name TEXT PRIMARY KEY,
                        account_token TEXT,
                        time_uploaded INTEGER,
                        file_size DECIMAL,
                        original_file_name TEXT
                    )''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def get_file_size(file_path: str) -> int:
    # Convert to an absolute path if it's a relative path
    file_path = os.path.abspath(file_path)
    # Get the size of the file in bytes
    file_size = os.path.getsize(file_path)
    return file_size

## THIS IS TEMP AND TO BE REMOVED AFTER THE LOGIN SYSTEM IS REWORKED
def get_token_from_username(username):
    if username=="":
        return ""
    con= sqlite3.connect(database_directory)
    cur=con.cursor()
    cur.execute(f"select token from accounts where username='{username}'")
    try:
        token=cur.fetchone()
        token=token[0]
        con.close()
        return token
    except:
        return ""
    
def get_token_from_email(email):
    if email=="":
        return ""
    con= sqlite3.connect(database_directory)
    cur=con.cursor()
    cur.execute(f"select token from accounts where email={dbify(email)}")
    try:
        token=cur.fetchone()
        token=token[0]
        con.close()
        return token
    except Exception as e:
        print(f"Exception in get_token_from_email: {e}")
        con.close()
        return ""


def validate_login(email, unhashed_password):
    con = sqlite3.connect(database_directory)
    cur = con.cursor()
    cur.execute(f"select hashed_password from accounts where email = {dbify(email)}")
    stored_password=cur.fetchone()
    stored_password=stored_password[0]
    con.close()
    stored_password = bytes.fromhex(stored_password) if not type(stored_password)==type(b"") else stored_password
    unhashed_password = unhashed_password.encode('utf-8') if type(unhashed_password)==type("") else unhashed_password
    return get_token_from_email(email) if bcrypt.checkpw(unhashed_password, stored_password) else False

def get_account_info_from_token(token):
    if token=="":
        return None
    con = sqlite3.connect(database_directory)
    cur = con.cursor()
    cur.execute(f"select * from accounts where token = {dbify(token)}")
    output=cur.fetchone()
    con.close()
    columns = table_columns("accounts")
    dict_output = dict(zip(columns, output))
    return dict_output

def get_files(account_token):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_directory)
    cursor = conn.cursor()

    # Query the file_data table for original_file_names
    cursor.execute('''SELECT original_file_name
                      FROM file_data
                      WHERE account_token = ?
                      ORDER BY time_uploaded ASC''', (account_token,))
    
    # Fetch all the results into a list
    file_names = [row[0] for row in cursor.fetchall()]

    # Close the connection
    conn.close()

    return file_names

get_file_info_cache={}
def get_file_info(file_name: str) -> list[str]:
    global get_file_info_cache
    if file_name in get_file_info_cache:
        return get_file_info_cache[file_name]
    DB_PATH=database_directory
    try:
        # Connect to the database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Query the file_data table for the given file_name
        cursor.execute('''SELECT * FROM file_data WHERE file_name = ?''', (file_name,))
        result = cursor.fetchone()  # Fetch the first matching row
        conn.close()
        if result:
            # Convert the result tuple to a list for easy access
            file_info = list(result)
            file_info[2] = time.ctime(file_info[2])
            file_info[3] = turn_size_to_string(file_info[3])
            get_file_info_cache[file_name]=file_info
            return file_info
        else:
            return None  # No data found for the given file_name

    except sqlite3.Error as e:
        print("SQLite error:", e)
        return None

def turn_size_to_string(file_size):
    # Define the units and their corresponding sizes
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    sizes = [1024 ** i for i in range(len(units))]

    # Find the appropriate unit for the file size
    for i in range(len(units)):
        if file_size < sizes[i] * 1024 or i == len(units) - 1:
            # Format the file size with one decimal place
            formatted_size = "{:.1f}".format(file_size / sizes[i])
            return f"{formatted_size} {units[i]}"

def add_tpu_to_existing_account(token, TPU_token):
    con = sqlite3.connect(database_directory)
    cur = con.cursor()
    cur.execute(f"UPDATE accounts SET TPU_token = {dbify(TPU_token)} WHERE token = {dbify(token)}")
    con.commit()
    con.close()

def get_new_file_names(account_token):
    conn = sqlite3.connect(database_directory)
    cursor = conn.cursor()

    # Query the file names in increasing order of timestamp for the given account_token
    cursor.execute('''SELECT file_name
                      FROM file_data
                      WHERE account_token = ?
                      ORDER BY time_uploaded ASC''', (account_token,))

    file_names = [f"{row[0]}" for row in cursor.fetchall()]

    conn.close()

    return file_names

def get_file_sizes(account_token):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_directory)
    cursor = conn.cursor()

    # Retrieve file sizes in increasing order of timestamp for the given account_token
    cursor.execute('''SELECT file_size
                      FROM file_data
                      WHERE account_token = ?
                      ORDER BY time_uploaded ASC''', (account_token,))
    
    file_sizes = [turn_size_to_string(row[0]) for row in cursor.fetchall()]

    # Close the database connection
    conn.close()

    return file_sizes

def add_file(file_name: str, account_token: str, time_uploaded: int, original_file_name: str):
    file_size: float = get_file_size(os.path.join("assets", "i", file_name))
    con=sqlite3.connect(database_directory)
    cur=con.cursor()
    cur.execute(f'''insert into file_data values ("{file_name}", "{account_token}", {round(time_uploaded)}, {file_size}, "{original_file_name}")''')
    con.commit()
    con.close()

def get_file_info_from_account_token(account_token: str) -> list[list[str]]: #returns [[file_name, account_token, time_uploaded, file_size, original_file_name]]
    file_names=get_new_file_names(account_token)
    file_info=[]
    for i in file_names:
        file_info.append(get_file_info(i))
    return file_info

def delete_file(file_name):
    # Connect to the SQLite database
    print(f"deleting {file_name}")
    conn = sqlite3.connect(database_directory)
    cursor = conn.cursor()

    try:
        # Delete the row associated with the given file_name
        cursor.execute('''DELETE FROM file_data WHERE file_name = ?''', (file_name,))
        conn.commit()
        print(f"File '{file_name}' deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error deleting file '{file_name}': {e}")
    finally:
        # Close the database connection
        conn.close()

