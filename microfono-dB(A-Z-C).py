import numpy as np
import pyaudio as pa 
import struct
import PyOctaveBand
from time import sleep
import time
    
FRAMES = 48000                               # Tamaño del paquete a procesar
Fs = 48000                                   # Frecuencia de muestreo típica para audio
FORMAT = pa.paInt16                          # Formato de lectura INT 16 bits
CHANNELS = 1

fpb = int(Fs*0.125)

F = (Fs/FRAMES)*np.arange(0,FRAMES//2)      # Creamos el vector de frecuencia para encontrar la frecuencia dominante

p = pa.PyAudio()

#n=0
#while n<1:

stream = p.open(                            # Abrimos el canal de audio con los parámeteros de configuración
    format = FORMAT,
    channels = CHANNELS,
    rate = Fs,
    input=True,
#    output=True,
    frames_per_buffer= fpb
)

mic_sens_dBV =  -0.05                              # mic sensitivity in dBV + any gain
mic_sens_lin = np.power(10.0,mic_sens_dBV/20.0) # calculate mic sensitivity conversion factor


data = stream.read(fpb)                         # Leemos paquetes de longitud FRAMES
dataInt = struct.unpack(str(fpb) + 'h', data)   # Convertimos los datos que se encuentran empaquetados en bytes

dataInt = ((dataInt/np.power(2.0,15))*5.0)/(mic_sens_lin)
dataInt = list(dataInt)
dataInt = dataInt + [0]*(Fs-len(dataInt))
dataInt = np.array(dataInt)

while True:
    
    vec_new_corr = []                               # Crear nuevo vectoe de correccion
    spl, freq = PyOctaveBand.octavefilter(dataInt, fs=Fs, fraction=1, order=6, limits=[12, 22530], show=0)
    
    print(f"{freq[0]}: {spl[0]} -- {freq[1]}: {spl[1]} -- {freq[2]}: {spl[2]} -- {freq[3]}: {spl[3]} -- {freq[4]}: {spl[4]} -- {freq[5]}: {spl[5]} -- {freq[6]}: {spl[6]} -- {freq[7]}: {spl[7]} -- {freq[8]}: {spl[8]} -- {freq[9]}: {spl[9]} -- {freq[10]}: {spl[10]}")
    
    # BUSCAR PONDERACION-A PARA 16HZ
    #------Bandas ------  16      -32     -63    -125    -250   -500   -1k    -2k    -4k    -8k    -16
    #    vec_cal = np.array([  9.8,    9.82,   9.62,   9.50,  9.75,  9.43, 10.58, 11.72, 12.17,  9.55, 11.57])
    vec_dba = np.array([-49.50, -39.40, -26.20, -16.10, -8.60, -3.20,  0.00,  1.20,  1.00, -1.10, -6.60])
    vec_dbc = np.array([ 0.00,    -0.8,   -0.2,   0.00,  0.00,  0.00,  -0,2,  -0.8,  -3.0,  -8.5])

    vec_100 = np.array([9.8, 9.8, 9.7, 9.8, 9.8, 9.6, 16.8, 17, 17.4, 9.8, 11.5])
#    vec_95 = np.array([9.8, 9.8, 9.7, 9.5, 9.8, 9.4, 1, 13, 13.8, 9.6, 11.5])
    vec_95 = np.array([1, 1, 1, 1, 1, 1, 1.8, 1, 1, 1, 1])
#    vec_90 = np.array([9.8, 9.8, 9.6, 9.5, 9.8, 9.4, 16.6, 10.3, 12, 9.6, 11.5])
    vec_90 = np.array([-10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10])
#    vec_85 = np.array([9.8, 9.8, 9.6, 9.4, 9.7, 9.4, 16.5, 10.3, 11.8, 9.5, 11.7])
    vec_85 = np.array([-20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20])
#    vec_80 = np.array([9.8, 9.9, 9.6, 9.4, 9.7, 9.4, 16.4, 10.3, 11.8, 9.5, 11.6])
    vec_80 = np.array([-30, -30, -30, -30, -30, -30, -30, -30, -30, -30, -30])
#    vec_75 = np.array([9.8, 9.9, 9.5, 9.4, 9.7, 9.4, 16.8, 10.3, 11.8, 9.5, 11.6])
    vec_75 = np.array([-30, -30, -30, -30, -30, -30, -30, -30, -30, -30, -30])

    i=0
    for x in spl:
        if 120 > x > 95:
            vec_new_corr.append(vec_100[i])
        elif 95 > x > 90:
            vec_new_corr.append(vec_95[i])
        elif 90 > x > 85:
            vec_new_corr.append(vec_90[i])
        elif 85 > x > 80:
            vec_new_corr.append(vec_85[i])
        elif 80 > x > 75:
            vec_new_corr.append(vec_80[i])
        elif 75 > x > 10:
            vec_new_corr.append(vec_75[i])
        i = i + 1

    print("Nuevo vector ---------", vec_new_corr)
       

    spl_cal = spl + np.array(vec_new_corr)                 # Se calcula vec_corr y se suma al SPL con la sensibil del microph en 10
    #    spl_cal = spl + vec_cal
    spl_cal_dba = spl_cal + vec_dba               
    spl_cal_dbc = spl_cal + vec_dbc

    Z_weight_sum = np.sum(np.power(10,spl_cal/10))         #calcular ponderacion Z
    val_dBZ = 10*np.log10(Z_weight_sum)

    A_weight_sum = np.sum(np.power(10,spl_cal_dba/10))     #calcular ponderacion A
    val_dBA = 10*np.log10(A_weight_sum)

    C_weight_sum = np.sum(np.power(10,spl_cal_dbc/10))     #calcular ponderacion C
    val_dBC = 10*np.log10(C_weight_sum)

    print(f"{freq[0]}: {spl_cal[0]} -- {freq[1]}: {spl_cal[1]} -- {freq[2]}: {spl_cal[2]} -- {freq[3]}: {spl_cal[3]} -- {freq[4]}: {spl_cal[4]} -- {freq[5]}: {spl_cal[5]} -- {freq[6]}: {spl_cal[6]} -- {freq[7]}: {spl_cal[7]} -- {freq[8]}: {spl_cal[8]} -- {freq[9]}: {spl_cal[9]} -- {freq[10]}: {spl_cal[10]}")
    print("p-dbZ", val_dBZ)
    print("p-dbA", val_dBA)
    #print("p-dbC", val_dBC)
    sleep(1)
    #n=n+1

    