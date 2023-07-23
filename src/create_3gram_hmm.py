import sys
from collections import defaultdict

l1 = float(sys.argv[2])
l2 = float(sys.argv[3])
l3 = float(sys.argv[4])
unk_file = sys.argv[5]
unk_probs = {}

with open(unk_file) as f:
    for line in f.readlines():
        pos, prob = line.split()
        unk_probs[pos] = float(prob)

sentences = sys.stdin.readlines()
tag_c = defaultdict(int) # count(tags), initialized with BOS
tag_c["BOS"] = len(sentences)
word_c = defaultdict(int) # count(words)
word_tag_c = defaultdict(int) # count(w_{i}, t_{i})
trigram_c = defaultdict(int) # count(t_1, t_2, t_3)
bigram_c = defaultdict(int) # count(t_1, t_2)

for s in sentences:
    pairs = s.split(" ")
    p_p_tag = "BOS"
    p_tag = "BOS"
    for p in pairs:
        # extract word and tag info
        p = p.strip().split("/")
        if len(p) != 2:
            word = '/'.join(p[0:2])
        else:
            word = p[0]
        tag = p[-1]
        w_t = word + " " + tag
        bigram = p_tag + " " + tag
        trigram = p_p_tag + " " + bigram

        # update counts
        word_c[word] += 1
        tag_c[tag] += 1
        word_tag_c[w_t] += 1
        bigram_c[bigram] += 1
        trigram_c[trigram] += 1
     
        # update tags 
        p_p_tag = p_tag
        p_tag = tag

    # handle end of sentence
    last_bigram = p_tag + " EOS"
    bigram_c[last_bigram] += 1

    last_trigram = p_p_tag + " " + last_bigram
    trigram_c[last_trigram] += 1

tag_sum = sum(tag_c.values())

transition_probs = {}
for trigram in trigram_c:
    t1, t2, t3 = trigram.split()
    t1t2 = t1 + " " + t2
    t2t3 = t2 + " " + t3
    if t1t2 in bigram_c: 
        p3 = trigram_c[trigram] / bigram_c[t1t2]
    # if t1 t2 unseen
    elif t3 == "BOS": 
        p3 = 0
    else: 
        p3 = 1 / (len(tag_c) + 1)
    p2 = bigram_c[t2t3]/ tag_c[t2]
    p1 = tag_c[t3] / tag_sum
    p_int = (l1 * p1) + (l2 * p2) + (l3 * p3)
    transition_probs[trigram] = p_int

emission_probs = {}
for p in word_tag_c:
    word, tag = p.split()
    prob = word_tag_c[p] / tag_c[tag]  # P(w_{i} | t{i}) = count(w_{i}, t_{i}) / count(t_{i})
    
    # smoothing 
    if tag in unk_probs:
        if word in word_c: 
            prob_smooth = prob * (1 - unk_probs[tag])
            emission_probs[tag + " " + word] = prob_smooth
        else: 
            emission_probs[tag + " " + word] = unk_probs[tag]
    else: 
         emission_probs[tag + " " + word] = prob

with open(sys.argv[1], "w") as m:
    m.write("state_num=" + str(len(bigram_c)) + "\n")
    m.write("sym_num=" + str(len(word_c)) + "\n")
    m.write("init_line_num=1\n")
    m.write("trans_line_num=" + str(len(trigram_c)) + "\n")
    m.write("emiss_line_num=" + str(len(word_tag_c)) + "\n\n")
    m.write("\init\n")
    m.write("BOS_BOS\t"+str(float(1)))
    m.write("\n\n")
    m.write("\\transition\n")

    sorted_transitions = sorted(transition_probs)
    for transition in sorted_transitions:
        t1, t2, t3 = transition.split()
        m.write(t1 + "_" + t2 + " " + t2 + "_" + t3 + " " + str(transition_probs[transition]) + "\n")

    m.write("\n\emission\n")
    sorted_emissions = sorted(emission_probs)
    for transition in sorted_emissions:
        m.write(transition + " " + str(emission_probs[transition]) + "\n")