from copy import deepcopy

__buffer__=[]
__=lambda s:getfulleq(getcoeffs(s)) if type(s)==str else deepcopy(s)
def getcoeffs(s):
		s=s.replace("-","+-").replace("**","^").replace("*","").replace("x+","x^1+")
		l=s.split("+")
		p=[]
		for i in l:
			if i.find("x^")!=-1:
				k=i.split("^")
				if k[0][0]=="x":k[0]=1
				elif k[0].find("-x")==0:
					k[0]=-1
				if type(k[0])==str:
					k[0]=eval(k[0][:-1])
				k[1]=eval(k[1])
				p.append(k)
			else:p.append([eval(i),0])
		return p


def execf(s,x):
	result=0
	if type(s)==str:
		for i in getcoeffs(s):result+=i[0]*x**i[1]
	elif type(s)==list:
		for i in s:result+=i[0]*x**i[1]
	return result


def getfulleq(s):
	p=None
	if type(s)==str:
		p=getcoeffs(s)
	elif type(s)==list:
		p=s
	power=p[0][1]
	i=1
	while i<power:
		b,a=p[i-1][1],p[i][1]
		delta=b-a
		#print (delta)
		for k in range(1,delta):
			#print(p)
			p.insert(i,[0,a+k])
		i+=delta
	return p


def modPolynoms(s1,s2):
	#ch=[]
	s1,s2=__(s1),__(s2)
	while s1[0][1]>=s2[0][1]:
		p=s1[0][0]/float(s2[0][0])
		deltaPower=s1[0][1]-s2[0][1]
		#ch.append([p,deltaPower])
		for i in range(s2[0][1]+1):
			s1[i][0]-=p*s2[i][0]
		while (not s1[0][0]) and len(s1)>1: del s1[0]
	return s1

def divPolynoms(s1,s2):
	ch=[]
	s1,s2=__(s1),__(s2)
	while s1[0][1]>=s2[0][1]:
		p=s1[0][0]/float(s2[0][0])
		deltaPower=s1[0][1]-s2[0][1]
		ch.append([p,deltaPower])
		for i in range(s2[0][1]+1):
			s1[i][0]-=p*s2[i][0]
		while (not s1[0][0]) and len(s1)>1: del s1[0]
	return ch

def getfshtrih(s):
	return [[x[0]*x[1],x[1]-1] for x in getcoeffs(s) if x[1]!=0] if type(s)==str else [[x[0]*x[1],x[1]-1] for x in s if x[1]!=0]


def getShturm(s):
	s=__(s)
	shturm=[s,getfshtrih(s)]
	while shturm[-1][0][1]>0:
		shturm.append([[i[0]*(-1),i[1]] for i in modPolynoms(shturm[-2],shturm[-1])])
	return shturm

def getV(Shturm,x):
	result=0
	values=[]
	for i in Shturm:
		fv=execf(i,x)
		if fv:values.append(fv)
	for i in range(1,len(values)):
		if values[i-1]*values[i]<0:result+=1
	return result

nrr=lambda Shturm,Interval:getV(Shturm,Interval[0])-getV(Shturm,Interval[1])

def getStartInterval(s):
	s=__(s)
	modM=1+max([abs(i[0]/float(s[0][0])) for i in s[1:]])
	return [-modM,modM]

def getEpsilon(root):
	return 10**(-17+len(str(int(max([abs(root[0]),abs(root[1])])))))


def NyutonMethod(s,startX,epsilon=1e-17):
	s0=getfshtrih(s)
	nm=lambda f,fshtrih,sx: sx-execf(f,sx)*execf(fshtrih,sx)**(-1.0)
	xlist=[]
	while abs(execf(s,startX))>epsilon:
		startX=nm(s,s0,startX)
		if not startX in xlist:xlist.append(startX)
		else:break
	return startX

def rootsLocalise(Shturm,startInterval,nrr_count):
	start,end=startInterval
	if nrr_count:
		nrr_=nrr(Shturm,[start,end])
		if nrr_==1:
			__buffer__.append([start,end])
			nrr_count-=1
			#return roots
		elif nrr_>1:
			rootsLocalise(Shturm,[start,(start+end)/2.],nrr_count)
			rootsLocalise(Shturm,[(start+end)/2.,end],nrr_count)
	return __buffer__[-nrr(Shturm,getStartInterval(Shturm[0])):]


def ceil(x):
	def c(x):
		if abs(int(x)-x)<1e-15:return int(x)
		elif abs(int(x)-x-9e-16)-int(abs(int(x)-x+9e-16))>1:return int(abs(int(x)-x-9e-16))
		elif abs(abs(int(x)-x+9e-16)-int(abs(int(x)-x-9e-16)))>1: return -int(abs(int(x)-x+9e-16))
		else: return x
	if type(x) in [int,float]:
		x=c(x)
	elif type(x)==complex:
		real,imag=c(x.real),c(x.imag)
		x=real+imag*1j
	return x

def pnod(s1,s2):
	s1,s2=__(s1),__(s2)
	r1=modPolynoms(s1,s2)
	while s2[0][1]:
		s2,s1,r1=modPolynoms(s1,s2),s2,s1
	else:
		return []
	return s1




def solve(s):
	global __buffer__
	__buffer__=[]
	#if s[0][1]==1:return [-s[1][0]]
	sh=getShturm(s)
	sI=getStartInterval(s)
	sIshtrih=getStartInterval(sh[1])
	nrr_count=nrr(sh,sI)
	if not nrr_count:return []
	rtsI=rootsLocalise(sh,sI,nrr_count)
	roots=[]
	for i in rtsI:
		value=(i[0]+i[1])/2. if execf(sh[1],(i[0]+i[1])/2.)!=0 else i[1]-sIshtrih[1]
		#eps=10**(-19+len(str(int(value))))
		root=ceil(NyutonMethod(s,value))
		roots.append(root)
	return roots

def getRoots(s):
	s=__(s)
	roots=solve(s)
	for i in roots:
		s=divPolynoms(s,[[1,1],[-i,0]])
	if s==[[1.0,0]]:return roots
	sh=getShturm(s)
	sI=getStartInterval(s)
	startValue=(sI[0]+sI[1])/2.*1j
	nrr_complex=s[0][1]-nrr(sh,sI)
	while nrr_complex:
		sh=getShturm(s)
		sI=getStartInterval(s)
		coef=1.0
		while abs(startValue)==0 or abs(execf(sh[1],startValue))==0:
			coef+=1
			startValue=(sI[0]+sI[1]/coef)/2.*1j
		root=ceil(NyutonMethod(s,startValue))
		roots.append(root)
		root2=ceil(root.real-root.imag*1j)
		roots.append(root2)
		nrr_complex-=2
		s=divPolynoms(s,[[1,2],[-((root+root2).real),1],[(root*root2).real,0]])
	return roots
