# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 13:23:09 2022

@author: Shaura Daria
"""


import pandas
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import sys
import pathlib
    
#reading data from files
def readData(fNameA,fNameB,fNameC):
        dfA = pandas.read_csv(fNameA, names=['date','name','work','fact_hours'], skiprows=[0],sep='\t',parse_dates=(True))
 
        dfB = pandas.read_csv(fNameB, names=['work','plan_hours'], skiprows=[0], sep='\t', index_col='work')
        dfA['date'] = pandas.to_datetime(dfA['date'], dayfirst=True)

        dfC = pandas.read_csv(fNameC, names=['name','salary'], skiprows=[0], sep='\t', index_col='name')
        return dfA, dfB, dfC


def getProfitability(income, hours, salary):   
    costs = (hours*salary).sum()
    profit = income - costs
    profitability = (profit * 100)/income
    return profitability
    

def savePlanAndFactHoursPlot(data, path):
    fig, axs = plt.subplots()    
    img = data.loc[data.index, ['plan_hours', 'fact_hours']]
    axs.xaxis.set_major_locator(ticker.MultipleLocator(2))
    fig.set_figwidth(16)
    img.plot(ax=axs)
    fig.savefig(path)
    #plt.show()
    
   
# making report:
# dfA - name, work, fact_hours dataframe
# dfB - work and plan_hours dataframe
# dfC - salary dataframe
def makeReport(dfA, dfB, dfC):
    sumHours = dfA.groupby(['work','name'])['fact_hours'].sum().to_frame(name='fact_hours').reset_index()
        
    # 1,2,3
    # estimate sum, mean, median hours for the project
    sumHoursParams = sumHours.agg({'fact_hours':['sum','mean','median']}).round(2)
    print('Общие трудозатраты на проект, среднее и медианное время выполнения задач в часах')
    print(sumHoursParams)
    
    # 4
    # estimate mean hours for the employee
    meanTime = sumHours.groupby(['name']).agg({'fact_hours':['mean']}).round(2)    
    print('')
    print('Среднее время, затраченное на решение задач каждым из исполнителей в часах')
    print(meanTime)
    
    # 5
    # estimate the project's profitability
    hours = sumHours.groupby(['name']).agg({'fact_hours':['sum']}).iloc[:,0]
    profitability = getProfitability(24000, hours, dfC.salary)
    print('рентабельность = ', profitability.round(2), '%')
    
    # 6
    # estimate the employee's mean hours per working day
    print('')
    print('Cреднее количество часов, отрабатываемое каждым сотрудником за день')
    meanTimePerDay = dfA.groupby(['date','name'])['fact_hours'].sum().groupby('name').mean()
    print(meanTimePerDay.round(2))
    
    # 7
    # estimate the employee's absence days
    print('')
    print('Дни отсутствия для каждого сотрудника')  
    bisness_days = pandas.Series(pandas.date_range(dfA.date.min(), dfA.date.max(), freq='B'))
    
    for person in dfC.index:
        wDays = dfA[dfA.name==person]
        flt = ~bisness_days.isin(wDays.date.values)
        print(person, 'не работал', bisness_days[flt].values)
        
        
    # 8
    # estimate the employee's mean difference between planned and fact hours as a percantage
    print('')
    print('Cредний «вылет» специалиста из оценки в процентах')
    sumHours = sumHours.set_index('work')
    
    summaryTable = pandas.merge(dfB, sumHours, left_index=True, right_index=True)    
    summaryTable['diff'] = (summaryTable['fact_hours'] - summaryTable['plan_hours'])/summaryTable['plan_hours']*100
    
    meanDiff = summaryTable.groupby(['name']).agg({'diff':['mean']})
    print(meanDiff.round(2))
    
    #9 
    # save the plot with planned hours and fact hours per task
    savePlanAndFactHoursPlot(summaryTable, 'Result.png')
    
    
def main(): 
    
    fNameA = sys.argv[1]
    fNameB = sys.argv[2]
    fNameC = sys.argv[3]    
            
    dfA, dfB, dfC = readData(fNameA, fNameB, fNameC)
    
    makeReport(dfA,dfB,dfC)
    
    

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Ошибка. Недостаточное число парамтеров.')
        sys.exit(1)
        
    else:
        
        fExist = False
        for i in range(3):
            if not pathlib.Path(sys.argv[i+1]).exists():
                print('Ошибка. Файл {} не существует'.format(sys.argv[i+1]))
                fNotExist = True
            
        if fExist:
            sys.exit(1)
                        
        main()

    