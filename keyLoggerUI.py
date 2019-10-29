#!/usr/local/bin/python
#!usr/bin/env python
from keyLogger import *
import pyxhook
from readLogger import *
from tkinter import *
import tkinter as tk
from tkinter import ttk , messagebox

# Code to add widgets will go here...

txt = ""
isRecording = False
def buildHook():
    global new_hook
    new_hook = pyxhook.HookManager()
    new_hook.KeyDown = OnKeyPress
    # set the hook
    new_hook.HookKeyboard()
#isRecordingLabel;
#isRecordingCircle
def startButtonPress() :
    global isRecording
    if isRecording == False:
        buildHook()
        try:
            new_hook.start()  # start the hook
            isRecording = True
            setGUIToRecordingStatus(1)
        except KeyboardInterrupt:
            # User cancelled from command line.
            pass
        except Exception as ex:
            # Write exceptions to the log file, for analysis later.
            msg = 'Error while catching events:\n  {}'.format(ex)
            pyxhook.print_err(msg)
            with open(log_file, 'a') as f:
                f.write('\n{}'.format(msg))
    else:
        messagebox.showinfo( "Error","The keyLogger is already at start mode ")


def stopButtonPress() :
    global isRecording
    if isRecording == True:
        try:
            new_hook.cancel()
            isRecording = False
            setGUIToRecordingStatus(0)
        except Exception as ex:
            msg = 'Error while catching events:\n  {}'.format(ex)
            pyxhook.print_err(msg)
    else:
        messagebox.showinfo( "Error","The keyLogger is already at stop mode \nPlease activate the keyLogger ")

def deleteJsonFile():
    try:
        deleteFile()
    except FileExistsError:
        messagebox.showinfo("Error","History is already empty")

def setGUIToRecordingStatus(status) :
    if status==1 :
        canvas.itemconfig(circle,fill="green")
        #statusLabel='Recording'
    else :
        canvas.itemconfig(circle,fill="red")
        #statusLabel='not recording'

def wordSearchPress() :
    txt = textBox.get()
    try:
        if txt != "":
            freqList = isWordExist(txt)
            for i in freqList:
                listbox.insert(END, i)
                #print(i)
        else:
            raise ValueError
    except FileNotFoundError:
        messagebox.showinfo("Error", "The key Log is empty")
    except Exception:
        messagebox.showinfo("Error", "Please insert word")



def cleanlog() :
    listbox.delete(0,END)



def create_circle(x, y, r, canvasName , fill ): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1,fill=fill,outline="black",width=5)


app = tk.Tk()
app.geometry("600x400")

tab_parent = ttk.Notebook(app)
tab1 = ttk.Frame(tab_parent)
tab2 = ttk.Frame(tab_parent)
tab3 = ttk.Frame(tab_parent)



## tabs ##
tab_parent.add(tab1,text="write")
tab_parent.add(tab2,text="search by word")
tab_parent.add(tab3,text="search by date")
tab_parent.pack(expand=1,fill="both")
app.title('key logger')


############# write tab  #############



## status circle ##
canvas = Canvas(tab1)

#circle = canvas.create_circle_arc(10,10,80,80,outline="black",fill="green",width=2,start=45, end=100)
circle = create_circle(320, 100, 30, canvas,"red")
canvas.pack( expand=1)


## status label ##
frame = tk.Frame(tab1)
frame.pack(expand='yes')
statusLabel = tk.Label(tab1 , text = "Recording" , font=("Helvetica", 30))
statusLabel.pack()
statusLabel.place(x=200,y=100)

## start recording button##
button = tk.Button(tab1,borderwidth=10, text = 'start recording'  , command = startButtonPress,anchor="c")
button.config(height=5 , width = 10)
button.place(x=180 , y=240)

## stop recording button##
stopButton = tk.Button(tab1,borderwidth=10, text = 'stop recording'  , command = stopButtonPress,anchor="c")
stopButton.config(height=5 , width = 10)
stopButton.place(x=320 , y=240)

def clearHistoryButton() :
    qw = Tk()
    frame1 = Frame(qw, highlightbackground="green", highlightcolor="green", highlightthickness=1, bd=0)
    frame1.pack()
    qw.overrideredirect(1)
    qw.geometry("264x70+650+400")
    qw.location(relx=.5, rely=.5)
    lbl = Label(frame1, text="are you sure you want to clear history?")
    lbl.pack()
    yes_btn = Button(frame1, text="Yes", bg="light blue", fg="black", command=deleteJsonFile, width=10)
    yes_btn.pack(padx=10, pady=10, side=LEFT)
    no_btn = Button(frame1, text="No", bg="light blue", fg="black", command=qw.destroy, width=10)
    no_btn.pack(padx=10, pady=10, side=LEFT)
    qw.mainloop()


## history button##
clearHistoryButton = tk.Button(tab1,borderwidth=5, text = 'clear history' , command = clearHistoryButton,anchor="c")
clearHistoryButton.config(height=1 , width = 8)
clearHistoryButton.place(x=493 , y=2)





############# search by word tab  #############

## search for a word in key logger button##
WordSearchButton = tk.Button(tab2,borderwidth=10, text = 'search'  , command = wordSearchPress,anchor="c")
WordSearchButton.config(height=2 , width = 10)
WordSearchButton.place(x=180, y=300)

## clean button##
cleanButton = tk.Button(tab2,borderwidth=10, text = 'clean'  , command = cleanlog,anchor="c")
cleanButton.config(height=2 , width = 10)
cleanButton.place(x=340, y=300)

## read label ##
readLabel = tk.Label(tab2 , text = "search for a word in the log" , font=("Helvetica", 25))
readLabel.pack()
readLabel.place(x=100,y=10)

## word input box ##
textBox = tk.Entry(tab2,width=25)
textBox.pack()
#textBox.config(height=10 , width= 50)
textBox.place(x=213,y=271)
#text = textBox.get("1.0",'end-1c')


## scroll window ##

frame =Frame(tab2)
yscroll = Scrollbar(frame)
yscroll.pack(side=RIGHT,fill=Y)
xscroll = Scrollbar(frame,orient='horizontal')
xscroll.pack(side=BOTTOM,fill=X)
listbox = Listbox(frame, yscrollcommand= yscroll.set)

#for i in range(1,51):
#   listbox.insert(END, "list" + str(i))
listbox.pack(side=LEFT)
frame.pack()
frame.place(x=5,y=50)
frame.config(height=11,width=70)
listbox.config(height=11,width=70)
yscroll.config(command=listbox.yview)
xscroll.config(command=listbox.xview)

############# search by date tab  #############

def searchByDate():
    startY = yearCombo.get()
    startY = startY[2]+startY[3]
    print(startY)
    startDate = dayCombo.get()+"/"+monthCombo.get()+"/"+startY
    myhour=hourCombo.get()
    if myhour == "24":
        myhour = "00"
    startHour= myhour + ":" + minutesCombo.get() + ":" + secondCombo.get()
    endDate = endDayCombo.get() + "/" + endMonthCombo.get() +"/" + endYearCombo.get()[2] + endYearCombo.get()[3]
    myendhour = endHourCombo.get()
    if myendhour == "24" :
        myendhour = "00"
    endHour = myendhour + ":" + endMinutesCombo.get() + ":" + endSecondCombo.get()
    try:
        if validationCheck(startDate,startHour,endDate,endHour) == True:
            valuesList = getValueBytime(startDate,startHour,endDate,endHour)
            for i in valuesList:
                listbox2.insert(END, i)
        else:
            raise ValueError
    except FileNotFoundError:
        messagebox.showinfo("Error", "The key Log is empty")
    except Exception:
        messagebox.showinfo("Error","Wrong input! ")

def validationCheck(startDate,startTime, endDate, endTime):
    if startDate > endDate or startDate > date.today().strftime("%d/%m/%y"):
        return False
    if startDate == endDate and startTime > endTime:
        return False
    return True

def cleanSearchByDate():
    listbox2.delete(0,END)



## search for a word in key logger button##
WordSearchButton = tk.Button(tab3,borderwidth=10, text = 'search'  , command = searchByDate,anchor="c")
WordSearchButton.config(height=1 , width = 10)
WordSearchButton.place(x=160, y=316)

## clean button##
cleanButton = tk.Button(tab3,borderwidth=10, text = 'clean'  , command = cleanSearchByDate,anchor="c")
cleanButton.config(height=1 , width = 10)
cleanButton.place(x=315, y=316)

## read label ##
readLabel = tk.Label(tab3 , text = "search for a word in the log" , font=("Helvetica", 25))
readLabel.pack()
readLabel.place(x=100,y=10)

## startTIme label ##
startTimeLabel = tk.Label(tab3 , text = "start time" , font=("Helvetica", 15 ))
startTimeLabel.pack()
startTimeLabel.place(x=70,y=210)

## date label ##
readLabel = tk.Label(tab3 , text = "Date: " , font=("Helvetica", 15))
readLabel.pack()
readLabel.place(x=10,y=240)

dayList =[]
for i in range(1,32) :
    if i<10:
        dayList.append("0"+str(i))
    else:
        dayList.append(str(i))

## day combobox ##
dayCombo = ttk.Combobox(tab3,value=dayList,width=4)
dayCombo.pack()
dayCombo.place(x=65,y=245)
dayCombo.set("day")

monthList =[]
for i in range(1,13) :
    if i<10:
        monthList.append("0"+str(i))
    else:
        monthList.append(str(i))

## month combobox ##
monthCombo = ttk.Combobox(tab3,value=monthList,width=6)
monthCombo.pack()
monthCombo.place(x=112,y=245)
monthCombo.set("month")

yearList = []
for i in range(2019,1935 , -1) :
    yearList.append(str(i))

## year combobox ##
yearCombo = ttk.Combobox(tab3,value=yearList,width=6)
yearCombo.pack()
yearCombo.place(x=175,y=245)
yearCombo.set("year")

## time ##
readLabel = tk.Label(tab3 , text = "Time: " , font=("Helvetica", 15))
readLabel.pack()
readLabel.place(x=10,y=275)

hourList =[]
for i in range(0,24) :
    if i<10:
        hourList.append("0"+str(i))
    else:
        hourList.append(str(i))

## hour combobox ##
hourCombo = ttk.Combobox(tab3,value=hourList,width=4)
hourCombo.pack()
hourCombo.place(x=65,y=280)
hourCombo.set("hour")

minutesList =[]
for i in range(0,60) :
    if i<10:
        minutesList.append("0"+str(i))
    else:
        minutesList.append(str(i))

## minutes combobox ##
minutesCombo = ttk.Combobox(tab3,value=minutesList,width=6)
minutesCombo.pack()
minutesCombo.place(x=112,y=280)
minutesCombo.set("minute")

secondList = []
for i in range(0,60) :
    if i<10:
        secondList.append("0"+str(i))
    else:
        secondList.append(str(i))

## second combobox ##
secondCombo = ttk.Combobox(tab3,value=secondList,width=6)
secondCombo.pack()
secondCombo.place(x=175,y=280)
secondCombo.set("second")

################################################
## endTIme label ##
startTimeLabel = tk.Label(tab3 , text = "end time" , font=("Helvetica", 15 ))
startTimeLabel.pack()
startTimeLabel.place(x=450,y=210)

## date label ##
readLabel = tk.Label(tab3 , text = "Date: " , font=("Helvetica", 15))
readLabel.pack()
readLabel.place(x=365,y=240)

endDayList =[]
for i in range(1,32) :
    if i < 10:
        endDayList.append("0" + str(i))
    else:
        endDayList.append(str(i))

## day combobox ##
endDayCombo = ttk.Combobox(tab3,value=endDayList,width=4)
endDayCombo.pack()
endDayCombo.place(x=420,y=245)
endDayCombo.set("day")

endMonthList =[]
for i in range(1,13) :
    if i < 10:
        endMonthList.append("0" + str(i))
    else:
        endMonthList.append(str(i))

## month combobox ##
endMonthCombo = ttk.Combobox(tab3,value=endMonthList,width=6)
endMonthCombo.pack()
endMonthCombo.place(x=467,y=245)
endMonthCombo.set("month")

endYearList = []
for i in range(2019,1935 , -1) :
    endYearList.append(str(i))

## year combobox ##
endYearCombo = ttk.Combobox(tab3,value=endYearList,width=6)
endYearCombo.pack()
endYearCombo.place(x=530,y=245)
endYearCombo.set("year")

## time ##
readLabel = tk.Label(tab3 , text = "Time: " , font=("Helvetica", 15))
readLabel.pack()
readLabel.place(x=365,y=275)

endHourList =[]
for i in range(0,24) :
    if i < 10:
        endHourList.append("0" + str(i))
    else:
        endHourList.append(str(i))

## hour combobox ##
endHourCombo = ttk.Combobox(tab3,value=endHourList,width=4)
endHourCombo.pack()
endHourCombo.place(x=420,y=280)
endHourCombo.set("hour")

endMinutesList =[]
for i in range(0,60) :
    if i < 10:
        endMinutesList.append("0" + str(i))
    else:
        endMinutesList.append(str(i))

## minutes combobox ##
endMinutesCombo = ttk.Combobox(tab3,value=endMinutesList,width=6)
endMinutesCombo.pack()
endMinutesCombo.place(x=467,y=280)
endMinutesCombo.set("minute")

endSecondList = []
for i in range(0,60) :
    if i < 10:
        endSecondList.append("0" + str(i))
    else:
        endSecondList.append(str(i))

## second combobox ##
endSecondCombo = ttk.Combobox(tab3,value=endSecondList,width=6)
endSecondCombo.pack()
endSecondCombo.place(x=530,y=280)
endSecondCombo.set("second")

######################################
"""## start time label ##
readLabel = tk.Label(tab3 , text = "search for a word in the log" , font=("Helvetica", 25))
readLabel.pack()
readLabel.place(x=100,y=10)

## end time label ##
readLabel = tk.Label(tab3 , text = "search for a word in the log" , font=("Helvetica", 25))
readLabel.pack()
readLabel.place(x=100,y=10)"""

#textBox.config(height=10 , width= 50)
textBox.place(x=213,y=271)
#text = textBox.get("1.0",'end-1c')


## scroll window ##

frame3 =Frame(tab3)
yscroll2 = Scrollbar(frame3)
yscroll2.pack(side=RIGHT,fill=Y)
xscroll2 = Scrollbar(frame3,orient='horizontal')
xscroll2.pack(side=BOTTOM,fill=X)
listbox2 = Listbox(frame3, yscrollcommand= yscroll.set)

#for i in range(1,51):
#   listbox.insert(END, "list" + str(i))
listbox2.pack(side=LEFT)
frame3.pack()
frame3.place(x=5,y=50)
frame3.config(height=8,width=70)
listbox2.config(height=8,width=70)
yscroll2.config(command=listbox.yview)
xscroll2.config(command=listbox.xview)



app.mainloop()













############# appjar ##############
"""def buttonPress(button) :
    if button == "startRecording" :
        print ("button pressed")
    elif button == "stop" :
        app.stop()


app = gui("keyLogger", "600x400")
app.addLabel("titla","dfd")
#app.addbuttons(["start recording","stop"],buttonPress)
app.addButton("one",buttonPress)
app.setbuttonwidth("one","202")
app.go()"""



