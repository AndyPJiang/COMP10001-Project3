def sort(group, val):
    ''' takes in a list of lists of cards, and a dictionary of all numerical values
    of cards in the deck, and sorts them according to their value,
    except for all aces will appear at the start of the sorted list'''

    # create a group without aces
    ace_list = list({'AH', 'AD', 'AS', 'AC'}.intersection(set(group)))
    group = sorted(list(set(group).difference(ace_list)))

    for ind in range(len(group) - 1):
        if val[group[ind][0]] > val[group[ind + 1][0]]:
            temp = group[ind + 1]
            group[ind + 1] = group[ind]
            group[ind] = temp

    # insert all aces to the front of the list
    for ace in ace_list:
        group.insert(0, ace)
    return group

def check_col(col, black_list):
    ''' takes in a list of cards and checks if the colors are alternating
    using black_list (list of suits that are black)'''

    for i in range(len(col) - 1):
        if col[i][1] in black_list and col[i + 1][1] in black_list:
            return False
        if col[i][1] not in black_list and col[i + 1][1] not in black_list:
            return False
    return True


def valid(groups, val):
    '''takes in a list of lists of cards, and a dictionary of all numerical values
    of cards in the deck, and returns a boolean indicating whether all lists
    of cards are valid (i.e. if it is an n-of-kind, run, or singleton card) '''

    from collections import defaultdict

    if groups == []:
        return True

    # check if valid for every list of cards in groups
    for group in groups:
        if len(group) == 1:
            continue

        # check if they are n of a kind. If yes, move on to next card
        if group[0][0]!='A' and len(group) > 1:
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
                if group[num- 1][1] in black:
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

        # check if colors are alternating. If yes, move on to next group
        if check_col(group, black) is True:
            continue

        return False

    return True

def score(card_list, val):
    '''Takes in a valid list of lists of cards, and dictionary of all numerical
    values of cards in the deck, and scores card_list accordingly to its
    type (i.e. if its a run, n of kind or singleton card)'''

    import math
    tot=0   # keep track of score

    # score each list of cards in card_list according to their type
    for cards in card_list:

        # check if it is n of kind
        cards=sort(sorted(cards), val)
        if cards[0][0]!='A' and len(cards)>1:
            for i in range(len(cards) - 1):
                    if cards[i][0] != cards[i + 1][0]:
                        break
            else:
                tot+= math.factorial(len(cards)) * val[cards[0][0]]
                continue

        # check if it is a run
        if len(cards) > 1:
            ace_less=[card for card in cards if card[0] != 'A']
            lst=sort(sorted(ace_less), val)
            for i in range(0, val[lst[-1][0]] - val[lst[0][0]] + 1):
                tot = tot + val[lst[0][0]] + i
        else:
            tot-=val[cards[0][0]]

    return tot


def partition(cards):
    """ takes in a list of cards
    returns all possible partitions of them """

    if len(cards) == 1:  # base case
        return [[cards]]

    all_list=[]  # list of all partitions
    extra_card=[cards[0]]  # first element in list


    # Create new partitions from all partitions of smaller list combined with
    # the first element in the larger list, by inserting the first element
    # into all smaller partitions, as well as on its own
    for small in partition(cards[1:]):
        for item in small:
            for i in range(len(small)):
                if i == small.index(item):
                    if i == 0:
                        mid=[extra_card + item]
                        right=small[1:]
                        all_list.append(mid + right)
                    else:
                        left=small[:i]
                        mid=[extra_card + item]
                        right=small[i + 1:]
                        all_list.append(left + mid + right)

        all_list.append([extra_card] + small)

    return all_list

def comp10001go_best_partitions(cards):
    ''' takes in a list of cards, and returns the combination of cards that
    will give the highest score'''

    # dictionary of the numerical value of each card in the deck
    val = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
           '9': 9, '0': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 20}


    cards = partition(cards)

    new_cards=[]    # list of all valid partitions
    for card in cards:
        if valid(card, val) is True:
            new_cards.append(card)

    max_score_list=[]   # list of all partitions that will yield highest score


    # find max score and return all combinations that give that max score
    max_score=max([score(x, val) for x in new_cards])

    for card2 in new_cards:
        tot=0
        tot+=score(card2, val)
        if tot == max_score:
            max_score_list.append(card2)

    return max_score_list
