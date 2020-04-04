# import necessary modules
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm
from matplotlib import style
from matplotlib.colors import Normalize
import numpy as np
import psutil
import time


class Memory:
    def __init__(self, figure, axes):
        self.figure, self.ax = figure, axes
        self.xvalues = [i for i in range(100)]  # initialise x values
        self.yvalues = [0 for _ in range(100)]  # initialise y values to 0

    # function to be called to update graph
    def update(self, j):
        # clear current plot
        self.ax.clear()
        # plot y v/s x
        self.ax.plot(np.array(self.xvalues), np.array(self.yvalues), color='orange', linestyle="--", linewidth=0.9)
        # add recent value as text in graph
        self.ax.text(self.xvalues[-1], self.yvalues[-1] + 2, f"{self.yvalues[-1]}%")
        # get new value
        usage = psutil.virtual_memory().percent
        # update x and y values
        self.xvalues.append(self.xvalues[-1] + 1)
        self.xvalues.__delitem__(0)
        self.yvalues.append(usage)
        self.yvalues.__delitem__(0)
        # set graph attributes
        self.ax.set_ylim(0, 120)
        self.ax.set_xlim(self.xvalues[0] - 1, self.xvalues[-1] + 10)
        self.ax.set_title('RAM', loc='left', fontsize=13)

    def show(self):
        self.anim = animation.FuncAnimation(self.figure, self.update, interval=1500)


class Network:
    def __init__(self, figure, axes):
        self.figure, self.ax = figure, axes
        self.xvalues = [i for i in range(100)]  # initialise x values
        self.upload = [0 for _ in range(100)]  # initialise upload values to 0
        self.download = [0 for _ in range(100)]  # initialise download values to 0
        self.t0 = time.time()  # get time
        self.upload0 = psutil.net_io_counters().bytes_sent  # count upload bytes
        self.download0 = psutil.net_io_counters().bytes_recv  # count download bytes

    def update(self, j):
        self.t1 = time.time()  # get new time
        self.upload1 = psutil.net_io_counters().bytes_sent  # count upload bytes
        self.download1 = psutil.net_io_counters().bytes_recv  # count download bytes
        # find upload and download speed
        upload = (self.upload1 - self.upload0) / (self.t1 - self.t0)
        upload = round(upload / 1000000, 3)
        download = (self.download1 - self.download0) / (self.t1 - self.t0)
        download = round(download / 1000000, 3)
        # set old values to new ones
        self.upload0 = self.upload1
        self.download0 = self.download1
        self.t0 = self.t1
        # clear current plot
        self.ax.clear()
        # plot graph
        self.ax.plot(self.xvalues, self.upload, label="Upload", color='red', linewidth=0.7)
        self.ax.plot(self.xvalues, self.download, label="Download", color='blue', linewidth=0.7)
        # update x values
        self.xvalues.append(self.xvalues[-1] + 1)
        self.xvalues.__delitem__(0)
        # update download values
        self.download.append(download)
        self.download.__delitem__(0)
        # update upload values
        self.upload.append(upload)
        self.upload.__delitem__(0)
        # set graph attributes
        self.ax.set_xlim(self.xvalues[0] - 1, self.xvalues[-1] + 10)
        self.ax.set_ylabel("Mbps", color="black")
        self.ax.set_title('Network', loc='left', fontsize=13)
        self.ax.legend()

    def show(self):
        self.anim = animation.FuncAnimation(self.figure, self.update, interval=1500)


class CPU_USAGE:
    def __init__(self, figure, axes):
        self.figure, self.ax = figure, axes
        # count number of logical cpu cores
        self.num_of_cores = psutil.cpu_count(logical=True)
        # set labels to be used in x axis
        self.labels = [""]
        for i in range(1, self.num_of_cores + 1):
            self.labels.append(f"Core\n{i}")
        self.labels.append("")
        # set array to be passed to bar plot
        self.cores = np.array([i for i in range(1, 9)])
        # get usage
        self.usage = np.array(psutil.cpu_percent(interval=0.1, percpu=True))
        # set a color map
        self.colormap = cm.get_cmap('rainbow')
        # set object to normalize values
        self.norm = Normalize(vmin=0, vmax=100)

    def update(self, j):
        # clear current plot
        self.ax.clear()
        # get usage
        self.usage = np.array(psutil.cpu_percent(interval=0.1, percpu=True))
        # plot bar graph
        self.ax.bar(self.cores, self.usage, width=0.5, alpha=1, color=self.colormap(self.norm(self.usage)))
        # add text for convenience
        for i in range(self.num_of_cores):
            self.ax.text(i+0.75, self.usage[i]+2, f"{self.usage[i]}%")
        # set graph attributes
        self.ax.set_ylim(0, 120)
        self.ax.set_xlim(0, 9)
        self.ax.set_xticklabels(self.labels, fontsize=11, color="black")
        self.ax.set_title('CPU', loc='left', fontsize=13)

    def show(self):
        self.anim = animation.FuncAnimation(self.figure, self.update, interval=1500)


if __name__ == "__main__":
    # setting a style to use
    style.use('Solarize_Light2')

    # create a figure, arg is title of window
    fig = plt.figure("System Performance")

    # define subplots and their positions in figure
    core_use = fig.add_subplot(212)
    memory_use = fig.add_subplot(221)
    network_use = fig.add_subplot(222)

    cpu = CPU_USAGE(fig, core_use)
    cpu.show()

    ram = Memory(fig, memory_use)
    ram.show()

    network = Network(fig, network_use)
    network.show()

    # add title to plot
    fig.suptitle("SYSTEM PERFORMANCE", fontname='Constantia', fontsize=20)

    # to start plot in maximised window by default
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())

    # show figure
    plt.show()
