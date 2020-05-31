# -*- coding: utf-8 -*-
"""
Created on Sat May 30 17:51:17 2020

@author: tvo
"""
import pandas as pd
import numpy as np

df = pd.read_csv('//uahdata/rstor/NASA-COVID19-hackathon-2020/DATA/SEDAC_socioeconomic/USA_unemployment_change.csv').T

df.columns = df.iloc[0]
df = df[1:]

df.index = pd.to_datetime(df.index,format='%b-%y')

import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10,7))
plt.plot(df.index, df.Average, '--r', marker="o", 
         markersize=3
         ,c="red")

plt.ylabel("Unemployment rate (%)", size=30,
           weight="bold")
plt.tick_params(axis='x',rotation=30,labelsize=25)
plt.tick_params(axis='y',labelsize=25)
plt.ylim(3,15)

plt.tight_layout(True)
plt.grid(True)



df['Average'] = np.round(df['Average'],3)


# NO2 graphs
df_no2 = pd.read_csv('//uahdata/rstor/NASA-COVID19-hackathon-2020/DATA/NO2/extract_NO2.csv')

cities = ['NYC','Wuhan','Milan']
for item in cities:
    df_no2_nyc = df_no2[['system:time_start',item]].dropna()
    df_no2_nyc['system:time_start'] = pd.to_datetime(df_no2_nyc['system:time_start'],
              format='%d-%b-%y')
    
    df_no2_nyc = df_no2_nyc.set_index('system:time_start')
    
    df_no2_nyc = df_no2_nyc.rename(columns={'system:time_start':'date_time'})
    
    
    fig,ax = plt.subplots(figsize=(12,7))
    plt.plot(df_no2_nyc.index, 
             df_no2_nyc[item], '--r', marker="o", 
             markersize=3
             ,c="blue",
             label='Original data')
    
    plt.plot(df_no2_nyc.index,
            df_no2_nyc[item].rolling(window=20).mean(),
            c='black',
            label='Average smoothing (kernel=20)'
             )
    
    plt.ylabel(r"Tropospheric vertical column "+
               "\n"+  
               "of $NO_{2}$"+
               "\n"+
               "$(\mu mol/m^{2})$", 
               size=20)
    
    
    plt.tick_params(axis='x',rotation=30,labelsize=15)
    plt.tick_params(axis='y',labelsize=15)
    plt.ylim(np.round(df_no2_nyc[item].min()),
             np.round(df_no2_nyc[item].max()))
    
    if item == 'Wuhan':
        plt.vlines(x="2020-01-10",
               ymin=df_no2_nyc[item].min() - 100,
               ymax = df_no2_nyc[item].max() + 100,
               color="r",
               linestyles='--',
               label='Pandemic starts')
        
        plt.xlim('2020-01-01','2020-05-27')
        ax.axvspan(xmin='2020-01-22', 
                         xmax='2020-02-22',
                         alpha=0.3,
                         color='pink',
                         hatch='/')

        
        
    elif item == 'NYC':
        plt.vlines(x="2020-03-01",
               ymin=df_no2_nyc[item].min() - 100,
               ymax = df_no2_nyc[item].max() + 100,
               color="r",
               linestyles='--',
               label='Pandemic starts')
        
        plt.xlim('2020-01-15','2020-05-27')
        
    else:
        plt.vlines(x="2020-03-01",
               ymin=df_no2_nyc[item].min() - 100,
               ymax = df_no2_nyc[item].max() + 100,
               color="r",
               linestyles='--',
               label='Pandemic starts')
        
        plt.xlim('2020-01-15','2020-05-27')
        ax.axvspan(xmin='2020-03-01', 
                         xmax='2020-04-15',
                         alpha=0.3,
                         color='pink',
                         hatch='/')
        
        
    
    plt.title(r'Changes in Air Quality at '+item+' City',
              size=15)
    
    plt.tight_layout(True)
    plt.legend(prop={'size':15})
    
    fig.savefig('//uahdata/rstor/NASA-COVID19-hackathon-2020/DATA/NO2/'
                +'no2_'+item+'.pdf')


# =============================================================================
# CO graphs
# =============================================================================
df = pd.read_csv('//uahdata/rstor/NASA-COVID19-hackathon-2020/DATA/CO/extract_CO_by_point.csv')

df['City'] = np.nan


df.loc[df['.geo'].str.slice(35, 38, 1) == str(114),'City'] = 'Wuhan'


df.loc[df['.geo'].str.slice(35, 38, 1) == str(9.1),'City'] = 'Milan'

df.loc[df['.geo'].str.slice(35, 38, 1) == str(-74),'City'] = 'NYC'

df = df.drop(columns=['.geo'])

keys = list(df.groupby('City').groups.keys())
df_grp = df.groupby('City')
for item in keys:
    df_item = df_grp.get_group(item)
    
    df_item = df_item.set_index('Date')
    print(df_item)
    df_item.index = pd.to_datetime(df_item.index,format='%Y-%m-%dT%H:%M:%S')
    
    
    # Plotting
    fig,ax = plt.subplots(figsize=(12,7))
    plt.plot(df_item.index, 
             df_item['mean'], '--r', marker="o", 
             markersize=3
             ,c="green",
             label='Original data')
    
    plt.plot(df_item.index,
            df_item['mean'].rolling(window=20).mean(),
            c='black',
            label='Average smoothing (kernel=20)'
             )
    
    plt.ylabel(r"CO concentration "+
               "\n"+  
               "$(mol/m^{2})$", 
               size=20)
    
    
    plt.tick_params(axis='x',rotation=30,labelsize=15)
    plt.tick_params(axis='y',labelsize=15)
    plt.ylim(df_item['mean'].min(),
             df_item['mean'].max())
    
    if item == 'Wuhan':
        plt.vlines(x="2020-01-10",
               ymin=df_item['mean'].min() - 0.01,
               ymax = df_item['mean'].max() + 0.01,
               color="r",
               linestyles='--',
               label='Pandemic starts')
        
        plt.xlim('2020-01-01','2020-05-27')
#        ax.axvspan(xmin='2020-01-22', 
#                         xmax='2020-02-22',
#                         alpha=0.3,
#                         color='pink',
#                         hatch='/')

        
        
    elif item == 'NYC':
        plt.vlines(x="2020-03-01",
               ymin = df_item['mean'].min() - 0.01,
               ymax = df_item['mean'].max() + 0.01,
               color="r",
               linestyles='--',
               label='Pandemic starts')
        
        plt.xlim('2020-01-15','2020-05-27')
        
    else:
        plt.vlines(x="2020-03-01",
               ymin=df_item['mean'].min() - 100,
               ymax = df_item['mean'].max() + 100,
               color="r",
               linestyles='--',
               label='Pandemic starts')
        
        plt.xlim('2020-01-15','2020-05-27')
#        ax.axvspan(xmin='2020-03-01', 
#                         xmax='2020-04-15',
#                         alpha=0.3,
#                         color='pink',
#                         hatch='/')
        
        
    
    plt.title(r'Changes in Air Quality at '+item+' City',
              size=15)
    
    plt.tight_layout(True)
    plt.legend(prop={'size':15})
    
    fig.savefig('//uahdata/rstor/NASA-COVID19-hackathon-2020/DATA/CO/'
                +'CO_'+item+'.pdf')

    
# =============================================================================
#    CHL concentration 
# =============================================================================
    
df_chl = pd.read_csv('//uahdata/rstor/NASA-COVID19-hackathon-2020/DATA/CHL/chl_extract.csv')
df_chl = df_chl.rename(columns={'CB':'Chesapeake Bay',
                       'LA':'Los Angeles, LA'})
cities = ['Chesapeake Bay','Los Angeles, LA','Shanghai']
for item in cities:
    df_chl_item = df_chl[['system:time_start',item]].dropna()
    df_chl_item['system:time_start'] = pd.to_datetime(df_chl_item['system:time_start'],
              format='%d-%b-%y')
    
    df_chl_item = df_chl_item.set_index('system:time_start')
    
    df_chl_item = df_chl_item.rename(columns={'system:time_start':'date_time'})
    
    
    fig,ax = plt.subplots(figsize=(12,7))
    plt.plot(df_chl_item.index, 
             df_chl_item[item], '--r', marker="o", 
             markersize=3
             ,c="orange",
             label='Original data')
    
    plt.plot(df_chl_item.index,
            df_chl_item[item].rolling(window=20).mean(),
            c='black',
            label='Average smoothing (kernel=20)'
             )
    
    plt.ylabel(r" Chlorophyll "+
               "\n"+  
               "$(mg/m^{-3})$", 
               size=20)
    
    
    plt.tick_params(axis='x',rotation=30,labelsize=15)
    plt.tick_params(axis='y',labelsize=15)

    
    plt.xlim('2019-11-01','2020-04-01')
    ylim_min = df_chl_item.loc[(df_chl_item.index > '2019-11-01')&
                               (df_chl_item.index < '2020-04-01')][item].min()
    
    ylim_max = df_chl_item.loc[(df_chl_item.index > '2019-11-01')&
                               (df_chl_item.index < '2020-04-01')][item].max()
    
    plt.ylim(ylim_min,
             ylim_max)
    
  
    
    plt.title(r'Changes in Water Quality at '+item+' City',
              size=15)
    
    plt.tight_layout(True)
    plt.legend(prop={'size':15})
    
    fig.savefig('//uahdata/rstor/NASA-COVID19-hackathon-2020/DATA/CHL/'
                +'chl_'+item+'.pdf')


# =============================================================================
# CHL concentration  - Venice 
# =============================================================================

df_chl = pd.read_csv('//uahdata/rstor/NASA-COVID19-hackathon-2020/DATA/CHL/chl_venice.csv')
df_chl = df_chl.rename(columns={'chlor_a':'Venice, Italy'})

cities = ['Venice, Italy']
for item in cities:
    df_chl_item = df_chl[['system:time_start',item]].dropna()
    df_chl_item['system:time_start'] = pd.to_datetime(df_chl_item['system:time_start'],
              format='%b %d, %Y')
    
    df_chl_item = df_chl_item.set_index('system:time_start')
    
    df_chl_item = df_chl_item.rename(columns={'system:time_start':'date_time'})
    
    
    fig,ax = plt.subplots(figsize=(12,7))
    plt.plot(df_chl_item.index, 
             df_chl_item[item], '--r', marker="o", 
             markersize=3
             ,c="orange",
             label='Original data')
    
    plt.plot(df_chl_item.index,
            df_chl_item[item].rolling(window=20).mean(),
            c='black',
            label='Average smoothing (kernel=20)'
             )
    
    plt.ylabel(r" Chlorophyll "+
               "\n"+  
               "$(mg/m^{-3})$", 
               size=20)
    
    
    plt.tick_params(axis='x',rotation=30,labelsize=15)
    plt.tick_params(axis='y',labelsize=15)

    
    #plt.xlim('2019-11-01','2020-04-01')
    ylim_min = df_chl_item.loc[(df_chl_item.index > '2019-11-01')&
                               (df_chl_item.index < '2020-04-01')][item].min()
    
    ylim_max = df_chl_item.loc[(df_chl_item.index > '2019-11-01')&
                               (df_chl_item.index < '2020-04-01')][item].max()
    
#    plt.ylim(ylim_min,
#             ylim_max)
    
    
    plt.title(r'Changes in Water Quality at '+item+' City',
              size=15)
    
    plt.tight_layout(True)
    plt.legend(prop={'size':15})
    
    fig.savefig('//uahdata/rstor/NASA-COVID19-hackathon-2020/DATA/CHL/'
                +'chl_'+item+'.pdf')


# =============================================================================
# NDVI
# =============================================================================
df_ndvi = pd.read_csv('//uahdata/rstor/NASA-COVID19-hackathon-2020/DATA/NDVI/NDVI_total.csv')

cities = ['NYC','Wuhan','Milan']
for item in cities:
    df_ndvi_item = df_ndvi[['system:time_start',item]].dropna()
    df_ndvi_item['system:time_start'] = pd.to_datetime(df_ndvi_item['system:time_start'],
              format='%d-%b-%y')
    
    df_ndvi_item = df_ndvi_item.set_index('system:time_start')
    
    df_ndvi_item = df_ndvi_item.rename(columns={'system:time_start':'date_time'})
    
    
    fig,ax = plt.subplots(figsize=(12,7))
    plt.plot(df_ndvi_item.index, 
             df_ndvi_item[item], '--r', marker="o", 
             markersize=3
             ,c="forestgreen",
             label='Original data')
    
    plt.plot(df_ndvi_item.index,
            df_ndvi_item[item].rolling(window=5).mean(),
            c='black',
            label='Average smoothing (kernel=5)'
             )
    
    plt.ylabel(r"NDVI index ",  
               size=20)
    
    
    plt.tick_params(axis='x',rotation=30,labelsize=15)
    plt.tick_params(axis='y',labelsize=15)
    plt.ylim(df_ndvi_item[item].min(),
             df_ndvi_item[item].max())
    
    if item == 'Wuhan':
        plt.vlines(x="2020-01-10",
               ymin=df_ndvi_item[item].min() - 0.1,
               ymax = df_ndvi_item[item].max() + 0.1,
               color="r",
               linestyles='--',
               label='Pandemic starts')
        
        plt.xlim('2019-10-01','2020-05-01')


        
        
    elif item == 'NYC':
        plt.vlines(x="2020-03-01",
               ymin=df_ndvi_item[item].min() - 0.1,
               ymax = df_ndvi_item[item].max() + 0.1,
               color="r",
               linestyles='--',
               label='Pandemic starts')
        
        plt.xlim('2019-10-01','2020-05-01')
        
    else:
        plt.vlines(x="2020-03-01",
               ymin=df_ndvi_item[item].min() - 0.1,
               ymax = df_ndvi_item[item].max() + 0.1,
               color="r",
               linestyles='--',
               label='Pandemic starts')
        
        plt.xlim('2019-10-01','2020-05-01')

        
        
    #plt.ylim(0,1)
    plt.title(r'Changes in NDVI at '+item+' City',
              size=15)
    
    plt.tight_layout(True)
    plt.legend(prop={'size':15})
    
    fig.savefig('//uahdata/rstor/NASA-COVID19-hackathon-2020/DATA/NDVI/'
                +'NDVI_'+item+'.pdf')


# =============================================================================
# Night time
# =============================================================================

df_nighttime = pd.read_csv('//uahdata/rstor/NASA-COVID19-hackathon-2020/DATA/Nighttime/Nightlight_total.csv')


cities = ['NYC','Wuhan','Milan']
for item in cities:
    df_nighttime_item = df_nighttime[['system:time_start',item]].dropna()
    df_nighttime_item['system:time_start'] = pd.to_datetime(df_nighttime_item['system:time_start'],
              format='%d-%b-%y')
    
    df_nighttime_item = df_nighttime_item.set_index('system:time_start')
    
    df_nighttime_item = df_nighttime_item.rename(columns={'system:time_start':'date_time'})
    
    
    fig,ax = plt.subplots(figsize=(12,7))
    plt.plot(df_nighttime_item.index, 
             df_nighttime_item[item], '--r', marker="o", 
             markersize=3
             ,c="darkviolet",
             label='Original data')
    
    plt.plot(df_nighttime_item.index,
            df_nighttime_item[item].rolling(window=2).mean(),
            c='black',
            label='Average smoothing (kernel=2)'
             )
    
    plt.ylabel(r"Night light consumption "+
               "\n"+
               "$nanoWatts/cm^{2}/sr$",  
               size=20)
    
    
    plt.tick_params(axis='x',rotation=30,labelsize=15)
    plt.tick_params(axis='y',labelsize=15)
    plt.ylim(df_nighttime_item[item].min(),
             df_nighttime_item[item].max())
    
#    if item == 'Wuhan':
#        plt.vlines(x="2020-01-10",
#               ymin=df_nighttime_item[item].min() - 0.1,
#               ymax = df_nighttime_item[item].max() + 0.1,
#               color="r",
#               linestyles='--',
#               label='Pandemic starts')
#        
#        plt.xlim('2019-10-01','2020-05-01')
#
#
#        
#        
#    elif item == 'NYC':
#        plt.vlines(x="2020-03-01",
#               ymin=df_nighttime_item[item].min() - 0.1,
#               ymax = df_nighttime_item[item].max() + 0.1,
#               color="r",
#               linestyles='--',
#               label='Pandemic starts')
#        
#        plt.xlim('2019-10-01','2020-05-01')
#        
#    else:
#        plt.vlines(x="2020-03-01",
#               ymin=df_nighttime_item[item].min() - 0.1,
#               ymax = df_nighttime_item[item].max() + 0.1,
#               color="r",
#               linestyles='--',
#               label='Pandemic starts')
#        
#        plt.xlim('2019-10-01','2020-05-01')
#
#        
        
    #plt.ylim(0,1)
    plt.title(r'Changes in Night light consumption  at '+item+' City',
              size=15)
    
    plt.tight_layout(True)
    plt.legend(prop={'size':15})
    
    fig.savefig('//uahdata/rstor/NASA-COVID19-hackathon-2020/DATA/Nighttime/'
                +'Nighttime_'+item+'.pdf')












