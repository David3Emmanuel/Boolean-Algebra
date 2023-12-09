from group_minterms import group_minterms
from simplify_minterms import simplify_minterms

if __name__ == "__main__":
    N_VARIABLES = int(input("How many variables? "))
    minterms = [int(n) for n in input("Enter minterms: ").split()]
    print()
    print(simplify_minterms(minterms, N_VARIABLES))
    input()