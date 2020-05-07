from tkinter import *
from Pizza import *
from PIL import ImageTk, Image
import sqlite3
import Pizza


BACKGROUND = "white"

class customer:
    def __init__(self, customer):
        self.frame = Tk()
        self.Customernow = customer
        self.end_results = None
        self.pizzaType = 0
        self.currentPizza = 0

        self.frame.title("Customer")
        self.frame.geometry("800x600+350+150")
        self.frame.config(bg=BACKGROUND)

        self.greeting = Label(self.frame, text="Hi " + self.Customernow, padx=10, pady=10).pack()

        mainframe = LabelFrame(self.frame, bg=BACKGROUND, width=25, height=15).pack(fill='both', expand=True, padx=20, pady=20)

        self.selectPizzaButton = Button(self.frame, text="Select", width=10, padx=10, pady=10, command=self.selectPizzaOnClick).pack()
        self.ExtBut = Button(self.frame, text="Extensions", width=10, padx=10, pady=10, command=self.extensionsOnClick).pack()

        self.OrdBut = Button(self.frame, text="Order", width=7, pady=5, command=self.orderOnClick).pack(side=BOTTOM)

    

    def selectPizzaOnClick(self):
        pizzaScreen = Toplevel(self.frame)
        pizzaScreen.title("Select your Pizza")
        pizzaScreen.geometry("+500+200")
        pizzaList = Listbox(pizzaScreen)

        db = sqlite3.connect("pizza_list.db")
        c = db.cursor()
        try:
        	c.execute("""CREATE TABLE pizzas_table (
        			pizzas text,
        			prices integer,
        			ingredients_list text
        	)""")
        except:
        	pass
        db.commit()
        for i in (c.execute("SELECT pizzas FROM pizzas_table")):
            pizzaList.insert(END,i[0])
        db.commit()

        def selectPizzaType():
            pizzaType = pizzaList.get(ANCHOR)
            self.currentPizza = Pizza.PizzaBuilder(self.pizzaType)
            c.execute("SELECT prices FROM pizzas_table WHERE pizzas=?",(pizzaType,))
            pizzaScreen.destroy()
            db.close()

        choosebut = Button(pizzaScreen,text = "Select", command = selectPizzaType)
    
        pizzaList.pack()
        choosebut.pack()

    def extensionsOnClick(self):
        extensframe = Toplevel(self.frame)
        extensframe.title("Extensions")
        extensframe.geometry("300x300+500+200")
        extensionsList = Listbox(extensframe, selectmod=MULTIPLE)

        db = sqlite3.connect("extensions.db")
        c = db.cursor()
        try:
            c.execute("""CREATE TABLE extensions (
                        name text
                )""")
        except:
            pass
        db.commit()

        for i in (c.execute("SELECT name FROM extensions")):
            extensionsList.insert(END, i[0])
        db.commit()

        def selectExtensions():
            list_of_results = list()
            selections = extensionsList.curselection()

            for i in selections:
                list_of_results.append(extensionsList.get(i))
            for val in list_of_results:
                c.execute("SELECT name FROM extensions WHERE name=?", (val,))
                self.currentPizza.add_extention(str(val))

            db.close()
            extensframe.destroy()

        choosebut = Button(extensframe,text = "Select", command=selectExtensions)
        extensionsList.pack()
        choosebut.pack()


    def orderOnClick(self):
        if self.end_results != None:
            self.end_results.destroy()
        self.end_results = Label(self.frame, text= "Pizza: " + self.currentPizza.get_status() + "\n" + "Price: " + str(self.currentPizza.get_price()))
        self.end_results.pack()