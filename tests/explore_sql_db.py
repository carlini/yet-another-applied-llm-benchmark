from evaluator import *

DESCRIPTION = "Test if the model can interact with an SQLite database and provide the correct command to add a new person with specific criteria."

TAGS = ['sql', 'agent']

question = """
I've just run `sqlite3 people.db` and you are now in the interpreter. I want to add another person named Victor. They should be as old as the youngest person. And have the most popular profession. What command should I run?

On each round you should just give me just one command to type, I'll run it exactly as-is, and give you the exact output. I will not make any changes. So do not write any placholder text. I'll get started:

INPUT: `.version`

OUTPUT: ```SQLite 3.39.5 2022-10-14 20:58:05```

INPUT: `.database`

OUTPUT: ```main: people.db r/w```

Now your turn. What do you want to run? Do not explain yourself, just give me exactly one command, ending with ; if necessary. Run small queries one at a time; think step by step. Start your response with INPUT:
"""

def setup():
    import sqlite3
    
    # Create a connection object using the connect function
    conn = sqlite3.connect('people.db')
    
    # Create a cursor object using the cursor method
    cursor = conn.cursor()
    
    # Create table named people with columns for name, favorite friend, age, and profession
    cursor.execute('''CREATE TABLE people
                 (a_name TEXT, favorite_friend TEXT, person_age INT, the_profession TEXT)''')
    
    # List of people data to insert into the people table
    people_data = [
        ('Alice', 'Bob', 29, 'Engineer'),
        ('Bob', 'Alice', 32, 'Doctor'),
        ('Charlie', 'Alice', 28, 'Artist'),
        ('David', 'Eve', 35, 'Doctor'),
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


def test_ok():
    import sqlite3
    
    # Create a connection object using the connect function
    conn = sqlite3.connect('people.db')
    
    # Create a cursor object using the cursor method
    cursor = conn.cursor()

    # Get Victor's age and profession
    cursor.execute('SELECT person_age, the_profession FROM people WHERE a_name = "Victor"')
    out = cursor.fetchone()
    if out is None:
        return False
    age, profession = out
    
    return age == 25 and profession == 'Doctor'
    


def do_extract(x):
    if 'INPUT:' in x:
        x = x.split("INPUT:")[1]
    try:
        to_send = x.split("`")[1]
    except:
        to_send = x.split("\n")[0]
    return to_send


def do_prepare(x):
    print("Preparing to pass back", x)
    x = x.replace("\nsqlite>","")
    return f"I get an OUTPUT: ```{x}```.\n\nWhat is the exact command I should run next? Start your response with INPUT:"


TestSqlExplore = Setup(setup) >> StartDockerJob("sqlite3 people.db", eos_string="sqlite>") >> question >> UntilDone(PyEvaluator(test_ok), (LLMConversation() >> PyFunc(do_extract) >> SendStdoutReceiveStdin() >> PyFunc(do_prepare)), max_iters=10) >> PyEvaluator(test_ok)
 
if __name__ == "__main__":
    print(run_test(TestSqlExplore))
