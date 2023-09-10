# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 11:23:16 2023

@author: USER
"""

from train import get_train_data,get_stations
from datetime import datetime

stations=get_stations()
menu={i+1:station for i,station in enumerate(stations)}

print('台鐵查詢系統v1.0')
while True:
    print(menu)       
    print('='*100)
    try:
        start=eval(input('請輸入起始站點編號(0:離開):'))
        if start==0:
            break
        end=eval(input('請輸入終止站點編號:'))
        # 取得實際的站點名稱
        startStation=menu[start]
        endStation=menu[end]
    except:
        print('輸入編號錯誤')
        continue
        
    # 輸出乘車區間
    print(f'[{startStation}=>{endStation}]')    
    if input('是否確定查詢(y/n)')=='n':
        continue        
    # 乘車時間/查詢週期
    rideDate=input('請輸入乘車時間(ex:2023/7/30):')    
    if rideDate=='':
        rideDate=datetime.now().strftime('%Y/%m/%d')    
    startTime=input('請輸入查詢起始時間(ex:00:00):')
    if startTime=='':
        startTime='00:00'        
    endTime=input('請輸入查詢終止時間(ex:23:59):')
    if endTime=='':
        endTime='23:59'
    # 是否需要查詢有票
    ticket=input('是否須查詢有票?(y/n)').lower()
    ticket=True if ticket=='y' else False      
    print(startStation,endStation,rideDate,startTime,endTime,ticket)
    print('='*100)    
    df=get_train_data(startStation,endStation,rideDate,startTime,endTime,ticket)
    # 取出對應的行
    print(df.iloc[:,[0,1,2,3,4,5,9,-1]])
    
    input('請按任Enter鍵...')
    
print('感謝使用本查詢系統...')