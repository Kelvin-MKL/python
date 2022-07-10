Tom = [['9:00','10:30'],['12:00','13:00'],['16:00','18:00']]
TomBoundary = ['8:15','20:00']
Peter = [['10:00','11:30'],['12:30','14:30'],['14:30','15:00'],['16:00','17:00']]
PeterBoundary = ['10:00','18:30']
duration = 30

def conVerToInt(list):
    newlist = []
    for i in list:
        Hour, Mini = i[0].split(':')
        Hour2, Mini2 = i[1].split(':')

        #Hour, Time = i.split(':')
        newlist.append([int(Hour)*60 + int(Mini), int(Hour2)*60 + int(Mini2)])
    return newlist

def findBoundary(Boundary):
    Hour, Mini = Boundary[0].split(':')
    Hour1, Mini1 = Boundary[1].split(':')
    return [int(Hour)*60 + int(Mini), int(Hour1)*60 + int(Mini1)]

def findAvaiTime(Tom,Peter):
    nonAvai = sorted(conVerToInt(Tom) + conVerToInt(Peter))
    #print(nonAvai)

    avaiTime = []
    Tomb = findBoundary(TomBoundary)
    Peterb = findBoundary(PeterBoundary)
    Finalb = [min(Tomb+Peterb), max(Tomb+Peterb)]

    #print(Finalb)
    for i in range(len(nonAvai)-1):
        if i == 0: #compare min time
            period = comPareTime(  Finalb[0],nonAvai[i][0])
            avaiTime.append(period)

                #avaiTime.append([time1,time2])
        #print(nonAvai[i])
        period = comPareTime( nonAvai[i][1],nonAvai[i+1][0],) #avaiTime in collaped schedule
        avaiTime.append(period)

        if i == len(nonAvai)-2: #compare max time
            period = comPareTime( nonAvai[i+1][1],Finalb[1])
            #print(period)
            avaiTime.append(period)

    RealAvaiTime = [i for i in avaiTime if i != None]
    return RealAvaiTime


            #avaiTime.append([time1, time2])
            #print(avaiTime)
            #avaiTime.append([nonAvai[i][1]/60, nonAvai[i+1][0]/60])
            #print(avaiTime)
def comPareTime(timee1, timee2):
    if timee2 - timee1 >= 30:
        a = timee2 // 60
        b = timee2 % 60
        c = timee1 // 60
        d = timee1 % 60
        if b == 0:
            b = "00"
        if d == 0:
            d = "00"

        time1 = str(a) + ":" + str(b)
        time2 = str(c) + ":" + str(d)
        #print(time1,time2)
        return [time2,time1]
    else:
        return None

print(findAvaiTime(Tom,Peter))
