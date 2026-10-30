import numpy as np
import os
from itertools import chain
from shapely.geometry import Polygon, Point

from general_functions import *
from pol_dir_VBM_func import *
from plot_functions import *
from shape_and_acf_functions import *


#Global variable for number of vertices to represent cell shape
global N
N = 25

#magnitude of the protrusive force
magnitude = 50*N #0.05 * (0.3*N*l0/0.4) * 2000 [nN]

#start with no forces on vertices (but can change this by inputing an integer/s 0 through (N-1) to denote which vertices start with protruding forces)
force_on_ind0 = np.array([]) #needs to be array

#initialize cell coordinates and get rest area
#in this example, the cell starts as a circle
d = 100 #cell diameter [um]
l0 = d*np.sin(np.pi/N) #initial length of edge of cell between vertices
x, y = points_in_cell(d/2,N)
xy = np.concatenate((np.reshape(x,(N,1)),np.reshape(y,(N,1))),axis=1)
A_0 = Polygon(xy).area #resting area [um^2]# #initialize random state

#Total sim time
T_tot = 300 #[min]
#step size
dt = .05 #[min]


#set parameter values
#on rate parameters
kon_star = 0.1 #base on rate
t_max = 250 #max tension at vertex
#off rate parameters
koff_star = 0.05 #base off rate
koff_max = 5 #scaling term for off rate
sigma_off = 100 # variance in off rate distribution (spread of how vertices' rates are affected by internal polarity direction)
#polarity bias friciton parameter
nuw = 5 #friction coefficient for polarity bias direction (affects how fast polarity bias aligns)
#vertex friction parameters
nu_star = 1.67 #the minimum (base) friction coefficient of a vertex
nu_max = 500 #scaling term for maximum value of friction coefficient
nu_sigma = 20 #width term that determines how many vertices are affected by the internal cell orientation/polarity bias direction
max_dist = 60 #the distance a vertex must exceed from the center of the cell to become unstuck
min_fric = 1.67 #the friction coefficient of unstuck vertices

params = [kon_star, t_max, koff_star, koff_max, sigma_off, nuw, nu_star, nu_max, nu_sigma, max_dist, min_fric]

#create a directory and save figures here
save_path = './figures'
if not os.path.exists(save_path):
    os.mkdir(save_path)

save_path = save_path + '/randmig_manycells_konstar{}_tmax{}_koffstar{}_koffmax{}_sigmaoff{}_nuw{}_nustar{}_numax{}_nusigma{}_maxdist{}_minfric{}'.format(kon_star,t_max,koff_star,koff_max,sigma_off,nuw,nu_star, nu_max, nu_sigma, max_dist,min_fric)
if not os.path.exists(save_path):
    os.mkdir(save_path)

#create new file to write parameters to
other_params = ['N: {}\n'.format(N), 'magnitude: {}\n'.format(magnitude), 'd: {}\n'.format(d)]
param_vals = open(save_path+'/params.txt','w')
file_lines = other_params + ['kon_star: {}\n'.format(kon_star), 't_max: {}\n'.format(t_max), 'koff_star: {}\n'.format(koff_star), 'koff_max: {}\n'.format(koff_max), 'sigma_off: {}\n'.format(sigma_off), 'nu_w: {}\n'.format(nuw), 'nu_star: {}\n'.format(nu_star), 'nu_max: {}\n'.format(nu_max), 'nu_sigma: {}\n'.format(nu_sigma), 'max_dist: {}\n'.format(max_dist), 'min_fric: {}\n'.format(min_fric)]
#write lines to text file 
param_vals.writelines(file_lines)
param_vals.close() 

#number of cells in simulation
num_cells = 10 
#Where data is stored from all individual cells in sim
data_sim = []
for cell in range(num_cells):
    
    #set initial conditions for vertex coordinates
    #initial polarity bias direction
    w0 = np.random.uniform(0, 2*np.pi) #set random direciton here

    y0 = [x, y, [w0]]
    y0 = list(chain.from_iterable(y0))

    T, Y, Norm_Dir, X_Norm_Comp, Y_Norm_Comp, force_ind, remove_p_events, add_p_events, tension, num_nn, kon_rates, koff_rates, bias_ang_true, tension_x, tension_y, all_unstuck_ind = EulerSolver(UpdateVertices, 0, T_tot, dt, y0, force_on_ind0, magnitude, N, l0, A_0, params)
    
    #Make dataframe of shape and motion metrics for track
    onecell_df = make_shape_motion_df(Y, dt, N)

    data_sim.append(onecell_df)



#Plot cell centroid position over time and cell shape at beginning and end of simulation
plot_centroid_manycells(data_sim, N, save_path)

#Plot velocity acf
plot_vel_acf_manycells(data_sim,save_path)

#Plot boxplots for shape and motion metrics
make_shape_motion_boxplots(data_sim, save_path)