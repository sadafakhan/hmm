import sys
import sysconfig

sentences = sys.stdin.readlines()

# count(tags), initialized with BOS
tag_c = defaultdict(int)
tag_c["BOS"] = len(sentences)

# count(words)
word_c = defaultdict(int)

# count(w_{i}, t_{i})
word_tag_c = defaultdict(int)

# count(t_{i-1}, t_{i})
bigram_c = defaultdict(int)

for s in sentences:
    pairs = s.split(" ")
    p_tag = "BOS"
    for p in pairs:
        p = p.strip().split("/")
        if len(p) != 2:
            word = '/'.join(p[0:2])
        else:
            word = p[0]
        tag = p[-1]
        w_t = word + " " + tag
        bigram = p_tag + " " + tag 

        # count frequencies
        word_c[word] += 1
        tag_c[tag] += 1
        word_tag_c[w_t] += 1
        bigram_c[bigram] += 1

        # update tag
        p_tag = tag

    # handle the end of the sentence
    last_bigram = p_tag + " EOS"
    bigram_c[last_bigram] += 1

state_num = len(tag_c)
sym_num = len(word_c)
init_line_num = 1
trans_line_num = len(bigram_c)
emiss_line_num = len(word_tag_c)


# for each bigram t_{i-1}, t_{i} of tags...
transition_probs = {}
for bigram in bigram_c:
    start_state = bigram.split(" ")[0]
    # find P(t_{i-1}, t_{i}) by dividing count(t_{i-1}, t_{i}) by the total # of bigrams that start with t_{i-1}
    prob = bigram_c[bigram] / tag_c[start_state]
    transition_probs[bigram] = prob

# for each w_{i}, t{i} pair...
emission_probs = {}
for p in word_tag_c:
    pair2 = p.split(" ")
    tag = pair2[1]
    word = pair2[0]
    # P(w_{i} | t{i}) = count(w_{i}, t_{i}) / count(t_{i})
    prob = word_tag_c[p] / tag_c[tag]
    emission_probs[tag + " " + word] = prob


with open(sys.argv[1], "w") as m:
    m.write("state_num=" + str(state_num) + "\n")
    m.write("sym_num=" + str(sym_num) + "\n")
    m.write("init_line_num=" + str(init_line_num) + "\n")
    m.write("trans_line_num=" + str(trans_line_num) + "\n")
    m.write("emiss_line_num=" + str(emiss_line_num) + "\n\n")
    m.write("\init\n")
    m.write("BOS\t"+str(init_line_num))
    m.write("\n\n\n")
    m.write("\\transition\n")

    sorted_transitions = sorted(transition_probs)
    for transition in sorted_transitions:
        trans = transition.split(" ")
        start_state = trans[0]
        end_state = trans[1]

        m.write(start_state + "\t" + end_state + "\t" + str(transition_probs[transition]) + "\n")

    m.write("\n\emission\n")
    sorted_emissions = sorted(emission_probs)
    for transition in sorted_emissions:
        trans = transition.split(" ")
        tag = trans[0]
        word = trans[1]

        m.write(tag + "\t" + word + "\t" + str(emission_probs[transition]) + "\n")

