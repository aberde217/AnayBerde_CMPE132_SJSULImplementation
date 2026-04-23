import sqlite3
import hashlib
import secrets

conn = sqlite3.connect("mlklibrary.db")
cursor = conn.cursor() # executes SQLite instructions
# cursor.execute("""CREATE TABLE Users(
#         first_name text,
#         last_name text,
#         library_id text,
#         password text,
#         role text
#         )""")

# # cursor.execute("""INSERT INTO Users VALUES ("Librarian", "Librarian", "000000000", "sjsu_librarian", "Librarian")""")
# # cursor.execute("""INSERT INTO Users VALUES ("Anay", "Berde", "016110809", "anaypassword", "Student")""")
# # cursor.execute("""INSERT INTO Users VALUES ("Bernie", "Kosar", "015667180", "*browns_football", "Professor")""")
# cursor.execute("""INSERT INTO Users VALUES ("John", "Smith", "567001119", "iloveRe@ading", "Borrower")""")

# cursor.execute("""ALTER TABLE Users ADD COLUMN active_status text default 'active'""")

# cursor.execute("""DROP TABLE Users""") # DELETES TABLE, WANTED TO RESET SO THAT DB STORES HASHED PASSWORDS

# cursor.execute("""CREATE TABLE Users( # RECREATES TABLE
#         first_name text,
#         last_name text,
#         library_id text,
#         password text,
#         role text,
#         active_status text default 'active'
#         )""")
cursor.execute("""ALTER TABLE Users ADD COLUMN salt""") # MADE AN ERROR HERE, OOPS!
cursor.execute("""ALTER TABLE Users DROP COLUMN salt""")
cursor.execute("""ALTER TABLE Users ADD COLUMN salt text""")
plaintext = "sjsu_librarian"
salt = secrets.token_hex(8)
temp = hashlib.sha256((salt + plaintext).encode())
password = temp.hexdigest()

cursor.execute("""INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?)"""
, ("Librarian", "Librarian", "000000000", password, "Librarian", "active", salt))
# STATEMENTS ABOVE ARE COMMENTED TO PREVENT UNINTENDED UPDATES UPON RUNNING PROGRAM

conn.commit() #commits changes to our database
conn.close()
