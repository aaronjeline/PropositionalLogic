class Agenda:
    items = None
    def __init__(self, items, key=lambda x:x):
        self.items = list(map(key, items))
    def __iter__(self):
        return self
    def __next__(self):
        try:
            return self.items.pop()
        except IndexError:
            raise StopIteration
    def add(self, item):
        self.items.append(item)


def forwardChaining(KB, q):
    count = {}
    inferred = {}
    agenda = Agenda(filter(lambda x: len(x[0])==0,KB), key=lambda x:x[1])
    for i in KB:
        count[i] = len(i[0])
        for j in i[0]:
            inferred[j] = False
        inferred[i[1]] = False
    for i in agenda:
        if i == q:
            return True
        if not inferred[i]:
            inferred[i] = True
            for j in filter(lambda x: i in x[0], KB):
                count[j] -= 1
                if count[j] == 0:
                    agenda.add(j[1])
    return False

