import MDR204
import poly
import time
import datetime

current_time = datetime.datetime.now(tz=None)
date = str(current_time.year) + str(current_time.month) + str(current_time.day)

ip = '192.168.10.80'
port = 8080

monochrom = MDR204.monochromator(ip, port)

file_for_recording = date + 'now_written.txt'
files_list = []
point = 0
#monochrom.setWavelength(1057)
for exp in range(1,2):
    for wav in range(10505, 10630, 1):
        wave = wav / 10
        print(wave)
        monochrom.setWavelength(wave)
        if point == 0:
            time.sleep(15)
            point +=1
        file_new = poly.saveData()
        print(file_new)
        files_list.append(file_new)

        with open(file_for_recording, 'a') as fast_file:
            fast_file.write(str(exp))
            fast_file.write('    ')
            fast_file.write(str(wave))
            fast_file.write('    ')
            fast_file.write(str(file_new))
            fast_file.write('\n')
        time.sleep(10)

    print('current wavelength: ', monochrom.curr_wl)

with open('written_files_list.txt', 'w') as file:
    for item in files_list:
        file.write(str(item))
        file.write('\n')

