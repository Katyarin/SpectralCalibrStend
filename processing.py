import matplotlib.pyplot as plt
import json
import math
import numpy as np
import raw_data_to_json_v2
import datetime

current_time = datetime.datetime.now(tz=None)
date = str(current_time.year) + str(current_time.month) + str(current_time.day)
group = 4

date = str(20221110)



polyn = 34
G = 10
exp_list = []
wave_list = []
file_list = []
with open(str(date) + 'now_written.txt', 'r') as file_written:
    for line in file_written:
        data = line.split()
        print(data)
        exp_list.append(int(data[0]))
        wave_list.append(float(data[1]))
        file_list.append(data[2])
#file_n = '100pages.json'
path = 'out/'
#path_real = 'd:/data/db/debug/drs/'
path_real = 'c:/code/TS_T15MD/fast/files/sp_char_divertor/lsAdc_'
delete_s = int(len(path_real))

plot_osc = False
plot_exp_sig = True # False
time_for_start_plot = 28 #ms
thomson = 'divertor' #or 'usual' #or 'ust' or 'divertor'
laser_const = 1

res_data_path = 'phe_data/'


def find_start_integration(signal):
    maximum = signal.index(max(signal))
    for i in range(0, maximum):
        if signal[maximum - i] > 0 and signal[maximum - i - 1] <= 0:
            return maximum - i - 1
    return 0


def find_end_integration(signal):
    maximum = signal.index(max(signal))
    for i in range(maximum, len(signal) - 1):
        if signal[i] > 0 and signal[i + 1] <= 0:
            return i + 1
    return len(signal) - 1



def to_phe(shotn, raw_data, exp):

    #filename = path + file_n

    M = 100
    el_charge = 1.6 * 10 ** (-19)
    #G = 10
    R_sv = 10000
    freq = 5  # GS/s
    time_step = 1 / freq  # nanoseconds
    event_len = 1024

    delta = {0: 0, 1: 770, 2: 790, 3: 790, 4: 800, 5: 810, 6: 830, 7: 0}
    delta_divertor = {0: 100, 1: 600, 2: 730, 3: 730, 4: 600, 5: 600, 6: 600, 7: 100}
    timestamps = []
    N_photo_el = {}
    var_phe = {}
    timeline = [i * time_step for i in range(event_len)]
    calc_err = {}
    #print(timeline)

    for ch in range(8):
        N_photo_el[ch] = []
        var_phe[ch] = []
        calc_err[ch] = []


    p = 0
    for event in raw_data:
        timestamps.append(event['t']/1000 + 3.73)

        #if max(event['ch'][1]) > 0.030:
        if event['t'] > time_for_start_plot and plot_osc and p < 5:
            fig2, axs2 = plt.subplots(3, 3)
            fig2.suptitle(event['t']/1000 + 3.73)
            p += 1
            print(p)
        for ch in range(8):
            signal = event['ch'][ch]
            if max(signal) > 0.8:
                calc_err[ch].append('off scale')
                #print(event['t']/1000 + 3.73)
            else:
                calc_err[ch].append('')
            if ch == 0 or ch == 7:
                pre_sig = 20
            else:
                pre_sig = 100

            if ch == 0:
                index_0 = 0
                for i, s in enumerate(signal[1:]):
                    if s > 0.200:
                        index_0 = i
                        #print(index_0)
                        break

            delta_exp = {}
            if thomson == 'usual':
                width = 120
                delta_exp[ch] = delta[ch]
            elif thomson == 'ust':
                width = 250
                delta_exp[ch] = delta[ch] - 100
            elif thomson == 'divertor':
                width = 100
                delta_exp[ch] = delta_divertor[ch]
            else:
                print('something wrong! Unnown config')
                stop

            base_line = sum(signal[index_0 + delta_exp[ch] - pre_sig:index_0 + delta_exp[ch]]) / len(signal[index_0 + delta_exp[ch] - pre_sig:index_0 + delta_exp[ch]])
            raw_signal = signal
            signal = []
            for i in range(len(raw_signal)):
                signal.append(raw_signal[i] - base_line)



            for i in range(len(signal)):
                signal[i] = signal[i] * 1000
            var_in_sr = np.var(signal[5:pre_sig])

            '''start_index = find_start_integration(signal[10:-10]) - 5
            end_index = find_end_integration(signal[10:-10]) + 5'''
            start_index = index_0 + delta_exp[ch]
            end_index = start_index + width


            if 6>p>0:
                #print(max(event['ch'][5]), event['t']/1000)
                axs2[int(ch//3), int(ch%3)].set_title('ch = ' + str(ch))
                axs2[int(ch//3), int(ch%3)].plot(signal)
                axs2[int(ch//3), int(ch%3)].vlines(start_index, min(signal), max(signal), color='m')
                axs2[int(ch//3), int(ch%3)].vlines(end_index, min(signal), max(signal), color='m')
                axs2[int(ch // 3), int(ch % 3)].hlines(sum(signal[10:pre_sig]) / len(signal[10:pre_sig]), 0, len(signal), color='r')
                axs2[int(ch // 3), int(ch % 3)].hlines(sum(signal[len(signal)-pre_sig:len(signal)-10]) / len(signal[len(signal)-pre_sig:len(signal)-10]), 0,
                                                       len(signal), color='g')


            Ni = np.trapz(signal[start_index:end_index],
                                timeline[start_index:end_index]) / (M * el_charge * G * R_sv * 0.5)
            '''if ch==6:
                Ni = Ni * (M * el_charge * G * R_sv * 0.5) * laser_const'''
            N_photo_el[ch].append(Ni *1e-12)
            var = math.sqrt(math.fabs(6715 * 0.0625 * var_in_sr - 1.14e4 * 0.0625) + math.fabs(Ni *1e-12) * 4)
            var_phe[ch].append(var)
        plt.show()
        #p=0
    '''plt.figure(figsize=(10, 3))
    plt.title('Shot #' + str(shotn))
    for ch in N_photo_el.keys():
        print(ch, sum(N_photo_el[ch]) / len(N_photo_el[ch]))
        #color = ['r', 'g', 'b', 'm', 'black', 'orange', 'brown', 'pink']
        if ch ==1:
            plt.errorbar(timestamps, N_photo_el[ch], yerr=var_phe[ch], label='ch' + str(ch))
            plt.hlines(sum(N_photo_el[ch]) / len(N_photo_el[ch]), 0, max(timestamps), colors='r')
            plt.scatter([t for i, t in enumerate(timestamps) if calc_err[ch][i] == 'off scale'],
                        [j for i, j in enumerate(N_photo_el[ch]) if calc_err[ch][i] == 'off scale'], marker='x', s=40, c='black', zorder=2.5)
        #plt.plot(timestamps, N_photo_el[ch], '^-', label='ch' + str(ch))
    #N_photo_el[6][0] = N_photo_el[6][1]
    plt.ylabel('N, phe')
    plt.grid()
    plt.xlabel('time')
    plt.legend()
    plt.figure(figsize=(10, 3))
    plt.title('Shot #' + str(shotn))
    #plt.errorbar(timestamps, N_photo_el[6], yerr=var_phe[6], label='ch' + str(6))
    plt.plot(timestamps, N_photo_el[7], label='ch' + str(7))
    #print(1.25 / (sum(N_photo_el[6][2:])/len(N_photo_el[6][2:])))
    plt.ylabel('N, phe')
    plt.grid()
    plt.xlabel('time')
    plt.legend()
    plt.figure(figsize=(10, 3))
    plt.title('Shot #' + str(shotn))
    plt.plot(timestamps, [N_photo_el[1][i]/N_photo_el[7][i] for i in range(len(timestamps))], label='ch1 normalized')
    plt.ylabel('N')
    plt.grid()
    plt.xlabel('time')
    plt.legend()
'''
    #plt.show()

    with open(res_data_path + date + str(exp)+ '_%d_N_phe.json' %shotn, 'w') as f:
        for_temp = {'timeline': timestamps, 'data': N_photo_el, 'err': var_phe, 'culc_err': calc_err, 'laser_en': N_photo_el[6]}
        json.dump(for_temp, f)

    with open(date + 'result_files' + str(exp) +'.txt', 'a') as f_r:
        f_r.write(str(shotn))
        f_r.write('    ')
        for ch in N_photo_el.keys():
            mean = sum(N_photo_el[ch]) / len(N_photo_el[ch])
            sigma = (sum([(i - mean) * (i - mean) for i in N_photo_el[ch]]) / len(N_photo_el[ch]) / (len(N_photo_el[ch]) - 1))**0.5
            f_r.write(str(mean))
            f_r.write('    ')
            f_r.write(str(sigma))
            f_r.write('    ')
            print(ch, mean, sigma)
        f_r.write('\n')

exp = 0
for i, wave in enumerate(wave_list):
    print(i, wave)
    if exp_list[i] > exp:
        exp = exp_list[i]
    if exp_list[i] != group:
        print('no')
        continue
    waves_read = []
    try:
        with open(date + 'result_files' + str(exp) +'.txt', 'r') as fin_file:
            for line in fin_file:
                waves_read.append(float(line.split()[0]))
    except FileNotFoundError:
        with open(date + 'result_files' + str(exp) + '.txt', 'w') as fin_file0:
            fin_file0.write('0')
            fin_file0.write('    ')
            for ch in range(8):
                fin_file0.write(str(ch))
                fin_file0.write('    ')
    if wave in waves_read:
        print(wave, ' already done')
        continue
    try:
        data = raw_data_to_json_v2.to_json(str(file_list[i][delete_s:]), False)
    except ValueError:
        print('value error in this datafile!!!')
        continue
    if wave == 1050 or wave == 1055 or wave == 1035 or wave == 1010 or wave == 950:
        plot_osc = True
    else:
        plot_osc = False
    to_phe(wave, data, exp_list[i])