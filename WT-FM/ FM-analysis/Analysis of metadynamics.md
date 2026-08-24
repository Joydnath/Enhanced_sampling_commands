_____________After metadynamics__________


                
        -----Are transitions rare and well separated?-----

>>  awk '{print $1, $2}' COLVAR > cv_time.dat   <<

@@@
import numpy as np
import matplotlib.pyplot as plt

t, s = np.loadtxt('cv_time.dat', unpack=True)
plt.figure(figsize=(10,3))
plt.plot(t, s, lw=0.8)
plt.xlabel('Time (ps)')
plt.ylabel('s')
plt.title('CV (s) vs Time')
plt.tight_layout()
plt.show()
@@@



        -----Was bias deposited during the transition?-----

>>  awk '{print $1, $4}' COLVAR > bias_time.dat  <<

@@@
import numpy as np
import matplotlib.pyplot as plt

t, V = np.loadtxt('bias_time.dat', unpack=True)
plt.figure(figsize=(10,3))
plt.plot(t, V, lw=0.8)
plt.xlabel('Time (ps)')
plt.ylabel('Bias (kJ/mol)')
plt.title('Bias deposition vs Time')
plt.tight_layout()
plt.show()
@@@


        -----Check whether a transition occurred (automatically)-----

@@@
import numpy as np
t, s = np.loadtxt('cv_time.dat', unpack=True)

# Define dividing surface
s_div = 3.5  # adjust depending on your system (midpoint between basins)

# Define a minimum dwell time (in ps) to filter recrossings
min_dwell = 500.0

inA = s < s_div
state = inA[0]
trans_times = []
last_switch_time = None

for ti, isinA in zip(t, inA):
    if isinA != state:
        if last_switch_time is None:
            last_switch_time = ti
        elif ti - last_switch_time >= min_dwell:
            trans_times.append(last_switch_time)
            state = isinA
            last_switch_time = None
    else:
        last_switch_time = None

print("Detected transitions (ps):", trans_times)
print("Number of transitions:", len(trans_times))
@@@


        ----Combine bias & CV to check “bias during transition

@@@
import matplotlib.pyplot as plt

transition_times = [221970]

plt.figure()
for tr in transition_times:
    plt.axvline(tr, color='r', ls='--')

plt.xlim(0, max(transition_times) + 10)   # set visible range
plt.ylim(0, 1)                             # needed for vertical lines!
plt.show()

@@@









        ----- Free energy surface -----
        
        
>>  plumed sum_hills --hills HILLS --outfile fes.dat --kt 2.494 <<
   
        
        ----- plotting 1D FES -----
        
@@@ 
import numpy as np
import matplotlib.pyplot as plt

# load
data = np.loadtxt('fes.dat', comments='#')
s = data[:,0]          # path.sss
F = data[:,1]          # free energy

# shift F to min = 0
#F = F - F.min()

plt.plot(s, F, linewidth=2)
plt.xlabel("Path CV (s)")
plt.ylabel("Free Energy (kJ/mol)")
plt.title("1D Free Energy Profile")
plt.grid(True)
plt.tight_layout()
plt.show()
@@@        
        
        
        
        
        
        
        ----- Plotting 2D FES -----        

@@@
import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('fes.dat', comments='#')
s1 = data[:,0]
s2 = data[:,1]
V  = data[:,2]

# To plot a 2D FES (heatmap)
import matplotlib.pyplot as plt
from matplotlib import cm

plt.tricontourf(s1, s2, -V, levels=30, method='cubic')
plt.xlabel('CV1 (s)')
plt.ylabel('CV2 (z)')
plt.title('Approximate Free Energy Surface')
plt.colorbar(label='Free Energy (kJ/mol)')
plt.show()
@@@



















>> << means terminal commands 

@@ @@ means python scripts
--- save all these python scripts in name.py file and run python3 name.py file
