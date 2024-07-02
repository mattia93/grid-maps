from map_utils import Map
import json
import configparser
from project_utils import set_working_dir, get_script_name, get_list_from_config
import os

if __name__ == '__main__':

    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    set_working_dir()

    config.read(f'{get_script_name()}.ini')
    if config['DEFAULT'].getboolean('run_debug_mode'):
        main_tag = 'DEBUG_SETTINGS'
        exp_tag = 'DEBUG_SETTINGS'
    else:
        main_tag = 'DEFAULT'
        exp_tag = 'EXPERIMENTAL_SETTINGS'
    

    target_maps_dir = config[main_tag]['maps_dir']
    target_problems_dir = config[main_tag]['pddl_dir']

    if not os.path.exists(target_maps_dir):
        os.makedirs(target_maps_dir)
    if not os.path.exists(target_problems_dir):
        os.makedirs(target_problems_dir)

    rows = get_list_from_config(config[exp_tag]['rows'], int)
    obstacle_percs = get_list_from_config(config[exp_tag]['obstacle_percs'], int)
    num_maps = int(config[exp_tag]['num_maps'])
    
    index = 0

    for row in rows:
        for obstacle_perc in obstacle_percs:
            json_file = os.path.join(target_maps_dir, f'maps_{row}x{row}_{obstacle_perc}.json')
            maps_set = set()
            count = 0
            while len(maps_set) < num_maps and count < 1000:
                map = Map(row, row, obstacle_perc)
                if tuple(map.array.flatten()) not in maps_set:
                    maps_set.add(tuple(map.array.flatten()))
                    count = 0
                    tuples = map.select_sources_targets(20)
                    for source, target in tuples:
                        fname = f'p{index :06d}'
                        with open(json_file, 'a') as f:
                            json.dump({'problem' : fname, 'map': map.array.tolist(), 'source_destination' : (source, target)}, f)
                            f.write('\n')
                            f.close()
                        with open(os.path.join(target_problems_dir, f'{fname}.pddl'), 'w') as f:
                            f.write(map.to_pddl((source, target)))
                            f.close()
                        index += 1
                else:
                    count += 1
                if obstacle_perc == 0:
                    break
            
                
                