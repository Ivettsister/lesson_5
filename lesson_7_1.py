import RPi.GPIO as gpio
import time
from time import sleep
from matplotlib import pyplot

gpio.setmode(gpio.BCM)

leds = [21, 20, 16, 12, 7, 8, 25, 24]
gpio.setup(leds, gpio.OUT)

dac = [26, 19, 13, 6, 5, 11, 9, 10]
gpio.setup(dac, gpio.OUT, initial=gpio.HIGH)

comparator = 4
troyka = 17

gpio.setup(comparator, gpio.IN)
gpio.setup(troyka, gpio.OUT, initial = gpio.HIGH)

def translate(num):
    return [int (elem) for elem in bin(num)[2:].zfill(8)]

def adc():
    k = 0
    for i in range(7, -1, -1):
        k += 2 ** i
        gpio.output(dac, translate(k))
        sleep(0.005)
        if gpio.input(comparator) == 0:
            k -= 2 ** i
    return k

try:
    u = 0
    result_mer = []
    time_start = time.time()
    cnt = 0

    print('Зарядка конденсатора:\n')
    while u < 256 * 0.9:
        u = adc()
        result_mer.append(u)
        time.sleep(0)
        cnt += 1
        gpio.output(leds, translate(u))

    gpio.setup(troyka, gpio.OUT, initial=gpio.LOW)

    print('Разрядка конденсатора:\n')
    while u > 256 * 0.02:
        u = adc()
        result_mer.append(u)
        time.sleep(0)
        cnt += 1
        gpio.output(leds, translate(u))

    time_experiment = time.time() - time_start

    print('Запись данных в файл:\n')

    with open('data.txt', 'w') as file:
        for i in result_mer:
            file.write(str(i) + '\n')
    with open('settings.txt', 'w') as f:
        f.write(str(1/time_experiment/cnt) + '\n')
        f.write('0.01289')

    print('Длительность эксперимента {}, период измерений {}, частота дискретизации {}, шаг квантования {}\n'.format(time_experiment, time_experiment/cnt, 1/time_experiment/cnt, 0.013))
    print('Графики\n')

    y = [i/256*3.3 for i in result_mer]
    x = [i*time_experiment/cnt for i in range (len(result_mer))]
    pyplot.plot(x, y)
    pyplot.show()

finally:
    gpio.output(dac, 0)
    gpio.cleanup()