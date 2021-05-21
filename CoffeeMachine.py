#Import json to __parseJsonArray& read json file into array
import json
from pathlib import Path
from json.decoder import JSONDecodeError

class CoffeeMachine:
    #constructor or init method with json test array as input
    def __init__(self, array):
        self.__array = array                    # Json TC Array
        self.__outlets = 0                      # Number of Outlets, N
        self.__maxi = 0                         # maxi-->Max Beverages that can be served in Parallel
        self.__items_quantity = {}              # stock details: {item:quantity}
        self.__beverages = {}
        self.__items_unavail = {}
        self.__res = []   # To store maximum beverages that can be served in N outlets
        self.__parseJsonArray()
        self.__getAllBevrgsServed(0, [])
        self.__printPreparedBeverages()
        
        #print(self.__res)   #-->print this to get all possible served beverages

    # Check if any items are running low
    # print beverages that can't be served incase of items shortage
    def __checkItemQuantity(self, item, stock):
        for bev,ings in self.__beverages.items():
            if item in ings and ings[item] > stock:
                print(bev+ " cannot be prepared because "+item+" is not sufficient")

    # Indicate Shortage/Unavailable Items after serving some beverages
    def __notifyItemsShortage(self):
        print("----------Beverages that are Shortage of Items after serving above bvrgs------------")
        for item,stock in self.__items_quantity.items():
            self.__checkItemQuantity(item, stock)
        for item,bev in self.__items_unavail.items():
            print(bev+ " cannot be prepared because "+item+" is not available")

    # Print Prepared Beverages
    def __printPreparedBeverages(self):
        if not len(self.__res) or not len(self.__res[-1]):
            print("No Beverage can be Prepared")
            return
        # Print all possible ways of serving max beverages at same time.
        for __res in self.__res:
            if(len(__res) != self.__maxi):
                continue
            print("++++++++++++++++++++++Prepared Beverages++++++++++++++++++++")
            for bev in __res:
                print(bev + " is prepared")
                items = self.__beverages[bev]
                self.__updateQuantity("SUB", items)
            
            print()
            # Notify if there is shortage of items after serving above beverages
            self.__notifyItemsShortage()
            for bev in __res:
                items = self.__beverages[bev]
                self.__updateQuantity("ADD", items)
            print("*****************************************************************")
            print()
            #print ("Items stock after preparing Bvrgs:" + str(self.__items_quantity))

    #Set outlets value    
    def __setOutletsVal(self, outletsOb):
        for name,val in outletsOb.items():
            if(name == "count_n"):
                self.__outlets = val
    
    # Construct Items & quantity pairs
    def __setItemsQuantity(self, Items):
        for item, quant in Items.items():
            self.__items_quantity[item]=quant
    
    # Construct Beverages & Ingredient pairs and put them into Beverages map
    def __setBeverages(self, Bvrgs):
        for bev, ings in Bvrgs.items():
            for item in ings.keys():
                if item not in self.__items_quantity:
                    self.__items_unavail[item] = bev
            self.__beverages[bev] = ings

    #construct coffee machine
    def __parseJsonArray(self):
        for att in self.__array.values():
            for (k,v) in att.items():
                if(k == "outlets"):
                    self.__setOutletsVal(v)
                elif(k == "total_items_quantity"):
                    self.__setItemsQuantity(v)
                elif(k == "beverages"):
                    self.__setBeverages(v)
    
    # Check if Beverage can be prepared
    # params(Ingredients): Ingredients of Beverage
    def __prepareBeverage(self, Ingredients):
        for item,quant in Ingredients.items():
            if item not in self.__items_quantity.keys():
                return False
            elif(quant > self.__items_quantity[item]):
                return False
        return True

    # Update items quantities based on operation
    def __updateQuantity(self, oper, Items):
        for ing,quant in Items.items():
            if(oper == "ADD"):
                self.__items_quantity[ing] += quant
            elif(oper == "SUB"):
                self.__items_quantity[ing] -= quant
    
    # This is a recursive backtracking function which checks if beverage can be prepared
    # and adds it to result list until we reach N outlets count. We then pop added beverage
    # and backtrack to see if we can serve more beverages than before    
    def __getAllBevrgsServed(self, count, res):
        if(count == self.__outlets):
            if(len(res) > 0 and len(res) >= self.__maxi):
                temp = sorted(res)
                # To avoid permutations of beverages we store sorted list into result
                if temp not in self.__res:
                    self.__res.append(temp)
                
                # Update maxi, which has maximum bvrgs that can be prepared in parallel
                self.__maxi = len(res)
                #print (res)
            return

        for k,v in self.__beverages.items():
            if(self.__prepareBeverage(v)):
                self.__updateQuantity("SUB", v)               # Sub item quantity if Bvrg can be prepared
                self.__getAllBevrgsServed(count+1, res+[k])
                self.__updateQuantity("ADD", v)               # Add item quantity back during backtrack

        self.__getAllBevrgsServed(self.__outlets, res)

# copy test files & this program into same directory
# pick all .json files into list        
json_folder = Path('.').rglob('*.json')
files = [x for x in json_folder]

print("Available test files are:")
for filename in files:
    print(str(filename))
    
print("Enter test file name from above files-->")
filename = input()
try:
    with open(filename, 'r') as f:
        print("**************************"+filename+"*****************************")
        #parse & load json into list format 
        array = json.load(f)
    
        #Instantiate coffee machine
        coffeeMachine = CoffeeMachine(array)
        print("****************************************************************")
        print()
except FileNotFoundError:
    print("Entered Filename is wrong")
except JSONDecodeError:
    print("Json test file decode error")
#print(array)
