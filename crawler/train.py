# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 11:17:50 2023

@author: USER
"""
from tools import get_soup
import pandas as pd

url='https://www.railway.gov.tw/tra-tip-web/tip'
api_url='https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip112/querybytime'

form_data={
    '_csrf': '61f9648c-af6e-4e8d-a22a-d4702c1f54ae',
    'trainTypeList': 'ALL',
    'transfer': 'ONE',
    'startStation': '1000-臺北',
    'endStation': '7000-花蓮',
    'rideDate': '2023/07/23',
    'startOrEndTime': 'true',
    'startTime': '12:00',
    'endTime': '23:59',   
}

def get_stations():
    soup=get_soup(url)
    stations={button.text.strip():button.get('title') for button in soup.find(id="cityHot")\
          .find_all('button')}
    return stations

def get_train_data(startStation,endStation,rideDate,startTime,endTime,ticket=False):
    soup=get_soup(url)
    crsf_code=soup.find(id="queryForm").find('input').get('value')
    stations=get_stations()
    form_data['startStation']=stations[startStation]
    form_data['endStation']=stations[endStation]
    form_data['_csrf']=crsf_code
    form_data['rideDate']=rideDate
    form_data['startTime']=startTime
    form_data['endTime']=endTime
    
    #print(form_data)
    soup=get_soup(api_url,form_data)
    table=soup.find('table',class_="itinerary-controls")
    if table is None:
        return '查詢失敗，請重新查詢...'
    
    trs=table.find_all('tr',class_="trip-column")
    datas=[]
    for tr in trs:       
        data=[]
        for i,td in enumerate(tr.find_all('td')):
            if i==0:         
                data.extend(td.text.strip().replace('(','').replace(')','')\
                      .replace('→','').split())
            else:             
                data.append(td.text.strip())   

        #print(data)
        datas.append(data)

    columns=[th.text.strip() for th in table.find('tr').find_all('th')]
    df=pd.DataFrame(datas,columns=['車種','車次','始發站','終點站']+columns[1:])
    if ticket:
        df=df[df['訂票']=='訂票']
        
    temp_str='_訂票' if ticket else ''
    
    df.to_csv(f'{startStation}-{endStation}_{rideDate.replace("/","-")+temp_str}.csv',encoding='utf-8-sig')
    return df



if __name__=='__main__':
    print(get_train_data('臺北','中壢','2023/07/30','00:00','23:59',True))


