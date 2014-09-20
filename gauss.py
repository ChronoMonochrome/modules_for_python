from mymath import NOD

def NOK(m,n):
	return m * n / NOD(m, n)

def multiNOK(lst):
	while len(lst)>1:
		lst=[NOK(lst[0],lst[1])]+lst[2:]
	return lst[0]

def method_gauss(llst):
	k=1
	count=l=len(llst)
	while count>1:
		main_index=l-count
		main_nok=multiNOK([abs(i) for i in llst[main_index] if i!=0])
		for j in range(count-1):
			try:tmp=main_nok/llst[main_index][j+main_index+1]
			except: tmp=main_nok
			if not NOD(main_nok, llst[main_index][j+main_index+1]) in [0,1]:
				dopoln_mn=tmp
			else: dopoln_mn=main_nok
			for i in range(l):
				llst[i][j+main_index+1]*=dopoln_mn
			dopoln_mn2=llst[main_index][j+main_index+1]/llst[main_index][main_index]
			for i in range(l):
				llst[i][j+main_index+1]-=llst[i][main_index]*dopoln_mn2
			k*=dopoln_mn
			#print(dopoln_mn2)
		count-=1
	return llst,k
#print(method_gauss([[2,2,1],[5,1,2],[7,9,4]]))
