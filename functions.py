#from pandas import DataFrame, read_csv
#import pandas as pd 
from .models import plik
import os
import re
import codecs
import smtplib
def readtxt(export):
    path=export.path
    print(path)
    bash="cat " + str(path)+ ">apps/kasa/export.txt"
    os.system(bash)
    print("dfdfsdf",codecs.getencoder('utf-8'))
    myfile=codecs.open('apps/kasa/export.txt','r',encoding='cp1250',errors='ignore')
    #myfile=codecs.open('apps/kasa/export.txt','r',encoding='utf-8',errors='ignore')
    
    filecontent=myfile.read()
    rows=filecontent.split("\n")
    tablica = []
    licznik=0
    for row in rows[1:]:
        licznik+=1
        pola=row.split(";")
        if len(pola)>10:
            print(pola[6])
            polakasa = []
            polakasa.append("110") #110 - stala wartosc
            data=pola[6][0:4]+ pola[6][5:7]+pola[6][8:]
            polakasa.append(data) # do przerobki na date RRRRMMDD
            kwota = pola[8].split(",")
            kwota_str=kwota[0].strip()+kwota[1]
            polakasa.append(kwota_str) # kwota, przcinek do usuniecia
            polakasa.append("10901069") # Nr Konta przedsiebiorstwa
            polakasa.append("0") # Zero - nie wiedziec po co
            polakasa.append("\""+"68109010690000000131826350"+"\"")
            polakasa.append("\""+"0"+"\"")
            polakasa.append("\""+"Janipol Meble Polska sp. z o.o.  Sp. K.||Przemysłowa 2|88-160 Janikowo"+"\"")
            ## Teraz trzeba skręcic Imie|Nazwisko|Adr|00-000|Miejsc
            dane_adr=pola[2].split(" ")
            dane_str=dane_adr[1]+"|"+dane_adr[0]+"|Adr|00-000|Miejsc"
            polakasa.append("\""+dane_str+"\"")
            data2=pola[7][0:4]+ pola[7][5:7]+pola[7][8:]
            polakasa.append(data2) # data dostawy
            polakasa.append("0") # Zero - nie wiedziec po co
            polakasa.append("\""+pola[5]+"\"") # tytul
            #polakasa.append(pola[10][0]) # 1,2,3...
            polakasa.append("1") # 1,2,3...
            #pesel

            polakasa.append("\""+"PS"+"||"+pola[3]+"\"")
            #55
            polakasa.append("\""+"55"+"\"")
            
            polakasa.append("\""+str(licznik)+"\"")
            polakasa.append("0")
            tablica.append(polakasa)
    print(tablica)   
    #myoutputfile = codecs.open('apps/kasa/out.txt','w',encoding='utf-8',errors='ignore')
    myoutputfile = codecs.open('apps/kasa/out.txt','w',encoding='cp1250',errors='ignore')
    for wiersz in tablica:
        wiersz_str=",".join(str(x) for x in wiersz)
        wiersz_str+="\n"
        #myoutputfile.writelines(wiersz)
        myoutputfile.write(wiersz_str)
    myfile.close()
    myoutputfile.close()





    
        

        #print(row)
    return None

def xls2intr(export):
    path=export.path
    print(path)

    #tab2colon="tail -n +12 " + str(path) + "| sed 's/\t/;/g' | tr -d '\000'"
    tab2colon="tail -n +12 " + str(path) + "| sed 's/\t/;/g'| sed 's/ //g'> apps/intrastat/wywoz_tmp.csv"
    #tab2colon="cat " +  str(path)
    print("xls2intr")
    os.system(tab2colon)
    os.system('apps/intrastat/bin/createcsv')
    myfile = open('apps/intrastat/wywoz_tmp1.csv','r')
    zawartosc = myfile.read()
    wiersze = zawartosc.split("\n")
    i=0
    tablica = []
    for wiersz in wiersze:
        pola=wiersz.split(";")
        polaintrastat = []
        #przestawiamy kolumny
        if  len(pola)>20:
            wiersz_intrastat = []
            polaintrastat.append("") # Opis Towaru

            polaintrastat.append(pola[11]) # Kraj przez - KrPrz
            polaintrastat.append(pola[12]) # IncoT
            polaintrastat.append(pola[13]) # Rodz. trans. handl. - Rtra
            polaintrastat.append(pola[15]) # NrKodu
            polaintrastat.append(pola[14]) # SpT
            polaintrastat.append("") # Pusta
            polaintrastat.append(pola[21]) # MasaWl WYCIAC KROPKI

            if pola[23]!="":
                 polaintrastat.append(pola[23])
            else:
                 polaintrastat.append("0")  # SPecJednMiary 
            polaintrastat.append(cleardotsandspaces(pola[19])) # Wart. fakt
            polaintrastat.append(cleardotsandspaces(pola[17])) # Wart. stat
            polaintrastat.append(cleardotsandspaces(pola[16])) # NIP
#--



#            polaintrastat.append(pola[16]) # Nr mat./ Nr surowca - NrKodu
#            polaintrastat.append("") # Kraj pochodzenia
#            polaintrastat.append(cleardotsandspaces(pola[22])) # Masa własna      usun kropki i spacje
#            if len(pola)>24:
#                polaintrastat.append(pola[24]) # SpecJdMiar - Jwg
#            else: 
#                 polaintrastat.append("0") #30.10.2018
#            polaintrastat.append(cleardotsandspaces(pola[18])) # Wart. fakt
#            polaintrastat.append(cleardotsandspaces(pola[20])) # Wart. stat
#            polaintrastat.append(pola[17]) # NrNip
            wiersz_intrastat = ";".join(polaintrastat)
            tablica.append(wiersz_intrastat)

            i+=1
    myoutputfile = open('apps/intrastat/out.csv','w')
    for wiersz in tablica:
        myoutputfile.writelines(wiersz + "\n")
    myfile.close()
    myoutputfile.close()
    






    

    #wywoz_csv=read_csv('apps/intrastat/wywoz_tmp1.csv',error_bad_lines=False)  
    
    return "345"

def xls2intr2(export):
    path=export.path
    print(path)

    #tab2colon="tail -n +12 " + str(path) + "| sed 's/\t/;/g' | tr -d '\000'"
    tab2colon="tail -n +13 " + str(path) + "| sed 's/\t/;/g'| sed 's/ //g'> apps/intrastat/wywoz_tmp.csv"
    #tab2colon="cat " +  str(path)
    #print(tab2colon)
    print("xls2intr2222222")
    os.system(tab2colon)
    os.system('apps/intrastat/bin/createcsv')
    myfile = open('apps/intrastat/wywoz_tmp1.csv','r')
    zawartosc = myfile.read()
    wiersze = zawartosc.split("\n")
    i=0
    tablica = []
    for wiersz in wiersze:
        pola=wiersz.split(";")
        polaintrastat = []
        #przestawiamy kolumny
        if  len(pola)>20:
            wiersz_intrastat = []
            polaintrastat.append("") # Opis Towaru
            polaintrastat.append(pola[12]) # Kraj przez
            polaintrastat.append(pola[13]) # IncoT
            polaintrastat.append(pola[14]) # Rodz. trans. handl.
            polaintrastat.append(pola[16]) # Nr mat./ Nr surowca
            polaintrastat.append(pola[15]) # Sposob transportu
            polaintrastat.append(pola[17]) # Kraj pochodzenia
            polaintrastat.append(cleardotsandspaces(pola[22])) # Masa własna      usun kropki i spacje
            if len(pola)>24:
                polaintrastat.append(pola[24]) # SpecJdMiar
            else: 
                 polaintrastat.append("0") #30.10.2018
            polaintrastat.append(cleardotsandspaces(pola[18])) # Wart. fakt
            polaintrastat.append(cleardotsandspaces(pola[20])) # Wart. stat
            #polaintrastat.append(pola[17]) # NrNip
            wiersz_intrastat = ";".join(polaintrastat)
            tablica.append(wiersz_intrastat)

            i+=1
    myoutputfile = open('apps/intrastat/out.csv','w')
    for wiersz in tablica:
        myoutputfile.writelines(wiersz + "\n")
    myfile.close()
    myoutputfile.close()
    






    

    #wywoz_csv=read_csv('apps/intrastat/wywoz_tmp1.csv',error_bad_lines=False)  
    
    return "345"
def cleardotsandspaces(wartosc):
    wytnij=re.split('\.| ',wartosc)
    zlacz = "".join(wytnij)
    return zlacz

