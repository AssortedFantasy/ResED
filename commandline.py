import os
from core import picture
from core import sim
import math
from core import forcer
import numpy as np
import sys

SIMULATION_RANGE = range(0, 3_000, 10)

if __name__ == "__main__":
    print("python3 commandline.py <pvimage> <paraimage>")
    initials = picture.initial_conditions_pictures(sys.argv[1], sys.argv[2])

    sine_source = lambda t: 1*math.sin(t*8)

    forcing = forcer.Force(130, 300, sine_source)
    simulator = sim.RamSim(initials)

    # simulator.forcers.append(forcing)

    directory = 0
    while os.path.exists(f"output/sim{directory}"):
        directory += 1

    os.mkdir(f"output/sim{directory}")
    output_dir = f"output/sim{directory}"

    for t in SIMULATION_RANGE:
        print(f"Currently at time {t} steps")
        data = simulator.at_step(t)[0, :, :]
        image = picture.array_to_image(picture.scale_array(data))
        image.save(f"{output_dir}/{t}.png", format="png")