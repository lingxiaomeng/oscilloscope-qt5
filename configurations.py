class Configurations:
    def __init__(self):
        self.time_max = 100
        self.time_min = 0
        self.time_max_range = 100
        self.phase_max = 360
        self.phase_min = 0
        self.mag_max = 10
        self.mag_min = 0

    def update(self, time_min, time_max, time_max_range, phase_min, phase_max, mag_min, mag_max):
        self.time_min = time_min
        self.time_max = time_max
        self.time_max_range = time_max_range
        self.phase_min = phase_min
        self.phase_max = phase_max
        self.mag_min = mag_min
        self.mag_max = mag_max
