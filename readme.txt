Исправлена часть замечаний. 
1. Конечно, обработка корректности входных данных не является полной: например, при изменении порядка файлов или некорректном их содержимом программа упадет с ошибкой.
2. Не все что можно вынесено в функции. Наверно для более сложного отчета стоило бы разделить расчет числовых показателей и формирование отчета по некоторой форме.



При запуске необходимо указать 3 входных файла с данными: 
	A (данные выгрузки из системы учёта времени), 
	B (оценки по задачам), 
	C (стоимость часа специалиста)

Пример запуска:
	python3 main.py A B C


Пример вывода:

python3 main.py A.csv B.csv C.csv
Общие трудозатраты на проект, среднее и медианное время выполнения задач в часах
        fact_hours
sum         229.00
mean          6.19
median        6.00

Среднее время, затраченное на решение задач каждым из исполнителей в часах
     fact_hours
           mean
name           
Вася       6.00
Маша       7.11
Петя       5.79
рентабельность =  50.69 %

Cреднее количество часов, отрабатываемое каждым сотрудником за день
name
Вася    8.40
Маша    8.00
Петя    7.36
Name: fact_hours, dtype: float64

Дни отсутствия для каждого сотрудника
Вася не работал []
Маша не работал ['2021-05-05T00:00:00.000000000' '2021-05-13T00:00:00.000000000']
Петя не работал []

Cредний «вылет» специалиста из оценки в процентах
     fact_hours
           mean
name           
Вася      26.19
Маша      62.96
Петя      32.14
