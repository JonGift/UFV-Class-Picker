import sqlite3
import sys

con = sqlite3.connect('classes.db')

#Need: class, price, prerequisites, major, start and end date, day of week, time,

with con:

    cur = con.cursor()

    #cur.execute("DROP TABLE IF EXISTS Books")
    #cur.execute("DROP TABLE IF EXISTS Authors")

    """
    cur.execute("CREATE TABLE Books(Id INT, Name TEXT, AuthorId INT)")
    cur.execute("INSERT INTO Books VALUES(1,'Bridget Jones''s Diary', 1)")
    cur.execute("INSERT INTO Books VALUES(2,'Pride and Prejudice (Dover Thrift Editions)',2)")
    cur.execute("INSERT INTO Books VALUES(3,'The Martian Chronicles',3)")

    cur.execute("CREATE TABLE Authors(Id INT, Name TEXT)")
    cur.execute("INSERT INTO Authors VALUES(1,'Helen Fielding')")
    cur.execute("INSERT INTO Authors VALUES(2,'Jane Austen')")
    cur.execute("INSERT INTO Authors VALUES(3,'Ray Bradbury')")

    cur.execute("SELECT * FROM Books, Authors")

"""
    #rows = cur.fetchall()

    #for row in rows:
      #  print(row)
