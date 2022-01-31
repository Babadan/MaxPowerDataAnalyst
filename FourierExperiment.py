import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fftfreq, irfft, rfft,fft


def createSinusoid():

    A = 1 # Amptitude
    f = 100 # hetz
    tl = np.linspace(0,1,1000)
    dt = tl[1]-tl[0]

    yVal= A* np.sin(2*np.pi*f*tl)

    fD_yValues = fft(yVal)
    fD_xValues = fftfreq(yVal.size,d=dt)

    plt.plot(fD_xValues,fD_yValues)
    plt.show()

