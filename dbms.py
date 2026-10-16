import sqlite3 as sql



class DBMS:
    """class that contains all database attributes and methods"""
    def __init__(self, db = "data.db"):
        self.conn = sql.connect(db)
        self.cursor = self.conn.cursor()
        self.create_table()
        self.mut_fields ={
            1:"task",
            2:"priority",
            3:"is_done"
        }

        self.mut_fns ={
            1:self.update_task,
            2:self.update_priority,
            3:self.mark_done
        }

    def valid(self, targ):
        """checks if a value entered by the user is valid"""
        return targ in self.mut_fields
            

    def create_table(self):
        """this will create 1 table to store all tasks, autoincrement primary key
        [id , task , priority , time entered]"""

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS TASKS(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                priority TEXT NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_done INTEGER NOT NULL
            )
        """)
        self.conn.commit()

    def view(self):
        """get all of the entries in the tabel"""
        
        self.cursor.execute(""" SELECT * FROM TASKS""")
        rows = self.cursor.fetchall()

        if len(rows) == 0:#
            print("table is empty, nothing to show")
        else:
            print("getting all entries")
            for row in rows:
                print(row)
            print("finished")
       
    def create(self,task,priority):

        print(f"creating task:{task}, with priority{priority}")

        self.cursor.execute("""INSERT INTO TASKS (task,priority,is_done) VALUES (?,?,?)""",
                            (task,priority,0))

        self.conn.commit()
        
    def update_task(self,id):

        try:
            tasknew = str(input("enter the NEW name of the task"))

            self.cursor.execute ("""UPDATE TASKS
                                    SET task = (?)
                                    WHERE id = (?)""", (tasknew,id))

            self.conn.commit()

        except Exception as e:
            print(f"{e}")

            

    def update_priority(self,id):

        try:
            priority = str(input("enter the priority of the task,H(igh),M(edium) or L(ow): "))
        
            if priority.upper() == "H" or priority.upper() == "M" or priority.upper() == "L":

                self.cursor.execute("""UPDATE TASKS
                                    SET priority =  (?)
                                    WHERE id = (?)""", (priority.upper(), id))

                self.conn.commit()
            else:
                print("invalid input")
        except Exception as e:
            print(f"{e}")
                    
       
    def mark_done(self,id):
        try:
            is_done = int(input("enter either 1 or 0 to represent whether the task is done or not"))

            if is_done == 0 or is_done == 1:
                self.cursor.execute("""UPDATE TASKS
                                        SET is_done = (?)
                                        WHERE id = (?)""", (is_done, id))
            
                self.conn.commit()

            else:
                print("invalid input")
                return
        except Exception as e:
            print(e)

    
    def get_row(self,id):
        """gets a row with a target id , returns None if no row with the id exists"""
        self.cursor.execute("""SELECT * FROM TASKS WHERE id = (?)""",
                            (id,))
        
        row = self.cursor.fetchone() # fetchone doesnt crash for out of index
        
        return row

    def delete(self,id):
        # dead code that was going to ensure that there were no gaps in the ids of the database
        #self.cursor.execute("""SELECT * FROM TASKS WHERE id > (?) """, (id,))

        #rows = self.cursor.fetchall()

        self.cursor.execute("""DELETE
                           FROM TASKS
                          WHERE id = (?)""", (id,))

        self.conn.commit()

        # this would have gotten filled the gaps left by deleting the taks
        #for row in rows:
    
            #self.cursor.execute("""UPDATE TASKS
             #                       SET id = (?)
              #                      WHERE id = (?)""",(row[0] - 1 , row[0]))

        # this however messes with sqlite and causes issues later down the line since sqlite has its own internal count
        # that isnt reliant on the id's of the database :(

    def close_conn(self):
        self.conn.close()

