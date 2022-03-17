# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 13:23:09 2022

@author: Shaura Daria
"""


import pandas
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import sys

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Ошибка. Недостаточное число парамтеров.')
        sys.exit(1)
    else:
        fNameA = sys.argv[1]
        fNameB = sys.argv[2]
        fNameC = sys.argv[3]
        
    # fNameA = 'A.csv'
    # fNameB = 'B.csv'
    # fNameC = 'C.csv'
    
    dfA = pandas.read_csv(fNameA, names=['date','name','work','fact_hours'], skiprows=[0],parse_dates=(True))
    dfB = pandas.read_csv(fNameB, names=['work','plan_hours'], skiprows=[0], sep=';', index_col='work')
    dfC = pandas.read_csv(fNameC, names=['name','salary'], skiprows=[0], sep=';', index_col='name')
    
    sumHours = dfA.groupby(['work','name'])['fact_hours'].sum().to_frame(name='fact_hours').reset_index()
        
    
    # 1,2,3
    sumHoursParams = sumHours.agg({'fact_hours':['sum','mean','median']}).round(2)
    print('Общие трудозатраты на проект, среднее и медианное время выполнения задач в часах')
    print(sumHoursParams)
    
    # 4
    meanTime = sumHours.groupby(['name']).agg({'fact_hours':['mean']}).round(2)    
    print('')
    print('Среднее время, затраченное на решение задач каждым из исполнителей в часах')
    print(meanTime)
    
    # 5
    income = 24000
    p = sumHours.groupby(['name']).agg({'fact_hours':['sum']})
    
    costs = (p.iloc[:, 0]*dfC.salary).sum()
    profit = income - costs
    profitability = (profit * 100)/income
    print('рентабельность = ', profitability.round(2), '%')
    
    # 6
    print('')
    print('Cреднее количество часов, отрабатываемое каждым сотрудником за день')
    meanTimePerDay = dfA.groupby(['date','name'])['fact_hours'].sum().groupby('name').mean()
    print(meanTimePerDay.round(2))
    
    # 7
    print('')
    print('Дни отсутствия для каждого сотрудника')
    dfA['date'] = pandas.to_datetime(dfA['date'], dayfirst=True)
    
    bisness_days = pandas.Series(pandas.date_range(dfA.date.min(), dfA.date.max(), freq='B'))
    
    for person in dfC.index:
        wDays = dfA[dfA.name==person]
        flt = ~bisness_days.isin(wDays.date.values)
        print(person, 'не работал', bisness_days[flt].values)
        
        
    # 8
    print('')
    print('Cредний «вылет» специалиста из оценки в процентах')
    sumHours = sumHours.set_index('work')
    
    inner_merge = pandas.merge(dfB, sumHours, left_index=True, right_index=True)    
    inner_merge['diff'] = (inner_merge['fact_hours'] - inner_merge['plan_hours'])/inner_merge['plan_hours']*100
    
    meanDiff = inner_merge.groupby(['name']).agg({'diff':['mean']})
    print(meanDiff.round(2))
    
    fig, axs = plt.subplots()    
    img = inner_merge.loc[inner_merge.index, ['plan_hours', 'fact_hours']]
    axs.xaxis.set_major_locator(ticker.MultipleLocator(2))
    fig.set_figwidth(16)
    img.plot(ax=axs)
    fig.savefig('Result.png')
    #plt.show()
