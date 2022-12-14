from pathlib import Path
import json
import struct

res_data_path = 'out/'
raw_data_path = 'c:/code/TS_T15MD/fast/files/sp_char_divertor/'

ch_count = 6


def to_json(shotn, save_file=False) -> list:
    # try binary file first
    path: Path = Path('%s%s' % (raw_data_path, str(shotn)))
    if path.is_file():
        data = __bin_to_JSON(path_in=path)
    else:
        # try text file
        path: Path = Path('%s%s.txt' % (raw_data_path, str(shotn)))
        if path.is_file():
            data = __ascii_to_JSON(path_in=path)
        else:
            print(shotn)
            print('%s%s.bin' %(raw_data_path, str(shotn)))
            fuck

    if save_file:
        print('Warning! Data is ready, but saving to disk is slow')
        #path = Path('%s%s/' % (res_data_path, str(shotn)))
        '''if not path.is_dir():
            path.mkdir(parents=True)'''

        with open('%s/%s.json' % (res_data_path, str(shotn)), 'w') as file:
            json.dump(data, file, indent=2)
    return data

def __bin_to_JSON(path_in: Path) -> list:
    data: list = []
    with path_in.open(mode='rb') as file:
        raw = file.read()
        count = len(raw) / (8 * 1024 * 4 + 8)
        if not int(count) == count:
            fuck
        count = int(count)

        for event_ind in range(count):
            event = {
                't': 0,
                'ch': []
            }
            for ch in range(8):
                event['ch'].append(struct.unpack_from('1024f', raw, (event_ind * (8 * 1024 * 4 + 8)) + ch * 1024 * 4))
            event['t'] = event_ind #struct.unpack_from('d', raw, (event_ind * (8 * 1024 * 4 + 8)) + 8 * 1024 * 4)[0]
            data.append(event)
    return data


def __ascii_to_JSON(path_in: Path) -> list:
    data: list = []
    with path_in.open(mode='r') as file:
        count = 0
        event = {
            't': 0,
            'ch': [[] for ch in range(ch_count + 1)]
        }
        for line in file:
            if count > 1023:
                count += 1
                if count == 1026:
                    data.append(event.copy())
                    event = {
                        't': 0,
                        'ch': [[] for ch in range(ch_count + 1)]
                    }
                    count = 0
                continue
            sp = line.split()

            for ch in range(ch_count + 1):
                event['ch'][ch].append(float(sp[1 + ch]))
            if count == 0:
                event['t'] = int(sp[-2])
            count += 1
    return data
