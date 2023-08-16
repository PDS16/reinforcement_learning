import optparse
import numpy as np


#-----------------------INCLUDING COMMAND-LINE OPTIONS----------------------------

parser = optparse.OptionParser()

parser.add_option('--states', dest = 'states_file_name',
                  type = 'string')
parser.add_option('--parameters', dest = 'p1_parameters',
                  type = 'string')
parser.add_option("--q",
                  dest = "p2_parameters", type = 'string')
(options, args) = parser.parse_args()
if (options.states_file_name == None or options.p1_parameters == None or options.p2_parameters == None):
    print ("Invalid Usage")
    exit(0)

states_file = options.states_file_name
p1_file = options.p1_parameters
q = options.p2_parameters
q = float(q)


#-------------------------------READING STATEFILE--------------------------

file1 = open(states_file,'r')
contents_states = file1.readlines()
contents_states = list(map(int, contents_states))

#-------------------------------READ P1 PARAMETERS------------------------


file2 = open(p1_file,'r')
contents_p1 = file2.readlines()
p1_parameters = np.zeros((5,7))
for i in range(5) :
    for j in range(7) :
        p1_parameters[i,j] = contents_p1[i+1].split()[j+1]
        
# print(p1_parameters)


#------------------------------ENCODING-----------------------------------

runs = contents_states[0]//100
balls = contents_states[0]%100
numStates = 2*len(contents_states)+2
print("numStates " + str(numStates))
print("numActions 5")
print("end " + str(2*len(contents_states)) + " " + str(2*len(contents_states)+1))


contents_states.extend([a + 10000 for a in contents_states ])
contents_states.append(1)
contents_states.append(0)
transition = np.zeros((contents_states[0]+10001,5,contents_states[0]+10001))


for k in range(5) :
    for i in contents_states[:runs*balls] :
        transition[i][k][1] += p1_parameters[k][0]
        if (i//100)%6 == 1 :
            if i-100 in contents_states[:-2] : transition[i][k][i-100+10000] = p1_parameters[k,1]
            elif i-100 < 40 and i-100 > 0 : transition[i][k][1] += p1_parameters[k,1]
            else : transition[i][k][0] += p1_parameters[k,1]
            if i-101 in contents_states[:-2] : transition[i][k][i-101] = p1_parameters[k,2]
            elif i-101 < 40 and i-101 > 0 : transition[i][k][1] += p1_parameters[k,2]
            else : transition[i][k][0] += p1_parameters[k,2]
            if i-102 in contents_states[:-2] : transition[i][k][i-102+10000] = p1_parameters[k,3]
            elif i-102 < 40 and i-102 > 0 : transition[i][k][1] += p1_parameters[k,3]
            else : transition[i][k][0] += p1_parameters[k,3]
            if i-103 in contents_states[:-2] : transition[i][k][i-103] = p1_parameters[k,4]
            elif i-103 < 40 and i-103 > 0 : transition[i][k][1] += p1_parameters[k,4]
            else : transition[i][k][0] += p1_parameters[k,4]
            if i-104 in contents_states[:-2] : transition[i][k][i-104+10000] = p1_parameters[k,5]
            elif i-104 < 40 and i-104 > 0 : transition[i][k][1] += p1_parameters[k,5]
            else : transition[i][k][0] += p1_parameters[k,5]
            if i-106 in contents_states[:-2] : transition[i][k][i-106+10000] = p1_parameters[k,6]
            elif i-106 < 40 and i-106 > 0 : transition[i][k][1] += p1_parameters[k,6]
            else : transition[i][k][0] += p1_parameters[k,6]
        else : 
            if i-100 in contents_states[:-2] : transition[i][k][i-100] = p1_parameters[k,1]
            elif i-100 < 40 and i-100 > 0 : transition[i][k][1] += p1_parameters[k,1]
            else : transition[i][k][0] += p1_parameters[k,1]
            if i-101 in contents_states[:-2] : transition[i][k][i-101+10000] = p1_parameters[k,2]
            elif i-101 < 40 and i-101 > 0 : transition[i][k][1] += p1_parameters[k,2]
            else : transition[i][k][0] += p1_parameters[k,2]
            if i-102 in contents_states[:-2] : transition[i][k][i-102] = p1_parameters[k,3]
            elif i-102 < 40 and i-102 > 0 : transition[i][k][1] += p1_parameters[k,3]
            else : transition[i][k][0] += p1_parameters[k,3]
            if i-103 in contents_states[:-2] : transition[i][k][i-103+10000] = p1_parameters[k,4]
            elif i-103 < 40 and i-103 > 0 : transition[i][k][1] += p1_parameters[k,4]
            else : transition[i][k][0] += p1_parameters[k,4]
            if i-104 in contents_states[:-2] : transition[i][k][i-104] = p1_parameters[k,5]
            elif i-104 < 40 and i-104 > 0 : transition[i][k][1] += p1_parameters[k,5]
            else : transition[i][k][0] += p1_parameters[k,5]
            if i-106 in contents_states[:-2] : transition[i][k][i-106] = p1_parameters[k,6]
            elif i-106 < 40 and i-106 > 0 : transition[i][k][1] += p1_parameters[k,6]
            else : transition[i][k][0] += p1_parameters[k,6]
 
for k in range(5) :       
    for i in contents_states[runs*balls:2*runs*balls] :
        transition[i][k][1] += q
        if ((i-10000)//100)%6 == 1 :
            
            if i-100 in contents_states : transition[i][k][i-100-10000] = (1-q)/2
            elif i-100-10000 < 100 and i-100-10000 > 0 : transition[i][k][1] += (1-q)/2
            else : transition[i][k][0] += (1-q)/2
            if i-101 in contents_states : transition[i][k][i-101] = (1-q)/2
            elif i-101-10000 < 100 and i-101-10000 > 0 : transition[i][k][1] += (1-q)/2
            else : transition[i][k][0] += (1-q)/2
        else : 
                
            if i-100 in contents_states : transition[i][k][i-100] = (1-q)/2
            elif i-100-10000 < 100 and i-100-10000 > 0 : transition[i][k][1] += (1-q)/2
            else : transition[i][k][0] += (1-q)/2
            if i-101 in contents_states : transition[i][k][i-101-10000] = (1-q)/2
            elif i-101-10000 < 100 and i-101-10000 > 0 : transition[i][k][1] += (1-q)/2
            else : transition[i][k][0] += (1-q)/2
    
        
#---PRINTING---

trans = np.zeros((numStates,5,numStates))

for i in range(len(contents_states)) :
    for j in range(5) :
        for k in range(len(contents_states)) :
            if transition[contents_states[i],j,contents_states[k]] != 0 :
                if contents_states[k] == 0 :
                    print("transition " + str(i) + " " + str(j) + " " + str(k) + " 1.0 " + str(transition[contents_states[i],j,contents_states[k]]) )
                else :
                    print("transition " + str(i) + " " + str(j) + " " + str(k) + " 0.0 " + str(transition[contents_states[i],j,contents_states[k]]) )
print("mdptype episodic")
print("discount  1.0")
