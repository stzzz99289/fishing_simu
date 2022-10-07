import globvar as glob
from math import ceil, floor, sqrt
from obj import Sensor, Fish
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as patches

def set_layout():
    A = glob.A
    B = glob.B
    N = glob.N

    # compute number of columns (m) and number of sensors in each column (n)
    k = (B - 2*glob.d_c) / (A - 2*glob.d_c)
    m = ceil((1 - k + sqrt((k+1)**2 + 4*k*N)) / 2)
    n = floor(N / m)
    glob.m = m
    glob.n = n

    # get final layout
    glob.N_sigma = m * (n - 1) + ceil(m/2)
    glob.delta_Dx = (B - 2*glob.d_c) / (m - 1)
    glob.delta_Dy = (A - 2*glob.d_c) / (n - 1)
    glob.delta_t = glob.delta_Dy / glob.v_q

    # print debug info
    if glob.print_info:
        print("{} columns with {} sensors each column. \
        \n {} sensors in total.".format(m, n, glob.N_sigma))
        print("dx = {:.2f}, dy = {:.2f}, delta_t = {:.2f}" \
            .format(glob.delta_Dx, glob.delta_Dy, glob.delta_t))
    
    # question asks for no overlap between sensors
    assert (glob.delta_Dx >= 2 * glob.d_c)
    assert (glob.delta_Dy >= 2 * glob.d_c)

def initialize_sensors():
    # initialize sensors
    j = 0
    glob.sensor_lst = []
    for mi in range(glob.m):
        for ni in range(glob.n):
            xj = mi * glob.delta_Dx + glob.d_c
            yj = ni * glob.delta_Dy + glob.d_c
            group_num = int(mi / glob.m_sx)
            sensor_j = Sensor((xj, yj), group_num)
            glob.sensor_lst.append(sensor_j)
            j += 1
    glob.max_gn = group_num

def run_simulation(points_num=100, angles_num=6):
    initialize_sensors()
    glob.detected_times = 0
    max_dist = 2 * (glob.A + glob.B)
    dist_arr = np.linspace(0, max_dist, points_num)
    for dist in dist_arr:
        start_pos = get_start_pos(dist)
        for angle in np.linspace(0, 360, angles_num):
            if glob.print_info:
                print("start_pos: ({},{}), angle: {}".format(start_pos[0], start_pos[1], angle))
            run_trail(angle, start_pos)
    
    trails_num = points_num * angles_num
    print('total trails: {}, detected times: {}'.format(trails_num, glob.detected_times))
    return trails_num, glob.detected_times

def get_start_pos(dist):
    A = glob.A
    B = glob.B
    
    assert (0 <= dist and dist <= 2*(A+B))
    if 0 <= dist and dist < A:
        return (0, dist)
    elif A <= dist and dist < A+B:
        return (dist - A, A)
    elif A+B <= dist and dist < 2*A+B:
        return (B, 2*A+B - dist)
    elif 2*A+B <= dist and dist <= 2*(A+B):
        return (2*(A+B)-dist, 0)

def set_active_sensors():
    for sensor in glob.sensor_lst:
        if sensor.gn == glob.active_gn:
            sensor.active = True
        else:
            sensor.active = False

def run_trail(angle, start_pos):
    glob.time = 0
    glob.active_gn = 0
    glob.fish = Fish(angle, start_pos)
    glob.detected = False
    timestep = 0

    while(True):
        glob.time += glob.dt
        if timestep % 5 == 0 and glob.save_plots:
            save_sensor_plot()
        timestep += 1
        glob.active_gn = int(glob.time / glob.delta_t) % (glob.max_gn + 1)
        set_active_sensors()
        glob.fish.detect_and_move()
        if glob.detected or not glob.fish.check_border():
            if glob.save_plots:
                save_sensor_plot()
            break

def save_sensor_plot(with_fish=True):
    fig, ax = plt.subplots()
    border = patches.Rectangle((0, 0), glob.B, glob.A, linewidth=1, edgecolor='r', facecolor='none')
    ax.add_patch(border)
    for s in glob.sensor_lst:
        ax.scatter(s.x, s.y, c='blue')
        if not s.active:
            circle = patches.Circle((s.x, s.y), radius=glob.d_c, color='yellow', alpha = 0.2)
        else:
            circle = patches.Circle((s.x, s.y), radius=glob.d_c, color='red', alpha = 0.2)
        ax.add_patch(circle)
    if with_fish:
        ax.scatter(glob.fish.x, glob.fish.y, c='black')
    ax.axis('scaled')
    plt.savefig('plots/sensors{:.2f}.png'.format(glob.time))

