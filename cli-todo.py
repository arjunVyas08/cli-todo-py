#cli todo list

import sqlite3 as sql
from dbms import DBMS
import sys

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
            3:self.safe_exit
        }

        self.active = True

    def after(self):
        ent = str(input("enter 'exit' to close the application: "))
        if ent.lower() == "exit":
            self.active = False

            self.safe_exit()  
        else:
            pass
    

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


        while True:
            try:
                option = int(input("select an option by entering the number: "))
            except ValueError:
                print("enter a number")
                continue

            if option in funcs:
                funcs[option]()
                break

            print("index doesnt exist")

        self.after()

    def create(self):
        while True:

            print("creating new task")
            task_name = str(input("enter the name of the task: "))
      
            priority = str(input("enter the priority of the task,H(igh),M(edium) or L(ow):\n\r "))

            if priority.upper() == "H" or priority.upper() == "M" or priority.upper() == "L":
                self.database.create(task_name,priority.upper())
                return
            else:
                confirm = str(input("no valid input detected do you want to continue Y/N: ")).lower()
                if confirm == "n":  
                    print("Returning...")
                    return

                    
       
    def delete(self):

        try:
            targ = int(input("enter the id of the task you want to delete: \n\r"))

        except ValueError:
            print("enter a valid integer")
            return
        row = self.database.get_row(targ)#

        if row == None:
            print(f"No row with index: {targ}\n Returning...")
            return
        else:
            print(f"DELETING: \n{row}")
            confirm = str(input("Is this correct Y/N: ")).lower()

            if confirm == "n":
                print("Returning...")
                return
            elif confirm == "y":
                self.database.delete(targ)
            else:
                print("no valid input")
        


    def update(self):
        try:
            targ = int(input("enter the id of the task that you want to amend: "))
        except ValueError:
            print("enter a valid integer")
            return

        
        row = self.database.get_row(targ)


        #data base returns None if the index doesnt exist
        if row == None:
            print(f"No row with index: {targ}")
            return
        else:
            print(f"editing:{row}")
            confirm = str(input("Is this correct Y/N: ")).lower()

            
            if confirm == "y":

                print("select a field to edit")
                for x in self.database.mut_fields:
                    print(f"[{x}]: {self.database.mut_fields[x]}")

                try:
                    field = int(input("enter the field to be changed:\r\n "))
                    valid = self.database.valid(field)
                    if valid == True:

                        # now to actually edit the task in question
                        self.database.mut_fns[field](targ)
                        return
                    else:
                        print("enter a valid field")

                
                except ValueError:
                    print("Enter a valid int within the specified range")
                    return
                    
            elif confirm == "n":
                return
            else:
                print("invalid input\n\r Returning...")
                return
    
                    

       
    
    def eventloop(self):
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

                
            
    def safe_exit(self):
        self.database.close_conn()
        sys.exit(0)

if __name__ == "__main__":
    app = Task()
    app.eventloop()
