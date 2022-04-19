import matplotlib.pyplot as plt
import csv
import json

runs_to_plot = ["run1.csv", "run2.csv", "run3.csv", "run4.csv", "run5.csv", "run6.csv", "run7.csv"]
OUT_FILE = "graph.png"
X_LIMITS = [73.152,-15.24]
Y_LIMITS = [-21.336, 42.672]

plt.figure(0)

for run in runs_to_plot:

    run_data = list(csv.reader(open(run)))

    t = []
    x = []
    y = []

    for line in run_data:
        t.append(float(line[0]))
        x.append(float(line[1]))
        y.append(float(line[2]))

    plt.plot(x,y,'o')

with open("beacon_map.json", "r") as file:
    beacon_map = json.load(file)
    
beacon_x = []
beacon_y = []

for value in beacon_map.values():
    beacon_x.append(value["x"])
    beacon_y.append(value["y"])

plt.plot(beacon_x, beacon_y, 'o')

plt.xlim(X_LIMITS)
plt.ylim(Y_LIMITS)
plt.savefig(OUT_FILE)
plt.show()
