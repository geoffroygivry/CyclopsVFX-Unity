import os
import json
import nuke


def in_nuke():
    shot_name = os.getenv('SHOT')
    check = False
    cache_dir = os.getenv('CYC_HYDRA_CACHE')
    with open(os.path.join(cache_dir, 'shots.json')) as j:
        shots = json.load(j)
        for shot in shots:
            if shot_name == shot:
                check = True
        if check:
            first = shots.get(shot_name).get('first')
            last = shots.get(shot_name).get('last')
    root = nuke.Root()
    root['first_frame'].setValue(first)
    root['last_frame'].setValue(last)
