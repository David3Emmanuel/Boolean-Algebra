from string import ascii_uppercase as ABC
from group_minterms import group_minterms, to_binary

def simplify_minterms(minterms, N_VARIABLES):
    groups, alternatives = group_minterms(minterms, N_VARIABLES)
    if alternatives: print("Alternative simplification exists\n")
    return ' + '.join([group_to_expression(group, N_VARIABLES) for group in groups])

def group_to_expression(group, N_VARIABLES):
    binary = to_binary(group, N_VARIABLES)
    output = ""
    for i in range(N_VARIABLES):
        if binary[i] == '-': continue
        output += ABC[i]
        if binary[i] == '0': output += "'"
    return output