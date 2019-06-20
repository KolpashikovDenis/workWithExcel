from pylab import *
from matplotlib import pyplot as plt

x = linspace(0, 5, 15)
y = x ** 2
y1 = x **3 - 2*x**2

fig = plt.figure(figsize=(12, 8))
axes1=fig.add_subplot(2, 2, 1)

# Основной график
axes1.plot(x, y, 'b', label='Утилизация CPU')
axes1.plot([], [], 'g', label = 'Очередь CPU')
axes1.set_xlabel('Продолжительность теста, ч:мм')
axes1.set_ylabel('Утилизация CPU, %')
axes1.set_title('Утилизация CPU')
ylim = axes1.get_ylim()
legend(loc='upper left')
ax = axes1.twinx()
ax.plot(x, y1, 'g')
ax.set_ylabel("очереди CPU")
ax.set_ylim(ylim[0], ylim[1])
plt.grid()

axes2=fig.add_subplot(2, 2, 2)
axes2.plot(x, y, 'b', label='Утилизация CPU')
axes2.plot([], [], 'g', label = 'Очередь CPU')
axes2.set_xlabel('Продолжительность теста, ч:мм')
axes2.set_ylabel('Утилизация CPU, %')
axes2.set_title('Утилизация CPU')
ylim = axes2.get_ylim()
legend(loc='upper left')
ax2 = axes2.twinx()
ax2.plot(x, y1, 'g')
ax2.set_ylabel("очереди CPU")
ax2.set_ylim(ylim[0], ylim[1])
plt.grid()

plt.subplots_adjust(wspace=0.3, hspace=0.3)
plt.show()
