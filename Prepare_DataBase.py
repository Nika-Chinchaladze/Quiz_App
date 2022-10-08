import sqlite3

conn = sqlite3.connect("results.db")
curr = conn.cursor()

curr.execute('''UPDATE students SET last_name = 'Quridze' WHERE last_name = 'Qridze';''')

conn.commit()
conn.close()

    
# curr.execute('''CREATE TABLE IF NOT EXISTS students(
#     first_name TEXT,
#     last_name TEXT,
#     score INTEGER,
#     category TEXT
# )''')

# curr.execute('''INSERT INTO students(first_name, last_name, score, category)
# VALUES ('Leri', 'Chixladze', 8, 'General Topics'),
#        ('Leri', 'Chixladze', 5, 'Sport'),
#        ('Leri', 'Chixladze', 11, 'Science'),
#        ('Leri', 'Chixladze', 10, 'English Level Test'),
#        ('Lado', 'Qridze', 10, 'Science'),
#        ('Lado', 'Qridze', 11, 'Sport'),
#        ('Lado', 'Qridze', 12, 'Math'),
#        ('Lado', 'Qridze', 10, 'History'),
#        ('Lado', 'Quridze', 11, 'General Topics'),
#        ('Lado', 'Qridze', 12, 'English Level Test'),
#        ('Gio', 'Shonia', 8, 'Science'),
#        ('Gio', 'Shonia', 8, 'General Topics'),
#        ('Gio', 'Shonia', 8, 'Sport'),
#        ('Lana', 'Yipiani', 9, 'Science'),
#        ('Lana', 'Yipiani', 7, 'Sport'),
#        ('Lana', 'Yipiani', 11, 'General Topics'),
#        ('Lana', 'Yipiani', 12, 'History');
# ''')