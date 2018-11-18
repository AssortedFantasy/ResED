# Used for the BIG boi math
import math


# Default forcer class
class Force:
    # Default return value if the forcer cannot define the value at the given time
    DEFAULT_VALUE = 0

    def __init__(self, position_x, position_y, force):
        self.is_exhausted = False
        # Lambda function to describe force
        self.force = force
        # Position of the x coordinate of the force
        self.position_x = position_x
        # Position of the y coordinate of the force
        self.position_y = position_y

    # Call object to get force at set time
    def __call__(self, time):
        return self.force(time)

    def get_x_pos(self):
        return self.position_x

    def get_y_pos(self):
        return self.position_y


# Special Case for forcers of constant value
class ConstantForce(Force):

    def __init__(self, position_x, position_y, force):
        self.is_exhausted = False
        self.force = force
        self.position_x = position_x
        self.position_y = position_y

    # Call object to get force at set time
    def __call__(self, time):
        return self.force


# Forcers for forces with polynomial relation to time
class PolynomialForce(Force):

    def __init__(self, position_x, position_y, coefficients):
        self.is_exhausted = False
        # Every value in the coefficient array specifices the coefficeint for a given power of x
        # The 0th index corresponds to the constant term, the 2nd index corresponds to the 2nd power of x etc.
        for exponent in range(0,len(coefficients)):
            # Recursivly defines the force function
            self.force = lambda time: time * coefficients(exponent) ** exponent + self.force
        self.position_x = position_x
        self.position_y = position_y

    # Call object to get force at set time
    def __call__(self, time):
        return self.force(time)


# Defines the force as a sinodudal function using arguments of amplitude, phase_shift, and angular_frequency
class SinosudalForce(Force):

    def __init__(self, position_x, position_y, amplitude, phase_shift, angular_frequency):
        self.is_exhausted = False
        self.force = lambda time: amplitude * math.sin(phase_shift + time * angular_frequency)
        self.position_x = position_x
        self.position_y = position_y

    # Call object to get force at set time
    def __call__(self, time):
        return self.force(time)


class DiscreteForce(Force):
    def __init__(self, position_x, position_y, forces, time_domain):
        self.is_exhausted = False
        self.time_domain = time_domain
        self.forces = forces
        self.position_x = position_x
        self.position_y = position_y

    # Call object to get force at set time
    def __call__(self, time):
        for time_max in range(len(self.time_domain)):
            if time < self.time_domain[time_max]:
                return self.forces[time_max](time)
        return super.DEFAULT_VALUE

class AudioForce(Force):
    def __init__(self, position_x, position_y, force_array, sample_rate):
        self.force = lambda time: force_array[time * sample_rate]
        self.position_x = position_x
        self.position_y = position_y

    # Call object to get force at set time
    def __call__(self, time):
        try:
            return self.force(time)
        except IndexError:
            return super.DEFAULT_VALUE
