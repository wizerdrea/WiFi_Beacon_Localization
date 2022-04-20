import matplotlib.pyplot as plt
import csv
import json

runs_to_plot = [("run1.csv", 15.2, 24.4, "red", "Loc 1"), ("run2.csv", 29, 27.4, "blue", "Loc 2"), ("run3.csv", 24.4, 33.5, "green", "Loc 3"), ("run4.csv", 0, 21.3, "pink", "Loc 4"), ("run5.csv", 0, 0, "grey", "Loc 5"), ("run6.csv", 45.7, 0, "orange", "Loc 6"), ("run7.csv", 45.7, 27.4, "purple", "Loc 7")]
OUT_FILE = "graph.png"
X_LIMITS = [73.152,-15.24]
Y_LIMITS = [-21.336, 42.672]

plt.figure(0)

for run in runs_to_plot:

    plt.plot(run[1],run[2],'*', color=run[3])
    
    run_data = list(csv.reader(open(run[0])))

    t = []
    x = []
    y = []

    for line in run_data:
        t.append(float(line[0]))
        x.append(float(line[1]))
        y.append(float(line[2]))

    plt.plot(x,y,'o', color=run[3], label=run[4])
    

plt.xlim(X_LIMITS)
plt.ylim(Y_LIMITS)
plt.legend(loc="upper left")
plt.savefig(OUT_FILE)
plt.show()
