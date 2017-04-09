import nuke
def nodePresetsStartup():
  nuke.setUserPreset("ColorLookup", "EdgeDetect", {'selected': 'true', 'lut': 'master {}\nred {}\ngreen {}\nblue {}\nalpha {curve L 0 x0.5 1 x0.5808822513 1 x1 0}'})
