import sys

sentences = sys.stdin.readlines()
l1 = sys.argv[2]
l2 = sys.argv[3]
l3 = sys.argv[4]
unk_file = sys.argv[5]

# count(tags), initialized with BOS
tags = {"BOS": len(sentences)}

# count(words)
word_freq = {}

# count(w_{i}, t_{i})
word_tag_freq = {}

# count(t_{i-2}, t_{i-1}, t_{i})
tag_trigram_freq = {}

# count(t_{i-1}, t_{i})
tag_bigram_freq = {}

for sentence in sentences:
    pairs = sentence.split(" ")
    prev_prev_tag = "BOS"
    prev_tag = "BOS"
    for pair in pairs:
        pair = pair.strip().split("/")
        if len(pair) != 2:
            word = '/'.join(pair[0:2])
        else:
            word = pair[0]
        tag = pair[-1]

        # count word frequencies
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1

        # count tag frequencies
        if tag in tags:
            tags[tag] += 1
        else:
            tags[tag] = 1

        # count word-tags pairs themselves
        word_tag = word + " " + tag
        if word_tag in word_tag_freq:
            word_tag_freq[word_tag] += 1
        else:
            word_tag_freq[word_tag] = 1

        tag_bigram = prev_tag + " " + tag
        if tag_bigram in tag_bigram_freq:
            tag_bigram_freq[tag_bigram] += 1
        else:
            tag_bigram_freq[tag_bigram] = 1

        tag_trigram = prev_prev_tag + " " + prev_tag + " " + tag
        if tag_trigram in tag_trigram_freq:
            tag_trigram_freq[tag_trigram] += 1
        else:
            tag_trigram_freq[tag_trigram] = 1
        prev_prev_tag = prev_tag
        prev_tag = tag

    # handle the end of sentence
    last_bigram = prev_tag + " EOS"
    if last_bigram in tag_bigram_freq:
        tag_bigram_freq[last_bigram] += 1
    else:
        tag_bigram_freq[last_bigram] = 1

    last_trigram = prev_prev_tag + prev_tag + " EOS"
    if last_trigram in tag_trigram_freq:
        tag_trigram_freq[last_trigram] += 1
    else:
        tag_trigram_freq[last_trigram] = 1

state_num = len(tags)
sym_num = len(word_freq)
init_line_num = 1
trans_line_num = len(tag_trigram_freq)
emiss_line_num = len(word_tag_freq)

print(tag_trigram_freq)



# # for each tag_trigram t_{i-1}, t_{i} of tags...
# transition_probs = {}
# for tag_trigram in tag_trigram_freq:
#     start_state = tag_trigram.split(" ")[0]
#     # find P(t_{i-1}, t_{i}) by dividing count(t_{i-1}, t_{i}) by the total #tag_trigrams that start with t_{i-1}
#     prob = tag_trigram_freq[tag_trigram] / tags[start_state]
#     transition_probs[tag_trigram] = prob

# # for each w_{i}, t{i} pair...
# emission_probs = {}
# for pair in word_tag_freq:
#     pair2 = pair.split(" ")
#     tag = pair2[1]
#     word = pair2[0]
#     # P(w_{i} | t{i}) = count(w_{i}, t_{i}) / count(t_{i})
#     prob = word_tag_freq[pair] / tags[tag]
#     emission_probs[tag + " " + word] = prob

# # TODO: change this too
# with open(sys.argv[1], "w") as m:
#     m.write("state_num=" + str(state_num) + "\n")
#     m.write("sym_num=" + str(sym_num) + "\n")
#     m.write("init_line_num=" + str(init_line_num) + "\n")
#     m.write("trans_line_num=" + str(trans_line_num) + "\n")
#     m.write("emiss_line_num=" + str(emiss_line_num) + "\n\n")
#     m.write("\init\n")
#     m.write("BOS_BOS\t"+str(init_line_num))
#     m.write("\n\n\n")
#     m.write("\\transition\n")
#
#     sorted_transitions = sorted(transition_probs)
#     for transition in sorted_transitions:
#         trans = transition.split(" ")
#         start_state = trans[0]
#         end_state = trans[1]
#
#         m.write(start_state + "\t" + end_state + "\t" + str(transition_probs[transition]) + "\n")
#
#     m.write("\n\emission\n")
#     sorted_emissions = sorted(emission_probs)
#     for transition in sorted_emissions:
#         trans = transition.split(" ")
#         tag = trans[0]
#         word = trans[1]
#
#         m.write(tag + "\t" + word + "\t" + str(emission_probs[transition]) + "\n")