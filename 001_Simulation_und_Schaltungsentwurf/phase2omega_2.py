import numpy as np
import matplotlib.pyplot as plt

# Farben
my_blue  = (10/255, 85/255, 140/255)
my_red   = (195/255, 5/255, 35/255)
my_green = (0/255, 145/255, 90/255)

# Parameter
f_ref     = 1000.0       
f_current = 1050.0       
df        = 10.0         
fs        = 200_000.0    
T         = 0.05         
t         = np.arange(0, T, 1/fs)

ref = np.sin(2*np.pi*f_ref*t)
sig = np.zeros_like(t)
phi_sig = 0.0            

time_log = []
freq_log = []
phase_log = []  # jetzt ROH-Phase in [-180,180]

prev_ref = ref[0]

for i in range(1, len(t)):
    sig[i] = -np.sin(phi_sig)
    phi_sig += 2*np.pi*f_current/fs

    if prev_ref < 0 and ref[i] >= 0:
        # Exakte Interpolation
        dt = -prev_ref / (ref[i] - prev_ref) / fs
        t_exact = t[i-1] + dt
        
        phi_ref_exact = 2*np.pi*f_ref*t_exact % (2*np.pi)
        phi_sig_exact = phi_sig - 2*np.pi*f_current/fs*(1-dt)
        phi_sig_exact = phi_sig_exact % (2*np.pi)
        
        # **KORREKTE Phasendifferenz** [-pi, pi]
        phi_diff = phi_sig_exact - phi_ref_exact
        phi = ((phi_diff + np.pi) % (2*np.pi)) - np.pi  # immer [-180°,180°]
        
        phi_deg = np.degrees(phi)
        phase_log.append(phi_deg)

        # **KORREKTE REGELUNG**: -90°..+90° → erhöhen, sonst senken
        if abs(phi_deg) < 90:
            f_current += df
        else:
            f_current -= df

        time_log.append(t_exact)
        freq_log.append(f_current)

    prev_ref = ref[i]

# Plots
plt.figure(1,figsize=(12, 8))
plt.subplot(211)
plt.plot(time_log, freq_log, color=my_blue, label='f_current')
plt.axhline(y=f_ref, color=(0,0,0), linestyle='--', alpha=0.5, label='f_ref')
plt.title("Frequenzverlauf")
plt.xlabel("Zeit [s]"); plt.ylabel("Frequenz [Hz]")
plt.grid(True); 
plt.legend(loc='lower left')

#plt.figure(figsize=(12, 4))
plt.subplot(212)
plt.plot(time_log, phase_log, '.', color=my_green)
plt.axhline(y=90, color='r', linestyle=':', alpha=0.5, label='±90° Grenze')
plt.axhline(y=-90, color='r', linestyle=':', alpha=0.5)
plt.title("Phasendifferenz")
plt.xlabel("Zeit [s]"); plt.ylabel("Phase [°]")
plt.grid(True); 
plt.legend(loc='lower left')



plt.figure(figsize=(12, 4))
N = int(0.02 * fs)
plt.plot(t[:N]*1000, ref[:N], label="Referenz", color=my_blue)
plt.plot(t[:N]*1000, sig[:N], label="Tracking", color=my_red)
plt.xlabel("Zeit [ms]"); plt.ylabel("Amplitude")
plt.title("Signale (erste 5 ms)"); plt.grid(True); plt.legend()

plt.tight_layout()
plt.show()

#%%


import numpy as np
import matplotlib.pyplot as plt

# Farben
my_blue  = (10/255, 85/255, 140/255)
my_red   = (195/255, 5/255, 35/255)
my_green = (0/255, 145/255, 90/255)

# Parameter
f_ref     = 1000.0       
f_current = 1015.0       
df_max    = 10.0         # maximale Schrittweite [Hz]
fs        = 200_000.0    
T         = 0.5      
t         = np.arange(0, T, 1/fs)

ref = np.sin(2*np.pi*f_ref*t)
sig = np.zeros_like(t)
phi_sig = 0.0            

time_log = []
freq_log = []
phase_log = []  # Phase in [-180,180]

prev_ref = ref[0]

# Proportionalfaktor: bei |Abstand zu 90°| = 90° → volle Korrektur df_max
Kp = df_max / 90.0       # [Hz/°]

for i in range(1, len(t)):
    sig[i] = np.sin(phi_sig)
    phi_sig += 2*np.pi*f_current/fs

    if prev_ref < 0 and ref[i] >= 0:
        # Exakte Interpolation
        dt = -prev_ref / (ref[i] - prev_ref) / fs
        t_exact = t[i-1] + dt
        
        phi_ref_exact = 2*np.pi*f_ref*t_exact % (2*np.pi)
        phi_sig_exact = phi_sig - 2*np.pi*f_current/fs*(1-dt)
        phi_sig_exact = phi_sig_exact % (2*np.pi)
        
        # Phasendifferenz [-pi, pi]
        phi_diff = phi_sig_exact - phi_ref_exact
        phi = ((phi_diff + np.pi) % (2*np.pi)) - np.pi
        
        phi_deg = np.degrees(phi)
        phase_log.append(phi_deg)

 # ---------- ROBUSTE SYMMETRISCHE REGELUNG UM 90° ----------
 # Phase in [0, 360)
        phi_rel = phi_deg % 360.0

 # Richtung: links von 90° und rechts von 270° -> f↑, da näher an 0°/360°
 #          zwischen 90° und 270° -> f↓
        if 0 <= phi_rel < 90:
             direction = +1   # f↑
             dist = 90 - phi_rel
        elif 90 <= phi_rel < 180:
             direction = -1   # f↓
             dist = phi_rel - 90
        elif 180 <= phi_rel < 270:
             direction = -1   # f↓
             dist = 270 - phi_rel   # 180→90, 270→0
        else:  # 270..360
             direction = +1   # f↑
             dist = phi_rel - 270    # 270→0, 360→90

 # dist liegt jetzt immer in [0, 90]
        error = direction * dist   # Vorzeichen entscheidet über f↑/f↓
        
        delta_f = Kp * error
        delta_f = np.clip(delta_f, -df_max, df_max)
        f_current += delta_f
 # ----------------------------------------------------------


        time_log.append(t_exact)
        freq_log.append(f_current)

    prev_ref = ref[i]

# Plots
plt.figure(1,figsize=(12, 8))
plt.subplot(211)
plt.plot(time_log, freq_log, color=my_blue, label='f_current')
plt.axhline(y=f_ref, color=(0,0,0), linestyle='--', alpha=0.5, label='f_ref')
plt.title("Frequenzverlauf")
plt.xlabel("Zeit [s]"); plt.ylabel("Frequenz [Hz]")
plt.grid(True)
plt.legend(loc='lower left')

plt.subplot(212)
plt.plot(time_log, phase_log, '.', color=my_green)
plt.axhline(y=90,  color='r', linestyle=':', alpha=0.5, label='90° Grenze')
plt.axhline(y=-90, color='r', linestyle=':', alpha=0.5)
plt.title("Phasendifferenz")
plt.xlabel("Zeit [s]"); plt.ylabel("Phase [°]")
plt.grid(True)
plt.legend(loc='lower left')

plt.tight_layout()
plt.show()


