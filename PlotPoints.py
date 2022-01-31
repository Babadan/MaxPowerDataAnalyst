import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import seaborn as sbn
print (mpl.pyplot.get_backend())

from scipy.fftpack import ifft,fft, rfft,fftfreq

from matplotlib.ticker import AutoMinorLocator,MultipleLocator
from scipy.interpolate import interp1d
import ReadWrite as rw
import Fourier_Filters as ff

FONT={'fontsize': 10,
            'fontstyle': "italic"}
legent_FONT= mpl.font_manager.FontProperties( style="italic",size=8,)



def printDistribution(csvFile):
    dataFrame = pd.read_csv(csvFile.name)


    domainWidth = 100

    mcList =[]
    for i in range(0, 2400, domainWidth):

        dataf = dataFrame[["Z"]]
        barrierL = []

        b = -3.0
        while (b<=3.0):
            barrierL.append(b)
            b+=0.2

        d = np.array(dataf["Z"].iloc[i:i + domainWidth]).tolist()

        pList = []
        for barrier in barrierL :
            possitive=0
            for accelZ in d:
                if(accelZ>barrier and accelZ<(barrier+0.1)):
                    possitive = possitive + 1

            pList.append(possitive)

        object=[]
        for b in barrierL:
           # object.append("("+ "%.1f"%b +","+"%.1f"%(b+0.1)+")")
            object.append("("+"%.1f"%b+")")

        plt.plot(barrierL, pList, color='g' )
        ylist = np.arange(len(object))

        plt.figure(num = None, figsize = (20, 6), dpi = 300, facecolor = 'w', edgecolor = 'k')
        plt.bar(ylist, pList, align='center', alpha=0.5)
        plt.xticks(ylist,object)
        plt.ylabel('Count')
        plt.title('AccelFreequency')
        plt.savefig("./figures/range_"+"%d"%i+"-"+"%d"%(i+domainWidth)+".png",dp=300)

        plt.close()

def interpolate(csvFile):
    '''Interpolates acceleration data using linear and cubic and plot the result on a graph.
      arguments:
        csvFile : Source file. (Format is three colums with header "Z" "X" "Y") '''

    dataFrame = pd.read_csv(csvFile)

    dataf = dataFrame[["Z", "X", "Y"]]
    x = np.linspace(0, dataf.shape[0] * 10, num=dataf.shape[0], endpoint=True, dtype=np.int32)
    y = np.array(dataf["Z"].iloc[:])

    f = interp1d(x, y)
    f2 = interp1d(x, y, kind='cubic')


    xnew = np.linspace(0, dataf.shape[0]*10, num= dataf.shape[0], endpoint=True ,dtype=np.int32)
    plt.plot(x, y, 'o', xnew, f(xnew), '-', xnew, f2(xnew), '--')
    plt.legend(['data', 'linear', 'cubic'], loc='best')
    plt.show()

def createSubPlot(i,fig,list_dataFrame,title="Scaterplot",legent=[],ylabel="",
               xlabel="",xMajorTickFrequency=-1,yMajorTickFrequency=-1):
    '''Adds Scaterplots  to existing figure with 2*2 Subplots in position i'''

    fig.tight_layout()
    ax = fig.add_subplot(2,2,i)
    ax.set_title(title, fontdict=FONT, color="#045a8d")
    ax.set_ylabel(ylabel, fontdict=FONT, color="#045a8d")
    ax.set_xlabel(xlabel, fontdict=FONT, color="#045a8d")
    ax.tick_params(which="both", direction="in", top=True, right=True, labelsize=6)

    # ax.set_xticks(numpy.arange(round(min(np[:, 1]),-1) - 10, round(max(np[:, 1]),-1) + 10, 10))
    if (xMajorTickFrequency != -1):
        ax.xaxis.set_major_locator(MultipleLocator(xMajorTickFrequency))
    if (yMajorTickFrequency != -1):
        ax.yaxis.set_major_locator(MultipleLocator(yMajorTickFrequency))

    # ax.set_yticks(numpy.arange(round(min(np[:, 0]),-1) - 10, round(max(np[:, 1]),-1) + 10, 10))
    # ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    # ax.yaxis.set_minor_locator(AutoMinorLocator(2))

    ax.minorticks_on()

    # colors = sbn.color_palette("CMRmap", len(list_dataFrame))
    colors = sbn.color_palette("CMRmap", 10)
    markers = ["o", "8", "s", "p", "d"]
    for i, df in enumerate(list_dataFrame):
        np = df.to_numpy(dtype="float")
        if len(legent) == 0:
            ax.plot(np[:, 1], np[:, 0], marker=markers[i % 5], mfc="#525252", markersize=3, c=colors[i])
        else:
            ax.plot(np[:, 1], np[:, 0], marker=markers[i % 5], mfc="#525252", markersize=3, c=colors[5 + i * 3],
                    label=legent[i])
    if len(legent) != 0:
        leg = ax.legend(prop=legent_FONT, loc="upper left")
        for text in leg.get_texts():
            text.set_color("#045a8d")

    ax.grid(c="white", alpha=0.2, which="both")
    # ax.patch.set_facecolor('#ababab')
    ax.patch.set_facecolor('#a6bddb')
    ax.patch.set_alpha(0.9)

    # fig.add_subplot(ax)
    # ax.scatter(x=np[:,1],y=np[:,0])


    return fig

def scaterPlot(list_dataFrame,title="Scaterplot",legent=[],ylabel="",
               xlabel="",xMajorTickFrequency=-1,yMajorTickFrequency=-1):

    fig = plt.figure(dpi=300,figsize=(4,4))
    #fig.set_facecolor("#d9d9d9")
    fig.set_facecolor("white")
    ax=fig.add_subplot(111)
    ax.set_title(title,fontdict=FONT,color="#045a8d")
    ax.set_ylabel(ylabel,fontdict=FONT,color="#045a8d")
    ax.set_xlabel(xlabel,fontdict=FONT,color="#045a8d")
    ax.tick_params(which="both",direction="in",top=True, right=True,labelsize=6)

    #ax.set_xticks(numpy.arange(round(min(np[:, 1]),-1) - 10, round(max(np[:, 1]),-1) + 10, 10))
    if(xMajorTickFrequency!=-1):
        ax.xaxis.set_major_locator(MultipleLocator(xMajorTickFrequency))
    if (yMajorTickFrequency != -1):
        ax.yaxis.set_major_locator(MultipleLocator(yMajorTickFrequency))

    #ax.set_yticks(numpy.arange(round(min(np[:, 0]),-1) - 10, round(max(np[:, 1]),-1) + 10, 10))
    #ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    #ax.yaxis.set_minor_locator(AutoMinorLocator(2))

    ax.minorticks_on()

    #colors = sbn.color_palette("CMRmap", len(list_dataFrame))
    colors = sbn.color_palette("CMRmap", 10)
    markers=["o","8","s","p","d"]
    for i,df in enumerate(list_dataFrame):
        data_points = df.to_numpy(dtype="float")
        if len(legent)==0:
            ax.plot(data_points[:,1],data_points[:,0],marker=markers[i%5],mfc="#525252",markersize=3,c=colors[i])
        else:
            ax.plot(data_points[:,1],data_points[:,0],marker=markers[i%5],mfc="#525252",markersize=3,c=colors[7-i],label=legent[i])
    if len(legent)!=0:
        leg =ax.legend(prop=legent_FONT,loc="upper left")
        for text in leg.get_texts():
            text.set_color("#045a8d")


    ax.grid(c="white",alpha=0.2 ,which="both")
    #ax.patch.set_facecolor('#ababab')
    ax.patch.set_facecolor('#a6bddb')
    ax.patch.set_alpha(0.9)


    #fig.add_subplot(ax)
    #ax.scatter(x=np[:,1],y=np[:,0])


    return fig


if __name__ == "__main__":

    #path = "./Measurments_Feb10/Mazda/Exellent/Accelaration/"
    #filename = "1MazdaDelay(10)"

    #path = "./GPSOnlyResults/"

    #movingAverage("Testing_Audi.txt")
    #movingAverage("RawAccelerometerData/GPS_Accel+GPS_Alcatel_16April_Audi_S3/1/1_Alcatel_Pure_Acceleration_16 april.txt")

    #fe.createSinusoid()
    #modifyAccelerationFile("./acc10(5)Audi.txt","./5_acc10_Audi_Moto.txt")

    data = ff.fourierTransform("./filtered_acceleration.csv")
    rw.writeAccelerationsToFile(data,"FourierFilteredAccelerations.csv")

    #fourierTransform("./filtered_acceleration.csv")

    # path = "./AccelGPSResults/"
    # path2 = "./GPSOnlyResults/"
    #
    # phoneList=["Motorola GS5","Alcatel","SonyXA_Ultra","Huawei"]
    # carList=["AudiS3","Maserati","Citroen_C1","Mazda_MX5","Mazda_6"]
    # carSpeed_RPM_List={"AudiS3":51.82,"MazdaMX5":47.34,"Mazda6":51.30,"Maserati":44.31,"Citroen_C1":64.60}
    #
    #
    # rpm_kmh = carSpeed_RPM_List["AudiS3"]
    # car = carList[0]
    # phone = phoneList[0]
    #
    # # English
    # title = "Power Output " + carList[0]
    # legend = ["1" +phoneList[1]+ " GPS","2"+phoneList[1]+" GPS","3"+phoneList[1]+" GPS","4"+phoneList[1]+" GPS"]
    # ylabel = "Power: $HP_{(SAE)}$"
    # xlabel = "$Speed_{(km/h)}$"
    # xlabel = "Rotations Per Minute $_{(еng)}$"
    # lang = "eng"
    #
    # # Greek
    # title = "Απόδοση Κινητήρα " + carList[0]
    # legend = ["1" +phoneList[0]+ " GPS","2"+phoneList[0]+" GPS","3"+phoneList[1]+" GPS","4"+phoneList[1]+" GPS"]
    # ylabel = "Ισχυς: $HP_{(SAE)}$"
    # xlabel = "$Ταχύτητα_{(km/h)}$"
    # xlabel = "Περιστροφές το λεπτό $_{(Κιν)}$"
    # lang = "gr"
    #
    #
    # list_dataframe = []
    # for i in range(11,12):
    #
    #
    #     df = pd.read_csv(path+str(i)+"_PowerSpeed_Audy_MotorollaGS5.csv", delimiter=" ",
    #                      names=["Power", "Speed"])
    #     df.iloc[:, 1] = df.iloc[:, 1].multiply(rpm_kmh)
    #     list_dataframe.append(df)
    #     # df = pd.read_csv(path+"PowerSpeed_Masserati_MotorollaGS5(" + str(i) + ").csv", delimiter=" ",
    #     #                  names=["Power", "Speed"])
    #     # df = df.iloc[:-2, :]
    #     # df.iloc[:, 1] = df.iloc[:, 1].multiply(44.31)
    #     # list_dataframe.append(df)
    #
    #     #df.iloc[:, 1] = df.iloc[:,1].multiply(44.35)
    #     #df= df.iloc[:-2,:]
    #
    #
    #
    # fig = scaterPlot(list_dataframe, title, legend, ylabel, xlabel, 500, 40, )
    # fig.savefig(path + "Result Figures/28_12_1_PowerSpeed_AudiS3_MotorollaGS5(" + str(5) + ")" + lang + ".png")
    #
    #
    #
    #
    # print("stop")

    # import PowerFromGpsSpeeds
    #
    # for i in range(1,11):
    #     PowerFromGpsSpeeds.createCsvFilePowerSpeed("./Gps Speeds Only/","GPSSpeedsMaserati("+str(i)+").txt")
    #
    # path = "./"
    # filename = "acc10(5)Au]di"
    # extension = ".txt"
    # with open(path+filename+extension,"r") as file:
    #
    #     csvfile = open(filename+'.csv', 'w')
    #     csvWriter = csv.writer(csvfile, delimiter=',',
    #                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #     csvWriter.writerow(['TIME','Z','Y','X'])
    #
    #     next(file)
    #     next(file)
    #     next(file)
    #     for line in file:
    #         words =  line.split();
    #         csvWriter.writerow([words[0],words[4],words[5], words[6]])
    #
    #     csvfile.close()
    #
    #
    #
    #
    #     printDistribution(csvfile)
    #     #movingAverage(filename+'.csv')
    #     #interpolate(csvfile)
    #
    #     dataFrame = pd.read_csv("Acceleration.csv")
    #     d = dataFrame[["TIME","Z","X","Y"]]
    #     data =np.array(d)
    #     time = np.array(d["TIME"].iloc[:])
    #     z = np.array(d["Z"].iloc[:])
    #     plt.plot(time,z, color='g')
    #     plt.xlabel('Time (millis)')
    #     plt.ylabel('Acceleration (m/s)')
    #     plt.title('Acceleration')
    #     plt.show()






