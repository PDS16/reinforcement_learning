import optparse
import numpy as np


#-----------------------INCLUDING COMMAND-LINE OPTIONS----------------------------

parser = optparse.OptionParser()

parser.add_option('--states', dest = 'states_file_name',
                  type = 'string')
parser.add_option('--value-policy', dest = 'value_policy',
                  type = 'string')
(options, args) = parser.parse_args()
if (options.states_file_name == None or options.value_policy == None):
    print ("Invalid Usage")
    exit(0)

states_file = options.states_file_name
pv_file = options.value_policy


#-------------------------------READING STATEFILE--------------------------

file1 = open(states_file,'r')
contents_states = file1.readlines()



#------------------------------READING VALUE POLICY FILE---------------------

file2 = open(pv_file,'r')
contents_pv = file2.readlines()

for i in range(len(contents_states)) :
    temp = contents_pv[i].split()
    if temp[1] == '3' :
        print(contents_states[i][:-1] + " 4 " + temp[0])
    elif temp[1] == '4' :
        print(contents_states[i][:-1] + " 6 " + temp[0])
    else :
        print(contents_states[i][:-1] + " " + temp[1] + " " + temp[0])