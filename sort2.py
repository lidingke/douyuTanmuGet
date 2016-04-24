# inputdata 是一个列表 列表里存了[IP,次数]

def count(inputdata):
    length = len(inputdata)
    if length==0 or length==1:
        return inputdata
    m = max(inputdata)

    ret = []
    storage = [0]*(m+1)
    for x in inputdata:
        storage[x[1]] = ret.append(x[0])
        #桶排序 O(N)时间常数
    printend = 0
    if length <10:
        print(length)
        return
    #从后往前打印空桶
    for x in range(0,length)[::-1]:
        if x:#跳过空桶
            if printend == 10:#只打印前10个
                return
            print(storage[x])
            printend +=1

count(inputdata)
