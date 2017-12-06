class squareInfo():
    section = {}
    found = []
    direction = None
    def __init__(bl, br, tl, tr, idx, di, cnt, labelNum):
        section['bl'] = bl # bottom-left
        section['br'] = br # bottom-right
        section['tl'] = tl # top-left
        section['tr'] = tr # top-right
        found = []
        direction = di
        for i in range(labelNum):
            found.append(cnt)

class squareList():
    sqrlist = []
    def __init__(init):
        pass

    def found(section, val):
        if section == None:
            section = ['br','bl','tr','tl']
            for sec in sections:
                for sqr in sqrlist:
                    if sqr.section[section] == val:
                        return sqr, section
        else:
            for sqr in sqrlist:
                if sqr.section[section] == val:
                    return sqr, section
        return None, None

    def modifyAll(inSqr):
        for sqr in sqrlist:
            if sqr.index == inSqr.index:
                sqr = inSqr

    def modifyBottomLeft(idx, bl):
        sqrlist[idx].section['bl'] = bl

    def modifyBottomRight(idx, br):
        sqrlist[idx].section['br'] = br

    def modifyTopLeft(idx, tl):
        sqrlist[idx].section['tl'] = tl

    def modifyTopRight(idx, tr):
        sqrlist[idx].section['tr'] = tr

    def modifyDirection(idx, di):
        sqrlist[idx].direction = di

    def modifyTagCount(idx, tagIdx, num):
        sqrlist[idx].found[tagIdx] = num

    def addSquare(bl, br, tl, tr, di, cnt, labelNum):
        sqrlist.append(squareInfo(bl, br, tl, tr, di, cnt, labelNum))

