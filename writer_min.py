import poly
import time
import datetime

current_time = datetime.datetime.now(tz=None)
date = str(current_time.year) + str(current_time.month) + str(current_time.day)

file_for_recording = date + 'now_written.txt'
files_list = []
point = 0
exp = 2
wave = 1055

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