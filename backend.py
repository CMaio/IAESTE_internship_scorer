import tkinter
from tkinter import filedialog as fd
from tkinter import messagebox
import csv

#Data
allData=[]
allIDs=[]
allBidsConf=[]
result=[]


##get all the ids
def getOffersIds(fileCSV):
    global allIDs
    with open(fileCSV, errors="ignore") as file_obj:
        reader_obj = csv.DictReader(file_obj)
        for row in reader_obj:
                if "ES-20" in row['Ref.No']:
                    allIDs.append(row['Ref.No'])
                    allData.append(row)
    return allIDs

#Get the information of csv realted to one row
def getOfferInfo(id):
    return allData[allIDs.index(id)]

#Get the selected things for one bid already saved
def getOfferBidParameters(id):
    for bid in allBidsConf:
        if bid[0] == id:
            return bid
  
        
#Get the final result of the the offer, and save it in the array result
def getResultBid(row):
    global result
    resultBid = 0
    resultRow=[]
    for element in row:
        if isinstance(element, str):
            resultRow[0] = element
        if isinstance(element, int):
            resultBid += element
    
    resultRow[1] = resultBid
    result.append(resultRow)



#Make all the correct points with for the different rows
def startCheckingRules():
    
    pass


#Find if there is already a row with that id that is saved and if not just adds the row to config
def setOfferBidParameters(row):
    for index,line in enumerate(allBidsConf):
        if line[0] == row[0]:
            allBidsConf[index] = row
            return
    allBidsConf.append(row)


#Saves all the information in the csv file, it needs the format also will break in the last for and it need and end windows(there is a finish method)
def saveConfigToPoints():
    resultdocument = "ResultOffers"
    with open(resultdocument,'w',) as file2_obj:
        writer_obj = csv.writer(file2_obj)
        for row in result:
            writer_obj.writerow(row)














##def start_offers_scores():
    ##mainWorking(fileCS,checkIsSecond.get())


def change_state_bar(self,value):
    self.progressbar_1.set(value)

def select_restriction(self,value):
    self.restrictionchoosed.set(value)

def finish_scores(self):
    messagebox.showinfo("","Se han puntuado todas las ofertas!")
    self.destroy()
    print("finish----------")





def findPosition(self, discipline):
    allDisciplines = self.reglas['generalDisciplines']['disciplines']
    i = 0
    j = 0

    while i < len(allDisciplines):
        if discipline != allDisciplines[i]['field'].lower():
            j = 0
            while j < len( allDisciplines[i]['FieldsOfStudy']):
                if discipline == allDisciplines[i]['FieldsOfStudy'][j]['field']:
                    return allDisciplines[i]['FieldsOfStudy'][j]
                j += 1
        else:
            return allDisciplines[i]
        
        i += 1

    return 0


def disciplines(self, fila, reglascheck):
    result = 0
    generalDiscipline = fila[reglascheck[0]]
    fieldsofstudy = fila[reglascheck[1]].split(";")

    if "|" in generalDiscipline:
        generalDiscipline =  generalDiscipline.split("|")


    
    if isinstance(generalDiscipline, str):
        position = self.findPosition(generalDiscipline.lower())
        if position != 0:
                if result <= position['points']:
                    result = position['points']
    else:
        for ds in generalDiscipline:
            position = self.findPosition(ds.lower())
            if position != 0:
                if result <= position['points']:
                    result = position['points']


    if len(fieldsofstudy):
        for fs in fieldsofstudy:
            position = self.findPosition(fs.lower())
            if position != 0:
                if result <= position['points']:
                    result = position['points']

    return result


def countryRestrictions(self,fila,reglascheck):
    result = 0
    salida = -1
    self.textbox.configure(state="normal")
    self.textbox.delete("0.0",tkinter.END)
    self.textbox.insert("0.0",fila['Ref.No']+"\n\n")
    if fila[reglascheck[0]] != "":
        self.textbox.insert("2.0",fila[reglascheck[0]])
    else:
        self.textbox.insert("2.0","No requeriments")
    self.textbox.configure(state="disable")
    print("arrived")
    self.wait_variable(self.restrictionchoosed)
    print("passed")
    salida = self.restrictionchoosed.get()

    ##print(fila[reglascheck[0]])
    ##salida = int(input("Si hay alguna restriccion referente a paises escribe el numero:\n[0] No hay restriccion \n[1] Restricción a un solo pais \n[2] Union Europea \n[3] Europa \n[4] Latinoamerica \n[5] Otros grupos de paises "))

    if salida == 0:
        result = 0
    elif salida == 1:
        result = self.reglas['country']['only']
    elif salida == 2:
        result = self.reglas['country']['UE']
    elif salida == 3:
        result = self.reglas['country']['EUROPA']
    elif salida == 4:
        result = self.reglas['country']['LATINOAMERICA']
    elif salida == 5:
        result = self.reglas['country']['OTRO']

    self.restrictionchoosed.set(-1)
    return result

def payment(self,fila, reglascheck):
    result = 0
    frequency = fila[reglascheck[1]]
    pay = float(fila[reglascheck[0]])
    period = self.reglas['payment'][frequency]['period']
    startrange = self.reglas['payment'][frequency]['startrange'].split(",")
    startpay = float(startrange[0])
    endpay = float(startrange[1])

    while result < 30:
        if startpay <= pay <= endpay:
            break        
        
        result += 2
        startpay = startpay + period
        endpay = endpay + period

    return result

def monthPeriod(self,fila, reglascheck):
    if int(fila[reglascheck[0]].split("-")[0]) != int(fila[reglascheck[0]].split("-")[1]): 
        return 0 
    
    startMonth = int(fila[reglascheck[0]].split("-")[1])
    finishMonth = int(fila[reglascheck[1]].split("-")[1])

    if startMonth >= 6 and finishMonth <= 9:
        return 20

    return 0

def weeksPeriod(self,fila, reglascheck):
    result = 0
    maxStartWeeks = 27
    weeksStart = int(fila[reglascheck[0]])
    weeksEnd =  int(fila[reglascheck[1]])

    tmp= self.reglas['weeks']
    for i in tmp:
        if ',' in i:
            tmpwk = i.split(",")

            if int(tmpwk[1]) != -1:
                if int(tmpwk[0]) <= weeksEnd <= int(tmpwk[1]):
                    return self.reglas['weeks'][i]
            else:
                if int(tmpwk[0]) <= weeksEnd:
                    return self.reglas['weeks'][i]

    return result

def languagePoints(self,fila, reglascheck):
    result = 0
    allresutlts=[]
    isSpanish = 0
    checkOrAdd = 0

    for opt in reglascheck:
        lang = fila[opt]
        if lang != "":
            if opt[-1].isdigit():
                if lang != 'Spanish':
                    if lang in self.reglas['language']:
                        allresutlts.append(self.reglas['language'][lang])
                    else:
                        allresutlts.append(self.reglas['language']['default'])
                        
                else:
                    isSpanish = 1
            else:
                if 'Level' in opt and isSpanish == 1:
                    allresutlts.append(self.reglas['language']['Spanish'][lang])
                    isSpanish = 0
                elif 'Level' not in opt:
                    allresutlts.append(fila[opt])
                    
    
    for option in allresutlts:
        if isinstance(option, int):
            if checkOrAdd == 1:
                    result += option
            else:
                if result < option:
                    result = option
                else:
                    if option == 'Or':
                        checkOrAdd = 0
                    else: 
                        checkOrAdd = 1
                

    return result


def baseRules(self,type):
    result = 0
    if type == '' or type =='off':
        type = "1"
    else:
        type = "2"


    result += self.reglas['base']
    result += self.reglas['term'][type]

    return result


def practica(self,fila, typeOffert):
    header = ['Ref.No','language','weeks','period','payment', 'country','generalDisciplines']
    puntuacion = 0
    result = []

    puntuacion += self.baseRules(typeOffert)



    for opt in header:
        if opt == 'Ref.No':
            result.append(fila[opt])
        
        if opt == 'language':
            puntuacion += self.languagePoints(fila,self.reglas[opt]['check'])
            print("Puntos por lenguaje-----------------------")
            print(puntuacion)
            print("-----------------------")

        if opt == 'weeks':
            puntuacion += self.weeksPeriod(fila,self.reglas[opt]['check'])
            print("Puntos por weeks-----------------------")
            print(puntuacion)
            print("-----------------------")

        if opt == 'period':
            puntuacion += self.monthPeriod(fila,self.reglas[opt]['check'])
            print("Puntos por period-----------------------")
            print(puntuacion)
            print("-----------------------")

        if opt == 'payment':
            puntuacion += self.payment(fila,self.reglas[opt]['check'])
            print("Puntos por payment-----------------------")
            print(puntuacion)
            print("-----------------------")

        if opt == 'country':
            puntuacion += self.countryRestrictions(fila,self.reglas[opt]['check'])
            print("Puntos por country-----------------------")
            print(puntuacion)
            print("-----------------------")

        if opt == 'generalDisciplines':
            puntuacion += self.disciplines(fila,self.reglas[opt]['check'])
            print("Puntos por generalDisciplines-----------------------")
            print(puntuacion)
            print("-----------------------")
    
    result.append(puntuacion)

    return result


def settingResultname(self,namedocument):
    tmpresult = namedocument.split("/")
    tmpdoc = tmpresult[len(tmpresult)-1]
    tmpdoc = tmpdoc.split(".csv")
    resultdoc = tmpdoc[0] + "-Resultado.csv"

    resultdir =""
    for index,x in enumerate(tmpresult):
        if index == len(tmpresult) - 1:
            resultdir = resultdir + resultdoc
        else:
            resultdir = resultdir + x + "/"

    return resultdir


def mainWorking(self,namedocument,typeOffer):
    totallines = 0
    actualline=0
    numstoadd = 0
    self.change_state_bar(0)
    resultdocument = self.settingResultname(namedocument)

    with open(namedocument, errors="ignore") as file_obj:
        with open(resultdocument,'w',) as file2_obj:
            reader_obj = csv.DictReader(file_obj)
            writer_obj = csv.writer(file2_obj)
            numstoadd = totallines / 0.1
            for row in reader_obj:
                if "ES-20" in row['Ref.No']:
                    
                    resultrow = self.practica(row,typeOffer)
                    actualline = actualline + numstoadd
                    self.change_state_bar(actualline)
                    writer_obj.writerow(resultrow)
            
    self.finish_scores()