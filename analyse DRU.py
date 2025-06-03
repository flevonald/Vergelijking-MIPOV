# -*- coding: utf-8 -*-
"""
Created on Mon May 12 11:37:18 2025

@author: kuinr01
"""
import os
import pandas as pd
import json
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
        print(f'{tijd} niet omgezet')
        
def tijd_datetime2(tijd):
    try:
        dt_x = timedelta(hours=int(tijd.split(':')[0]), minutes=int(tijd.split(':')[1]))
        return dt_x
    except:
        print(f'{tijd} niet omgezet')
#%%    
if __name__ == "__main__":
#%% Controle-informatie inladen
    
#%% Files inladen
    for input_filename in os.listdir('input_nieuw'):
        print(input_filename)
        file_type = input_filename.split("_")[0]
        print(f"Bestandstype: {file_type}")
        
        if not file_type == 'DRG':
            continue
        
        df = pd.read_csv(os.path.join('input_nieuw', input_filename), dtype=str , sep=';', decimal='.')
        
        df['Datum'] = pd.to_datetime(df['Datum'])
        df['dagvandeweek'] = df['Datum'].dt.weekday
        
        for kolom in ['DruPlan','DruPubl']:        
            df[kolom] = df[kolom].apply(tijd_datetime).dt.total_seconds()/3600
        for kolom in ['AantalPlan','AantalPubl','DrkPlan','DrkPubl']:        
            df[kolom] = df[kolom].astype(float)
            
            
        df['DruVerschil'] = df['DruPlan']-df['DruPubl']
        df['DrkVerschil'] = df['DrkPlan']-df['DrkPubl']
        df_lijn = df.groupby(['Lijnnummer'])[['AantalPlan','AantalPubl','DruPlan','DruPubl','DrkPlan','DrkPubl','DruVerschil','DrkVerschil']].sum()
        
        df_lijn_type = df.groupby(['Lijnnummer','Type'])[['AantalPlan','AantalPubl','DruPlan','DruPubl','DrkPlan','DrkPubl','DruVerschil','DrkVerschil']].sum()
        df_lijn_type.to_excel('output_vergelijking/DRG per lijn-type-maand.xlsx')
        df_lijn_type_rit = df.groupby(['Lijnnummer','Type'])['Eerste Rit'].min()
        
        k=df['DrkPubl']/df['AantalPubl']
#%% oud
    for input_oud_filename in os.listdir('input_oud'):
        print(input_oud_filename)
        file_type = input_oud_filename.split("_")[0]
        print(f"Bestandstype: {file_type}")
        
        if not file_type == 'KE2':
            continue
        
        df_oud = pd.read_csv(os.path.join('input_oud', input_oud_filename), dtype={' .1':str}, header=5, sep=';', decimal=',')
        df_oud = df_oud.drop(index=0)
        df_oud = df_oud.rename(columns = {' .1':'DRU Totaal'})
        for kolom in ['Geplande ritten','Geplande ritten.1']:        
            df_oud[kolom] = df_oud[kolom].str.replace('.','').astype(float).fillna(0)
            
        df_oud['DRU Totaal'] = df_oud['DRU Totaal'].apply(tijd_datetime2).dt.total_seconds()/3600
            
        df_oud['Geplande ritten'] = df_oud[['Geplande ritten','Geplande ritten.1']].sum(axis=1)    
        df_oud['Lijnnummer'] = df_oud[' '].apply(lambda x: x.split('(')[-1].strip(')'))

        df_oud_lijn = df_oud.groupby(['Lijnnummer'])[['Geplande ritten','DRU Totaal']].sum()

#%% Samenvoegen
    #ritten
    #df
    df_ritten = pd.concat([df_lijn[['AantalPlan','AantalPubl']], df_oud_lijn[['Geplande ritten']]], axis=1)
    df_ritten.to_excel('output_vergelijking/vergelijking aantal ritten.xlsx')
    df_druk = pd.concat([df_lijn[['DruPlan','DruPubl']], df_oud_lijn[['DRU Totaal']]], axis=1)
    df_ritten.to_excel('output_vergelijking/vergelijking dru.xlsx')
    print(f'Klaar met bestand {input_filename}! \n\n')
