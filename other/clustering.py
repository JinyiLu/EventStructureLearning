# extract events

# agent: agent
# dobj: direct object
# iobj: indirect object
# nsubj: nominal subject
# nsubjpass: passive nominal subject
# pobj: object of a preposition?

import sys
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup

mypath = sys.argv[1]
outPath = sys.argv[2]
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

objs = ["dobj", "iobj"]
subj = ["nsubj", "nsubjpass"]
types = objs+subj

for f in onlyfiles:
    if not f.endswith(".xml"):
        continue
    fPath = join(mypath, f)
    xmldoc = BeautifulSoup(open(fPath))
    sentences = xmldoc.find_all("sentence")

    print f
    docRe = []
    for s in sentences:
        if s == None:
            continue
        dep = s.find(type="basic-dependencies")
        if dep == None:
            continue

        # print 'sentence %s' % s.get("id")

        reObjs = []
        reSubjs = []
        result = []

        for t in objs:
            for i in dep.find_all(type=t):
                reObjs.append(i)

        for t in subj:
            for i in dep.find_all(type=t):
                reSubjs.append(i)


        # for re in reObjs+reSubjs:
        #     print re.get("type"), re.governor.get_text(), re.dependent.get_text()

        # combine
        for objT in reObjs:
            governor = objT.get("idx")
            for subjT in reSubjs:
                if governor == subjT.get("idx"):
                    docRe.append([subjT.dependent.get_text(), subjT.governor.get_text(), objT.dependent.get_text()])

        # print result
    # print docRe
    outF = open(join(outPath, f), 'w')
    for i in docRe:
        outF.write(i[0]+"\t"+i[1]+"\t"+i[2]+"\n")
    outF.close()



