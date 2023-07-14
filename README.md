# hmm
```hmm``` takes annotated training data and creates an HMM for a bigram and trigram POS tagger, as well as checks input HMMs for validity. 

```create_2gram_hmm.sh```: Program that creates a Hidden Markov Model for a bigram POS tagger.

Args: 
* training_data: The training data is of the format “w1/t1 .... wn/tn” (cf. wsj sec0.word pos)

Returns: 
* output_hmm: a file that represents an HMM. Header relays basic data about HMM, followed by delineation of initial state, transition, and emission probabilities. 

To run: 
```
cat training_data | create_2gram_hmm.sh output_hmm
```

```create_3gram_hmm.sh```: Program that creates a Hidden Markov Model for a trigram POS tagger.

Args: 
* training_data: The training data is of the format “w1/t1 .... wn/tn” (cf. wsj sec0.word pos)
* unk_prob_file: The file’s format is “tag prob” (see unk prob sec22). prob is P (< unk >| tag). They are used to smooth P(word|tag). 
* l1: lambda_1 for interpolation. 
* l2: lambda_2 for interpolation
* l3: lambda_3 for interpolation

Returns: 
* output_hmm: a file that represents an HMM. Header relays basic data about HMM, followed by delineation of initial state, transition, and emission probabilities. 

To run: 
```
cat training_data | create_3gram_hmm.sh output_hmm l1 l2 l3 unk_prob_file

```

```check_hmm.sh```: Reads in a state-emission HMM file, checks its format, and outputs a warning file if there are errors or discrepancies in the file. 

Args: 
* input_hmm: a file that represents an HMM. Header relays basic data about HMM, followed by delineation of initial state, transition, and emission probabilities.

Returns: 
* warning_file: a file that contains any warnings about the HMM's validity (cf. hmm ex1.warning). 

To run: 
```
check_hmm.sh input_hmm > output/warning_file
```

HW7 OF LING570 (11/18/2021)