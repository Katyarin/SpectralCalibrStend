import matplotlib.pyplot as plt
import json
import math
import numpy as np
import raw_data_to_json

polyn = 34
G = 10
wave_list = []
file_list = []
with open('now_written.txt', 'r') as file_written:
    for line in file_written:
        data = line.split()
        print(data)
        wave_list.append(int(data[0]))
        file_list.append(data[1])
#file_n = '100pages.json'
path = 'drs_raw_data/'
path_real = 'C:/Users/user/Desktop/drs/'
delete_s = int(len(path_real))

plot_osc = False
plot_exp_sig = True # False
time_for_start_plot = 26 #ms
thomson = 'usual' #or 'usual' #or 'ust' or 'divertor'
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



def to_phe(shotn, file_n):

    filename = path + file_n

    M = 100
    el_charge = 1.6 * 10 ** (-19)
    #G = 10
    R_sv = 10000
    freq = 5  # GS/s
    time_step = 1 / freq  # nanoseconds
    event_len = 1024

    delta = {0: 0, 1: 150, 2: 170, 3: 190, 4: 200, 5: 210, 6: 0, 7: 0}
    delta_divertor = {0: 0, 1: -480, 2: -470, 3: -460, 4: -450, 5: -440, 6: -25, 7: 0}
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

    with open(filename, 'r') as file:
        raw_data = json.load(file)

    p = 0
    for event in raw_data[1:]:
        timestamps.append(event['t']/1000 + 3.73)

        #if max(event['ch'][1]) > 0.030:
        if event['t']/1000 + 3.73 > time_for_start_plot and plot_osc:
            fig2, axs2 = plt.subplots(3, 3)
            fig2.suptitle(event['t']/1000 + 3.73)
            p = 1
        for ch in range(8):
            signal = event['ch'][ch]
            if max(signal) > 0.8:
                calc_err[ch].append('off scale')
                #print(event['t']/1000 + 3.73)
            else:
                calc_err[ch].append('')
            if ch == 0 or ch == 7:
                pre_sig = 100
            else:
                pre_sig = 200
            base_line = sum(signal[5:pre_sig]) / len(signal[5:pre_sig])
            for i in range(len(signal)):
                signal[i] = signal[i] - base_line

            if ch == 0:
                index_0 = 0
                for i, s in enumerate(signal[10:]):
                    if s > 0.250:
                        index_0 = i - 20
                        #print(index_0)
                        break

            for i in range(len(signal)):
                signal[i] = signal[i] * 1000
            var_in_sr = np.var(signal[5:pre_sig])
            delta_exp = {}
            if thomson == 'usual':
                width = 100
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
            start_index = find_start_integration(signal[10:-10]) - 5
            end_index = find_end_integration(signal[10:-10]) + 5


            if p:
                #print(max(event['ch'][5]), event['t']/1000)
                axs2[int(ch//3), int(ch%3)].set_title('ch = ' + str(ch))
                axs2[int(ch//3), int(ch%3)].plot(signal)
                axs2[int(ch//3), int(ch%3)].vlines(start_index, min(signal), max(signal))
                axs2[int(ch//3), int(ch%3)].vlines(end_index, min(signal), max(signal))


            Ni = np.trapz(signal[start_index:end_index],
                                timeline[start_index:end_index]) / (M * el_charge * G * R_sv * 0.5)
            '''if ch==6:
                Ni = Ni * (M * el_charge * G * R_sv * 0.5) * laser_const'''
            N_photo_el[ch].append(Ni *1e-12)
            var = math.sqrt(math.fabs(6715 * 0.0625 * var_in_sr - 1.14e4 * 0.0625) + math.fabs(Ni *1e-12) * 4)
            var_phe[ch].append(var)
        #plt.show()
        p=0
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

    with open(res_data_path + '%d_N_phe.json' %shotn, 'w') as f:
        for_temp = {'timeline': timestamps, 'data': N_photo_el, 'err': var_phe, 'culc_err': calc_err, 'laser_en': N_photo_el[6]}
        json.dump(for_temp, f)

    with open('result_files.txt', 'a') as f_r:
        f_r.write(str(shotn))
        f_r.write('    ')
        for ch in N_photo_el.keys():
            f_r.write(str(sum(N_photo_el[ch]) / len(N_photo_el[ch])))
            f_r.write('    ')
        f_r.write('\n')

for i, wave in enumerate(wave_list):
    print(i, wave)
    waves_read = []
    with open('result_files.txt', 'r') as fin_file:
        for line in fin_file:
            waves_read.append(int(line.split()[0]))
    if wave in waves_read:
        print(wave, ' already done')
        continue
    raw_data_to_json.to_json(str(file_list[i][delete_s:]), 7, 'c:/work/Code/SpectralCalibrStend/drs_raw_data/')
    to_phe(wave, str(file_list[i][delete_s:]) + '.json')