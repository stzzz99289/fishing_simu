# global params
A = 30 # short edge
B = 50 # long edge
v_q = 8 * 1.852 # velocity of fish
d_c = 2 # sensing radius
m_sx = 2 # number of columns of sensors activated at the same time
delta_Dx = None # distance between columns
delta_Dy = None # distance between sensors in one column
delta_t = None # active time of one group of sensor
m = None # number of columns
n = None # number of sensors in odd columns
N_sigma = None # real number of sensors (integer) given input N (float)

# params used in analytical formula
# currently set to 1 for comparision with simulation result
p_k = 1
p_jc = 1

# input
N = None

# debug params
print_info = False
save_plots = False

# simulation params
max_gn = None
active_gn = 0
sensor_lst = None
fish = None
detected = False
dt = 0.02
time = 0
detected_times = 0
