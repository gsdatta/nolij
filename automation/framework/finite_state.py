from fst import *
AZ = set("abcdefghijklmnopqrstuvwxyz")
VOWS = set("aeiou")
CONS = set("bcdfghjklmnprstvwxz")
E = set("E")
def buildFST():
    print "Your task is to implement a better FST in the buildFST() function, using the methods described here"
    print "You may define additional methods in this module (hw1_fst.py) as desired"
    f = FST("q0") # q0 is the initial (non-accepting) state
    f.addState("q1") # a non-accepting state
    f.addState("q_ing") # a non-accepting state
    f.addState("q_EOW", True) # an accepting state (you shouldn't need any additional accepting states)
    f.addSetTransition("q0", AZ, "q1")
    f.addSetTransition("q1", AZ-E, "q0")   
    f.addSetTransition("q1", AZ, "q_ing")
    f.addTransition("q_ing", "", "ing", "q_EOW")
    return f
if __name__ == "__main__":
    if len(sys.argv) < 2:
	print "This script must be given the name of a file containing verbs as an argument"
	quit()
    else:
        file = sys.argv[1]
    f = buildFST()
    f.parseInputFile(file)
