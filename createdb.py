import sqlite3

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

# STATEMENTS ABOVE ARE COMMENTED TO PREVENT NEW CREATIONS UPON FILE EXECUTION

cursor.execute("""ALTER TABLE Users ADD COLUMN active_status text default 'active'""")
conn.commit() #commits changes to our database
conn.close()
