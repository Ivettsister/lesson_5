from matplotlib import pyplot as plt
import numpy
import matplotlib.ticker as tick
from textwrap import wrap

with open('settings.txt') as file:
    settings = [float(i) for i in file.read().split('\n')]

data = numpy.loadtxt('data.txt', dtype=int) * settings[1]
data_time = numpy.array([i * settings[0] for i in range(data.size)])

fig, ax = plt.subplots(figsize=(16, 10), dpi=500)

ax.axis([data_time.min(), data_time.max() + 1, data.min(), data.max() + 0.2])

ax.xaxis.set_major_locator(tick.MultipleLocator(2))
ax.xaxis.set_minor_locator(tick.MultipleLocator(0.5))
ax.yaxis.set_major_locator(tick.MultipleLocator(0.5))
ax.yaxis.set_minor_locator(tick.MultipleLocator(0.1))

ax.set_title("\n".join(wrap('Зарядка и разрядка конденсатора RC-цепи')), loc='center')

ax.grid(which='major', color='c')
ax.minorticks_on()
ax.grid(which='minor', color='b', linestyle=':')

ax.set_xlabel('Time, s')
ax.set_ylabel('Voltage, v')

ax.plot(data_time, data, c='black', linewidth=1, label='V(t)')
ax.scatter(data_time[0:data.size:20], data[0:data.size:20], marker='s', c='grey')
ax.legend(shadow=False, loc='upper right', fontsize = 20)

ax.text(15, 2.25 , "Время зарядки - 10.76 s", fontsize = 15)
ax.text(15, 2.4, "Время разрядки - 13.49 s", fontsize = 15)

fig.savefig('figure.png')
plt.savefig('graph.svg')
plt.show()
