class newSquare():
    def __init__(bl, br, tl, tr, idx, dir, cnt, labelNum):
        section['bl'] = bl # bottom-left
        section['br'] = br # bottom-right
        section['tl'] = tl # top-left
        section['tr'] = tr # top-right
        found = []
        direction = dir
        for i in range(labelNum):
            found.append(cnt)

class squareList():
    def __init__():
        sqrlist = []

    def found(section, val):
        for sqr in sqrlist:
            if sqr.section[section] == val:
                return sqr
        return None

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

    def modifyDirection(idx, dir):
        sqrlist[idx].direction = dir

    def modifyTagCount(idx, tagIdx, num):
        sqrlist[idx].found[tagIdx] = num

    def addSquare(idx, bl, br, tl, tr, dir, cnt, labelNum):
        sqrlist[idx] = newSquare(bl, br, tl, tr, dir, cnt, labelNum)
