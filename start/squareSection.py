
class sectionInfo():
    point = {}
    def __init__(self, first, second, cnt):
        self.point = {}
        self.point['first'] = first # bottom-left
        self.point['second'] = second # bottom-right
        self.found = cnt
    def pointChange(self, point, val):
        self.point[point] = val
    def getPoints(self):
        return self.point
    def setFound(self, num):
        self.found = num
    def getFound(self):
        return self.found

class sectionList():
    def __init__(self):
        self.li = []

    def find(self, point, num):
        if point == None:
            point = ['first', 'second']
        for l in self.li:
            sec = l.getPoints()
            if type(point) is list:
                for p in point:
                    if sec[p] == num:
                        return l, p
            else:
                if sec[point] == num:
                    return l, point
        return None, None

    def modifyAll(self, inSec):
        retInSec = inSec.getPoints()
        for sec in self.li:
            retSec = sec.getPoints()
            for itr in retSec:
                if retSec[itr] == retInSec[itr]:
                    sec = inSec
                    return

    def addSection(self, first, second, cnt):
        self.li.append(sectionInfo(first, second, cnt))
