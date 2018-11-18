import os
from core import picture
from core import sim
import numpy as np
import sys

SIMULATION_RANGE = range(0, 2_000, 10)

if __name__ == "__main__":
    print("python3 commandline.py <pvimage> <paraimage>")
    initials = picture.initial_conditions_pictures(sys.argv[1], sys.argv[2])

    simulator = sim.RamSim(initials)

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