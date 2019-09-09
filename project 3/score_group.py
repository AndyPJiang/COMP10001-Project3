def sort(cards, val):
    ''' takes in a sorted list of cards without aces and
    re-sorts them by their actual card values using "val"  '''

    for ind in range(len(cards) - 1):
        if val[cards[ind][0]] > val[cards[ind + 1][0]]:
            temp=cards[ind + 1]
            cards[ind + 1]= cards[ind]
            cards[ind]=temp
    return cards

def check_col(col, black_list):
    ''' takes in a list of cards and list of black suits and checks if the
    colors are alternating'''

    for i in range(len(col) - 1):
        if col[i][1] in black_list and col[i + 1][1] in black_list:
            return False
        if col[i][1] not in black_list and col[i + 1][1] not in black_list:
            return False
    return True

def comp10001go_score_group(cards):
    ''' takes in a list of cards checks if the cards is an n-of-kind, run,
    or invalid, and returns the score according to what type it is'''

    import math
    from collections import defaultdict

    # a dictionary that gives the value of each card in the deck
    val={'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
         '9': 9, '0': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 20}


    tot=0   # tot is the value returned if cards are invalid
    for card in cards:
        tot+=val[card[0]]

    # check if cards form n of a kind. If yes, return its score
    if cards[0][0]!='A' and len(cards)>1:
        for i in range(len(cards) - 1):
                if cards[i][0] != cards[i + 1][0]:
                    break
        else:
            return math.factorial(len(cards)) * val[cards[0][0]]

    if len(cards)<3:
        return -tot

    # if cards don't form n of kind, if they repeat, then they are invalid
    count_d=defaultdict(int)
    for item in cards:
            count_d[item[0]] += 1
    for key in count_d:
        if key != 'A' and count_d[key] > 1:
            return -tot


    black=['C', 'S']  # suits that are black
    val_opp={10: '0', 11: 'J', 12: 'Q', 13: 'K'}

    # creating a list of all aces, and a sorted list without the aces
    ace_list=list({'AH', 'AD', 'AS', 'AC'}.intersection(cards))
    cards=sort(sorted(list(set(cards).difference(ace_list))), val)

    if len(cards) == 0:
        return -tot

    # check if cards form a run. Create a list with all missing items if the
    # cards were to be a run, and then concatenate it with cards
    cards2=[]
    for i in range(1, val[cards[-1][0]] - val[cards[0][0]]):
        for c in cards:
            if val[c[0]] == val[cards[0][0]] + i:
                break
        else:
            if val[cards[0][0]] + i in val_opp:
                cards2.append(val_opp[val[cards[0][0]] + i])
            else:
                cards2.append(str(val[cards[0][0]] + i))
    cards=sort(sorted(cards + cards2), val)

    # invalid if not enough/ too many aces
    if len(ace_list) != len(cards2):
        return -tot


    # check there is an ace of the right color for each missing item
    for num in range(len(cards)):
        if len(cards[num])==1:
            if cards[num - 1][1] in black:
                for ace in ace_list:
                    if ace[1] not in black:
                        ace_list.remove(ace)
                        break
                else:
                    return -tot
                cards[num]+='D'
            else:
                for ace in ace_list:
                    if ace[1] in black:
                        ace_list.remove(ace)
                        break
                else:
                    return -tot
                cards[num]+='S'

    # check if colors alternating. If yes, return sum of value of cards
    if check_col(cards, black) is True:
        total=0
        for card in cards:
            total+=val[card[0]]
        return total
    else:
        return -tot
    
