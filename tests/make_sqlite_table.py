from evaluator import *

DESCRIPTION = "Test if the model can generate a SQL query to create a database table."

TAGS = ['sql']

question = """
I'm working with a sqlite3 database. Write a query that creates a new database with a table for peoples name, job, and age. Then add a researcher named Nicholas who is 5. Write this directly as a sql query that I can pipe into sqlite3. Do not give the 'sqlite' command, I'll just do `sqlite3 database.db < [your output]`.
"""

def myfn():
    open("/tmp/query.sql", "w").write("SELECT * FROM people;")
    import os
    out = os.popen("sqlite3 -init /tmp/query.sql database.db .exit").read()
    return "Nicholas" in out and "5" in out and "research" in out.lower()


TestSqlMakeTable = question >> LLMRun() >> ExtractCode(manual="I'm going to run `sqlite3 database.db < /tmp/query.sql`. Given the following answer tell me exactly what to put into `query.sql`. DO NOT MODIFY THE CODE OR WRITE NEW CODE.\n<A>") >> Echo() >> SQLRun() >> PyEvaluator(myfn)
                                                                    

if __name__ == "__main__":
    print(run_test(TestSqlMakeTable))
