import os
from core import picture
from core import sim
import math
from core import forcer
import numpy as np
import sys

SIMULATION_RANGE = np.linspace(0, 200, 1300)

if __name__ == "__main__":
    print("python3 commandline.py <pvimage> <paraimage>")
    initials = picture.initial_conditions_pictures(sys.argv[1], sys.argv[2])

    sine_source = lambda t: (math.exp(-0.0002*t)*0.75 + 0.25)*math.sin(t)

    forcing = forcer.Force(400, 300, sine_source)
    simulator = sim.RamSim(initials)

    simulator.forcers.append(forcing)

    directory = 0
    while os.path.exists(f"output/sim{directory}"):
        directory += 1

    os.mkdir(f"output/sim{directory}")
    output_dir = f"output/sim{directory}"

    for t in SIMULATION_RANGE:
        print(f"Currently at time {t} steps")
        data = simulator.at_time(t)[0, :, :]
        image = picture.array_to_image(picture.scale_array(data))
        image.save(f"{output_dir}/{t}.png", format="png")