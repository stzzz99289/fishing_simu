import globvar as glob
from math import cos, sin, pi, sqrt

class Sensor:
    def __init__(self, pos, group_num) -> None:
        self.x = pos[0]
        self.y = pos[1]
        self.R = glob.d_c
        self.gn = group_num
        self.active = False

class Fish:
    def __init__(self, angle, start_pos) -> None:
        self.v = glob.v_q
        self.angle = angle * (pi / 180)
        self.vx = self.v * cos(self.angle)
        self.vy = self.v * sin(self.angle)
        self.start_x = start_pos[0]
        self.start_y = start_pos[1]
        self.x = self.start_x
        self.y = self.start_y

    def detect_and_move(self):
        # check if the fish is detected then move the fish
        self.detect()
        self.x += self.vx * glob.dt
        self.y += self.vy * glob.dt

    def detect(self):
        # check if the fish is detected at current time
        # if detected, set glob.detected to True
        range = glob.d_c
        for sensor in glob.sensor_lst:
            if sensor.active:
                dist = sqrt((self.x - sensor.x)**2 + (self.y - sensor.y)**2)
                if dist <= range:
                    glob.detected = True
                    glob.detected_times += 1
                    if glob.print_info:
                        print("fish detected at ({:.2f}, {:.2f}) \
                        \n by sensor at ({:.2f}, {:.2f}) at time {:.2f}!"
                        .format(self.x, self.y, sensor.x, sensor.y, glob.time))

    def check_border(self):
        # if the fish is still in the detection range, returns True
        # else returns False
        in_border = (self.x >= 0 and self.x <= glob.B \
            and self.y >= 0 and self.y <= glob.A)
        if not in_border:
            if glob.print_info:
                print("fish out of border at time {}! \
                \n current position: ({}, {})".format(glob.time, self.x, self.y))
        return in_border
