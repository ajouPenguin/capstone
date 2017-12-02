from multiprocessing import Pool, Process, Manager

def fp(name, numList=None, what='no'):
    print ('hello %s %s' % (name, what))
    numList.append(name+'44')

if __name__ == '__main__':

    manager = Manager()

    numList = manager.list()
    for i in range(10):
        keywords = {'what': 'yes', 'numList': numList}
        p = Process(target=fp, args=['bob'+str(i)], kwargs=keywords)
        p.start()
        print("Start done")
        p.join()
        print("Join done")
    print (numList)