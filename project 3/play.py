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


def make_run(my_discard, hand, val, black_list):
    '''takes in my current discards, current hand, a dictionary of numerical
    values of the cards, and a list of black suits, and finds the highest
    scored run that can be made from combining one card from hand to my
    discards. This is the optimal run, and the card from hand will be returned
    If no runs can be made from any of the cards in my hand, return an
    empty list'''

    from itertools import combinations
    run_list = []    # keep track of all possible runs

    # loop through every card in hand to find make possible runs
    for card in hand:
        lst3=[]
        lst3.append(card)
        my_discards = my_discard + lst3
        for i in range(3, len(my_discards) + 1):
            for group in combinations(my_discards, i):
                group = list(group)

                # check if the group is a valid group
                if valid([group], val) is False:
                    continue

                # if valid, check that its not a run or singleton card
                elif len(group) < 3:
                    continue
                else:
                    if val[group[0][0]] == val[group[1][0]]:
                        continue

                if sorted(group) in run_list:
                    continue
                run_list.append(sorted(group))

    if run_list == []:
        return []

    # only consider runs that are made from the addition of a new card
    for run in run_list:
        for card in run:
            if card in hand:
                break
    else:
        return []

    # find the maximum score of all runs, and returns optimal card to discard
    max_score = -999
    for run in run_list:
        total=0
        total += score([run], val)
        if total > max_score:
            max_score = total
            max_run = run

    for card in max_run:
        if card in hand:
            return card


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
            if len(group[num]) == 1:
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

        # check if colors are alternating. If yes, move on to next group
        if check_col(group, black) is True:
            continue

        return False

    return True

def partition(cards):
    """ takes in a list of cards
    returns all possible partitions of the list of cards """

    if len(cards) == 1:  # base case
        return [[cards]]

    all_list=[]  # list of all partitions
    extra_card=[cards[0]]  # first element of cards


    # for all partitions of a smaller list( by exluding the first element),
    # find all possible ways that the first element can be added to the smaller
    # list, i.e. inserting it into every subgroup of the the smaller list, or
    # adding it as a single list. Do so for all smaller lists recursively

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


def choose_col(discards, hand, my_card, val, black):
    '''takes in my discards, current hand, a repeated card in my hand, a
    dictionary of all numerical values and list of black suits, and returns
    the optimal suit of the repeated card to return based upon the suit
    of the card with the closest value to the repeated card'''

    # find the card closest to my_card, and create a list of optimal suits
    # of my_card
    min_dis=10
    for card in discards:
        if card != 'A':
            if val[card[0]] - val[my_card[0]] < min_dis:
                min_dis = val[card[0]] - val[my_card[0]]
                min_card = card

    if min_card[1] in black:
        if val[min_card[0]] - val[my_card[0]] % 2 == 1:
            lst=[my_card[0] + 'D', my_card[0] + 'H']
        else:
            lst=[my_card[0] + 'S', my_card[0] + 'C']
    else:
        if val[min_card[0]] - val[my_card[0]] % 2 == 1:
            lst=[my_card[0] + 'S', my_card[0] + 'C']
        else:
            lst=[my_card[0] + 'H', my_card[0] + 'D']

    # if the optimal suit of my_card is in hand, return it,
    # otherwise, return original card
    for item in lst:
        if item in hand:
            return item
    else:
        return my_card


def comp10001go_play(discard_history, player_no, hand):
    '''takes in a list of lists of cards of all discards from previous rounds,
    the player number, and my current hand, and returns a card from hand
    that is the optimal card to discard in the current round'''

    import math
    from collections import defaultdict

    # dictionary of all numerical values of cards in the deck
    val = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
           '9': 9, '0': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 20}

    # suits that are black
    black = ['C', 'S']

    # sorted list of cards of all my discards in the previous rounds
    my_discard = sort([discard[player_no] for discard in discard_history], val)

    if len(hand) == 1:
        return hand[0]

    hand = sort(sorted(hand), val)

    # create dictionary counts for my hand, my discards, and all discards
    my_dict = defaultdict(int)
    for card in my_discard:
        my_dict[card[0]] += 1

    discard_dict=defaultdict(int)
    for discards in discard_history:
        for card in discards:
            discard_dict[card[0]] += 1

    hand_dict=defaultdict(int)
    for card in hand:
        hand_dict[card[0]] += 1

    if len(hand) == 10:
        return hand[-1]

    elif len(hand) == 9 or len(hand) == 8:

        # Prioritise n of a kind. If not, return the largest card in hand
        for i in range(len(hand) - 1, -1, -1):
            for j in range(len(my_discard) - 1, -1, -1):
                if my_discard[j][0] == hand[i][0]:
                    return hand[i]

        if hand_dict[hand[-1][0]] > 1:
            return choose_col(my_discard, hand, hand[-1], val, black)
        return hand[-1]

    else:
        # group cards by their frequency, and try to make n of of a kind,
        # prioritising making 4 of a kind / 3 of a kind

        lst =sort([c for c in my_dict if c != 'A' and my_dict[c] == 3], val)
        lst2 = sort([c for c in my_dict if c != 'A' and my_dict[c] == 2], val)
        lst3 = sort([c for c in my_dict if c != 'A' and my_dict[c] == 1], val)

        for i in range(len(hand) - 1, -1, -1):
            if hand[i][0] in lst:
                return hand[i]
        for j in range(len(hand) - 1, -1, -1):
            if hand[j][0] in lst2:
                return hand[j]
        for k in range(len(hand) - 1, -1, -1):
            if hand[k][0] in lst3:
                if hand_dict[hand[k][0]] > 1:
                    return choose_col(my_discard, hand, hand[k], val, black)
                return hand[k]

        # if can't make n of kind, return the card that has been discarded
        # relatively less times, to maximise my chances of geting n of kind

        for ind in range(len(hand) - 1, -1, -1):
            if discard_dict[hand[ind][0]] < 2 and hand[ind][0] != 'A':
                if hand_dict[hand[ind]] > 1:
                    return choose_col(my_discard, hand, hand[ind], val, black)
                return hand[ind]

        if hand_dict[hand[-1]] > 1:
            return choose_col(my_discard, hand, hand[-1], val, black)
        return hand[-1]

        if len(hand) <= 3:

            # remove n of a kinds
            cur_cards=[]
            for card in my_discard:
                if card[0] not in lst and card[0] not in lst2:
                    cur_cards.append(card)
                elif card[0] in lst2 and val[card[0]] <= 7:
                    cur_cards.append(card)

            # return card that will yield highest score
            cur_score=-999
            optimal=make_run(cur_cards, hand, val, black)
            if optimal != []:
                cur_score=-9999
                my_discard.append(optimal)
                cur_score = score([my_discard], val)

            max_score=-999
            for card in hand:
                cur_round=[['2C', '2C', '2C', '2C']]
                cur_round[0][player_no] = card
                d_history=discard_history + cur_round
                cur=score(comp10001go_group(d_history, player_no), val)
                if cur > max_score:
                    max_score=cur
                    max_card=card

            if max_score < cur_score:
                return optimal
            return max_card


def comp10001go_group(discard_history, player_no):
    val = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
           '9': 9, '0': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 20}

    my_cards=[card[player_no] for card in discard_history]

    cards = partition(my_cards)

    new_cards=[]
    for card in cards:
        if valid(card, val) is True:
            new_cards.append(card)

    max_score=-999
    for card2 in new_cards:
        tot=0
        tot+=score(card2, val)
        if tot > max_score:
            max_score = tot
            max_cards=card2

    return max_cards
