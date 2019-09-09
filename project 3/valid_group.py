def sort(group, val):
    ''' takes in a sorted list of cards without aces and
    re-sorts them by their actual card values using "val"  '''

    for ind in range(len(group) - 1):
        if val[group[ind][0]] > val[group[ind + 1][0]]:
            temp=group[ind + 1]
            group[ind + 1]= group[ind]
            group[ind]=temp
    return group

def check_col(col, black_list):
    ''' takes in a list of cards and list of black suits and checks if the
    colors are alternating'''

    for i in range(len(col) - 1):
        if col[i][1] in black_list and col[i + 1][1] in black_list:
            return False
        if col[i][1] not in black_list and col[i + 1][1] not in black_list:
            return False
    return True

def comp10001go_valid_groups(groups):
    '''Takes in a list of lists of cards, and returns a boolean indicating
    whether all lists of cards are valid (i.e. if it is an n-of-kind, run, or
    singleton card) '''

    from collections import defaultdict

    # a dictionary that gives the value of each card in the deck
    val={'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
         '9': 9, '0': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 20}

    if groups == []:
        return True

    # for ecah group in groups, check if they are valid.
    for group in groups:
        if len(group) == 1:
            continue

        # check if it is n-of-kind. If yes, move on to next group
        if group[0][0]!='A' and len(group)>1:
            for i in range(len(group) - 1):
                    if group[i][0] != group[i + 1][0]:
                        break
            else:
                continue

        # if not n-of-kind, check other trivial cases, e.g. length of group,
        # and whether there are repeated cards
        if len(group)<3:
            return False
        count_d=defaultdict(int)
        for item in group:
            count_d[item[0]] += 1
        for key in count_d:
            if key != 'A' and count_d[key] > 1:
                return False

        # suits that are black
        black=['C', 'S']

        val_opp={10: '0', 11: 'J', 12: 'Q', 13: 'K'}

        # creating a list of all aces, and a sorted list without the aces
        ace_list=list({'AH', 'AD', 'AS', 'AC'}.intersection(set(group)))
        group=sort(sorted(list(set(group).difference(ace_list))), val)

        if len(group) == 0:
            return False
        # check if group form a run. Create a list with all missing items if
        # group were to be a run, and then concatenate it with the group
        group2=[]
        for i in range(1, val[group[-1][0]] - val[group[0][0]]):
            for c in group:
                if val[c[0]] == val[group[0][0]] + i:
                    break
            else:
                if val[group[0][0]] + i in val_opp:
                    group2.append(val_opp[val[group[0][0]] + i])
                else:
                    group2.append(str(val[group[0][0]] + i))

        group=sort(sorted(group + group2), val)

        # invalid if not enough/ too many aces
        if len(ace_list) != len(group2):
            return False

        # check there is an ace of the right color for each missing item
        for num in range(len(group)):
            if len(group[num])==1:
                if group[num - 1][1] in black:
                    for ace in ace_list:
                        if ace[1] not in black:
                            ace_list.remove(ace)
                            break
                    else:
                        return False
                    group[num]+='D'
                else:
                    for ace in ace_list:
                        if ace[1] in black:
                            ace_list.remove(ace)
                            break
                    else:
                        return False
                    group[num]+='S'

        # check if colors alternating. If yes, move on to next group
        if check_col(group, black) is True:
            continue
        else:
            return False

    return True

       
