import ReadWrite as rw
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.fftpack import ifft,fft, rfft,fftfreq


def movingAverage(csvFile,window):
    '''Accelerometer data in csvFile must be in the form of 3 columns with a header of ["Z","X","Y"] 
           Arguments:
               filename: File or path to source file.'''

    #dataFrame = pd.read_csv(csvFile)
    dataFrame = rw.readAccelerationsToDF(csvFile)
    dataFrame.columns  = ["Z","X","Y"]

    dataf = dataFrame[["Z","X","Y"]]

    filteredData=[]
    timeList =[]

    print(dataf.shape)


    for i in range(window,dataf.shape[0]):
        zList=np.array(dataf["Z"].iloc[i-window:i]).tolist()
        xList=np.array(dataf["X"].iloc[i-window:i]).tolist()
        yList=np.array(dataf["Y"].iloc[i-window:i]).tolist()
        sumZ=0
        sumX=0
        sumY=0
        for z in zList:
            sumZ += z
        for x in xList:
            sumX += x
        for y in yList:
            sumY+=y

        avgZ= sumZ/len(zList)
        avgX= sumX/len(xList)
        avgY= sumY/len(yList)



        #sol = np.sqrt(pow(avgZ, 2) + pow(avgX, 2) + pow(avgY, 2))
        #sol = np.sqrt(pow(avgZ, 2) + pow(avgY, 2))
        #sol = avgZ
        #sol = avgY
        #sol = avgX
        sol = [avgZ,avgX,avgY]

        filteredData.append(sol)

    plt.figure(dpi=200,figsize=(7,7))

    for t in range(0,len(filteredData)):
        timeList.append(t*10)

    timeList = [i /1000 for i in timeList]
    # x = timeList
    # y = filteredData
    # f = interp1d(x, y)
    # f2 = interp1d(x, y, kind='cubic')
    #
    # xnew = timeList
    # plt.plot(x, y, 'o', xnew, f(xnew), '-', xnew, f2(xnew), '--')
    # plt.legend(['data', 'linear', 'cubic'], loc='best')
    # plt.show()

    with open('filtered_acceleration.csv', 'w') as f:

        # using csv.writer method from CSV package
        write = csv.writer(f)

        write.writerow(["Z","X","Y"])
        write.writerow(["Z","X","Y"])
        write.writerow(["Z","X","Y"])
        write.writerow(["Z","X","Y"])
        write.writerows(filteredData)



    ax = plt.gca()
    ax.xaxis.set_major_locator(MultipleLocator(2))
    plt.plot(timeList ,filteredData, color='g')
    plt.grid(b=True, which='both', color='b', linestyle='-')
    plt.xlabel('Time (millis)')
    plt.ylabel('Acceleration (m/s^2)')
    plt.title('Acceleration')
    plt.show()

    # csvfile = open('acc10(6)filtered.csv', 'w')
    # csvWriter = csv.writer(csvfile, delimiter=',',
    #                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
    # csvWriter.writerow(['TIME','Z','X','Y'])
    # for i in range(0,len(filteredData)):
    #     df=[]
    #     df.append(timeList[i])
    #     df.append(filteredData[i][0])
    #     df.append(filteredData[i][1])
    #     df.append(filteredData[i][2])
    #     csvWriter.writerow(df)

def lowPassFilter(yArray,xArray,freqCutOff):


    cut_f_signal = yArray.copy()
    np.argsort(xArray)
    cut_f_signal[(np.abs(xArray)>freqCutOff)] = 0

    return cut_f_signal

def amptitudeFilter(yV_fft,N_THRESH):

    idx_sorted = np.argsort(-np.abs(yV_fft))
    idx = idx_sorted[0:N_THRESH]
    mask = np.zeros(yV_fft.shape).astype(bool)
    mask[idx] = True

    D_below = yV_fft.copy()
    D_below[mask] = 0
    D_above = yV_fft.copy()
    D_above[~mask] = 0

    return {"Bellow":D_below ,"Above":D_above}

def fourierTransform(csvFile):

    #dataFrame = readAcceleration(csvFile)
    dataFrame = rw.readAccelerationsToDF(csvFile)

    zArray = np.array(dataFrame["Z"])
    xArray = np.array(dataFrame["X"])
    yArray = np.array(dataFrame["Y"])

    tValues = np.arange(0,np.size(zArray)*10,10)
    yVal=fft(zArray)
    xVal=fftfreq(np.size(zArray),0.001)


    iYVal=ifft(yVal)

    #filtered_signal = lowPassFilter(yVal,xVal,500)
    filtered_signal= amptitudeFilter(yVal,20)["Above"]
    iYVal = ifft(filtered_signal)

    #plt.plot(np.abs(xVal),yVal)

    #plt.plot(xVal,filtered_signal)
    plt.plot(tValues,iYVal)


    plt.show()

    return iYVal.real