def forwardChaining(KB, q):
    count = {}
    inferred = {}
    agenda = list(filter(lambda x: len(x[0])==0,KB))
    for i in KB:
        count[i] = len(i[0])
        for j in i[0]:
            inferred[j] = False
        inferred[i[1]] = False
    for i in agenda:
        agenda.remove(i)
        if i == q:
            return True
        if not inferred[i]:
            inferred[i] = True
            for j in filter(lambda x: i in x[0], KB):
                count[j] -= 1
                if count[j] == 0:
                    agenda.append(j[1])
    return False

