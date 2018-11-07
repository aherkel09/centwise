#Welcome to Centwise 1.0, a tangled mess of a GUI for generating budgets using the python standard library & tkinter.
#Developed by Avery Herkel at Delta-Lyceum

from datetime import datetime
import collections
import _tkinter
import tkinter as tk
from tkinter import StringVar, BOTH, X, END, TOP, LEFT, RIGHT

class Budget():
    def __init__(self, month, budget):
        #inititalizes variables for month and budget.
        self.month = month
        self.budget = budget
        
class GUI():
    def __init__(self):
        #initializes master window.
        self.master = tk.Tk()
        self.master.title('Centwise 0.0.1')
        self.master.geometry("400x600")
        
        #label to welcome the user
        self.welcomeText = "Welcome to Centwise by Avery Herkel\nClick Start to Begin"
        self.welcomeLabel = tk.Label(self.master, text=self.welcomeText)
        self.welcomeLabel.pack()
        
        #start menu with options to create a new budget, edit a budget, or view a budget.
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        self.startMenu = tk.Menu(self.menu, fg='white', bg='#448d76')
        self.menu.add_cascade(label="Start", menu=self.startMenu)
        self.startMenu.add_command(label="New Budget", command=self.createBudget)
        self.startMenu.add_command(label="View Budget", command=self.viewStart)
        
        #list of valid months.
        self.months = ['January', 'February', 'March', 'April', 'May', 'June','July', 'August', 'September', 'October', 'November', 'December']
        
        #creates lists of budget months & years, as well as an index to store used months.
        self.usedMonths = []
        self.usedYears = []
        self.monthIndex = []
        
        #creates list of categories for use in GUI.
        self.categoryList = ['Bills', 'Credit Card Payments', 'Groceries', 'Miscellaneous', 'Vehicle Expenses']
        self.sorted = sorted(self.categoryList)
        
        #creates dictionary from categoryList with initial value of 0 for each key.
        self.categories = collections.OrderedDict()
        for category in self.sorted:
            self.categories[category] = 0
    
    def genError(self, frame, errorType):   
        #error message to prompt a valid input.
        self.error = tk.Label(frame, fg='red')
        self.error.config(text='Error: Please Enter a Valid ' + errorType)
        self.error.pack()
        if errorType == 'Category & Amount':
            self.chooseCategory()
        
    def readLines(self, mode):
        #index to track how many views have been created.
        self.generated = 0
        
        #reads lines from storeBudget.txt.
        self.textFile = open('storeBudget.txt')
        self.readFile = self.textFile.readlines()
        self.lines = [line.rstrip('\n') for line in self.readFile]
            
        #checks each line in file to see if it contains a month.
        for line in self.lines:
            self.initSplit = line.split(': ')
            self.monthSplit = self.initSplit[0].split('/')

            #populates monthIndex, usedMonths and usedYears from storeBudget.txt.
            if mode == 'Create':
                try:
                    if isinstance(int(self.monthSplit[0]), int):
                        self.monthIndex.append(self.monthSplit[0])
                                    
                    self.usedMonths.append(str(int(self.monthSplit[0])-1))
                                
                    if self.monthSplit[1] not in self.usedYears:
                        self.usedYears.append(self.monthSplit[1])
                except:
                        None
                        
            #generates data to populate viewBox for budget selection.
            if mode == 'View':
                self.monthIndex.sort(key=int)
                for m in self.monthIndex:
                    if str(m) == self.monthSplit[0]:
                        #replaces month number with text for viewing purposes.
                        self.viewText = line.replace(self.monthSplit[0]+'/', self.months[int(self.monthSplit[0])-1]+' ')
                        
                        #increments self.generated to track how many views have been created.
                        self.generated += 1
                        self.generateView(self.viewText)
            
        if mode == 'Select':
            #creates list to hold category text.
            self.categoryText = []
            
            #populates categoryText and calls displaySelected.
            for line in range(0, len(self.lines)):
                if (self.currentView + '/') in self.lines[line]:
                    self.lineStart = line
                    self.monthText = self.lines[line]
            
            #stores category data for selected month in categoryText and removes current budget data from storeBudget.txt
            for line in range(self.lineStart + 1, self.lineStart + 6):
                self.categoryText.append(self.lines[line])
            
            #writes new budget data to overwrite.txt
            self.overwriteFile = open('overwrite.txt', 'w')
            
            for line in range(0, len(self.lines)):
                if line < self.lineStart:
                    self.overwriteFile.write(self.lines[line] + "\n")
                    
                elif line > self.lineStart + 5:
                    self.overwriteFile.write(self.lines[line] + "\n")
            
            self.overwriteFile.close()
            self.saveAndClose('Overwrite')  
        self.textFile.close()
        
    def clearScreen(self, errorType):
        #checks reason for error and resets screen accordingly.
        if errorType == 'Create':
            try:
                self.createFrame.destroy()
            except:
                None
                
        elif errorType == 'View':
            try:
                self.viewFrame.destroy()
            except:
                None
            
        elif errorType == 'Month' or errorType == 'Budget':
            self.clearScreen('Create')
            self.genError(self.master, errorType)
            self.createBudget(None)
            
        elif errorType == 'Category & Amount':
            self.clearScreen('Remove Error')
            try:
                self.categoryFrame.destroy()
                self.updateFrame.destroy()
            except:
                None
            self.genError(self.budgetFrame, errorType)
        
        elif errorType == 'Selection':
            self.clearScreen('Remove Error')
            try:
                self.listFrame.destroy()
            except:
                None 
            self.genError(self.viewFrame, errorType)
            self.viewLink()
                
        elif errorType == 'Remove Error':
            try:
                self.error.pack_forget()
            except:
                None
    
    def saveAndClose(self, mode='Store'):
        if mode == 'Store':
            #saves budget to storeBudget.txt and calls viewStart().
            self.file = open('storeBudget.txt', 'a')
            self.file.write(str(self.getMonth) + ": " + str(self.getBudget) + "\n")
            for k, v in self.categories.items():
                self.file.write(k + ": " + str(v) + "\n")
            self.file.close()
            self.viewStart()
        
        elif mode == 'Overwrite':
            #reads data from overwrite.txt by line
            self.overwriteFile = open('overwrite.txt')
            self.overRead = self.overwriteFile.readlines()
            self.overLines = [line.rstrip('\n') for line in self.overRead]
            self.overwriteFile.close()
            
            #rewrites storeBudget.txt to remove current budget and allow for editing.
            self.file = open('storeBudget.txt', 'w')
            for line in self.overLines:
                self.file.write(line + "\n")
            self.file.close()
            
            #displays selected budget.
            self.displaySelected()
        
    def createBudget(self, attempt=None):
        #populates usedMonths and clears screen to prevent repeated enrtries.
        self.usedMonths = []
        self.clearScreen('Create')
        self.clearScreen('View')
        self.readLines('Create')
        
        #creates and packs frame for new budget.
        self.createFrame = tk.Frame(self.master, padx=1)
        self.createFrame.pack(side=TOP)
        
        #creates and packs frame for budget widgets.
        self.budgetFrame = tk.Frame(self.createFrame)
        self.budgetFrame.pack(side=TOP)
        
        #changes welcome label text and disables new budget menu option while budget is being created.
        self.welcomeLabel.config(text="Centwise by Delta-Lyceum")
        self.startMenu.entryconfig(1, state='disabled')
        self.startMenu.entryconfig(2, state='normal')
        
        #user enters month here.
        self.monthLabel = tk.Label(self.budgetFrame, text='Enter Month & Year (mm/yyyy):')
        self.monthString = StringVar()
        
        #user enters total budget here.
        self.budgetLabel = tk.Label(self.budgetFrame, text='Enter Expected Income:')
        self.budgetString = StringVar()
        
        #establishes value to put in month entry.
        if attempt == 'Edit':
            self.monthString.set(self.isoMonth[0])
            self.budgetString.set(self.isoMonth[1])
        else:
            self.monthString.set(str(datetime.now().month) + '/' + str(datetime.now().year))
            self.budgetString.set("0000.00")
        
        #entry widgets for month, year and budget.    
        self.monthEntry = tk.Entry(self.budgetFrame, textvariable=self.monthString, justify='center')
        self.budgetEntry = tk.Entry(self.budgetFrame, textvariable=self.budgetString, justify='center', width=27)
        
        #button to generate budget.
        self.generateBudgetButton = tk.Button(self.budgetFrame, text='Generate Budget', 
                                              fg='white', bg='#fb8604', activebackground='#448d76',
                                              command=self.generateBudget)
        
        #packs widgets on screen.
        self.monthLabel.pack()
        self.monthEntry.pack() 
        self.budgetLabel.pack()
        self.budgetEntry.pack()
        self.generateBudgetButton.pack()
    
    def generateBudget(self):
        #removes errors before proceeding.
        self.clearScreen('Remove Error')
        
        #gets user month and budget, uses data to generate budget.
        self.getMonth = self.monthEntry.get()
        self.ripMonth = self.getMonth.split('/')
        self.getBudget = self.budgetEntry.get()
        self.budget = Budget(self.getMonth, self.getBudget)
        self.validateBudget()
    
    def validateBudget(self):
        #checks if user input for budget is a float.
        try: 
            isinstance(float(self.getBudget), float)
            self.validateFormat()
        except:
            self.clearScreen('Budget')
            print('FAIL: User failed to input a valid budget.')
    
    def validateFormat(self):
        #verifies month entry is in proper format.
        datetime.strptime(self.getMonth, '%m/%Y')
        self.validateMonth(self.months)
        
    def validateMonth(self, list):
        #checks if month is valid & unique.
        self.containsMonth = 0
        self.checkMonth = int(self.ripMonth[0]) - 1
        
        for x in range(0, len(list)):
            if list == self.months:
                if list[x] == list[self.checkMonth]:
                    self.containsMonth += 1
                    
            elif list == self.usedMonths:
                if list[x] == str(self.checkMonth):
                    if self.ripMonth[1] in self.usedYears:
                        self.containsMonth += 1
        
        if self.containsMonth > 0:
            if list == self.months:
                self.validateMonth(self.usedMonths)
                
            elif list == self.usedMonths:
                self.clearScreen('Month')
                print('FAIL: User failed to input a unique month.')
        else:
            if list == self.months:
                self.clearScreen('Month')
                print('FAIL: User failed to input a valid month.')
                
            elif list == self.usedMonths:
                self.allowUpdates()
                
    def allowUpdates(self):
        #clears errors before proceeding.
        self.clearScreen('Remove Error')
        
        #freezes user entries for month and budget.
        self.monthEntry.config(state='readonly')
        self.budgetEntry.config(state='readonly')
        self.generateBudgetButton.config(state='disabled')
                
                
        #shows label for total budget.
        self.newBudgetLabel = tk.Label(self.budgetFrame, text=self.months[self.checkMonth] + " " + self.ripMonth[1] + 
                                                            " Budget: $" + self.getBudget)
                
        #allows user to break budget into categories.
        self.categoryButton = tk.Button(self.budgetFrame, text='Add Categories', 
                                       fg='white', bg='#fb8604', activebackground='#448d76',
                                        command=self.chooseCategory)
                
        #save budget and close
        self.saveButton = tk.Button(self.budgetFrame, text='Save & Close Budget',
                                    fg='white', bg='#448d76', activebackground='#fb8604',
                                    command=self.saveAndClose)
              
        self.saveButton.pack()
        self.newBudgetLabel.pack()
        
        #creates and packs label for remaining budget.
        self.incrementCategory(0, None, 'Display')
        
        self.categoryButton.pack()
        
    def chooseCategory(self):
        #clears screen
        try:
            self.updateFrame.destroy()
            self.categoryFrame.destroy()
        except:
            None
        
        #creates frames for category widgets and updates.
        self.categoryFrame = tk.Frame(self.createFrame)
        self.updateFrame = tk.Frame(self.createFrame)
        self.categoryFrame.pack(side=TOP)
        
        #disables add category button.
        self.categoryButton.pack_forget()
        
        #user enters amount for category here.
        self.amountLabel = tk.Label(self.categoryFrame, text='Enter Category Amount:')
        self.amountLabel.pack()
        self.updateString = StringVar()
        self.default = "000.00"
        self.updateEntry = tk.Entry(self.categoryFrame, textvariable=self.updateString, width=24, justify='center')
        self.updateString.set(self.default)
        self.updateEntry.pack()
        self.categoryLabel = tk.Label(self.categoryFrame, text='Choose a Category:')
        self.categoryLabel.pack()
        
        #listbox from which user can choose category.
        self.categoryBox = tk.Listbox(self.categoryFrame, fg='white', bg='#448d76',
                                      selectbackground='#fb8604', takefocus=True)
        
        #places values in listbox.
        for y in self.sorted:
            self.categoryBox.insert(END, y)
        self.categoryBox.pack()
        
        #updates budget with category information.
        self.updateButton = tk.Button(self.categoryFrame, text="Update Budget",
                                      fg='white', bg='#fb8604', activebackground='#448d76',
                                      command=self.updateCategory)
        self.updateButton.pack()
        
    def updateCategory(self):
        #removes label displaying remaining budget to make room for a new one.
        try:
            self.showRemaining.destroy()
        except:
            None
        
        self.validateSelection('Category Box')
        
    def validateSelection(self, listbox):
        #gets data and verifies user has selected a valid category.
            if listbox == 'Category Box':
                try:
                    self.selection = self.categoryBox.curselection()[0]
                    self.currentAmount = self.updateEntry.get()
                    self.currentCategory = self.sorted[self.selection]
                    self.incrementCategory(self.currentAmount, self.currentCategory, mode='Update')
                except:
                    self.failAmount('Category & Amount')
                    
            elif listbox == 'View Box':
                try:
                    self.viewSelection = int(self.viewBox.curselection()[0])
                    self.currentView = str(int(self.usedMonths[self.viewSelection])+1)
                    self.viewBudget(self.currentView)
                except:
                    None
                    
    def failAmount(self, failType):
        #prints failure and clears screen.
        print('FAIL: User failed to select a valid category.')
        self.clearScreen(failType)
        
    
    def incrementCategory(self, amount=0, category=None, mode='Display'):
        #initializes variables to track budget data.
        self.runningTotal = 0
        self.percentTotal = 0
        
        if mode != 'Display':
            #adds user amount to specified category and runningTotal.
            self.categories[category] += float(amount)
            for c in self.categories:
                self.runningTotal += self.categories[c]
                    
            #verifies that runningTotal does not exceed total budget.
            if self.runningTotal > float(self.budget.budget):
                #shows error and resets if expenses exceed budget.
                self.clearScreen('Category & Amount')
                self.categories[category] -= float(amount)
                self.runningTotal = 0
                
            else:
                #removes errors before proceeding.
                self.clearScreen('Remove Error')
                
                #generates new budget data and clears screen.
                self.definePercent()
                self.categoryFrame.destroy()
                
        else:
            for c in self.categories:
                self.runningTotal += self.categories[c]
        
        #shows remaining budget.
        self.remaining = format(float(self.budget.budget) - self.runningTotal, '.2f')
        self.showRemaining = tk.Label(self.budgetFrame, text="Remaining: $" + self.remaining)
        self.showRemaining.pack()
        
    def definePercent(self):
        #defines percentage of budget used.
        self.rawPercent = (float(self.categories[self.currentCategory])/float(self.budget.budget))*100
        self.percentage = float(format(self.rawPercent, '.2f'))
        self.percentTotal += self.percentage
        self.showUpdate()
    
    def showUpdate(self):
        #packs frame to show updated data.
        self.updateFrame.pack(side=TOP)
        
        #shows updated category and percentage of budget spent.
        self.showUpdated = tk.Label(self.updateFrame, text="Updated " + str(self.currentCategory) + " : $" + str(self.categories[self.currentCategory])
                                                    + "\n(" + str(self.percentage) + " % of " + self.budget.month + " Budget)")
        
        #allows user to add additional categories.
        self.addCategories = tk.Button(self.updateFrame, text='Add Another Category',
                                 fg='white', bg='#fb8604', activebackground='#448d76',
                                 command=self.chooseCategory)
        
        #packs amount widgets.
        self.showUpdated.pack()
        self.addCategories.pack()
        
    def viewStart(self, attempt='Initial'):
        #clears screen and reconfigures menu before proceeding.
        self.clearScreen('Create')
        self.clearScreen('View')
        self.startMenu.entryconfig(1, state='normal')
        self.startMenu.entryconfig(2, state='disabled')
        self.usedMonths = []
        self.usedYears = []
        self.monthIndex = []
        
        #creates and packs frames for viewing budgets.
        self.viewFrame = tk.Frame(self.master)
        self.viewFrame.pack(side=TOP)
        
        #creates listbox for viewing budgets when save & close is called.
        if attempt != 'Display':
            self.readLines('Create')
            self.viewLink()
    
    def viewLink(self):
        #creates and packs frames for viewing listbox.
        self.listFrame = tk.Frame(self.viewFrame)
        self.listFrame.pack(side=TOP)
        
        #listbox from which user can choose budget to view.
        self.viewBox = tk.Listbox(self.listFrame, fg='white', bg='#448d76', selectbackground='#fb8604', 
                                  width=27, takefocus=True)
        
        #populates viewBox with data from usedMonths.
        self.readLines('View')
    
    def generateView(self, line):
                            
        #inserts data from readLines into viewBox.
        self.viewBox.insert(END, line)
        self.viewBox.pack()
           
        if self.generated == len(self.usedMonths):
            #creates button to view selected budget.
            self.viewBudgetButton = tk.Button(self.listFrame, text='View Budget',
                                        fg='white', bg='#fb8604', activebackground='#448d76',
                                        command=self.validateView)
            self.viewBudgetButton.pack()
    
    def validateView(self):
        self.validateSelection('View Box')        
    
    def viewBudget(self, view):
        #clears screen before proceeding.
        self.clearScreen('Remove Error')
        
        #recreates and packs viewFrame for new widgets.
        self.viewStart('Display')
        
        #reads data from storeBudget.txt to display selected budget.
        self.readLines('Select')
    
    def displaySelected(self):
        #separates month and budget for editing.
        self.isoMonth = self.monthText.split(': ')
        
        #creates and packs widget to display selected budget.
        self.monthDisplay = tk.Label(self.viewFrame, text=self.monthText, width=27,
                                     fg='white', bg='#fb8604')
        self.monthDisplay.pack()
        
        #creates and packs widgets to display categories for selected budget.
        for c in self.categoryText:
            self.categoryDisplay = tk.Label(self.viewFrame, text=c, width=27,
                                            fg='white', bg='#448d76')
            self.categoryDisplay.pack()
            
        #creates and packs buttons for editing current budget and viewing other budgets.    
        self.editButton = tk.Button(self.viewFrame, text='Edit Budget',
                                    fg='white', bg='#fb8604', activebackground='#448d76',
                                    command=self.editBudget)
        
        self.restartButton = tk.Button(self.viewFrame, text='Return to Home Screen',
                                           fg='white', bg='#448d76', activebackground='#fb8604',
                                           command=self.restart)
        
        self.editButton.pack()
        self.restartButton.pack()
    
    def editBudget(self):
        #separates categories from amounts and establishes index for mapping amounts to categories.
        self.isoAmount = []
        index = 0
        
        for item in self.categoryText:
            categorySplit = item.split(': ')
            self.isoAmount.append(categorySplit[1])
            
        for k, v in self.categories.items():
            v = self.isoAmount[index]
            index += 1
        
        self.createBudget('Edit')
    
    def restart(self):
        #rewrites data removed from storeBudget.txt
        self.file = open('storeBudget.txt', 'a')
        self.file.write(self.monthText + '\n')
        for c in self.categoryText:
            self.file.write(c + '\n')
        self.file.close()
                    
        #clears screen for user to begin anew.
        self.clearScreen('View')
        self.startMenu.entryconfig(1, state='normal')
        self.startMenu.entryconfig(2, state='normal')
        self.welcomeLabel.config(text=self.welcomeText)
        self.welcomeLabel.pack()   
 
def main():
    #creates GUI instance and enters mainloop.
    budgetGUI = GUI()
    budgetGUI.master.mainloop()

if __name__.endswith('__main__'):
    main()