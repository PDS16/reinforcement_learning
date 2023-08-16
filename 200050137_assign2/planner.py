import numpy as np
import optparse
from pulp import *

#-----------------------INCLUDING COMMAND-LINE OPTIONS----------------------------

parser = optparse.OptionParser()

parser.add_option('--mdp', dest = 'file_name',
                  type = 'string')
parser.add_option('--algorithm', dest = 'algo',
                  type = 'string', default = 'vi')
parser.add_option("--policy",
                  dest = "policy", type = 'string')
(options, args) = parser.parse_args()
if (options.file_name == None):
    print ("Invalid Usage")
    exit(0)

file_mdp = options.file_name
algorithm = options.algo
policy_additional = options.policy


#----------------READING MDP FILE----------------------------------

file = open(file_mdp,'r')
contents = file.readlines()
numStates = int(contents[0][10:-1])
numActions = int(contents[1][11:-1])
mdtype = contents[-2][8:-1]
discount  = float(contents[-1][10:-1])
States = range(numStates)
Actions = range(numActions)
rewards = np.zeros((numStates,numActions,numStates),dtype=np.float64)
transition = np.zeros((numStates,numActions,numStates),dtype=np.float64)
for i in range(3,len(contents)-2) :
    temp = contents[i].split()
    transition[int(temp[1]),int(temp[2]),int(temp[3])] = np.float64(temp[5])
    rewards[int(temp[1]),int(temp[2]),int(temp[3])] = np.float64(temp[4])
    
    
#-------------------CHECKING FOR ADDITIONAL POLICY-------------------------------


if policy_additional != None :
    file1 = open(policy_additional,'r')
    custom_policy = file1.readlines()
    custom_policy = np.array(list(map(int, custom_policy)))
    A = np.identity(numStates) - discount*transition[range(numStates),custom_policy[range(numStates)],:]
    b = np.sum(transition[range(numStates),custom_policy[range(numStates)],:]*rewards[range(numStates),custom_policy[range(numStates)],:],axis=1)
    V = np.matmul(np.linalg.inv(A),b)
    for i in range(numStates) :
        print(str(format(V[i],'.6f')) + " " + str(custom_policy[i]))
    exit(0)

    
#--------------------APPLING DIFFERENT POLICIES---------------------------------

V = np.zeros((numStates),dtype=np.float64)+1000
V_next = np.zeros((numStates),dtype=np.float64)+1000
pi = np.zeros((numStates))


#--------------------VALUE ITERATION-------------------------------------------

if algorithm == 'vi' :
    while 1 :
        matrix = transition*(rewards+discount*V_next)
        matrix2 = np.sum(matrix,axis=2)
        V = V_next
        V_next = np.max(matrix2,axis=1)
        if np.sum(np.abs(V-V_next)) < numStates*1e-11 : 
            pi = np.argmax(matrix2,axis=1)
            break


#--------------------HOWARD'S POLICY ITERATION------------------------------


if algorithm == 'hpi' :
    while 1 :
        matrix = transition*(rewards+discount*V_next)
        matrix2 = np.sum(matrix,axis=2)
        V = V_next
        pi = np.argmax(matrix2,axis=1)
        A = np.identity(numStates) - discount*transition[range(numStates),pi[range(numStates)],:]
        b = np.sum(transition[range(numStates),pi[range(numStates)],:]*rewards[range(numStates),pi[range(numStates)],:],axis=1)
        V_next = np.matmul(np.linalg.inv(A),b)
        if np.sum(np.abs(V-V_next)) < numStates*1e-11 : 
            break


#--------------------LINEAR PROGRAMMING--------------------------------------


if algorithm == 'lp' :
    C = np.sum(transition*rewards,axis=2)
    set_D = range(0, transition.shape[0])
    set_I = range(0, transition.shape[1])

    prob = LpProblem("numpy_constraints", LpMinimize)
    Variable = pulp.LpVariable.dicts("Variable", set_D, cat='Continuous')
    prob += lpSum([Variable[i] for i in set_D])

    for d in set_D:
        for i in set_I:
            prob += Variable[d] - discount*lpSum([transition[d][i][j]*Variable[j] for j in set_D]) >= C[d][i]

    prob.solve(PULP_CBC_CMD(msg=0))
    V = np.array([Variable[i].varValue for i in set_D])


#--------------------PRINTING---------------------------------

V = np.round(V,decimals=6)
pi = pi.astype(int)
for i in range(numStates) :
    print(str(format(V[i],'.6f')) + " " + str(pi[i]))

