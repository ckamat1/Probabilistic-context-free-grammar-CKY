
string = ''

def buildTree(begin,end,root,back,flag='old'):
    if flag == 'new':
        global string
        string = ''
        flag = 'old'
    if root:
        children = back[begin][end][root]
        if children:
            string += "[" + root + " "
        else:
            string += root + " "
            return
        left_child_list = children[0]
        left_begin = left_child_list[0][0]
        left_end = left_child_list[0][1]

        buildTree(left_begin, left_end, left_child_list[1], back)

        right_child_list = children[1]
        if not right_child_list:
            string += "]" + " " + root
            return
        right_begin = right_child_list[0][0]
        right_end = right_child_list[0][1]


        buildTree(right_begin,right_end,right_child_list[1],back)
        string += "]" + root
        return string


def CKY(words,grammar):
    word_len = len(words)
    non_terminals = []
    for g in grammar.keys():
        if g[0] in non_terminals:
            continue
        else:
            non_terminals.append(g[0])

    score_chart = []
    back = []
    for i in range(word_len):
        inner_list = []
        inner_list_back = []
        for j in range(word_len+1):
            x={}
            y={}
            for n in non_terminals:
                x.update({n:0.0})
                y.update({n:[[],[]]})
            inner_list.append(x)
            inner_list_back.append(y)
        score_chart.append(inner_list)
        back.append(inner_list_back)

    for i in range(word_len):
        for a in non_terminals:
            if (a,words[i]) in grammar.keys():
                score_chart[i][i+1][a] = grammar[(a,words[i])]
                back[i][i+1][a] = [[(i,i+1),words[i]],[]]
                back[i][i+1].update({words[i]:None})

        added = True
        while added:
            added = False
            for a in non_terminals:
                for b in non_terminals:
                    if score_chart[i][i+1][b] > 0.0 and (a,b) in grammar.keys():
                        prob = grammar[(a,b)] * score_chart[i][i+1][b]
                        if prob > score_chart[i][i+1][a]:
                            score_chart[i][i+1][a] = prob
                            back[i][i+1][a] = [[(i,i+1),b],[]]
                            added = True

    # print score_chart[3][4]['V']
    for span in range(1,word_len):
        diff = word_len - span
        for begin in range(diff):
            end = begin + span + 1
            split = begin + 1
            # End = end - 1
            for Split in range(split, end):
                for a in non_terminals:
                    for b in non_terminals:
                        for c in non_terminals:
                            if (a,b,c) in grammar.keys():
                                prob = score_chart[begin][Split][b] * score_chart[Split][end][c] * grammar[(a,b,c)]
                                if prob > score_chart[begin][end][a]:
                                    score_chart[begin][end][a] = prob
                                    back[begin][end][a] = [[(begin,Split),b],[(Split,end),c]]

                # handle unaries
                added = True
                while added:
                    added = False
                    for a in non_terminals:
                        for b in non_terminals:
                            # prob = P(A->B)*score[begin][end][B]
                            if (a,b) in grammar.keys() and score_chart[begin][end][b] > 0.0:
                                prob = score_chart[begin][end][b] * grammar[(a,b)]
                                if (prob > score_chart[begin][end][a]):
                                    score_chart[begin][end][a] = prob
                                    back[begin][end][a] = [[(begin,end),b],[]]
                                    added = True


    if score_chart[0][word_len]['S'] != 0.0:
        s =  buildTree(begin=0,end=word_len,root='S',back=back,flag='new')
    else:
        s = "Sentence Doesn't exist!"
    return (score_chart[0][word_len]['S'],s)

grammar = {
    ('S','NP','VP'):0.9,
    ('S','VP'):0.1,
    ('VP','V','NP'):0.5,
    ('VP','V'):0.1,
    ('VP','V','@VP_V'):0.3,
    ('VP','V','PP'):0.1,
    ('@VP_V','NP','PP'):1.0,
    ('NP','NP','NP'):0.1,
    ('NP','NP','PP'):0.2,
    ('NP','N'):0.7,
    ('PP','P','NP'):1.0,
    ('N','people'):0.5,
    ('N','fish'):0.2,
    ('N','tanks'):0.2,
    ('N','rods'):0.1,
    ('V','people'):0.1,
    ('V','fish'):0.6,
    ('V','tanks'):0.3,
    ('P','with'):1.0
}


print CKY(['fish','people','fish','tanks'], grammar)
print CKY(['people','with','fish','rods','fish','people'], grammar)
print CKY(['fish','with','fish','fish'], grammar)
print CKY(['fish','with','tanks','people','fish'], grammar)
print CKY(['fish','people','with','tanks','fish','people','with','tanks'], grammar)
print CKY(['fish','fish','fish','fish','fish'], grammar)
print CKY(['rods','rods','rods','rods'], grammar)
