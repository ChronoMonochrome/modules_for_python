import radix
import copy

from math import log, sqrt, modf

try:
	from symbols import radical
	rad=radical[0]
except: 
	rad='sqrt'

try:
	# I really don't know how to get NaN by another way :)
	NaN = log(-1)
except:
	NaN = None

__n=1

def NOD(x, y):
	global __n 
	
	if x != 0:
		__n = NOD(y % x, x)
	else:
		__n = y
	
	return __n

def multiNOD(llst):
	def tempnod():
 		tmpn = NOD(llst[0], llst[1])
		del llst[0]
	 	llst[0] = tmpn
		return llst
		
	while len(llst) > 1:
		tempnod()
	else:
		return llst[0]

def isPrime(x):
	global NaN
	
	if x==1 or x==0:
		# we don't know if 0 or 1 is prime :P
		return NaN
		
	n,count = x/2,2
	
	while count <= n:
		if abs(x / count)  /  (x / float(count)) == 1:
			return 0
			
		count += 1
		
	return 1 

def __nextPrime (x, direct):
	while True:
		x += 1 * (1 if direct >= 0 else -1)
			
		if isPrime(x):
			return x 
			
def nextPrime(x, direct = 1):
	return __nextPrime(x, direct)
				
def factorization(x):
	factors = []
 	count = 0
	d = x
	n = 2
	r = x / 2.
	
	while n <= r:
		if isPrime(x): break
	
		while (x / n)  /  (x / float(n)) == 1:
			x /= n
			factors.append(n)
			n = 2
			
		n = nextPrime(n)
	if x != 1: 
		factors.append(x)
		
	return factors

def sqrt2(integer, power = 2):
	global rad
	
	fct = factorization(integer)
	lst = []
 
	for x in fct:
		if not x in lst:
			lst.append(x)
	n = 1
	
	for x in lst:
		count=fct.count(x)
		if count%power==1:count-=1
		n*=x**(count/power)
		for i in range(count):
			del fct[fct.index(x)]
	s=1
	for x in fct:
		s*=x 
	
	expr = "%s*%s(%s)" % (str(n), rad, str(s))
	expr = expr.replace('\x1a','').replace('*sqrt(1)','')
	return expr

def factors(lst):
	def toString(s):
		n = 1
		count = 0
		for i in s:
			if i == '1': n*=lst[count]
			count+=1
		return n
		
	from10=radix.from10
	factors=[]
	
	for c in xrange(1, 2**len(lst)):
		s = from10(c,2).rjust(len(lst))
		factor = toString(s)
		if not factor in factors:
		factors.append(factor)
		
	return factors

_n=1

def pack(lst):
	
	c = 0
	st = lst[c]
	l = len(lst)
	A = []
	
	while c < l:
		n = lst.count(st)
		A.append(str(st)+'**'+str(n))
		c += n
		try:
			st = lst[c]
		except:break
	
	return A
	
def nfactors(lst):
	
	def test(s):
		exec(s)
	
	if type(lst)==int:
		lst=pack(factorization(lst))
	try:
		[test(i) for i in lst]
	except TypeError:
		lst=pack(lst)
	except SyntaxError:
		return 'SyntaxError'
		
	n=1
	try:
		for x in lst: 
			n *= int(x[x.index('**')+2:]) + 1
	except ValueError: return 'ValueError'
	
	return n-1

def fseek(_x,delta=10**-5):
	if type(_x)!=float: 
		return _x
	if modf(_x)[0] <= delta:
		return int(_x)
	else: return _x

def decompIR(irrational):
	denom,insqrt,ceil='1','1','0'
	findslash=irrational.find('/')
	
	if findslash!=-1:
		irrational,denom = irrational[:findslash],irrational[findslash+1:]
		
	findsqrt = irrational.find('sqrt(')
	
	if findsqrt != -1:
		
		insqrt = irrational[findsqrt+5:irrational.find(')',findsqrt+5)]
		irrational = irrational[:findsqrt]
		
	ceil = irrational.replace('*','').replace('(','').replace(')','')
	if ceil == '': ceil = '1'
	
	if denom.count('sqrt'):
		ds = denom.find('sqrt') 
		tmp = insqrt
		tmpdenom,insqrt = 1,
		
		if ds != 0:
			return denom[:ds]
			
		tmpdenom *= eval(denom[ds+5:-1])
		denom = str(tmpdenom)
		insqrt *= eval(denom)
		tmpsqrt = decompIR(sqrt2(insqrt))
		ceil = str(eval(ceil)*eval(tmpsqrt[2]))
		insqrt = tmpsqrt[1]
		return i1i2(compIR([denom,insqrt,ceil]),'sqrt(%s)'% tmp)
	return denom,insqrt,ceil

def compIR(lst):
	global rad
	
	if type(lst) in [str, unicode]: 
		return lst
		
	if '0' in lst[1:] and lst[0]!='0':
		return u'0' 
		
	tmp = "%ssqrt(%s)/%s" % (lst[2], lst[1], lst[0])
	tmp = tmp.replace('sqrt(1)','').replace('1sqrt','sqrt')
	
	if tmp[-2:]=='/1': tmp=tmp[:-2]
	return unicode(tmp)


def i1i2(i1, i2):
	seek = fseek
	nod = multiNOD
	decomp = decompIR
	
	i1denom,i1sqrt,i1ceil=[float(e) for e in decomp(i1)]
	i2denom,i2sqrt,i2ceil=[float(e) for e in decomp(i2)]
	i1i2denom,i1i2sqrt,i1i2ceil = [seek(i) for i in [i1denom*i2denom,i1sqrt*i2sqrt,i1ceil*i2ceil]]
	
	decsqrt = decomp(sqrt2(i1i2sqrt))
	i1i2ceil *= seek(float(decsqrt[2]))
	i1i2sqrt = decsqrt[1]
	
	NOD=nod([i1i2ceil,i1i2denom])
	i1i2ceil /= NOD
	i1i2denom /= NOD
	return normform([str(e) for e in [i1i2denom,i1i2sqrt,i1i2ceil]])

def vectxvect(lst1,lst2):
	[x1, y1, z1]=lst1
	[x2, y2, z2]=lst2
	
	def tmpres(i1,j2,j1,i2):
		
		p1 = i1i2(i1,j2)
		p2 = i1i2(compIR(i1i2(j1,i2)),'-1')
		if p1[1] == p2[1]:
			insqrt = compIR(p1[1])
			tmp = [compIR(p1),compIR(p2)]
			tmp = pfractions(tmp)
			return compIR(i1i2(tmp,insqrt))
		else:
			return (compIR(p1) + '+' + compIR(p2))
			 	.replace('+-',  '-')
				.replace('0+',  '')
				.replace('+0',  '')
				.replace('0-', '-')
				.replace('-0',  '')
	return tmpres(y1,z2,z1,y2),tmpres(x2,z1,x1,z2),tmpres(x1,y2,y1,x2)

def add(i1,i2):
	if type(i1) in [str,unicode]:
		i1=decompIR(i1)
	if type(i2) in [str,unicode]: 
		i2=decompIR(i2)
	if i1[1]==i2[1]:
		insqrt='sqrt('+i1[1]+')'
		tmp=[compIR(i1),compIR(i2)]
		tmp=pfractions(tmp)
		return compIR(i1i2(tmp,insqrt))
	else:
		return (compIR(i1)+'+'+compIR(i2))
				.replace('+-','-')
				.replace('0+','')
				.replace('+0','')
				.replace('0-','-')
				.replace('-0','')

def vectxscal(lst1,lst2):
	[x1, y1, z1] = lst1
	[x2, y2, z2] = lst2
  
	return i1i2(x1,x2),i1i2(y1,y2),i1i2(z1,z2)

def vectxmix(lst1,lst2,lst3):
	vect = vectxvect(lst2,lst3)
	tmp = vectxscal(lst1,vect)
  
	tmp2 = []
	sqrts = [i[1] for i in tmp]
	if sqrts[0]==sqrts[1] and sqrts[1]==sqrts[2]:
		tmp2=add(tmp[0],tmp[1])
		return add(tmp2,tmp[2])
	elif sqrts[0]==sqrts[1]:
		tmp2=add(tmp[0],tmp[1]),tmp[2]
	elif sqrts[0]==sqrts[2]:
		tmp2=add(tmp[0],tmp[2]),tmp[1]
	elif sqrts[1]==sqrts[2]:
		tmp2=add(tmp[1],tmp[2]),tmp[0]
	else:
		tmp=[compIR(i) for i in tmp]
		return tmp[0]+tmp[1]+tmp[2]
	return add(tmp2[0],tmp2[1])

def vectmodul(lst):
	tmp=[i1i2(i,i) for i in lst]
	s=add(tmp[0],tmp[1])
	s=add(s,tmp[2])
	s=decompIR(s)
	
	return compIR(i1i2('sqrt('+s[1]+')'+'/sqrt('+s[0]+')', 'sqrt('+s[2]+')'))

def normform(x):
	if type(x) in [str,unicode]:
		x = compIR(decompIR(x)).replace(rad,'sqrt')
		x = compIR( i1i2(x,'1')).replace(rad,'sqrt')
	elif type(x) == tuple: 
		x = list(x)
		
	try:
		if eval(x[2]) == 0: 
			return ['1','0','0']
		if int(x[0])<0:
			x[0] = str(int(x[0])*(-1))
			x[2] = str(int(x[2])*(-1))
	except: pass

	return x

def pfractions(lstfracts_str):
	fracts = []
	
	for s in lstfracts_str:
		if type(s) in [str,unicode]: 
			s=decompIR(s)
		elif type(s)==int: 
			s=decompIR(str(s))
		elif type(s)==float:
			c=0
			while type(s)!=int:
				s*=10
				s=fseek(s)
				c+=1
			s=[str(s),'1',str(10**c)]
		return s
		fracts.append(s)
		
	#fracts=[decompIR(s) for s in lstfracts_str]
	
	denums,denoms = [fseek(float(i[2])) for i in fracts],[fseek(float(i[0])) for i in fracts]
	denom = 1
	
	for i in denoms:
		denom *= i
		
	denum = 0
	count = 0
	
	for i in denums:
		denum += i*(denom / denoms[count])
		count += 1
		
	nod = NOD(denom, denum)
	denom /= nod
	denum /= nod
	
	return compIR([str(denom),'1',str(denum)])
	
	
class determinant(list):
	def __add__(self,lst):
            return self.evalf()+lst.evalf()
        def __mul__(self,k):
		for i in range(len(self[0])):self[0][i]*=k
		return determinant(self)
        def evalf(self):
		length=len(self)
		if length==1:
			return self[0][0]
		elif length==2:
			return self[0][0]*self[1][1]-self[0][1]*self[1][0]
		elif length==3:
			return self[0][0]*self[1][1]*self[2][2]+self[2][0]*self[0][1]*self[1][2]+self[0][2]*self[1][0]*self[2][1]-(self[0][2]*self[1][1]*self[2][0]+self[2][2]*self[1][0]*self[0][1]+self[0][0]*self[1][2]*self[2][1])
		elif length>3:
			result=0
			for i in range(length):
				result+=self[0][i]*self.alg_addon(0,i).evalf()
			return result
	def minor(self,i,j):
		lst=copy.deepcopy(self)
		del lst[i]
		for x in lst:del(x[j])
		return determinant(lst)
	def alg_addon(self,i,j):
		return determinant(self.minor(i,j))*(-1)**(i+j)
def NOK(m,n):
	m*n*(NOD(m, n))
	
def multiNOK(lst):
	while len(lst)>1:
		lst=[NOK(lst[0],lst[1])]+lst[2:]
	return lst[0]

def _mul(b):
	global _n
	_n*=b
	return _n
 
def factorial(N):
	global _n
	_n = 1
	[_mul(i) for i in range(2, N+1)]
	N,_n=_n,1
	return N
