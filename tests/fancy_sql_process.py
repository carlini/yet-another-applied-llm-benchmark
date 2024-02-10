from evaluator import *

DESCRIPTION = "Test if the model can generate a Python program that retrieves data from a SQL file."

TAGS = ['sql']

question = """
I have a sqlite3 database name TEXT, favorite_friend TEXT, age INT, profession TEXT.
Write me a python program that prints out the favorite friend of the youngest person who isn't anyone's favorite friend.
The database is called people.db and the table is called people.
"""

def setup():
    import sqlite3
    
    # Create a connection object using the connect function
    conn = sqlite3.connect('people.db')
    
    # Create a cursor object using the cursor method
    cursor = conn.cursor()
    
    # Create table named people with columns for name, favorite friend, age, and profession
    cursor.execute('''CREATE TABLE people
                 (name TEXT, favorite_friend TEXT, age INT, profession TEXT)''')
    
    # List of people data to insert into the people table
    people_data = [
        ('Alice', 'Bob', 29, 'Engineer'),
        ('Bob', 'Alice', 32, 'Doctor'),
        ('Charlie', 'Alice', 28, 'Artist'),
        ('David', 'Eve', 35, 'Architect'),
        ('Eve', 'Frank', 26, 'Teacher'),
        ('Frank', 'Alice', 31, 'Scientist'),
        ('Grace', 'Heidi', 30, 'Nurse'),
        ('Heidi', 'Ivy', 25, 'Lawyer'),
        ('Ivy', 'Charlie', 34, 'Chef'),
        ('Judy', 'Grace', 27, 'Accountant')
    ]
    
    # Insert each person into the people table
    cursor.executemany('INSERT INTO people VALUES (?,?,?,?)', people_data)
    
    # Commit the changes
    conn.commit()
    
    # Close the connection
    conn.close()


TestSqlSubquery = Setup(setup) >> question >> LLMRun() >> ExtractCode(keep_main=True, lang='python') >> Echo() >> PythonRun() >> SubstringEvaluator("Grace")

if __name__ == "__main__":
    print(run_test(TestSqlSubquery))
