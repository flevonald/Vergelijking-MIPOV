# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 15:17:38 2025

@author: kuinr01
"""
import pandas as pd
import os

#per vervoerder
lijnen = {}

reserveerlijnen = pd.read_excel("300_2025_00_k01.xlsx", dtype=str ,
                                sheet_name='Blad1')
lijnen['EBS'] = reserveerlijnen.loc[reserveerlijnen['ReserveerRRReis']=='ja','LN_ID_OV_MIJ']

lijnen['ARR'] = pd.Series(['8850','8852','8858','6244','6245','6260','6262'])

for vervoerder_selectie, vraaglijnen in lijnen.items():
    print(vervoerder_selectie)
    print(list(vraaglijnen))
    for input_filename in os.listdir('input_nieuw'):
        vervoerder = input_filename.split("_")[-1].strip('.csv')
        if not vervoerder == vervoerder_selectie:
            continue
        
        print(input_filename)
        file_type = input_filename.split("_")[0]

        if (file_type in ['DRG']) & (vervoerder == 'EBS'):
            df = pd.read_csv(os.path.join('input_nieuw', input_filename), dtype=str , sep=';', decimal=',')
        elif (file_type in ['IUS','OVS', 'VAP']) & (vervoerder == 'EBS'):
             df = pd.read_csv(os.path.join('input_nieuw', input_filename), dtype=str , sep='\t', decimal=',')
        elif (vervoerder == 'ARR'):
            df = pd.read_csv(os.path.join('input_nieuw', input_filename), dtype=str , sep=';', decimal=',')
         
        # zitten er vraagafhankelijke ritten in DRG
        if file_type =='DRG':
            drg_vraag_lijnen = df.loc[df['Type']=='Vraaggestuurd','Lijn'].unique()
            lijnen_niet_in_drg = list(lijnen[vervoerder].loc[~lijnen[vervoerder].isin(drg_vraag_lijnen)])
            print(f'Vraagafhankelijke lijnen niet vraaggestuurd in DRG: {lijnen_niet_in_drg}')
            
            drg_vraag_lijnen = df.loc[:,'Lijn'].unique()
            lijnen_niet_in_drg = list(lijnen[vervoerder].loc[~lijnen[vervoerder].isin(drg_vraag_lijnen)])
            print(f'Vraagafhankelijke lijnen niet in DRG: {lijnen_niet_in_drg}')
        
        elif file_type =='IUS':
            print('Nog geen info over haltes vraagafhankelijk')
            
        elif file_type == 'OVS':
            df['AantalOver'] = df['AantalOver'].astype(int)
            ovs_lijnen = df.loc[:,'LijnVan'].unique()
            lijnen_niet_in_ovsvan = list(lijnen[vervoerder].loc[~lijnen[vervoerder].isin(ovs_lijnen)])
            print(f'Vraagafhankelijke lijnen niet in OVS (van): {lijnen_niet_in_ovsvan}')
        
            df_ovs_vraag_van = df.loc[df['LijnVan'].isin(lijnen[vervoerder])]
            df_ovs_vraag_van.groupby('LijnVan')['AantalOver'].sum()
    
            df_ovs_vraag_naar = df.loc[df['LijnNaar'].isin(lijnen[vervoerder])]
            df_ovs_vraag_naar.groupby('LijnNaar')['AantalOver'].sum()
    
        # zijn er in/uitstappers voor deze lijnen
        
        # zijn er overstappers voor deze lijnen
        # is er VAP voor deze lijnen
        elif file_type == 'VAP':
            vap_lijnen = df.loc[:,'Lijn'].unique()
            lijnen_niet_in_vap = list(lijnen[vervoerder].loc[~lijnen[vervoerder].isin(vap_lijnen)])
            print(f'Vraagafhankelijke lijnen niet in VAP: {lijnen_niet_in_vap}')
            lijnen_niet_in_vap = list(lijnen[vervoerder].loc[~lijnen[vervoerder].isin(vap_lijnen)])
            
        elif file_type == 'NVG':
            nvg_lijnen = df.loc[:,'Lijn'].unique()
            lijnen_niet_in_nvg = list(lijnen[vervoerder].loc[~lijnen[vervoerder].isin(nvg_lijnen)])
            print(f'Vraagafhankelijke lijnen niet in NVG: {lijnen_niet_in_nvg}')
            
        elif file_type == 'VGR':    
            vgr_vraag_lijnen = df.loc[df['Type']=='Vraaggestuurd','Lijn'].unique()
            lijnen_niet_in_drg = list(lijnen[vervoerder].loc[~lijnen[vervoerder].isin(drg_vraag_lijnen)])
            print(f'Vraagafhankelijke lijnen niet vraaggestuurd in VGR: {lijnen_niet_in_drg}')
            
            vgr_lijnen = df.loc[:,'Lijn'].unique()
            lijnen_niet_in_vgr = list(lijnen[vervoerder].loc[~lijnen[vervoerder].isin(vgr_lijnen)])
            print(f'Vraagafhankelijke lijnen niet in VGR: {lijnen_niet_in_vgr}')
            
        print('\n')