import sys
import re

with open(sys.argv[1], "r") as f:
    unformat_hmm = f.readlines()

asserted_num_states = int(re.sub(".*\=","",unformat_hmm[0]))
asserted_sym_num = int(re.sub(".*\=","",unformat_hmm[1]))
asserted_init_line_num = int(re.sub(".*\=","",unformat_hmm[2]))
asserted_trans_line_num = int(re.sub(".*\=","",unformat_hmm[3]))
asserted_emiss_line_num = int(re.sub(".*\=","",unformat_hmm[4]))

unformat_hmm = unformat_hmm[6:]

three = []
i = 0
j_holder = 0
for j in range(0, len(unformat_hmm)):
    if unformat_hmm[j].startswith("\\"):
        if j == 0:
            pass
        else:
            section = unformat_hmm[i:j]
            three.append(section)
            i = j
            j_holder = j

last_section = unformat_hmm[j_holder:len(unformat_hmm)]
three.append(last_section)

init_old = three[0]
trans_old = three[1]
emiss = three[2]

init_new = []
for item in init_old:
    if item == "\n" or item == "\t\n":
        pass
    else:
        item = item.strip()
        init_new.append(item)

trans_new = []
for item in trans_old:
    if item == "\n" or item == "\t\n":
        pass
    else:
        item = item.strip()
        trans_new.append(item)

actual_states = set()
trans_probs = {}
for line in trans_new[1:]:
    line = line.split("\t")
    if len(line) == 1:
        line = line[0].split()
    if len(line) == 0:
        pass
    else:
        start = line[0]
        end = line[1]
        prob = float(line[2])
        actual_states.add(start)
        actual_states.add(end)
        if start in trans_probs:
            trans_probs[start] += prob
        else:
            trans_probs[start] = prob

actual_words = set()
emiss_probs = {}
for line in emiss[1:]:
    line = line.split("\t")
    prob = float(line[2].strip())
    state = line[0]
    word = line[1]
    prob = float(line[2].strip())
    if state in emiss_probs:
        emiss_probs[state] += prob
    else:
        emiss_probs[state] = prob
    actual_words.add(word)

actual_num_states = len(actual_states) - 1
actual_sym_num = len(actual_words)
actual_init_line_num = len(init_new) - 1
actual_trans_line_num = len(trans_new) - 1
actual_emiss_line_num = len(emiss) - 1


if actual_num_states != asserted_num_states:
    print("warning: different numbers of states: claimed=" + str(asserted_num_states) + ", real=" + str(actual_num_states))
else:
    print("state_num="+str(actual_num_states))

if actual_sym_num != asserted_sym_num:
    print("warning: different numbers of symbols: claimed=" + str(asserted_sym_num) + ", real=" + str(actual_sym_num))
else:
    print("sym_num=" + str(actual_sym_num))

if actual_init_line_num != asserted_init_line_num:
    print("warning: different numbers of init_line_num: claimed=" + str(asserted_init_line_num)
          + ", real=" + str(actual_init_line_num))
else:
    print("init_line_num=" + str(actual_init_line_num))

if actual_trans_line_num != asserted_trans_line_num:
    print("warning: different numbers of trans_line_num: claimed=" + str(asserted_trans_line_num)
          + ", real=" + str(actual_trans_line_num))
else:
    print("trans_line_num=" + str(actual_trans_line_num))

if actual_emiss_line_num != asserted_emiss_line_num:
    print("warning: different numbers of emiss_line_num: claimed=" + str(asserted_emiss_line_num)
          + ", real=" + str(actual_emiss_line_num))
else:
    print("emiss_line_num=" + str(actual_emiss_line_num))

for state in trans_probs:
    if trans_probs[state] != 1.0:
        print("warning: the trans_prob_sum for state "+ state + " is " + str(trans_probs[state]))

for state in emiss_probs:
    if emiss_probs[state] != 1.0:
        print("warning: the emiss_prob_sum for state " + state + " is " + str(emiss_probs[state]))