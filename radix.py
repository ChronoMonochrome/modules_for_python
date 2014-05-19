_nmap= {0 : '0', 1 : '1', 2 : '2', 3 : '3', 4 : '4', 5 : '5', 6 : '6', 7 : '7', 8 : '8', 9 : '9', 10 : 'A', 11 : 'B', 12 : 'C', 13 : 'D', 14 : 'E', 15 : 'F'}
_mapn={'0' : 0, '1' : 1, '2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9, 'A' : 10, 'B' : 11, 'C' : 12, 'D' : 13, 'E' : 14, 'F' : 15}

def from10(x, SI, map = []):
    map=[str(i) for i in map]
    if SI==1:
        return str(['I' for i in range(x)])[1:-1].replace(', ','').replace('\'','')
    global _nmap
    d=''
    def placere(st):
        def asm(d):
            st=''
            for i in d: st+=i 
            return st
        if map==[] or len(map) != SI : 
            if type(st)==list: return asm(st)
            elif type(st)==str: return st
            else: raise('type of argument must be is str or list')
        stdchrrange=[str(i) for i in range(SI)]+[chr(i+65) for i in range(SI-10)]
        try:st=[map[stdchrrange.index(i)] for i in st]
        finally:return asm(st)
    if SI <= 16 and map==[]: 
        while x > 0 : 
            d = _nmap[(x % SI)] + d
            x /= SI;x=int(x)
        pass
    else : 
        d=[]
        while x > 0 : 
            ost = (x % SI)
            if ost > 9 : 
                if map==[]:
                    ost = chr((ost + 55))
                else:
                    ost = map[ost]
            else : 
                ost = str(ost)
            d.insert(0,ost)
            x /= SI;x=int(x)
        return placere(d)
    return d



def to10(x, fromSI, map=[]):
    if fromSI==1:
        return len(x)
    global _mapn
    if type(x) is int: return x
    s=str(x)
    map=[str(i) for i in map]
    def placere(stroke):
        if map==[] or len(map) != fromSI : 
            raise('error: SI!=len(map) or map==[]')
        n,count=[],0
        for i in stroke:
            n.append(i)
            count+=1
        return n
    r, count=0, len(s)-1
    if map!=[]:
        s=placere(s)
        r, count=0, len(s)-1
        #print s,map
        for i in s:
         r+=map.index(i)*(fromSI**count)
         #print i,'in count='+str(count)
         count-=1
    else:
        for i in s:
            number=ord(i)-55
            if i.isdigit(): number+=7
            r+=number*(fromSI**count)
            count-=1
    return r
