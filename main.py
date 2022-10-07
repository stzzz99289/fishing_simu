import globvar as glob
from utils import initialize_sensors, set_layout, run_simulation, save_sensor_plot
from math import exp, pi

def dp_tianze():
    # set sensor layout
    set_layout()
    initialize_sensors()

    # call this function during simulation to get current plot
    save_sensor_plot(with_fish=False)

    # run simulation
    trails_num, detected_times = run_simulation(points_num=200, angles_num=12)

    return detected_times / trails_num

def dp_prof_wang():
    pass

def dp_prof_tan():
    set_layout()
    # TODO: how to define t_jt?
    t_jt = glob.delta_t
    dp = 1 - exp( -glob.N_sigma/(glob.A*glob.B) \
    * ((pi*(glob.d_c**2) + 2*glob.d_c*glob.v_q*t_jt) * glob.p_k*glob.p_jc))
    return dp

if __name__ == "__main__":
    # set input (configure other params in file globvar.py)
    glob.N = 80

    # compute Detection Probability as function of total number of sensors (N)
    dp = dp_tianze()
    print("(tianze) detection probability = {:.2f}".format(dp))

    # TODO: generate animation for certain trail
    pass
