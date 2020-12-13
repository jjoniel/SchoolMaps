from heapq import heappush, heappop, heapify
import webbrowser
import tkinter as tk

def print_name(place):
    nums = "0123456789"
    if len(place) == 1 or place[1] in nums:
        return "Room " + str(place)
    place = names[place]
    ret = ""
    for word in place:
        ret += word + " "
    return ret


with open("names.txt") as n:
    names = {line.split()[0]: line.split()[1:] for line in n}


def get_original(name):
    if(name[0:4] == "Room"):
        return name[4:]
    fin = ""
    n = name.split()
    n[0] = n[0]
    n[-1] = n[-1]
    for a in names:
        if names[a] == n:
            return a

with open("pottypens.txt") as b:
    bathrooms = {line.split()[0] for line in b}

with open("rooms.txt") as r:
    rooms = {line.split()[0]: line.split()[1:] for line in r}

with open("paths.txt") as p:
    paths = {}
    for line in p:
        if (line.split()[0] in paths):
            paths[line.split()[0]].add((line.split()[1], int(line.split()[2])))
        else:
            paths.update({line.split()[0]: {(line.split()[1], int(line.split()[2]))}})
        if (line.split()[1] in paths):
            paths[line.split()[1]].add((line.split()[0], int(line.split()[2])))
        else:
            paths.update({line.split()[1]: {(line.split()[0], int(line.split()[2]))}})
with open("stairs.txt") as s:
    stairs = {line.split()[0]: (line.split()[1], line.split()[2]) for line in s}


def dijkstra(init, dest):
    if init not in rooms.keys():
        for commons in rooms:
            if init in rooms[commons]:
                init = commons
                break
    if dest not in rooms.keys():
        for commons in rooms:
            if dest in rooms[commons]:
                dest = commons
                break
    visited = set()
    start_node = (0, init)
    fringe = []
    parents = {init: None}
    heapify(fringe)
    heappush(fringe, start_node)
    while fringe:
        v = heappop(fringe)
        if v[1] == dest:
            v = v[1]
            path = [v]
            while (parents[v] != None):
                if (v in stairs.keys()):
                    if (stairs[v][0] == parents[v]):
                        path.append("STAIRCASE")
                v = parents[v]
                path.append(v)
            return path[::-1]
        if v[1] not in visited:
            visited.add(v[1])
            for c in paths[v[1]]:
                if c[0] not in visited:
                    parents.update({c[0]: v[1]})
                    temp = (v[0] + c[1], c[0])
                    heappush(fringe, temp)
    return None


def bathroom(init):
    if init not in rooms.keys():
        for commons in rooms:
            if init in rooms[commons]:
                init = commons
                break
    visited = set()
    start_node = (0, init)
    fringe = []
    parents = {init: None}
    heapify(fringe)
    heappush(fringe, start_node)
    while fringe:
        v = heappop(fringe)
        if v[1] in bathrooms:
            v = v[1]
            path = [v]
            while (parents[v] != None):
                if (v in stairs.keys()):
                    if (stairs[v][0] == parents[v]):
                        path.append("STAIRCASE")
                v = parents[v]
                path.append(v)
            return path[::-1]
        if v[1] not in visited:
            visited.add(v[1])
            for c in paths[v[1]]:
                if c[0] not in visited:
                    parents.update({c[0]: v[1]})
                    temp = (v[0] + c[1], c[0])
                    heappush(fringe, temp)
    return None
OPTIONS = set()
for list in rooms:
    for room in rooms[list]:
        if (print_name(room)[0:4] != "Room"):
            OPTIONS.add(print_name(room))
ops = []
for a in OPTIONS:
  ops.append(a)
ops.sort()
window = tk.Tk()
window.configure(background='cyan')
window.title("SchoolMaps")
window.iconbitmap(r'icon.ico')
greeting = tk.Label(text="Welcome to SchoolMaps", font=("Trebuchet MS", 44), background='cyan')
greeting.pack()
label = tk.Label(text="Where are you? Choose from the list or type room #",padx=10,pady=10, font=("Trebuchet MS", 22), background='cyan')
entry = tk.Entry()
variable = tk.StringVar(window)
variable.set(ops[0])
variable2 = tk.StringVar(window)
variable2.set(ops[1])
w = tk.OptionMenu(window, variable, *ops)
w2 = tk.OptionMenu(window, variable2, *ops)
label2 = tk.Label(text="Where do you want to go? Choose from the list or type room #",padx=10,pady=10, font=("Trebuchet MS", 22), background='cyan')
entry2 = tk.Entry()
label.pack()
w.pack()
entry.pack()
label2.pack()
w2.pack()
entry2.pack()
store = [None,None]
def close_window ():
    store[0] = entry.get()
    store[1] = entry2.get()
    if(store[0] == ""):
        store[0] = get_original(variable.get())
    if(store[1] == ""):
        store[1] = get_original(variable2.get())
    window.destroy()
button = tk.Button(
    text="SUBMIT",
    font=("Trebuchet MS", 20),
    width=10,
    height=1,
    bg="white",
    fg="green",
    bd=3,
    command=close_window
)
button.pack()
window.mainloop()
start = store[0]
end = store[1]
if (end == "BATHROOM"):
    route = bathroom(start)
else:
    route = dijkstra(start, end)
x = 0
for step in route:
    if x == 0:
        if (print_name(start)[0:4] == "Room"):
            print("You are in", print_name(start), "which is located in", print_name(step))
        else:
            print("You are in", print_name(step))
    elif step == "STAIRCASE":
        print("Use the staircase")
    else:
        print("Turn into", print_name(step))
    x += 1
print("You have arrived at your destination, " + print_name(end))
print("Thank you for using SchoolMaps!")
print("Have a nice day!")
file = open("web.html", "w")
file.write("<html><body>")
file.write('<link rel="stylesheet" href="style.css">')
file.write("\n<h2>Welcome to SchoolMaps</h2>")
file.write("\n<h3>Showing route from " + print_name(start) + " to " + print_name(end) + "<h3/>")
file.write('<table><tr><th>STEPS</th></tr>')
x = 0
for step in route:
    if x == 0:
        if (print_name(start)[0:4] == "Room"):
            file.write("\n<tr><td>You are at " + print_name(start) + " in " + print_name(step) + "</td></tr>")
        else:
            file.write("\n<tr><td>You are at " + print_name(step) + "</td></tr>")
    elif step == "STAIRCASE":
        file.write("\n<tr><td>Use Staircase</td></tr>")
    else:
        file.write("\n<tr><td>Turn into " + print_name(step) + "</td></tr>")
    x += 1
if(route[0] == route[-1]):
  file.write('\n<tr id="end"><td>You are already in the same hallway/commons as your destination.</td></tr></table>')
elif (print_name(end)[0:4] == "Room"):
  file.write('\n<tr id="end"><td>You have arrived at your destination, ' + print_name(end) + ', located in, ' + print_name(route[-1])+'</td></tr></table>')
else:
  file.write('\n<tr id="end"><td>You have arrived at your destination, ' + print_name(end) + '</td></tr></table>')

file.write("\n<h3>Thank you for using SchoolMaps!</h3>")
file.write("\n<h3>Have a nice day!</h3>")
file.write("\n<h3>Maps:</h3>")
file.write('\n<img src="Floor1.jpg" alt="LOGO" width="400" height="400">')
file.write('\n<img src="Floor2.jpg" alt="LOGO" width="400" height="400">')
file.write('\n<marquee><img src="logo.png" alt="LOGO" width="100" height="100"><h4>Download Our iOS App If It Ever Comes Out</h4></marquee>')
file.write("</body></html>")
file.close()
webbrowser.open("web.html", new=0, autoraise=True)
