import globvar as glob
from utils import set_layout, run_simulation, save_sensor_plot

def dp_tianze():
    # set sensor layout
    set_layout()

    # call this function during simulation to get current plot
    save_sensor_plot(with_fish=False)

    # run simulation
    trails_num, detected_times = run_simulation(points_num=200, angles_num=12)

    return detected_times / trails_num

if __name__ == "__main__":
    # set input (configure other params in file globvar.py)
    glob.N = 80

    # compute Detection Probability as function of total number of sensors (N)
    dp = dp_tianze()
    print("detection probability = {:.2f}".format(dp))

    # TODO: generate animation for certain trail
    pass
