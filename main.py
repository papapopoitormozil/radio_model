# Python 3; расчёты используют только стандартную библиотеку.
# Все значения — результаты расчёта, не физические измерения.
import math, csv

def fspl(f_mhz, d_km):
    return 32.44 + 20*math.log10(f_mhz) + 20*math.log10(d_km)

def knife_edge_loss(v):
    if v <= -0.78: return 0.0
    return 6.9 + 20*math.log10(math.sqrt((v-0.1)**2+1)+v-0.1)

def nu_edge(h_m, f_hz, d1_m, d2_m):
    wavelength = 299_792_458.0/f_hz
    return h_m*math.sqrt(2*(d1_m+d2_m)/(wavelength*d1_m*d2_m))

distances_km=[0.1,0.2,0.5,1,2,5,10]
frequencies_mhz=[900,2400,5800]
with open("fspl_results.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["frequency_MHz","distance_km","FSPL_dB"])
    for freq in frequencies_mhz:
        for distance in distances_km: w.writerow([freq,distance,round(fspl(freq,distance),3)])
with open("edge_results.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["height_m","nu","diffraction_dB"])
    for h in [-5,0,1,5]:
        nu=nu_edge(h,2.4e9,500,500); w.writerow([h,round(nu,4),round(knife_edge_loss(nu),3)])
with open("material_scenarios.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["frequency_MHz","distance_km","assumed_material_loss_dB","total_loss_dB","Pr_dBm"]); base=fspl(2400,0.01)
    for loss in [0,6,15]: w.writerow([2400,0.01,loss,round(base+loss,3),round(-base-loss,3)])
print("FSPL at 1 km (dB):",{f:round(fspl(f,1),2) for f in frequencies_mhz})
print("Created CSV result tables")
