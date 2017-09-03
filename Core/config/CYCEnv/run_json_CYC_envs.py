import os
import json


def create_json_CYC_envs(root_dir):
    DI_ROOT = root_dir
    CYC_ROOT = "%s/CyclopsVFX" % DI_ROOT
    DATA_FILENAME = os.path.join(CYC_ROOT, "CYC_envs.json")
    CYC_HYDRA_PATH = "%s/Hydra" % (CYC_ROOT)
    CYC_HYDRA_CACHE = "%s/Hydra/cache" % (CYC_ROOT)
    CYC_CORE_PATH = "%s/Core/config/" % (CYC_ROOT)
    CYC_NUKE_ENV = "%s/Core/config/NukeEnv" % (CYC_ROOT)
    CYC_MAYA_ENV = "%s/Core/config/MayaEnv" % (CYC_ROOT)
    CYC_RV_ENV = "%s/Core/config/RVEnv" % (CYC_ROOT)
    CYC_MARI_ENV = "%s/Core/config/MariEnv" % (CYC_ROOT)
    CYC_3DE_ENV = "%s/Core/config/3DeEnv" % (CYC_ROOT)
    CYC_CLARISSE_ENV = "%s/Core/config/ClarisseEnv" % (CYC_ROOT)
    CYC_SHOW_ENV = "%s/Core/config/ShowEnv" % (CYC_ROOT)
    CYC_POLYPHEMUS_PATH = "%s/Apps/Polyphemus" % (CYC_ROOT)
    CYC_STEROPES_PATH = "%s/Apps/Steropes" % (CYC_ROOT)
    CYC_ENGINE_NUKE = "%s/Apps/Engines/Nuke" % (CYC_ROOT)
    CYC_ICON = "%s/icons" % (CYC_ROOT)
    NUKE_PATH = CYC_NUKE_ENV
    SHOW_PATH = os.path.join(DI_ROOT, "jobs")

    with open(DATA_FILENAME, mode='w') as feedsjson:
        CYC_envs = {
            "CYC_envs": {
                "DI_ROOT": DI_ROOT,
                "CYC_ROOT": CYC_ROOT,
                "CYC_HYDRA_PATH": CYC_HYDRA_PATH,
                "CYC_HYDRA_CACHE": CYC_HYDRA_CACHE,
                "CYC_CORE_PATH": CYC_CORE_PATH,
                "CYC_NUKE_ENV": CYC_NUKE_ENV,
                "CYC_MAYA_ENV": CYC_MAYA_ENV,
                "CYC_RV_ENV": CYC_RV_ENV,
                "CYC_MARI_ENV": CYC_MARI_ENV,
                "CYC_3DE_ENV": CYC_3DE_ENV,
                "CYC_CLARISSE_ENV": CYC_CLARISSE_ENV,
                "CYC_SHOW_ENV": CYC_SHOW_ENV,
                "CYC_POLYPHEMUS_PATH": CYC_POLYPHEMUS_PATH,
                "CYC_STEROPES_PATH": CYC_STEROPES_PATH,
                "CYC_ENGINE_NUKE": CYC_ENGINE_NUKE,
                "CYC_ICON": CYC_ICON,
                "NUKE_PATH": NUKE_PATH,
                "SHOW_PATH": SHOW_PATH
            }
        }

        json.dump(CYC_envs, feedsjson, indent=4, sort_keys=True)


create_json_CYC_envs("/home/geoff/Dropbox")
