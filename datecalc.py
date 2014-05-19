# -*- coding: cp1251 -*-
import time
daysinmonth =[ 31, #Январь
	       28, #Февраль
	       31, #Март
	       30, #Апрель
	       31, #Май
	       30, #Июнь
	       31, #Июль
	       31, #Август
	       30, #Сентябрь
	       31, #Октябрь
	       30, #Ноябрь
	       31, #Декабрь
	                     ]
class Date(str):
	def __new__(self,s):
                if s in [today,"today"]:return today()
                sep=_getsep(s)
		s=sep.join(['%d'%int(i) for i in s.split(sep)])
		return ''.__new__(self,s)                
	def __add__(self,number):
		firstdate=date2days(self[:])
		if type(number) in [Date,str]: number=date2days(number[:])
        	return Date(days2date(firstdate+number))
        def __sub__(self,number):
		firstdate=date2days(self[:])
		if type(number) in [Date,str]: number=date2days(number[:])
        	return Date(days2date(firstdate-number))
        def __mul__(self,k):
                return Date(days2date(date2days(self)*k))
        def dayofweek(self):
                week=["воскресенье","понедельник","вторник","среда","четверг",
                      "пятница","суббота"]
                return week[date2days(self)%7-1]
def today():
        struct=time.strptime(time.asctime())
        return Date(".".join([str(i) for i in [struct.tm_mday,
                                          struct.tm_mon,struct.tm_year]]))
def _divcf(m,n):
	  d=m/float(n)
	  mod=d-int(d)
	  return int(d),mod
def _int(x):
	 result=int(x)
	 if x-result>=0.5: result+=1
	 return result
def _getsep(date):
                sep=[",",".",":",";","/"]
                for i in date:
			if i in sep: sep=i;break
		else: sep="."
		return sep
def date2days(date):
		sep=_getsep(date)
		day,month,year=[int(i) for i in date.split(sep)]
		md=0
		for m in range(month-1): md+=daysinmonth[m]
		days=day+md+(year-1)*365+(year-1)/4
		if year%4==0 and month>2:days+=1
		return days
def days2date(days):
	 year=_divcf(days,365.25)[0]
	 if year!=0:
                 delta=(year*365+year/4)/float(year)
         elif year%4==3: delta=366
         else: delta=365
	 mod=_int(_divcf(days,delta)[1]*delta)
	 month,day=0,0
	 dim=daysinmonth[:]
	 if (year%4==3 and mod>59):dim[1]+=1
	 while mod>dim[month]:
 		mod-=dim[month]
	 	month+=1
	 day=mod
	 if day==0:
                 month=11 if month==0 else month-1
                 day=daysinmonth[month]
	 return ".".join([str(i) for i in [day,month+1,year+1]])
