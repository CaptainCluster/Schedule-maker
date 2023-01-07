#Schedule maker, made by CaptainCluster
from tkinter import *

class PROGRAM():
    def __init__(self):
        self.LabelsList = []
        self.ScrollList = ""
        root = Tk()
        root.title("Schedule maker")
        root.configure(bg = "gray")
        root.resizable(0,0)
        
        self.Base = Frame(root, bg = "black")
        self.Base.pack_propagate(0)
        self.Base.pack()

        self.managementFrame()
        self.scheduleFrame()

        self.fileExistence()
        root.mainloop()
        return None

    def managementFrame(self):
        Management = Frame(self.Base, width = 300, height = 500, bg = "gray")
        Management.grid_propagate(0)
        Management.pack_propagate(0)
        Management.grid(column = 0, row = 0, padx = 5, pady = 5)

        Label(Management, text = "Event name", width = 15).grid(column = 0, row = 0, padx=7, pady = 5)
        self.UserEvent = Entry(Management, width = 25)
        self.UserEvent.grid(column = 1, row = 0, padx=7)
        
        Label(Management, text = "Date", width = 15).grid(column = 0, row = 1, pady = 3)
        self.UserTime = Entry(Management, width = 25)
        self.UserTime.grid(column = 1, row = 1)
        
        Button(Management, text = "Instructions", command = self.instructionPanel, width = 13).grid(column = 0, row = 2)
        Button(Management, text = "Add to schedule", command = self.writeFile).grid(column = 1, row = 2, pady = 5)
        
        self.Notification = Frame(Management, width = 280, height = 390, bg = "white")
        self.Notification.pack_propagate(0)
        self.Notification.place(x = 10, y = 100)
        return None

    def scheduleFrame(self):
        ScheduleBg = Frame(self.Base, width = 400, height = 500, bg = "gray")
        ScheduleBg.grid_propagate(0)
        ScheduleBg.grid(column = 1, row = 0, padx = 5)

        Button(ScheduleBg, text = "Remove selected events", command = self.eventDeleteSelect).grid(pady = 5)

        self.Schedule = Frame(ScheduleBg, width = 390, height = 450, bg = "white")
        self.Schedule.pack_propagate(0)
        self.Schedule.grid(padx = 5, pady = 5)

        self.Scroll = Scrollbar(self.Schedule)
        self.Scroll.pack(side = RIGHT, ipadx = 2, fill = "y")
        return None

    def createFile(self): #creates a new file for reading contents if one doesn't exist
        File = open("schedule.txt", "w", encoding = "utf-8")
        File.close()
        return None

    def fileExistence(self):
        try:
            self.schedulePanel()
        except Exception:
            File = open("schedule.txt", "w", encoding = "utf-8")
            File.close()
        return None

    def readFile(self):
        List = []
        File = open("schedule.txt", "r", encoding = "utf-8")
        File.readline()
        while True:
            Line = File.readline()
            if(len(Line) == 0):
                break
            List.append(Line)
        File.close()
        return List

    def notificationSelect(self, PreviousInputs, File):
        UserEvent = self.UserEvent.get()
        UserTime = self.UserTime.get()
        WrittenFormat = str(UserEvent) + " ; " + str(UserTime) + "\n"
        if(UserEvent == "" or UserEvent == " " or UserTime == "" or UserTime == " "):
            self.notifySuccess("You need to write both the event and the time!", "red")
        elif(PreviousInputs.count(WrittenFormat) != 0):
            self.notifySuccess("Your event is already on the schedule.", "red")
        else:
            File.write(WrittenFormat)
            self.notifySuccess("Your event has been added to the schedule.", "green")
        return None


    def notifySuccess(self, Written, Color): 
        self.Notifications = Label(self.Notification, text = Written, fg = Color, bg = "white")
        self.Notifications.pack()
        self.Notifications.after(4000, self.Notifications.destroy)
        return None

    def writeFile(self): 
        try:
            PreviousInputs = self.readFile()
            File = open("schedule.txt", "w", encoding="utf-8")
            File.write("Event ; Date" + "\n")
            for i in PreviousInputs:
                File.write(i)
            self.notificationSelect(PreviousInputs, File)
            File.close()
            self.schedulePanel()
            PreviousInputs.clear()
        except Exception:
            self.notifySuccess("ERROR! Your event was not added to the schedule.", "red")
        return None

    def schedulePanel(self): #Updates the schedule panel
        if(self.ScrollList != ""):
            self.ScrollList.destroy()
        Read = self.readFile()
        self.ScrollList = Listbox(self.Schedule, yscrollcommand = self.Scroll.set, selectmode = EXTENDED, width = 65, height = 31, justify = "center")
        self.ScrollList.pack_propagate(0)
        for i in Read:
            self.ScrollList.insert(END, i)
        self.ScrollList.pack(side = LEFT)
        self.Scroll.configure(command = self.ScrollList.yview)
        return None

    def eventDeleteSelect(self): #Deletes every single event the user has selected
        List = []
        for i in self.ScrollList.curselection():
            Event = self.ScrollList.get(i)
            List.append(Event)
        for i in List:
            self.eventDeletion(i)
        List.clear()
        return None
        
    def eventDeletion(self, Event): 
        List = []
        Read = self.readFile()
        for i in Read:
            List.append(i)
            if(List.count(Event) > 0):
                Read.remove(Event)
                break
        File = open("schedule.txt", "w", encoding = "utf-8")
        File.write("Event ; Date" + "\n")
        for i in Read:
            File.write(i)
        File.close()
        self.schedulePanel()
        return None

    def instructionPanel(self):
        newroot = Tk()
        newroot.title("Instructions")
        newroot.configure(bg = "white")
        newroot.resizable(0,0)
        Label(newroot, text = "Greetings. This app is designed to help you arrange your very own schedule.").grid()
        Label(newroot, text = "Start off by typing both the name of the event and the time it takes place.").grid()
        Label(newroot, text = "After doing so, press the 'Add to schedule' button in order to register it.").grid()
        Label(newroot, text = "The event should now be displayed on the right. You will also get").grid()
        Label(newroot, text = "a notification regarding the successful process. If you wish to delete any").grid()
        Label(newroot, text = "of the events, you can go to the schedule, click the events you want to delete").grid()
        Label(newroot, text = "and press the 'Remove selected events' button. Your schedule will be").grid()
        Label(newroot, text = "automatically saved so you don't have to worry about losing anything.").grid()
        newroot.mainloop()
        return None

PROGRAM()
