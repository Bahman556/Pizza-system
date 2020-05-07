from tkinter import * 
import sqlite3
import customer

class main_menu :
    def __init__ (self, screen, db) :
        self.conn = db
        self.curs = self.conn.cursor()
        Label(text = "Log in and registration  ", bg = "grey", width = "300", height = "2" ).pack()
        self.screen = screen  
        Button(self.screen,text = "Log in", width = "100" , height = "1", font = ("calibri", 13), command = self.open_log_in_screen).pack()
        Label(self.screen,text = "").pack()
        Button(self.screen,text = "Register", width = "100" , height = "1", font = ("calibri", 13), command = self.open_registration_screen).pack()
    
    def open_registration_screen(self):
        self.screen1 = Toplevel(self.screen)
        self.screen1.title("Registration")
        self.screen1.geometry("300x200")
        reg = registration(self.screen1, self.conn)
    
    def open_log_in_screen(self):
        self.screen2 = Toplevel(self.screen)
        self.screen2.title("Registration")
        self.screen2.geometry("300x200")
        log = login(self.screen2, self.conn)

class login:
    def __init__ (self , screen2, db) :
        self.db = db
        self.c = self.db.cursor()
        self.screen2 = screen2      
        Label(self.screen2, text = "Please enter details ").pack
        Label(self.screen2, text = "").pack 
        Label(self.screen2, text = "Enter Username ").pack()
        self.login_username = Entry(self.screen2)
        self.login_username.pack()
        Label(self.screen2 , text = "").pack 
        Label(self.screen2, text = "Enter Password ")
        self.login_password = Entry(self.screen2)
        self.login_password.pack()
        Button(self.screen2 , text = "Log in ", width = "10" , height ="1", command = self.log_in).pack()
    def log_in (self):
        #print(self.login_password.get())
        self.c.execute("SELECT rowid FROM users WHERE login = ?", (str(self.login_username.get()),)) 
        if len(self.c.fetchall()) == 0:
            myLabel = Label(self.screen2, text = 'This user is not found ').pack()
        else:
            a = customer.customer(str(self.login_username.get()))

class registration:
    def __init__ (self , screen1, db) :
        self.db = db
        self.c = self.db.cursor()
        self.screen1 = screen1      
        Label(self.screen1, text = "Please enter details ").pack
        Label(self.screen1, text = "").pack 
        Label(self.screen1, text = "Enter Username ").pack()
        self.login_username = Entry(self.screen1)
        self.login_username.pack()
        Label(self.screen1 , text = "").pack 
        Label(self.screen1, text = "Enter Password ")
        self.login_password = Entry(self.screen1)
        self.login_password.pack()
        Button(self.screen1 , text = "Register ", width = "10" , height ="1", command = self.register).pack()

    def register(self):
        #print(self.login_password.get())
        self.c.execute("SELECT rowid FROM users WHERE login = ?", (str(self.login_username.get()),))
        if len(self.c.fetchall()) == 0:
            user =  User(self.login_username.get(), self.login_password.get(), self.db)
        else:
            Label(self.screen1, text = 'This user already exists').pack()

class User:
    def __init__(self, login, password, db):
        self.login = login
        #print(login)
        self.db = db
        self.password = password
        #print(password)
        self.c = self.db.cursor()
        self.c.execute("SELECT rowid FROM users WHERE login = ?", (str(self.login),))
        if len(self.c.fetchall())==0:
            self.c.execute("INSERT INTO users VALUES (?, ?)", (str(self.login), str(self.password), ))
        #self.c.execute("SELECT * FROM users WHERE login = ?", (str(self.login), ))
        #print(self.c.fetchone())
        self.db.commit()

def  main (): 
    conn = sqlite3.connect('users_list.db')
    c = conn.cursor()
    try:
        c.execute("""CREATE TABLE users (
                login text,
                password text
        )""")
    except:
        pass
    #c.execute("DELETE FROM users WHERE login = 'Bahman'")
    conn.commit()
    screen = Tk()
    screen.geometry("300x200")
    screen.title("Log in or registration ")
    root = main_menu(screen, conn)
    screen.mainloop()

if __name__ == "__main__" :
    main()