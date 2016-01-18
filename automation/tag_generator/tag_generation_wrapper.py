import random
import sys
import math 
from collections import defaultdict
from wtforms import validators

company_name = " "


if company_name is None:
    raise validators.ValidationError('Company does not exist! Please create a company first.')


def readCorpus(f):
    if os.path.isfile(f):
        file = open(f,"r")

    len(names.split(" "))

def readFolio(f):
    if os.path.isfile(f):
        file = open(f, "r") 
        i = 0 
        corpus = [] 
        print "Reading file ", f
        for line in file:
            i += 1
            sentence = line.split() 
	    corpus.append(sentence)
            if i % 1000 == 0:
                sys.stderr.write("Reading sentence " + str(i) + "\n")
        return corpus
    else:
        print "Error: corpus file ", f, " does not exist"
        sys.exit()
def preprocess(corpus):
    freqDict = defaultdict(int)
    for sen in corpus:
	for word in sen:
	    freqDict[word] += 1
    for sen in corpus:
	for i in range(0, len(sen)):
	    word = sen[i]
	    if freqDict[word] < 2:
		sen[i] = UNK
    for sen in corpus:
	sen.insert(0, start)
	sen.append(end)

    return corpus

def preprocessTest(vocab, corpus):
    #replace test words that were unseen in the training with unk
    for sen in corpus:
	for i in range(0, len(sen)):
	    word = sen[i]
	    if word not in vocab:
		sen[i] = UNK
	    #endif
	#endfor
    #endfor
    
    #bookend the sentences with start and end tokens
    for sen in corpus:
	sen.insert(0, start)
	sen.append(end)
    #endfor

    return corpus
#enddef

# Constants 
UNK = "UNK"     # Unknown word token
start = "<s>"   # Start-of-sentence token
end = "</s>"    # End-of-sentence-token


#--------------------------------------------------------------
# Language models and data structures
#--------------------------------------------------------------

# Parent class for the three language models you need to implement
class LanguageModel:
    # Initialize and train the model (ie, estimate the model's underlying probability
    # distribution from the training corpus)
    def __init__(self, corpus):
        print """Your task is to implement three kinds of n-gram language models:
      a) an (unsmoothed) unigram model (UnigramModel)
      b) a unigram model smoothed using Laplace smoothing (SmoothedUnigramModel)
      c) an unsmoothed bigram model (BigramModel)
      d) a bigram model smoothed using absolute discounting (SmoothedBigramModel)
      """
    #enddef

    # Generate a sentence by drawing words according to the 
    # model's probability distribution
    # Note: think about how to set the length of the sentence 
    #in a principled way
    def generateSentence(self):
        print "Implement the generateSentence method in each subclass"
        return "mary had a little lamb ."
    #enddef

    # Given a sentence (sen), return the probability of 
    # that sentence under the model
    def getSentenceProbability(self, sen):
        print "Implement the getSentenceProbability method in each subclass"
        return 0.0
    #enddef

    # Given a corpus, calculate and return its perplexity 
    #(normalized inverse log probability)
    def getCorpusPerplexity(self, corpus):
        print "Implement the getCorpusPerplexity method"
        return 0.0
    #enddef

    # Given a file (filename) and the number of sentences, generate a list
    # of sentences and write each to file along with its model probability.
    # Note: you shouldn't need to change this method
    def generateSentencesToFile(self, numberOfSentences, filename):
        file=open(filename, 'w+')
        for i in range(0,numberOfSentences):
            sen = self.generateSentence()
            prob = self.getSentenceProbability(sen)
            print >>file, prob, " ", sen
	#endfor
    #enddef
#endclass

# Unigram language model
class UnigramModel(LanguageModel):
    def __init__(self, corpus):
        self.counts = defaultdict(float)
        self.sentence = 0.0 
        self.total = 0.0
        self.train(corpus) 
        self.sentenceProbability = 0.0 
        self.CorpusPerplexity = 0.0
        self.ungiram_corpus = corpus 
        self.sentence = generateSentence(self) 
        print "Subtask: implement the unsmoothed unigram language model"
    #endddef
    def train(self, corpus):
        for sentence in corpus: 
            self.sentence += 1.0
            self.total +=1.0
        #endfor
    #enddef
    def prob(self,sentence): 
        return self.counts[sentence]/self.total
    def draw(self): 
        rand = random.random()
        for word in self.counts.keys():
            rand -= self.prob(word)
            if rand <= 0.0:
                return word
    def generateSentence(self):
        if (start == True): 
            sentence = [] 
            temporary_variable = draw() 
            while (temporary_variable != end):
                sentence.append(temporary_variable)
                temporary_variable = draw() 
            return sentence
        else: 
            return  
    def getSentenceProbability(self,sen):
        unigram_model = self.unigram_corpus    
        sentenceProbability = 0.0 
        for i in range(0,len(unigram_model)):
            if (start == True): 
                temporary_sentence = draw() 
                if (self.generateSentence() == temporary_sentence):
                    sentenceProbability +=1.0 
        return sentenceProbability

    def getCorpusPerplexity(self,corpus):
        overall_probability = 0.0 
        for sentence in corpus: 
            for word in sentence:   
                if word == start: 
                    while (word != end): 
                        overall_probability += self.prob(word)
                if word == end: 
                    overall_probability = math.log10(overall_probability)
                    return (math.exp(-overall_probability/len(word)))  
        return 
    def generateSentenceToFile(self,numberOfSentences,filename):
        file = open(filename,'w+')
        for i in range(0, numberOfSentences):
            sen = self.generateSentence()
            prob = self.getSentenceProbability(sen)
            print >> file, prob, " ", sen
    #endfor
    #enddef
#endclass

#Smoothed unigram language model (use laplace for smoothing)
class SmoothedUnigramModel(LanguageModel):
    def __init__(self, corpus):
        self.counts = defaultdict(float)
        self.sentence = 0.0 
        self.total = 0.0
        self.train(corpus) 
        self.sentenceProbability = 0.0 
        self.CorpusPerplexity = 0.0 
    def train(self,corpus):
        for sentence in corpus: 
            self.sentence += 1.0 
            self.total += 1.0
    def prob(self,sentence):
        return self.counts[sentence]/self.total
    def generateSentence(self):
        if (start == True): 
            sentence = [] 
            temporary_variable = draw() 
            while (temporary_variable != end):
                sentence.append(temporary_variable)
                temporary_variable = draw() 
            return sentence
        else: 
            return  
    def getSentenceProbability(self,sentence):
        for i in range(1,len(sen)):
            self.sentenceProbability += sen[self.counts[sentence]+1/self.total] 
            return self.sentenceProbability
    def getCorpusPerplexity(self,corpus):
        overall_probability = 0.0 
        for sentence in corpus: 
            for word in sentence: 
                if word == start: 
                    while (word != end): 
                        overall_probability += self.prob(self,corpus[word])
                if word == end: 
                    overall_probability = math.log10(overall_probability)
                    return (math.exp(-overall_probability/len(word)))  
        return 
    def generateSentenceToFile(self,numberOfSentences,filename): 
        file = open(filename,'w+')
        for i in range(0, numberOfSentences):
            sen = self.generateSentence()
            prob = self.getSentenceProbability(sen)
            print >> file, prob, " ", sen
	print "Subtask: implement the smoothed unigram language model"
    #endddef
#endclass

# Unsmoothed bigram language model
class BigramModel(LanguageModel):
    def __init__(self, corpus):
        print "Subtask: implement the unsmoothed bigram language model"
    #endddef
#endclass

# Smoothed bigram language model (use absolute discounting for smoothing)
class SmoothedBigramModel(LanguageModel):
    def __init__(self, corpus):
        print "Subtask: implement the smoothed bigram language model"
    #endddef
#endclass


# Sample class for a unsmoothed unigram probability distribution
# Note: 
#       Feel free to use/re-use/modify this class as necessary for your 
#       own code (e.g. converting to log probabilities after training). 
#       This class is intended to help you get started
#       with your implementation of the language models above.
class UnigramDist:
    def __init__(self, corpus):
        self.counts = defaultdict(float)
        self.total = 0.0
        self.train(corpus)
    #endddef

    # Add observed counts from corpus to the distribution
    def train(self, corpus):
        for sen in corpus:
            for word in sen:
                self.counts[word] += 1.0
                self.total += 1.0
            #endfor
        #endfor
    #enddef

    # Returns the probability of word in the distribution
    def prob(self, word):
        return self.counts[word]/self.total
    #enddef

    # Generate a single random word according to the distribution
    def draw(self):
        rand = random.random()
        for word in self.counts.keys():
            rand -= self.prob(word)
            if rand <= 0.0:
                return word
	    #endif
	#endfor
    #enddef
#endclass
#-------------------------------------------
# The main routine
#-------------------------------------------
if __name__ == "__main__":
    #read your corpora
    trainCorpus = readFolio('train.txt')
    trainCorpus = preprocess(trainCorpus)
    posTestCorpus = readFolio('pos_test.txt')
    negTestCorpus = readFolio('neg_test.txt')
    vocab = set()
    print """Task 0: create a vocabulary 
(collection of word types) for the train corpus"""
    posTestCorpus = preprocessTest(vocab, posTestCorpus)
    negTestCorpus = preprocessTest(vocab, negTestCorpus)

    # Run sample unigram dist code
    unigramDist = UnigramDist(trainCorpus)
    print "Sample UnigramDist output:"
    print "Probability of \"vader\": ", unigramDist.prob("vader")
    print "Probability of \""+UNK+"\": ", unigramDist.prob(UNK)
    print "\"Random\" draw: ", unigramDist.draw()
    # Sample test run for unigram model
    unigram = UnigramModel(trainCorpus)
    # Task 1   (*** remember to generate 20 sentences for final output ***)
    unigram.generateSentencesToFile(1, "unigram_output.txt")
    # Task 2
    posTestCorpus = readFolio('pos_test.txt')
    negTestCorpus = readFolio('neg_test.txt')
    trainPerp = unigram.getCorpusPerplexity(trainCorpus)
    posPerp = unigram.getCorpusPerplexity(posTestCorpus)
    negPerp = unigram.getCorpusPerplexity(negTestCorpus)   
    print "Perplexity of positive training corpus:    "+ str(trainPerp) 
    print "Perplexity of positive review test corpus: "+ str(posPerp)
    print "Perplexity of negative review test corpus: "+ str(negPerp)
    
    ## Fill in the functionality for SmoothedUnigramModel, BigramModel and SmoothedBigramModel, as well
    smoothUnigram = SmoothedUnigramModel(trainCorpus)
    bigram = BigramModel(trainCorpus)
    smoothBigram = SmoothedBigramModel(trainCorpus)

