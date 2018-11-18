import numpy as np
import scipy.ndimage.filters as filters


# Global Parameters
DEFAULT_TIME_STEP = 0.01
ARRAY_BREAK_LENGTH = 1_000    # Must be > 3
RAM_SAVER_SAVER = 100


class Simulator:
    # Main simulator for program.
    def __init__(self, initial_conditions: np.ndarray, timestep=DEFAULT_TIME_STEP, edge_conditions="constant", edge_value=0):
        if edge_conditions not in ['reflect', 'constant', 'nearest', 'mirror', 'wrap']:
            raise RuntimeError("invalid edge condition!")
        edge_value = float(edge_value)
        initial_conditions = np.array(initial_conditions, dtype=np.float)

        self.edge_value = edge_value
        self.edge_conditions = edge_conditions
        self.timestep = timestep
        self.simulation_parameters = initial_conditions[2:, :, :]
        self.sim_data = []
        self.forcers = []

        # First step (step 0) is defined.
        self.step = 1

        z, self.height, self.width = initial_conditions.shape

        if z != 5:
            raise RuntimeError("invalid initial conditions!")

        data = np.zeros((ARRAY_BREAK_LENGTH, 3, self.height, self.width), dtype=np.float)
        self.sim_data.append(data)

        # Initial calculations done manually.

        # Setting initial positions
        data[0, 0, :, :] = initial_conditions[0, :, :]
        # Setting initial velocity
        data[0, 1, :, :] = initial_conditions[1, :, :]
        # Calculating initial acceleration using positions and velocities.
        compute_accelerations(data[0, 2, :, :], data[0, 1, :, :], data[0, 0, :, :], self.simulation_parameters,
                              self.forcers, 0, self.edge_conditions, self.edge_value)

    def simulate(self, steps=1):
        for _ in range(steps):
            data = self.sim_data[-1]
            index = self.step % ARRAY_BREAK_LENGTH

            # These are not copies, they are views
            prev_position = data[index-1, 0, :, :]
            prev_velocity = data[index-1, 1, :, :]
            prev_acceleration = data[index-1, 2, :, :]

            # Handling split arrays
            if self.step % ARRAY_BREAK_LENGTH == 0:
                # Split magically
                new_data = np.zeros((ARRAY_BREAK_LENGTH, 3, self.height, self.width), dtype=np.float)
                self.sim_data.append(new_data)
                data = self.sim_data[-1]

            # Also not copies, these are views
            curr_position = data[index, 0, :, :]
            curr_velocity = data[index, 1, :, :]
            curr_acceleration = data[index, 2, :, :]

            # Forward Euler Method
            curr_position += prev_position + prev_velocity*self.timestep + 1/2*prev_acceleration*self.timestep**2
            curr_velocity += prev_velocity + prev_acceleration*self.timestep
            # Compute Current Acceleration
            compute_accelerations(curr_acceleration, curr_velocity, curr_position, self.simulation_parameters,
                                  self.forcers, self.step*self.timestep, self.edge_conditions, self.edge_value)
            self.step += 1

    def simulate_time(self, time=1):
        number_of_steps = int(time/self.timestep)
        self.simulate(number_of_steps)

    def at_step(self, step):
        if self.step < step:
            self.simulate(step - self.step + 1)

        data = self.sim_data[step // ARRAY_BREAK_LENGTH]
        return data[step % ARRAY_BREAK_LENGTH, :, :, :].copy()

    def at_time(self, time):
        # Nearest Calculated point, then do forward Euler integration on it.
        nearest_lower_step = int(time/self.timestep)
        # Now that we have this we need to grab the nearest lower step and perform forward Euler on it.
        previous_values = self.at_step(nearest_lower_step)
        delta_t = time - self.timestep*nearest_lower_step

        previous_values[0, :, :] += previous_values[1, :, :]*delta_t + 1/2*previous_values[2, :, :]*delta_t**2
        previous_values[1, :, :] += previous_values[2, :, :]*delta_t

        # Now we need to calculate the accleration, again.
        compute_accelerations(previous_values[2, :, :], previous_values[1, :, :], previous_values[0, :, :],
                              self.simulation_parameters, self.forcers, time, self.edge_conditions, self.edge_value)
        return previous_values[:, :, :]


class RamSim(Simulator):
    # Much less ram murdering :^) Only stores one set of frames.
    def simulate(self, steps=1):
        data = self.sim_data[0]
        for _ in range(steps):
            index = self.step % ARRAY_BREAK_LENGTH

            # These are not copies, they are views
            prev_position = data[index-1, 0, :, :]
            prev_velocity = data[index-1, 1, :, :]
            prev_acceleration = data[index-1, 2, :, :]
            # For the ram saver version, we just roll with the fact we are overwriting previous data.

            # Also not copies, these are views
            curr_position = data[index, 0, :, :]
            curr_velocity = data[index, 1, :, :]
            curr_acceleration = data[index, 2, :, :]

            # Forward Euler Method
            curr_position += prev_position + prev_velocity*self.timestep + 1/2*prev_acceleration*self.timestep**2
            curr_velocity += prev_velocity + prev_acceleration*self.timestep
            # Compute Current Acceleration
            compute_accelerations(curr_acceleration, curr_velocity, curr_position, self.simulation_parameters,
                                  self.forcers, self.step*self.timestep, self.edge_conditions, self.edge_value)
            self.step += 1

    def at_step(self, step):
        if self.step < step:
            self.simulate(step - self.step + 1)

        data = self.sim_data[0]
        return data[step % ARRAY_BREAK_LENGTH, :, :, :].copy()


def compute_accelerations(current_acceleration, current_velocities, current_positions, simulation_parameters, forcers,
                          time, edge_conditions, edge_value):
    # First Laplace * E
    filters.laplace(current_positions, current_acceleration, edge_conditions, edge_value)
    current_acceleration *= simulation_parameters[0, :, :]

    # Then -B * V
    current_acceleration -= current_velocities * simulation_parameters[2, :, :]

    # Then forcers forces
    for forcer in forcers:
        current_acceleration[forcer.position_y, forcer.position_x] += forcer(time)

    current_acceleration *= simulation_parameters[1, :, :]
