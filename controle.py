# -*- coding: utf-8 -*-
"""
Created on Mon May 12 11:37:18 2025

@author: kuinr01
"""
import os
import pandas as pd
import json
import numpy as np
from datetime import timedelta
#%% Functies voor verschillende deeltypen

def datumcontrole(datumserie):
    resultaat = True
    return resultaat

def tijd_datetime(tijd):
    try:
        tijd_x = [0,int(tijd[0:2]),int(tijd[2:4]), int(tijd[4:6])]
        if tijd_x[1]>=24:
            tijd_x[0] = tijd_x[1]//24
            tijd_x[1] = tijd_x[1]%24
        dt_x = timedelta(days=tijd_x[0], hours=tijd_x[1], minutes=tijd_x[2], seconds=tijd_x[3])
        return dt_x
    except:
        # Fout bij omzetten, teruggeven van de originele waarde
        print(f'{tijd} niet omgezet')
    
if __name__ == "__main__":
# Controle-informatie inladen
    with open("enumeraties.json", "r") as read_content: 
        MIPOV_enumeraties = json.load(read_content)

    
    with open("veldtypes_nieuw.json", "r") as read_content: 
        MIPOV_dtypes = json.load(read_content)

    print('Controleinformatie geladen')
    
# Files inladen
    for input_filename in os.listdir('input_nieuw'):
        print(input_filename)
        file_type = input_filename.split("_")[0]
        print(f"Bestandstype: {file_type}")
        
        if file_type not in MIPOV_dtypes.keys():
            print('Bestandstype niet bekend')
            continue
        
        df = pd.read_csv(os.path.join('input_nieuw', input_filename), dtype=str , sep=';', decimal=',')
        
# kolommen
        kolommen_file = df.columns.to_list()
        if len(kolommen_file) == 1:
            print('Slechts 1 kolom! \n \
                  Poging met komma als separator')
            df = pd.read_csv(os.path.join('input_nieuw', input_filename), dtype=str, sep=',')
            kolommen_file = df.columns.to_list()
            
        extra_kolommen = [x for  x in kolommen_file if x not in MIPOV_dtypes[file_type].keys()]
        print(f'{len(extra_kolommen)} extra kolommen: {extra_kolommen}')
        missende_kolommen = [x for  x in list(MIPOV_dtypes[file_type].keys()) if x not in kolommen_file]
        print(f'{len(missende_kolommen)} missende kolommen: {missende_kolommen}')

        for kolom in [x for  x in kolommen_file if x in MIPOV_dtypes[file_type].keys()]:
            try:
                df[kolom] = df[kolom].astype(MIPOV_dtypes[file_type][kolom])
            except:
                print(f'{kolom} kan niet worden omgezet')
        
        #Datum
        if 'Datum' in kolommen_file:
            try:
                df['Datum'] = pd.to_datetime(df['Datum'], format='%Y%m%d')
            except:
                print('Omzetten datum niet geslaagd')
 #tijd
        ## nog in json te zetten
        for tijdkolom in ["Eerste Rit", "Laatste Rit","DruPlan", "DruPubl"]:
            if tijdkolom in kolommen_file:
                lengte = df[tijdkolom].apply(lambda x: len(x))
                if not df.loc[lengte != 6].empty:
                    print('Niet alle rijen hebben 6 karakters')
                print(f'Omzetten van tijdkolom: {tijdkolom}')    
                df[tijdkolom] = df[tijdkolom].apply(tijd_datetime)
                ## nog in json te zetten
        for haltekolom in ["RitVan","RitNaar","Haltecode"]:
            if haltekolom in kolommen_file:
                #aantal waarden
                lengte = len(df[haltekolom])
                # aantal dat begint met NL:
                len_q = len(df.loc[df[haltekolom].str.startswith('NL:CHB:Quay:')])
                perc = round(len_q / lengte * 100, 2)
                print(f'{len_q} van {lengte} waarden in {haltekolom} beginnen met NL:CHB:Quay: ({perc}%)')

        
#veldtypes

# enumeraties
        print(f'Klaar met bestand {input_filename}! \n\n')
