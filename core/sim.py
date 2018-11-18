import numpy as np
import scipy.ndimage.filters as filters


# Global Parameters
DEFAULT_TIME_STEP = 0.01
ARRAY_BREAK_LENGTH = 1_000    # Must be > 3


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

        # First two steps must be DEFINED.
        self.step = 2

        z, self.height, self.width = initial_conditions.shape

        if z != 5:
            raise RuntimeError("invalid initial conditions!")

        data = np.zeros((ARRAY_BREAK_LENGTH, 3, self.height, self.width), dtype=np.float)

        # Initial calculations done manually.

        # First two positions defined
        data[:2, 0, :, :] = initial_conditions[:2, :, :]
        # First velocity is zero, Second is deltaX / t
        data[1, 1, :, :] = (data[1, 0, :, :] - data[0, 0, :, :]) / self.timestep
        # Instead of using the wave equation to calculate a for the two points, its forced into position.
        # So its actually going to be defined using v
        data[0, 2, :, :] = data[1, 1, :, :] / self.timestep
        # We need to calculate the first acceleration MANUALLY.
        filters.laplace(data[1, 0, :, :], data[1, 2, :, :], self.edge_conditions, self.edge_value)
        data[1, 2, :, :] = self.simulation_parameters[0, :, :]
        data[1, 2, :, :] -= data[1, 1, :, :] * self.simulation_parameters[2, :, :]
        for forcer in self.forcers:
            data[1, 2, forcer.position_y, forcer.position_x] += forcer(self.timestep * self.step)
        data[1, 2, :, :] *= self.simulation_parameters[1, :, :]
        self.sim_data.append(data)

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
            # Laplace(U) * E
            filters.laplace(curr_position, curr_acceleration, self.edge_conditions, self.edge_value)
            curr_acceleration *= self.simulation_parameters[0, :, :]
            # - B * V
            curr_acceleration -= curr_velocity * self.simulation_parameters[2, :, :]
            # Forces
            for forcer in self.forcers:
                curr_acceleration[forcer.position_y, forcer.position_x] += forcer(self.timestep*self.step)
            # Forces has become acceleration
            curr_acceleration *= self.simulation_parameters[1, :, :]

            self.step += 1

    def at_step(self, step):
        if self.step < step:
            self.simulate(step - self.step + 1)

        data = self.sim_data[step // ARRAY_BREAK_LENGTH]
        return data[step % ARRAY_BREAK_LENGTH, :, :, :]

    def at_time(self, step):
        pass
