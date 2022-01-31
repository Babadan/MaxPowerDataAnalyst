import csv
import pandas as pd
import numpy as np
import re

def createCsvFilePowerSpeed( path,filename ):
    with open(path+filename,"r") as file:

        fixedFName = re.sub(".txt$","fixed.csv",filename)
        with open( path+"fixed/"+fixedFName,"w+",newline='') as csvfile :

            csvWriter = csv.writer(csvfile, delimiter=' ')
            csvWriter.writerow(['time','speed','accuracy'])

            next(file)
            next(file)
            next(file)
            next(file)
            for line in file:
                words =  line.split();
                csvWriter.writerow([words[0],words[1],words[2]])


