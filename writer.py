import MDR204
import poly
import time


ip = '192.168.10.80'
port = 8080

monochrom = MDR204.monochromator(ip, port)

file_for_recording = 'now_written.txt'
files_list = []
#monochrom.setWavelength(1057)
for wave in range(1057, 1046, -1):
    print(wave)
    monochrom.setWavelength(wave)
    file_new = poly.saveData()
    print(file_new)
    files_list.append(file_new)

    with open(file_for_recording, 'a') as fast_file:
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

