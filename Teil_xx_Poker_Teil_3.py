import itertools


def numeric_ranks(cards):
    """
    Changes the input list of card strings to a list of 
    strings with numbers substituting for face cards.
    ex.
    numeric_ranks(['AS','3S','4S','5S','JC'])
    returns ['14S','3S','4S','5S','11C']
    """
    suits = get_suits(cards)
    face_numbers = {'A': 14, 'J': 11, 'Q': 12, 'K': 13}
    for index, card in enumerate(cards):
        rank = card[0:-1]
        try: 
            int(rank)
        except:
            # Rank is a letter, not a number
            cards[index] = str(face_numbers[rank])+suits[index]
    return cards


def get_ranks(cards):
    """
    Returns a list of ints containing the rank of each card in cards.
    ex. 
    get_ranks(['2S','3C','5C','4D','6D'])
    returns [2,3,5,4,6]
    """
    cards = numeric_ranks(cards) # Convert rank letters to numbers (e.g. J to 11)
    return [int(card[0:-1]) for card in cards]


def get_suits(cards):
    """
    Returns a list of strings containing the suit of each card in cards.
    ex. 
    get_ranks(['2S','3C','5C','4D','6D'])
    returns ['S','C','C','D','D']
    """
    return [card[-1] for card in cards]


def evaluate_hand(hand):
    """
    Returns a string containing the name of the hand in poker.
    Input hand must be a list of 5 strings.
    ex. 
    evaluate_hand(['2S','3C','5C','4D','6D'])
    returns 'Straight'
    """
    hand = numeric_ranks(hand)
    ranks = get_ranks(hand)
    suits = get_suits(hand)
    if len(set(hand)) < len(hand) or max(ranks) > 14 or min(ranks) < 1:
        # There is a duplicate
        return 'Invalid hand'
    if isconsecutive(ranks):
        # The hand is a type of straight
        if all_equal(suits):
            # Hand is a flush
            if max(ranks) == 14:
                # Highest card is an ace
                return 'Royal flush'
            return 'Straight flush'
        return 'Straight'
    if all_equal(suits):
        return 'Flush'
    total = sum([ranks.count(x) for x in ranks])
    hand_names = {
        17: 'Four of a kind',
        13: 'Full house',
        11: 'Three of a kind',
        9: 'Two pair',
        7: 'One pair',
        5: 'High card'
        }
    return hand_names[total]


def all_equal(lst):
    """ 
    Returns True if all elements of lst are the same, False otherwise 
    ex.
    all_equal(['S,'S','S']) returns True
    """
    return len(set(lst)) == 1


def show_cards(cards):
    """ Prints the rank and suit for each card in cards. """
    cards = sort_cards(cards)
    all_suits = ['C','D','H','S']
    symbols = dict(zip(all_suits,['\u2667','\u2662','\u2661','\u2664']))
    faces = {14: 'A', 11: 'J', 12: 'Q', 13: 'K'}
    card_symbols = []
    for card in cards:  
        rank = card[0:-1]
        if int(rank) in faces:
            card_symbols.append(faces[int(rank)] + symbols[card[-1]])
        else:
            card_symbols.append(rank + symbols[card[-1]])
    for symbol in card_symbols:
        print(symbol, end = ' ')
    print('')
    return card_symbols

def isconsecutive(lst):
    """ 
    Returns True if all numbers in lst can be ordered consecutively, and False otherwise
    """
    return len(set(lst)) == len(lst) and max(lst) - min(lst) == len(lst) - 1    


def sort_cards(cards):
    """
    Sorts cards by their rank.
    If rank is a string (e.g., 'A' for Ace), then the rank is changed to a number.
    Cards of the same rank are not sorted by suit.
    ex.
    sort_cards(['AS','3S','4S','5S','JC'])
    returns 
    ['3S','4S','5S','11C','14S']
    """ 
    cards = numeric_ranks(cards)
    rank_list = get_ranks(cards)
    # Keep track of the sorting permutation
    new_order = sorted((e,i) for i,e in enumerate(rank_list))
    unsorted_cards = list(cards)
    for index, (a, b) in enumerate(new_order):
        cards[index] = unsorted_cards[b]
    return cards


def get_best_hand(cards):
    """ 
    Returns the best hand of five cards, from a larger list of cards.
    If ranks are alphabetical (e.g., A for ace), it will convert the rank to a number.
    ex.
    get_best_hand(['7C', '7S', '2H', '3C', 'AC', 'AD', '5S'])
    returns
    ['5S', '7C', '7S', '14C', '14D']
    """
    # All combinations of 5 cards from the larger list
    all_hand_combos = itertools.combinations(cards, 5) 
    hand_name_list = [
        'Invalid hand',
        'High card',
        'One pair',
        'Two pair',
        'Three of a kind',
        'Straight',
        'Flush',
        'Full house',
        'Four of a kind',
        'Straight flush',
        'Royal flush'
        ]
    num_hand_names = len(hand_name_list)
    max_value = 0
    best_hands = {x: [] for x in range(num_hand_names)}
    for combo in all_hand_combos:
        hand = list(combo)
        hand_name = evaluate_hand(hand) # Get the type of hand (e.g., one pair)
        hand_value = hand_name_list.index(hand_name)
        if hand_value >= max_value:
            # Stronger or equal hand has been found
            max_value = hand_value
            best_hands[hand_value].append(hand) # Store hand in dictionary
    max_hand_idx = max(k for k, v in best_hands.items() if len(best_hands[k])>0)
    rank_sum, max_sum = 0, 0
    # The strongest hand type out of the combinations has been found
    for hand in best_hands[max_hand_idx]: 
        # Iterate through hands of this strongest type
        ranks = get_ranks(hand)
        rank_sum = sum(ranks)
        if rank_sum > max_sum:
            max_sum = rank_sum
            best_hand = hand # Choose hand with highest ranking cards
    return best_hand

table = ['2H', '5C', 'AC', 'AD', '6C']
hand = ['7C','AS']
cards = hand + table
best_hand = get_best_hand(cards)

print('Hand:')
show_cards(hand), print('')

print('Cards on table:')
show_cards(table), print('')

print('Best hand of five:')
show_cards(best_hand)

print(evaluate_hand(best_hand))