from tkinter.ttk import *
from tkinter import *
import random as rnd


# time to constantly change without having to refresh the tablet: (wait, might be really ez)
# what happens at closing times?

win = Tk()

# some attributes
my_machines = []
shop_preferability = 50
# store_spinboxes = {"Coffee": coffee_spinbox, "Decaf Coffee": decaf_spinbox, "Sugar": sugar_spinbox, "Water": water_refill_spinbox}
time_settings = {"time": 7, "day_time_corresponds": {"morning": [7, 14], 'afternoon': [15, 18], "evening": [19, 20]},
                 "day_time_preferences": {"morning": {"Normal": [1, 7], "Double": [8, 9], 'Decaf': [10]}, "afternoon": {"Normal": [1, 3], "Double": [4, 7], 'Decaf': [8, 10]}, "evening": {"Normal": [1, 3], "Double": [4, 9], 'Decaf': [10]}}, "perfect_days": 0,"days_passed": 0}
attraction = {"possible_values": [[0, 1], [2, 4], [5]], "attraction_index": 1, "current_attraction": 1, "mistake_number_in_a_day": 0}

ingredients = {"report": {"Water": 1000, "Milk": 500, "Coffee": 100, "Sugar": 100, "Decaf Coffee": 50, "money": 0},
               "prices": {"Water": {"for": 25, "price": 0.1}, "Milk": {"for": 20, "price": 0.5}, "Coffee": {"for": 20, "price": 0.4}, "Sugar": {"for": 20, "price": 0.3}, "Decaf Coffee": {"for": 20, "price": 0.5}},
               "Espresso": {"ingredients": {"Water": 50, "Coffee": 18, "Milk": 0}, "price": 1.5},
               "Latte": {"ingredients": {"Water": 200, "Coffee": 24, "Milk": 150}, "price": 2.5},
               "Cappuccino": {"ingredients": {"Water": 250, "Coffee": 24, "Milk": 100}, "price": 3}}
counters = {"counter1": None, "counter2": None, "other3": [], "leftovers": [], "machines": []}

# needed function to clear a window when moving to another screen
def clear_window():
    for widget in win.winfo_children():
        widget.pack_forget()
        widget.grid_forget()

# images
note_icon_image = PhotoImage(file="pics/Note_icon.png")
store_icon_image = PhotoImage(file="pics/store_icon.png")
coffee_machine_image = PhotoImage(file="pics/coffee_machine_hopefully.png")
add_coffee_machine_image = PhotoImage(file="pics/add_coffee_machine.png")
cash_register_image = PhotoImage(file="pics/cash_register.png")
order_paper_image = PhotoImage(file="pics/order_paper.png")
# classes



# Problems:
# coffee specifications in a coffee machine are not shown, so mistakes are imminent.
# possible solutions: leave it or fix it
# customers after closing times remain and idk what to do with them
# possible solutions: make them stay for a specific duration depending on when they arrived OR make them leave immediately, adding up to the mistakes possibly ruining reputation..

# variables
coffee_kind = StringVar(value="Espresso")

coffee_strength = StringVar(value="Normal")

sweetness = StringVar(value="Black")
def show_warning(text):
    label = Label(text=text, fg="red")
    label.place(x=(win.winfo_width()//2-label.winfo_width())//2, y=win.winfo_height()//2)
    win.after(2000, label.place_forget)
# classes
class CoffeeMachine(Canvas):
    def __init__(self, id):
        super().__init__()
        # self.pack()
        self.id = id
        self.config(width=50, height=50)
        self.button = Button(self, image=coffee_machine_image, command=lambda: self.customise_coffee() if self.in_use == False else self.serve_coffee())
        self.button.grid(row=0, column=0)
        self.status = Progressbar(self, length=100, orient="horizontal", mode="determinate")



        self.status.grid(row=1, column=0)
        self.coffee_specs = Label()
        self.coffee_specs.grid(row=2, column=0)
        self.in_use = False
        self.coffee_in = None

    def finish_order(self):
        self.status['value'] = 0
        self.coffee_in = None
        self.in_use = False
    def make_coffee(self, ingredients_needed=None, coffee=None):


        reserves = ingredients["report"]


        # see if the ingredients you have are sufficient


        if coffee is None:

            base_coffee = ingredients[coffee_kind.get()]["ingredients"]
            ingredients_needed = {"Sugar": {"Black": 0, "Medium": 6, "Sweet": 12}[sweetness.get()]}
            coffee = {"kind": coffee_kind.get(), "strength": coffee_strength.get(), "sweetness": sweetness.get(), "origin_id": self.id}
            for _ in base_coffee:
                if base_coffee[_] == "Coffee":
                    if coffee_strength.get() == "Decaf":
                        ingredients_needed["Decaf Coffee"] = base_coffee[_]
                    elif coffee_strength.get() == "Normal":
                        ingredients_needed[_] = base_coffee[_]
                    else:
                        ingredients_needed[_] = base_coffee[_] * 2
                else:
                    ingredients_needed[_] = base_coffee[_]

            for ingredient in ingredients_needed:
                if ingredients_needed[ingredient] > reserves[ingredient]:
                    return show_warning(f"Not enough {ingredient.lower()}")



        self.in_use = True



        if self.status['value'] < 100:
            self.status['value'] += 2


            if self.status['value'] == 100:
                self.coffee_in = coffee
                self.coffee_specs.config(text=f"{coffee["kind"]}\n{coffee["strength"]}\n{coffee["sweetness"]}")

                for ingredient in ingredients_needed:
                    reserves[ingredient] -= ingredients_needed[ingredient]





            else:

                return win.after(200, self.make_coffee, ingredients_needed, coffee)

    def serve_coffee(self):
        if not self.coffee_in is None:
            registers()
            coffee_av.config(text=f"{self.coffee_in["kind"]}\n{self.coffee_in["strength"]}\n{self.coffee_in["sweetness"]}")
            coffee_av.grid(row=0, column=2)
            self.coffee_specs.config(text="")
            counters["machine1"].button.config(command=lambda: check_order(coffee=self.coffee_in, order=counters["counter1"], register="counter1"))
            counters["machine2"].button.config(command=lambda: check_order(coffee=self.coffee_in, order=counters["counter2"], register="counter2"))

    def customise_coffee(self):
        clear_window()
        #       kind
        Label(text="Coffee Kind").grid(row=0, column=0)
        Radiobutton(text="Espresso", variable=coffee_kind, value="Espresso").grid(row=1, column=0)
        Radiobutton(text="Cappuccino", variable=coffee_kind, value="Cappuccino").grid(row=2, column=0)
        Radiobutton(text="Latte", variable=coffee_kind, value="Latte").grid(row=3, column=0)

        #       strength
        Label(text="Coffee Strength").grid(row=0, column=1)
        Radiobutton(text="Normal", variable=coffee_strength, value="Normal").grid(row=1, column=1)
        Radiobutton(text="Decaf", variable=coffee_strength, value="Decaf").grid(row=2, column=1)
        Radiobutton(text="Double", variable=coffee_strength, value="Double").grid(row=3, column=1)

        #       sweetness
        Label(text="Sweetness").grid(row=0, column=2)
        Radiobutton(text="Black", variable=sweetness, value="Black").grid(row=1, column=2)
        Radiobutton(text="Medium (one to one ratio)", variable=sweetness, value="Medium").grid(row=2, column=2)
        Radiobutton(text="Sweet (two to one ratio)", variable=sweetness, value="Sweet").grid(row=3, column=2)
        def func():
            self.make_coffee()
            machines_room()
        Button(text="Make Coffee", command=func).grid(row=4, column=0)


        Button(text="<--", command=machines_room).grid(row=4, column=1)


class CashRegister(Canvas):
    def __init__(self):
        super().__init__()
        self.config(bg="pink")
        self.button = Button(self, image=cash_register_image)
        self.button.pack()


def check_order(coffee, order, register):

    if coffee["kind"] == order["Coffee_type"] and coffee["strength"] == order["strength"] and coffee["sweetness"] == order["sweetness"]:
        ingredients["report"]["money"] += ingredients[coffee["kind"]]["price"]



    else:
        # While trying to copy the kindness of humanity by adding a randomness value is something to be considered from impossible to even hubris, that is what humans are best designed to do
        if rnd.randint(1, 3) == 1:
            ingredients["report"]["money"] += ingredients[coffee["coffee_kind"]]["price"]
        attraction["mistake_number_in_a_day"] += 1
        show_warning("You got the order wrong")
    counters[register] = None
    counters["machine2"].button.config(command=N)
    counters["machine1"].button.config(command=N)

    for _ in my_machines:
        if _.id == coffee["origin_id"]:
            _.finish_order()

    coffee_av.grid_forget()

# dif_screens

# machines room where you will work
def new_machine(button):
    if len(my_machines) < 5:
        if ingredients["report"]["money"] >= 60:

            '''make it work when there's enough money'''


            my_machines.append(CoffeeMachine(id=len(my_machines) + 1))
            machines_room()
            show_warning("-$60")
        else:
            show_warning("Not enough money")
    else:
        button.config(text="Already reached max coffee machine limit", state='disabled')

new_button = Button(text="Add coffee machine ($60) ", fg='black', command=lambda: new_machine(button=new_button),
                        image=add_coffee_machine_image, compound=LEFT)


def machines_room():
    clear_window()
    for machine in my_machines:
        machine.grid(column=machine.id-1, row=0)
    return_to_registers_button.grid(column=0, row=1)


    new_button.grid(column=1, row=1)

def orders():
    '''    {"Coffee_type": rnd.choice(["Latte", "Espresso", "Cappuccino"]),
     "sweetness": rnd.choice(["Black", "Medium", "Sweet"]), "waiting_time": 0}'''
    clear_window()
    counter1 = counters["counter1"]
    counter2 = counters["counter2"]

    if counter1 != None:
        c_1 = Canvas(win, width=130, height=180)
        c_1.grid(row=1, column=0)

        c_1.create_image(65, 90, image=order_paper_image, anchor="center")
        c_1.create_text(70, 15, text="Register One", font=("Helvetica", 9))
        c_1.create_text(70, 35, text=counter1["Coffee_type"], font=("Helvetica", 16))
        c_1.create_text(55, 70, text=counter1["sweetness"], font=("Helvetica", 16))
        c_1.create_text(50, 125, text=counter1["strength"], font=("Helvetica", 16))
    if counters["counter2"] != None:
        c_2 = Canvas(win, width=130, height=180)
        c_2.grid(row=1, column=1)
        c_2.create_image(65, 90, image=order_paper_image, anchor="center")
        c_2.create_text(70, 15, text="Register Two", font=("Helvetica", 9))

        c_2.create_text(70, 35, text=counter2["Coffee_type"], font=("Helvetica", 16))
        c_2.create_text(55, 70, text=counter2["sweetness"], font=("Helvetica", 16))
        c_2.create_text(50, 125, text=counter2["strength"], font=("Helvetica", 16))
    for _ in range(len(counters["other3"])):
        order = counters["other3"][_]
        c =  Canvas(win, width=130, height=180)
        c.grid(row=1, column=_+2)
        c.create_image(65, 90, image=order_paper_image, anchor="center")
        c.create_text(70, 35, text=order["Coffee_type"], font=("Helvetica", 16))
        c.create_text(55, 70, text=order["sweetness"], font=("Helvetica", 16))
        c.create_text(50, 125, text=order["strength"], font=("Helvetica", 16))
    return_to_registers_button.grid(row=0, column=0)
orders_button = Button(command=orders, text="Check Orders")

my_machines.append(CoffeeMachine(1))
counters["machine1"] = CashRegister()
counters["machine2"] = CashRegister()
machine_room_button = Button(text="Go to machines", command=machines_room)



# registers
# {"report": {"Water": 300, "Milk": 200, "Coffee": 100, "Sugar": 100, "money": 0, "Decaf Coffee": 50}
def buy_it(spinbox: Spinbox, ingredient):
    budget = ingredients["report"]["money"]
    amount = int(spinbox.get())
    price = amount / ingredients["prices"][ingredient]["for"] * ingredients["prices"][ingredient]["price"]
    if price > budget:
        return show_warning("Not enough money")
    ingredients["report"][ingredient] += amount
    ingredients["report"]["money"] -= price

coffee_spinbox = Spinbox(values=("0", '20', '40', '60', '80', '100'))
coffee_button = Button(text="Buy", command=lambda: buy_it(coffee_spinbox, "Coffee"))
decaf_spinbox = Spinbox(values=("0", '20', '40', '60', '80', '100'))
decaf_button = Button(text="Buy", command=lambda: buy_it(decaf_spinbox, "Decaf Coffee"))
milk_spinbox = Spinbox(values=("0", "20", "40", "80", "100"))
milk_button = Button(text="Buy", command=lambda: buy_it(milk_spinbox, "Milk"))
sugar_spinbox = Spinbox(values=("0", '20', '40', '60', '80', '100'))
sugar_button = Button(text="Buy", command=lambda: buy_it(sugar_spinbox, "Sugar"))
water_refill_spinbox = Spinbox(values=("0", '25', '50', '100', '200', '500'))
water_button = Button(text="Buy", command=lambda: buy_it(water_refill_spinbox, "Water"))


def shop_app():
    clear_window()
    Label(text="The shop", width=10, height=10).grid(row=0, column=0)
    Label(text=f"Coffee - ${ingredients['prices']['Coffee']["price"]} for every {ingredients["prices"]["Coffee"]["for"]} gr").grid(row=1, column=0)
    coffee_spinbox.grid(row=2, column=0)
    coffee_button.grid(row=2, column=1)
    Label(text=f"Decaf Coffee - ${ingredients['prices']['Decaf Coffee']["price"]} for every {ingredients["prices"]["Decaf Coffee"]["for"]} gr").grid(row=3, column=0)
    decaf_spinbox.grid(row=4, column=0)
    decaf_button.grid(row=4, column=1)
    Label(text=f"Milk - ${ingredients['prices']['Milk']["price"]} for every {ingredients["prices"]["Milk"]["for"]} ml").grid(row=5, column=0)
    milk_spinbox.grid(row=6, column=0)
    milk_button.grid(row=6, column=1)
    Label(text=f"Sugar - ${ingredients['prices']['Sugar']["price"]} for every {ingredients["prices"]["Sugar"]["for"]} gr").grid(row=7, column=0)
    sugar_spinbox.grid(row=8, column=0)
    sugar_button.grid(row=8, column=1)
    Label(text=f"Water - ${ingredients['prices']['Water']["price"]} for every {ingredients["prices"]["Water"]["for"]} ml").grid(row=9, column=0)
    water_refill_spinbox.grid(row=10, column=0)
    water_button.grid(row=10, column=1)
    Button(text="<--", command=tablet).grid(row=11, column=1)
customer_count = Label()
time_label = Label()
def report_app():
    clear_window()
    key_list = list(ingredients["report"].keys())
    for material in key_list:
        if material in ["Water", "Milk"]:
            Label(text=f"{material}: {ingredients["report"][material]} ml").grid(row=key_list.index(material), column=0)
        elif material in ["Coffee", "Decaf Coffee", "Sugar"]:
            Label(text=f"{material}: {ingredients["report"][material]} gr").grid(row=key_list.index(material), column=0)
        else:
            Label(text=f"{material}: ${ingredients["report"][material]}").grid(row=key_list.index(material), column=0)

        time_label.grid(row=0, column=1)

        customer_count.grid(column=1, row=1)
        Label(text=f"store rating:\n {(1 + attraction["attraction_index"]*2)*"⭐"}").grid(row=2, column=1)
        Button(text="<--", command=tablet).grid(row=11, column=1)

# finished i think wasnt because i changed smthn else
coffee_av = Label()
def registers():
    clear_window()
    counters["machine1"].grid(column=0, row=0)
    counters["machine2"].grid(column=1, row=0)
    Button(command=tablet, text="Tablet").grid(column=1, row=1)
    machine_room_button.grid(row=1, column=0)
    orders_button.grid(row=1, column=2)


# See available materials, buy more, buy machines
def tablet():
    clear_window()
    Button(text="Shop App", command=shop_app, image=store_icon_image, compound=TOP).grid(row=0, column=0)
    Button(text="Report App", command=report_app, image=note_icon_image, compound=TOP).grid(row=0, column=1)
    Button(text="Leave", command=registers).grid(row=1, column=0)

#   shop app with materials and machines



#   resources checking app



return_to_registers_button = Button(text="return to the registers", command=registers)


registers()


def update_people_status():
    people = 0
    if counters["counter1"] != None:
        people += 1
    if counters["counter2"] != None:
        people += 1
    people += len(counters["other3"]) + len(counters["leftovers"])
    customer_count.config(text=f"current customers: {people}")
def arrivals(time_passing):
    if time_settings["time"] == 21:

        time_settings["time"] = 6
        time_settings["days_passed"] += 1
    time_label.config(text=f"Time: {time_settings["time"]}: {time_passing}")
    time_passing += 1

    if counters["counter1"] == None:
        if len(counters["other3"]) > 0:
            counters["counter1"] = counters["other3"][0]
            counters["other3"].pop(0)
            if len(counters["leftovers"]) > 0:
                counters["other3"].append(counters["leftovers"][0])
                counters["leftovers"].pop(0)

    if counters["counter2"] == None:
        if len(counters["other3"]) > 0:
            counters["counter2"] = counters["other3"][0]
            counters["other3"].pop(0)
            if len(counters["leftovers"]) > 0:
                counters["other3"].append(counters["leftovers"][0])
                counters["leftovers"].pop(0)
    update_people_status()
    if time_passing == 60:

        time_passing = 0

        time_settings["time"] += 1

        current_time = time_settings["time"]

        times = time_settings["day_time_corresponds"]

        for time in times:
            if current_time in range(times[time][0], times[time][-1]+1):
                time_period = time
                attractiveness = attraction["possible_values"][attraction["attraction_index"]]
                new_customers = rnd.randint(attractiveness[0], attractiveness[-1])
                for customer in range(new_customers):
                    randnum = rnd.randint(1, 10)
                    current_preference = time_settings["day_time_preferences"][time_period]
                    coffee_expectation = {"Coffee_type": rnd.choice(["Latte", "Espresso", "Cappuccino"]), "sweetness": rnd.choice(["Black", "Medium", "Sweet"]), "waiting_time": 0}
                    for coffee_type in current_preference:
                        if randnum in range(current_preference[coffee_type][0], current_preference[coffee_type][-1]+1):
                            coffee_expectation["strength"] = coffee_type





                    if counters["counter1"] == None:
                        counters["counter1"] = coffee_expectation
                    elif counters["counter2"] == None:
                        counters["counter2"] = coffee_expectation
                        counters["counter1"]["waiting_time"] += 1
                    else:
                        counters["counter1"]["waiting_time"] += 1
                        counters["counter2"]["waiting_time"] += 1
                        for customer in counters["leftovers"]:
                            customer["waiting_time"] += 1
                        if len(counters["other3"]) < 3:
                            counters["other3"].append(coffee_expectation)
                        else:
                            counters["leftovers"].append(coffee_expectation)

                return win.after(1000, arrivals, time_passing)

        if current_time == 21:
            starting_screen()

            if counters["counter1"] != None:
                counters["counter1"] = None
                attraction["mistake_number_in_a_day"] += 1
            if counters["counter2"] != None:
                counters["counter2"] = None
                attraction["mistake_number_in_a_day"] += 1
            for _ in counters["other3"]:
                counters["other3"].remove(_)
                attraction["mistake_number_in_a_day"] += 1
            for _ in counters["leftovers"]:
                counters["leftovers"].remove(_)
                attraction["mistake_number_in_a_day"] += 1
            if attraction["mistake_number_in_a_day"] >= 10:
                if attraction["attraction_index"] > 0:
                    attraction["attraction_index"] -= 1
            else:
                if attraction["mistake_number_in_a_day"] == 0:

                    time_settings["perfect_days"] += 1
                    if time_settings["perfect_days"] == 3 and attraction["attraction_index"] < 2:
                        attraction["attraction_index"] += 1
                        time_settings["perfect_days"] = 0

                else:
                    time_settings["perfect_days"] = 0
            starting_screen()

    return win.after(1000, arrivals, time_passing)





def starting_screen():
    clear_window()
    Label().grid(row=0, column=0)
    if time_settings["days_passed"] == 0:
        Label(text="Coffee Shop Simulator").grid(row=0, column=1)
    else:
        Label(text=f"Number of mistakes yesterday: {attraction["mistake_number_in_a_day"]}")
    def start():
        arrivals(59)
        registers()
    Button(command=start, text=f"Start_day {time_settings["days_passed"] + 1}").grid(row=1, column= 1)
starting_screen()



win.mainloop()
