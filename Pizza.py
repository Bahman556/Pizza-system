import abc
from abc import ABCMeta
import sqlite3



class Pizza(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_price(self):
        pass
    @abc.abstractmethod
    def get_status(self):
        pass


class Concrete_Pizza(Pizza):
    pizza_price=0
    def __init__(self, ingredients, price):
        self.pizza_price = price
        self.ingredients = ingredients
    def get_price(self):
        return self.pizza_price
    def get_status(self):
        return self.ingredients

class PizzaDecorator(Pizza):
    def __init__(self, pizza):
        self.pizza=pizza
    
    def get_price(self):
        return self.pizza.get_price()
    
    def get_status(self):
        return self.pizza.get_status()
		
#==================================================

class MozarellaCheese(PizzaDecorator):
	def __init__(self, pizza):
		super(MozarellaCheese, self).__init__(pizza)
		self.__cheese_price = 2

	@property
	def price(self):
		return self.__cheese_price

	def get_price(self):
		return super(MozarellaCheese, self).get_price() + self.__cheese_price

	def get_status(self):
		return str(super(MozarellaCheese, self).get_status()) + ", Mozarella Cheese" 

class Beef(PizzaDecorator):
	def __init__(self, pizza):
		super(Beef, self).__init__(pizza)
		self.__beef_price = 4

	@property
	def price(self):
		return self.__beef_price

	def get_price(self):
		return super(Beef, self).get_price() + self.__beef_price

	def get_status(self):
		return str(super(Beef, self).get_status()) + ", Beef"


class BBQSauce(PizzaDecorator):
	def __init__(self, pizza):
		super(BBQSauce, self).__init__(pizza)
		self.__bbq_sauce_price = 3

	@property
	def price(self):
		return self.__bbq_sauce_price

	def get_price(self):
		return super(BBQSauce, self).get_price() + self.__bbq_sauce_price

	def get_status(self):
		return str(super(BBQSauce, self).get_status()) + ", BBQ Sauce"



class ExtraKetchup(PizzaDecorator):
	def __init__(self, pizza):
		super(ExtraKetchup, self).__init__(pizza)
		self.__ketchup_price = 1

	@property
	def price(self):
		return self.__ketchup_price

	def get_price(self):
		return super(ExtraKetchup, self).get_price() + self.__ketchup_price

	def get_status(self):
		return str(super(ExtraKetchup, self).get_status()) + ", Extra Ketchup"

#===================================================================================

class PizzaBuilder:
    def __init__(self, pizza_type):
        self.file = sqlite3.connect('pizza_list.db')
        self.cursor = self.file.cursor()
        #self.cursor.execute("DELETE FROM pizzas_table WHERE pizzas = 'Barbeque'")
        self.file.commit()
        self.pizza = 0
        self.extentions_list = []
        try:
        	self.c.execute("""CREATE TABLE pizzas_table (
        			pizzas text,
        			prices integer,
        			ingredients_list text
        	)""")
        except:
        	pass
        self.cursor.execute("SELECT rowid FROM pizzas_table WHERE pizzas = 'Barbeque'")
        if len(self.cursor.fetchall())==0:
            self.cursor.execute("INSERT INTO pizzas_table VALUES(?,?,?)", ('Barbeque', 15, 'GrilledChicken, Mushrooms, BBQSauce, MozzarellaCheese',))
        self.cursor.execute("SELECT rowid FROM pizzas_table WHERE pizzas = 'Margheritta'")
        if len(self.cursor.fetchall())==0:
            self.cursor.execute("INSERT INTO pizzas_table VALUES(?,?,?)", ('Margheritta', 16, 'GrilledChicken, Mushrooms, Pepper, Onions, MozzarellaCheese',))
        self.file.commit()
        self.cursor.execute("SELECT rowid FROM pizzas_table WHERE pizzas = ?", (str(pizza_type),))
        if len(self.cursor.fetchall())!=0:
            self.cursor.execute("SELECT prices FROM pizzas_table WHERE pizzas = ?", (str(pizza_type),))
            self.pizza_price = int(list(self.cursor.fetchone())[0])

            self.cursor.execute("SELECT ingredients_list FROM pizzas_table WHERE pizza = ?", (str(pizza_type),))
            self.ingredients = str(list(self.cursor.fetchone())[0])

            self.pizza_type = pizza_type
            self.pizza = Concrete_Pizza(self.ingredients, self.pizza_price)
    
    def add_extention(self, extention):
        self.pizza = eval(extention)(self.pizza)
        self.extentions_list.append(extention)
    
    def remove_extention(self, extention):

        if(extention in self.extentions_list):
            self.extentions_list.remove(extention)

        self.pizza = PizzaBuilder(self.pizza_type)
        for ex in self.extentions_list :
            self.pizza.add_extention(ex)

    def get_price(self):
        return self.pizza.get_price()
    
    def get_status(self):
        return self.pizza.get_status()
