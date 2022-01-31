import pandas as pd
import numpy as np
import csv


def modifyGpsSpeeds(sourcefilename,endFilename):
    '''Read GpsSpeeds from a Car Addict file and writes then in another with a different format.
     Format is : 2 columns with "Time" "Speed" '''

    with open(sourcefilename, "r") as file:
        csvfile = open(endFilename, 'w')
        csvWriter = csv.writer(csvfile, delimiter=' ',
                               quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvWriter.writerow(['Time', "Speed"])

        next(file)
        next(file)
        next(file)
        time = 1000
        for line in file:
            words = line.split()
            csvWriter.writerow([time,words[1]])
            time+=1000

        csvfile.close()


def readAccelerationfromCarAddictFile(filename):
    '''Loads accelerations of ZXY axes from a car addict file to dataframe 
        Arguments:
            filename: File or path to source file.'''

    with open(filename, "r") as file:

        list= []
        i=0
        for line in file:
            if(i>3):
                words = line.split()
                list.append([words[4],words[5],words[6]])
            i+=1

    #npArr = np.array(list, dtype=float)
    df=pd.DataFrame(list, dtype=float)


    return df


def modifyCarAddictAccelerationFile(source,target):
    '''Extracts accelerations only from Car Addict File and writes it in a new file with specified header 
     Arguments:
        source = File or Path to source file       
        target = File or Path to target file  
     Return:
         none '''
    df=readAccelerationfromCarAddictFile(source)
    df.columns = ["Z","X","Y"]
    df.to_csv(target,index = False)


def writeAccelerationsToFile(data,targetFile):

    dataFrame=pd.DataFrame(data)
    dataFrame.insert(0, "", np.zeros(data.size), True)
    dataFrame.insert(0, "", np.zeros(data.size), True)
    dataFrame.insert(0, "", np.zeros(data.size), True)
    dataFrame.insert(0, "", np.zeros(data.size), True)
    print(dataFrame)

    with open(targetFile,"w") as file:
        file.write("")
        file.write("")
        file.write("")
        arr=np.array(dataFrame,dtype=float)
        np.savetxt(file,arr,delimiter=" ",fmt="%.2f")

def readPowerSpeedFromCSV(sourceFilename):

    """ Load Power Speed file to np.array 
    File Format: 2 columns with header "Power" "Speed" """

    with open(sourceFilename, "r") as file:

        list= []
        next(file)
        for line in file:
            words = line.split()
            list.append(words,dtype=float)

    return np.array(list)

def readAccelerationsToDF(filename):
    '''Format of file must be  tree colums and a header "Z" "X" "Y" '''

    dataframe = pd.read_csv(filename,index_col=False)
    return dataframe
