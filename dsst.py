from appJar import gui
import random

win = gui("DSST")
win.showSplash("DSST - Loading","Gray", "Lightblue", "Black")

pressed_list = []
correct_list = []
result_list = []
correct = None

shuffled = [1, 2, 3, 4, 5, 6, 7, 8, 9]

def change_pic():
    global correct
    im_path = "pic/znak_"
    im_num = str(random.randint(1, 9))
    win.setImage("Znak", im_path + im_num + ".gif")
    correct = int(im_num)

def new_task_table():
    global shuffled
    random.shuffle(shuffled)
    for i in range(0, 9):
        im_name = "Znak" + str(i)
        im_path = "pic/znak_"
        im_num = str(shuffled[i])
        win.setImage(im_name, im_path + im_num + ".gif")

def press(name):
    if name == "Exit":
        win.stop()
    elif name == "Stop":
        win.enableButton("Start")
    elif name == "Start":
        win.disableButton("Start")
        win.enableButton("Stop")
        new_task_table()
        change_pic()
    elif name == "About":
        win.infoBox("About", "DSST - Digit Symbol Substitution Test\n\nMade by: Martin Barton\nEmail: ma.barton@seznam.cz\nYear: 2018\nUniversity: CTU FBMI\nPlace: Kladno, Czech Republic\nGit: https://github.com/mabartcz/DSST")


def answer_press(key):
    global pressed_list
    global correct_list
    pressed = shuffled[key-1]
    pressed_list.append(str(pressed))
    correct_list.append(str(correct))

    if pressed == correct:
        win.setImage("Status", "pic/Yes.gif")
    else:
        win.setImage("Status", "pic/No.gif")


    change_pic()
    new_task_table()


win.setBg("gray")
win.setFont(20)
#win.setSize("800x500")
win.setResizable(False)

# Add menu
fileMenus = [ "About", "-", "Exit"]
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

# Add space
win.addLabel("Space2", "", 5, 0, 9)
win.addLabel("Space3", "", 6, 0, 9)

# Add game picture
win.addImage("Znak", "pic/znak_blank.gif", 7, 0, 9)

#Add space
win.addLabel("Space4", "", 8, 0, 9)

#Add buttons
win.button("Start", press, 9, 0, 3)
win.button("Stop", press,9, 6, 3)
win.addImage("Status", "pic/Znak_blank.gif", 9, 3, 3)

# Bind key actions
for k in range(1, 10):
    win.bindKey(k, answer_press)


win.go()


# Statistic
if len(pressed_list) != len(correct_list):
    print(len(pressed_list))
    print(len(correct_list))

for x in range(len(pressed_list)):
    if pressed_list[x] == correct_list[x]:
        result_list.append(1)
    else:
        result_list.append(0)


print("pressed")
print(pressed_list)
print("correct")
print(correct_list)
print("result")
print(result_list)