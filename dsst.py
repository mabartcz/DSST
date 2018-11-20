from appJar import gui
import random
import time
import datetime
import sys
import statistics

#clear log file
open('log.txt', 'w').close()

win = gui("DSST")
win.showSplash("DSST - Loading","Gray", "Lightblue", "Black")
win.setBg("Gray")
win.setFont(20)
#win.setSize("800x500")
win.setResizable(False)

pressed_list = []
correct_list = []
result_list = []
correct = None
YN = None
current_status = "0/0"
start_status = 0
time_list = []
times = []
start_time = None
shuffled = [1, 2, 3, 4, 5, 6, 7, 8, 9]

def showLabels():
    axes.legend(['Time per action'])
    axes.set_xlabel("Number of actions (n)")
    axes.set_ylabel("Time per action (sec)")
    win.refreshPlot("plot")


def launch(app):
    win.showSubWindow(app)

def change_pic():
    # Change game pic
    global correct
    im_path = "pic/znak_"
    im_num = str(random.randint(1, 9))
    win.setImage("Znak", im_path + im_num + ".gif")
    correct = int(im_num)

def new_task_table():
    # Add new task table signs
    global shuffled
    random.shuffle(shuffled)
    for i in range(0, 9):
        im_name = "Znak" + str(i)
        im_path = "pic/znak_"
        im_num = str(shuffled[i])
        win.setImage(im_name, im_path + im_num + ".gif")

def press(name):
    global start_status, pressed_list, correct_list, result_list, time_list, times, start_time
    # Buttons
    if name == "Exit":
        win.stop()

    elif name == "Start":
        pressed_list = []
        correct_list = []
        result_list = []
        time_list = []
        times = []
        win.setLabel("CS", "0/0")
        win.setLabel("Times", "0")
        win.setLabel("Stat", "")
        win.setMeter("progress",0)
        win.updatePlot("plot", list(range(len(times))), times)
        win.setImage("Status", "pic/znak_blank_gray.gif")
        showLabels()
        win.setLabel("Meann", "0")

        start_status = 1
        win.disableButton("Start")
        win.unbindKey("<space>")
        win.setLabel("Startinfo", " ")


        new_task_table()
        change_pic()
        start_time = time.time()
        time_list.append(time.time())
    elif name == "About":
        win.infoBox("About", "DSST - Digit Symbol Substitution Test\n\nMade by: Martin Barton\nEmail: ma.barton@seznam.cz\nYear: 2018\nUniversity: CTU FBMI\nPlace: Kladno, Czech Republic\nGit: https://github.com/mabartcz/DSST")
    elif name == "Control":
        launch(name)
    elif name == "Save":
        f_name = "dsst-"+ str(datetime.datetime.now().strftime("%H%M%S-%d-%m-%y"))
        file = win.saveBox(title="Save", fileName=f_name, fileExt=".csv", asFile=True, parent="Control")
        file.write("Time of test," + str(datetime.datetime.now().strftime("%H:%M %d %m %Y")))
        file.write("\nTime (sec), Correct (T/F-1/0)")
        for k in range(len(times)):
            file.write("\n"+str(times[k])+","+str(result_list[k]))
        file.close()
        win.infoBox("SaveInfo", "File was successfully saved as: " +str(f_name) + "\nto the dsst folder.")



def answer_press(key):
    global start_status
    if start_status == 1: # If start was pressed
        # Game key press (1 - 9) than ->
        global pressed_list, time_list, correct_list
        pressed = shuffled[key-1]
        pressed_list.append(str(pressed))
        correct_list.append(str(correct))

        if pressed == correct:
            win.setImage("Status", "pic/Yes.gif")
            result_list.append(1)
            YN = 1
        else:
            win.setImage("Status", "pic/No.gif")
            result_list.append(0)
            YN = 0

        time_list.append(time.time())
        times.append((round((time_list[-1]-time_list[-2]), 3)))


        # show statistic
        current_status = str(sum(result_list)) + "/" + str(len(result_list))
        win.setLabel("CS", current_status )
        win.setLabel("Times", times[-1] )
        win.setMeter("progress",(sum(result_list)/len(result_list))*100 )

        change_pic()
        new_task_table()

        if time.time() > start_time+duration:
            win.enableButton("Start")
            win.setImage("Znak", "pic/znak_blank.gif")
            for i in range(0, 9):
                im_name = "Znak" + str(i)
                win.setImage(im_name, "pic/znak_blank.gif")
            start_status = 0
            win.setLabel("Meann", str(round((statistics.mean(times)), 3)) )

            win.setLabel("Startinfo", "Press spacebar to START !")
            win.bindKey("<space>", space_press)
            win.updatePlot("plot", list(range(1, len(times) + 1)), times)
            showLabels()

            # log all merurements through sesion
            file = open("log.txt", "a")
            file.write("\nTime of test," + str(datetime.datetime.now().strftime("%H:%M %d %m %Y")))
            file.write("\nTime (sec), Correct (T/F-1/0)")
            for k in range(len(times)):
                file.write("\n" + str(times[k]) + "," + str(result_list[k]))
            file.close()


def space_press(key):
    win.setLabel("Startinfo", " ")
    press("Start")

try:
    file = open("opt_duration.txt", "r")
    duration = int(file.read())
    file.close()
    if duration < 1 or duration > 60 * 60:
        sys.exit("Extended test duration time, in file opt_duration.txt change test duration from '1 to 3600' (sec)")

except:
    duration = 60


# Add menu
fileMenus = ["Control", "About", "-", "Exit"]
win.addMenuList("File", fileMenus, press)

# Add headline
win.addLabel("lb1", "Digit Symbol Substitution Test", 0, 0, 9)
win.setLabelBg("lb1", "lightblue")
win.setLabelFg("lb1", "black")
win.addLabel("Stat", "", 1, 0, 9)
win.addLabel("Space5", "", 2, 0, 9)

# Add image widgets
for i in range(9):
    im_name = "Znak"+str(i)
    im_path = "pic/znak_blank"
    win.addImage(im_name, im_path+".gif", 3, i)
# Add image lables
for j in range(1,10):
    lb_name = "Z"+str(j)
    win.addLabel(lb_name, str(j), 4, j-1)

win.addLabel("Space2", "", 5, 0, 9)
win.addLabel("Space3", "", 6, 0, 9)
win.addImage("Znak", "pic/znak_blank.gif", 7, 0, 9)
win.addLabel("Space4", "", 8, 0, 9)
win.addLabel("Startinfo", "Press spacebar to START !", 9, 0, 9)
#win.button("Start", press, 9, 0, 3)
#win.button("Restart", press,9, 6, 3)

# Bind key actions
for k in range(1, 10):
    win.bindKey(k, answer_press)
win.bindKey("<space>", space_press)


# Set Control window
win.startSubWindow("Control")
win.setBg("Gray")
win.setFont(20)
win.addLabel("l1", "DSST - Control window", 0, 0, 3)
win.setLabelBg("l1", "lightblue")
win.setLabelFg("l1", "black")
win.addLabel("Space22", "", 1)
win.addLabel("DD", "Duration:", 2, 0)
win.addLabel("DD2",str(duration) + " (sec)", 2, 1)
win.addLabel("l2", "Current: ", 3, 0)
win.addImage("Status", "pic/znak_blank_gray.gif", 3, 1)
win.addSplitMeter("progress", 4, 0, 3)
win.setMeterFill("progress", ["green", "red"])
win.addLabel("CS1", "Correct/All:    " , 5, 0)
win.addLabel("CS", current_status, 5, 1)
win.addLabel("Space55", "", 6, 0)
win.addLabel("Time", "Time: ", 7, 0)
win.addLabel("Times", "0", 7, 1)
win.addLabel("Mean", "Mean time: ", 8, 0)
win.addLabel("Meann", "0", 8, 1)
win.button("Start", press, 9, 0 )
win.button("Save", press, 9, 1)
axes = win.addPlot("plot", 0,0, 0, 4, 10, 10)
showLabels()
win.stopSubWindow()


win.go()
