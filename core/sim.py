import numpy as np
import scipy.ndimage.filters as filters


# Global Parameters
DEFAULT_TIME_STEP = 0.01
ARRAY_BREAK_LENGTH = 1_000    # Must be > 3


class Simulator:
    # Main simulator for program.
    def __init__(self, initital_conditions: np.ndarray, timestep=DEFAULT_TIME_STEP, edge_conditions="constant", edge_value=0):
        if edge_conditions not in ['reflect', 'constant', 'nearest', 'mirror', 'wrap']:
            raise RuntimeError("invalid edge condition!")
        edge_value = float(edge_value)

        self.edge_value = edge_value
        self.edge_conditions = edge_conditions
        self.timestep = timestep
        self.simulation_parameters = initital_conditions[2:, :, :]
        self.sim_data = []
        self.forcers = []

        # First two steps must be DEFINED.
        self.step = 2

        z, self.x, self.y = initital_conditions.shape

        if z != 5:
            raise RuntimeError("invalid initial conditions!")

        data = np.zeros((ARRAY_BREAK_LENGTH, 3, self.y, self.x), dtype=np.float16)
        # First two positions defined
        data[:2, 0, :, :] = initital_conditions[:2, :, :]
        # First velocity is zero, Second is deltaX / t
        data[1, 1, :, :] = (data[1, 0, :, :] - data[0, 0, :, :]) / self.timestep
        # Instead of using the wave equation to calculate a for the two points, its forced into position.
        # So its actually going to be defined using v
        data[1, 2, :, :] = data[1, 1, :, :] / self.timestep
        self.sim_data.append(data)

    def simulate(self, steps=1):
        for _ in range(steps):
            data = self.sim_data[-1]
            index = self.step % ARRAY_BREAK_LENGTH

            prev_position = data[index-1, 0, :, :]
            prev_velocity = data[index-1, 1, :, :]
            prev_acceleration = data[index-1, 2, :, :]

            # Handling split arrays
            if self.step % ARRAY_BREAK_LENGTH == 0:
                # Split magically
                new_data = np.zeros((ARRAY_BREAK_LENGTH, 3, self.y, self.x), dtype=np.float16)
                self.sim_data.append(new_data)
                data = self.sim_data[-1]

            curr_position = data[index, 0, :, :]
            curr_velocity = data[index, 0, :, :]
            curr_acceleration = data[index, 0, :, :]

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
            for

            # Forces has become acceleration
            forces *= self.simulation_parameters[1, :, :]

            # Compute the current position, velocity using the forward Euler method.
            self.c