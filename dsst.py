from appJar import gui
import random

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

shuffled = [1, 2, 3, 4, 5, 6, 7, 8, 9]

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
    global start_status, pressed_list, correct_list, result_list
    # Buttons
    if name == "Exit":
        win.stop()
    elif name == "Restart":
        win.enableButton("Start")
        win.setImage("Znak", "pic/znak_blank.gif")
        win.setImage("Status", "pic/znak_blank_gray.gif")
        for i in range(0, 9):
            im_name = "Znak" + str(i)
            win.setImage(im_name, "pic/znak_blank.gif")
        start_status = 0
        pressed_list = []
        correct_list = []
        result_list = []
        win.setLabel("CS", "0/0")
    elif name == "Start":
        start_status = 1
        win.disableButton("Start")
        win.enableButton("Restart")
        new_task_table()
        change_pic()
    elif name == "About":
        win.infoBox("About", "DSST - Digit Symbol Substitution Test\n\nMade by: Martin Barton\nEmail: ma.barton@seznam.cz\nYear: 2018\nUniversity: CTU FBMI\nPlace: Kladno, Czech Republic\nGit: https://github.com/mabartcz/DSST")
    elif name == "Control":
        launch(name)
    elif name == "Save":
        pass
    elif name == "Show":
        pass


def answer_press(key):
    if start_status == 1: # If start was pressed
        # Game key press (1 - 9) than ->
        global pressed_list
        global correct_list
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

        # show statistic
        current_status = str(sum(result_list)) + "/" + str(len(result_list))
        win.setLabel("CS", current_status )

        change_pic()
        new_task_table()


# Add menu
fileMenus = ["Control", "About", "-", "Exit"]
win.addMenuList("File", fileMenus, press)

# Add headline
win.addLabel("lb1", "Digit Symbol Substitution Test", 0, 0, 9)
win.setLabelBg("lb1", "lightblue")
win.setLabelFg("lb1", "black")
win.addLabel("Space1", "", 1, 0, 9)
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
win.button("Start", press, 9, 0, 3)
win.button("Restart", press,9, 6, 3)

# Bind key actions
for k in range(1, 10):
    win.bindKey(k, answer_press)


# Set Control window
win.startSubWindow("Control")
win.setBg("Gray")
win.setFont(20)
win.addLabel("l1", "DSST - Control window", 0, 0, 3)
win.setLabelBg("l1", "lightblue")
win.setLabelFg("l1", "black")
win.addLabel("Space11", "")
win.addLabel("Space22", "", 3, 2)
win.addLabel("l2", "Current: ", 3, 0)
win.addImage("Status", "pic/znak_blank_gray.gif", 3, 1)
win.addLabel("Space33", "", 4, 0)
win.addLabel("CS1", "Correct/All:    " , 5, 0)
win.addLabel("CS", current_status, 5, 1)
win.addLabel("Space44", "", 6, 0)
win.button("Show", press, 7, 0 )
win.button("Save", press, 7, 1)
win.stopSubWindow()


win.go()


# Statistic

print("pressed")
print(pressed_list)
print("correct")
print(correct_list)
print("result")
print(result_list)