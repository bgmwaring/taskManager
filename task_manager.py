#====Import Librarys====
from datetime import date as d
import datetime 

#====Function Section====

# checks username and password are correct
def login(user, password):
    
    with open("user.txt", "r") as f:
        
        lines = f.readlines()
        
        for line in lines:
            
            details = line.split(",")
            if details[0].strip() == user and details[1].strip() == password:
                return True
            
        return False

# check just username
def user_check(user):
    
    with open("user.txt", "r") as f:
        
        lines = f.readlines()
        
        for line in lines:
            
            details = line.split(",")
            if details[0].strip() == user:
                return False
            
        return True
    
# checks user is admin and add new user
def reg_user(user):
    
    if (user == "admin"):
        # request input for username
        username = input("Enter username: ")
        
        # check username doesn't exist
        while not user_check(username):
            print(f"The username {username} already exists.")
            username = input("Enter username: ")
            
        # request input for password and conformation
        password1 = input("Enter a password: ")
        password2 = input("Enter the same password again: ")
        
        # record information if passwords are the same
        if (password1 == password2):
            
            with open("user.txt", "a") as f:
                f.write("\n" + username + ", " + password1)
        else:
            print("Error passwords did not match!")
    
    else:
        print("Only admin can register a user.")

# add new task
def add_task():
    
    # request information for task
    user = input("Enter username of task recipient: ")
    title = input("Enter task name: ")
    desc = input("Enter task description: ")
    due = input("Enter task due date: ")
    date = str(d.today())
    
    # record information
    with open("tasks.txt", "a") as f:
        f.write("\n" + user + ", " + title + ", " + desc + ", " + due + ", " + date + ", " + "no")

# prints all task infomation
def view_all():
    
    # print all task information
    with open("tasks.txt", "r") as f:
        
        lines = f.readlines()
        count = 0
        
        for line in lines:
            line = line.strip()
            x = line.split(",")
            
            # count tasks
            count += 1
            
            print(f'''
                  _________________________________________________________
                                                                      #{count}
                  Task:                     {x[1]}
                  Assigned to:               {x[0]}
                  Date assigned:            {x[4]}
                  Due date:                 {x[3]}
                  Task complete?            {x[5]}
                      
                  Use task_manager.py to assign each team member tasks
                  _________________________________________________________
                  ''')
                  
# select task by number
def pick_task(number):
    
    # print all task information
    with open("tasks.txt", "r") as f:
        
        lines = f.readlines()
        count = 0
        
        # create storage to record task position in whole document
        full_task_index = -1
        
        for line in lines:
            line = line.strip()
            x = line.split(",")
            
            full_task_index += 1
            
            if (x[0] == user):
                
                # count tasks
                count += 1
                
                if count == number:
                    print(f'''
                          _________________________________________________________
                                                                              #{count}
                          Task:                     {x[1]}
                          Assigned to:               {x[0]}
                          Date assigned:            {x[4]}
                          Due date:                 {x[3]}
                          Task complete?            {x[5]}
                              
                          Use task_manager.py to assign each team member tasks
                          _________________________________________________________
                          ''')
                          
                    return full_task_index
                
# print user task info
def view_mine():
    
    with open("tasks.txt", "r") as f:
        
        lines = f.readlines()
        count = 0
        
        # check each lines username
        for i in range(0, len(lines)):
            
            x = lines[i].split(", ")
            
            if (x[0] == user):
                
                count += 1
                
                print(f'''
                      _________________________________________________________
                                                                          #{count}
                      Task:                     {x[1]}
                      Assigned to:              {x[0]}
                      Date assigned:            {x[4]}
                      Due date:                 {x[3]}
                      Task complete?            {x[5]}
                          Use task_manager.py to assign each team member tasks
                      _________________________________________________________
                      ''')
                                
def modify(index, new_user):
    
    with open("tasks.txt", "w+") as f:
        
        lines = f.readlines()
        
        # split the line of selected task
        line = lines[index].split(", ")
        
        if line[5] == "no":
            
            # change tasks user and restore it
            line[0] = new_user
            lines[index] = f"{line[0]}, {line[1]}, {line[2]}, {line[3]}, {line[4]}, {line[5]} \n"
            
            # write changes back to text file
            f.writelines(lines)
        
        else:
            print("Cannot modify completed tasks.")
        
def complete(index, condition):
    
    if condition == "yes":
        with open("tasks.txt", "w+") as f:
            
            lines = f.readlines()
            
            # split the line of selected task
            line = lines[index].split(", ")
            
            # change tasks user and restore it
            line[5] = "yes"
            lines[index] = f"{line[0]}, {line[1]}, {line[2]}, {line[3]}, {line[4]}, {line[5]} \n"
            
            # write changes back to text file
            f.writelines(lines)

def report():
    
    # setup statistics
    overdue = 0
    complete = 0
    incomplete = 0
    num_users = None
    user_overdue = 0
    user_complete = 0
    user_incomplete = 0
    
    with open("tasks.txt", "r") as f:
        
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            x = line.split(", ")
            
            # checks for completeness
            if x[5] == "no":
                incomplete += 1
                
                # check if task asigned to user
                if x[0] == user:
                    user_incomplete += 1
                    
                # check if task is overdue
                if datetime.datetime(x[4]) > d.today():
                    overdue += 1
                    
                    # check if task asigned to user
                    if x[0] == user:
                        user_overdue += 1
                    
            elif x[5] == "yes":
                complete += 1
                
                # check if task asigned to user
                if x[0] == user:
                    user_complete += 1
    
    with open("users.txt", "r") as f:
        
        lines = f.readlines()
        num_users = len(lines)
    
    # compute further statistics
    total_tasks = complete + incomplete
    total_user_tasks = user_complete + user_incomplete
    user_proportion = (total_user_tasks/ total_tasks) * 100 
    
    # record stats to file
    with open ("task_overview", "w") as f:
        f.write(f'''
                Total Tasks: {total_tasks}
                Complete: {complete}        {(complete/ (total_tasks)) * 100}
                Incomplete: {incomplete}    {(incomplete/ (total_tasks)) * 100}
                Overdue: {overdue}
                ''')
    
    # record user specific stats to file
    with open ("user_overview", "w") as f:
        f.write(f'''
                Total User Tasks: {total_user_tasks}
                Total Tasks: {total_tasks}
                
                Users Tasks
                    Propution of Total: {user_proportion}
                    Complete: {(user_complete/ total_user_tasks) * 100}
                    Incomplete: {(user_incomplete/ total_user_tasks) * 100}
                    Overdue: {(user_overdue/ total_user_tasks) * 100}
                ''')
                
def stats():
    
    report()
    
    with open ("task_overview", "r") as f:
        print(f)
        
    with open ("user_overview", "r") as f:
        print(f)
        
#====Login Section====

# request username and password
user = input("Enter username: ")
password = input("Enter a password: ")
         
# check username and password       
while not login(user, password):
    print("Username or password incorrect")
    user = input("Enter username: ")
    password = input("Enter a password: ")

#=====Main Section=====

while True:
    # presenting the menu to the user and 
    # making sure that the user input is coneverted to lower case.
        
    if (user == "admin"):
        menu = input('''Select one of the following Options below:
                        r - Registering a user
                        a - Adding a task
                        va - View all tasks
                        vm - View my task
                        s - Statistics
                        gr - Generate Report
                        e - Exit
                        : ''').lower()
                        
    else:
        menu = input('''Select one of the following Options below:
                        r - Registering a user
                        a - Adding a task
                        va - View all tasks
                        vm - View my task
                        e - Exit
                        : ''').lower()

    if menu == 'r':
        
        reg_user(user)
            
    elif menu == 'a':

        add_task()

    elif menu == 'va':
        
       view_all()

    elif menu == 'vm':
            
        view_mine()
        
        # call function to find position of the task in .txt
        index = pick_task(int(input("Select task number to modify: ")))
        
        menu = (input("Would you like to modify or complete task: ").lower())
        
        if menu == "modify":
            modify(index, input("Change assigned user to: ").lower())
            
        elif menu == "complete":
            complete(index, input("Change task to complete: ").lower())
            
        else:
            print("Sorry this choice is unavaliable.")
        
    elif menu == 'e':
        print('Goodbye!!!')
        quit()
    
    elif menu == 's':
        stats()
    
    elif menu == 'gr':
        
        report()
        
    else:
        print("You have made a wrong choice, Please Try again")