import sqlite3


#This is the table from the database
conn = sqlite3.connect('social.db')
cursorObj = conn.cursor()
cursorObj.execute(
        """CREATE TABLE IF NOT EXISTS social(
            id text PRIMARY KEY,
            username text,
            yearOfBirth integer,
            monthOfBirth integer,
            dayOfBirth integer,
            email text,
            password text,
            gender text)"""
        )
conn.commit()


