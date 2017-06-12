import os
import json


def run():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    shows_json = os.path.join(dir_path, "Core", "config", "shows.json")

    with open(shows_json) as j:
        env = json.load(j)
    for active_show in env:
        for show in env[active_show]:
            entered_show = raw_input("Show:")
            if entered_show == show:
                show_is_valid = True
                entered_seq = raw_input("Seq:")
                for seq in env[active_show][show]:
                    if seq == entered_seq:
                        seq_is_valid = True
                        entered_shot = raw_input("Shot:")
                        for shot in env[active_show][show][seq]:
                            if entered_shot == str(shot):
                                shot_is_valid = True
                                print show, seq, shot
                                break
                            else:
                                shot_is_valid = False
                    else:
                        seq_is_valid = False
            else:
                show_is_valid = False

    show_env = {}
    if show_is_valid:
        show_env['show'] = show
        if seq_is_valid:
            show_env['seq'] = seq
            if shot_is_valid:
                show_env['shot'] = shot
            else:
                print "Sorry can't find %s as a valid shot" % entered_shot
        else:
            print "Sorry can't find %s as a valid seq" % entered_seq
    else:
        print "Sorry can't find %s as a valid show" % entered_show
    if len(show_env) == 3:
        return show_env
    else:
        return None
