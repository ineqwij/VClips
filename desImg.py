class Img:
    descriptor = None
    ImgID = ""
    visited = False
    set = None
    def __init__(self, des, str, set):
        self.ImgID = str
        self.descriptor = des
        self.set = set
    def getVect(self, i):
        return self.descriptor[i]
    def getDesSize(self):
        return len(self.descriptor)
    def visit(self):
        self.visited = True
    def devis(self):
        self.visited = False
    def getSet(self):
        return self.set

class Edge:
    def __init__(self, a, b, weight, c, sf):
        self.a = a
        self.b = b
        self.weight = weight
        self.conn = c
        self.sflag = sf # 0->nocycle, 1->toacycle, 2->fromacycle, 3->twocycle
    def wt(self):
        return self.weight
    def frm(self):
        return self.a
    def to(self):
        return self.b
    def __lt__(self, other):
        return self.weight < other.wt()
    def __le__(self, other):
        return self.weight <= other.wt()
    def __gt__(self, other):
        return self.weight > other.wt()
    def __ge__(self, other):
        return self.weight >= other.wt()
    def __eq__(self, other):
        return self.weight == other.wt()
    def defold(self):
        return self.conn, self.sflag
    def updateNode(self, frm, to, wt):
        self.a = frm
        self.b = to
        self.weight = wt