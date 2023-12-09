def group_minterms(minterms, N_VARIABLES):
    minterms = sorted(minterms)
    all_minterm_groups = get_all_minterm_groups(minterms, N_VARIABLES)
    truncated_minterm_groups = list(filter(lambda minterms: not is_contained(minterms, all_minterm_groups), all_minterm_groups))

    remaining_minterms = minterms.copy()
    remaining_minterm_groups = truncated_minterm_groups.copy()
    confirmed_minterm_groups = []

    alternatives = False

    def confirm_group(group):
        confirmed_minterm_groups.append(group)
        remaining_minterm_groups.remove(group)
        for _minterm in group:
            if _minterm in remaining_minterms:
                remaining_minterms.remove(_minterm)

    while remaining_minterms:
        accumulated_minterms = tuple()
        for _minterms in remaining_minterm_groups:
            accumulated_minterms += _minterms
        
        previous_remaining_minterms = len(remaining_minterms)
        for minterm in remaining_minterms:
            if accumulated_minterms.count(minterm) == 1:
                for group in remaining_minterm_groups:
                    if minterm in group:
                        confirm_group(group)
                        break
                break
        
        if len(remaining_minterms) == previous_remaining_minterms:
            alternatives = True
            minterm = remaining_minterms[0]
            for group in remaining_minterm_groups:
                if minterm in group:
                    confirm_group(group)
                    break
        continue

    confirmed_minterm_groups.sort(key=lambda group: -len(group))
    return confirmed_minterm_groups, alternatives


def get_all_minterm_groups(minterms, N_VARIABLES):
    column1 = [[] for _ in range(N_VARIABLES+1)]
    for minterm in minterms:
        binary = to_binary((minterm,), N_VARIABLES)
        column1[binary.count('1')].append((minterm,))

    columns = [column1]

    while True:
        new_column = [[] for _ in range(N_VARIABLES + 1 - len(columns))]
        empty = True

        previous_columns = columns[-1]
        for i in range(N_VARIABLES + 1 - len(columns)):
            for first_term in previous_columns[i]:
                for second_term in previous_columns[i+1]:
                    if compare_minterms(first_term, second_term, N_VARIABLES) == 1:
                        empty = False
                        new_column[i].append(first_term + second_term)
        if empty: break
        else: columns.append(new_column)
    
    all_minterm_groups = []
    for column in columns:
        for group in column:
            for _minterms in group:
                all_minterm_groups.append(_minterms)
    
    return all_minterm_groups


def to_binary(minterms, N_VARIABLES):
    _bin = lambda n: '0'*(N_VARIABLES - len(bin(n)[2:])) + bin(n)[2:]
    output = list(_bin(minterms[0]))
    for minterm in minterms[1:]:
        b = _bin(minterm)
        for index, (i, j) in enumerate(zip(output, b)):
            if i != j: output[index] = '-'

    return ''.join(output)


def compare_minterms(a, b, N_VARIABLES):
    binary1 = to_binary(a, N_VARIABLES)
    binary2 = to_binary(b, N_VARIABLES)
    count = 0
    for i, j in zip(binary1, binary2):
        if i != j: count += 1
    return count

def is_contained(minterms, all_minterm_groups):
    for minterms2 in all_minterm_groups:
        if minterms == minterms2 or len(minterms) > len(minterms2): continue
        if set(minterms) == set(minterms2):
            return minterms > minterms2
        
        contained = True
        for i in minterms:
            if i not in minterms2:
                contained = False
                break
        if contained: return True
    return False