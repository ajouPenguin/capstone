class squareInfo():
    section = {}
    found = []
    direction = None
    def __init__(self, bl, br, tl, tr, cnt):
        self.section['bl'] = bl # bottom-left
        self.section['br'] = br # bottom-right
        self.section['tl'] = tl # top-left
        self.section['tr'] = tr # top-right
        self.found = cnt

class squareList():
    sqrlist = []
    def __init__(init):
        pass

    def found(self, section, val):
        if section == None:
            section = ['br','bl','tr','tl']
            for sec in section:
                for sqr in self.sqrlist:
                    if sqr.section[sec] == val:
                        return sqr, sec
        else:
            for sqr in self.sqrlist:
                if sqr.section[section] == val:
                    return sqr, section
        return None, None

    def modifyAll(self, inSqr):
        section = ['br', 'bl', 'tr', 'tl']
        for sqr in self.sqrlist:
            for sec in section:
                if sqr.section[sec] == inSqr.section[sec]:
                    sqr = inSqr
                    return

    def modifyBottomLeft(self, idx, bl):
        self.sqrlist[idx].section['bl'] = bl

    def modifyBottomRight(self, idx, br):
        self.sqrlist[idx].section['br'] = br

    def modifyTopLeft(self, idx, tl):
        self.sqrlist[idx].section['tl'] = tl

    def modifyTopRight(self, idx, tr):
        self.sqrlist[idx].section['tr'] = tr

    def modifyDirection(self, idx, di):
        self.sqrlist[idx].direction = di

    def modifyTagCount(self, idx, tagIdx, num):
        self.sqrlist[idx].found[tagIdx] = num

    def addSquare(self, bl, br, tl, tr, cnt):
        self.sqrlist.append(squareInfo(bl, br, tl, tr, cnt))
