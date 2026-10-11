#cli todo list

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
            3:"is done"
        }

    def valid(self,field):
        for i in self.mut_fields:
            if field == self.mut_fields[i]:
                return True

        return False

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
        
    def update(self,id):
        
        pass
        
        
    def get_row(self,id):
        print(f"{id}")
        
        self.cursor.execute("""SELECT * FROM TASKS WHERE id = (?)""",
                            (id))
        
        row = self.cursor.execute()

        return row




class Task:
    def __init__(self):
        self.database = DBMS()

        self.options = {
            1:"view",
            2:"edit",
            3:"exit"
        }
        self.funcs = {
            1:self.view,
            2:self.edit,
            3:exit
        }

        self.active = True

    def after(self):
        ent = str(input("enter 'exit' to close the application: "))
        if ent.lower() == "exit":
            self.active = False
        else:
            exit
    

    def view(self):
        self.database.view()
        self.after()
            
    def edit(self):
        """editing tasks, includes adding new, or updating old"""
        print("editing")
        
        choices = {
            1:"create",
            2:"delete",
            3:"update"
        }

        funcs = {
            1:self.create,
            2:self.delete,
            3:self.update,
        }

        for x in choices:
            print(f"[{x}]:{choices[x]}")

        satis = False
        
        while not satis:
            try:
                option = int(input("select an option by entering the number: "))
                funcs[option]()
                satis = True

            except ValueError:
                print("enter a number")

            self.after()

    def create(self):
        print("creating new task")

        task_name = str(input("enter the name of the task: "))
        satis = False

        while not satis:
            priority = str(input("enter the priority of the task,H(igh),M(edium) or L(ow): "))


            if priority.upper() == "H" or priority.upper() == "M" or priority.upper() == "L":
                satis = True
                self.database.create(task_name,priority.upper())

        
        pass
    def delete(self):
        pass
    def update(self):

        targ = int(input("enter the id of the task that you want to amend: "))
        row = self.database.get_row(targ)

        if row == None:
            print(f"No row with index: {id}")
            self.after()
        else:
            print(f"editing:{row}")
            confirm = str(input("Is this correct Y/N: ")).lower()

            satis = False
            while not satis:
                if confirm == "y":

                    field = str(input("enter the field to be changed: ")).lower()
                    valid = self.database.valid(field)
                    if valid == True:
                        satis = True
                    else:
                        print("enter a valid field")

                    pass
                elif confirm == "n":
                    pass
                else:
                    pass

       
    
    def eventloop(self):
        self.database.create_table()

        print("---CLI todolist---")


        while self.active:
            
            #input validation condition
            satis = False

            while not satis:
                for x in self.options:
                    print(f"[{x}]:{self.options[x]}")

                try:
                    option = int(input("select an option by entering the number"))

                    if option in self.options:
                        satis = True
                        self.funcs[option]()
                    else:
                        print("enter a number within that corresponds to a choice")
                        pass
                except ValueError:
                    print("enter a number")


        exit()
                
            
        

if __name__ == "__main__":
    app = Task()
    app.eventloop()
