#⚠️⚠️ this game dont have readme file but you could enter 'help' to see the rules

import random

#=========================================
# card deck class
#=========================================

class CardDeck:
    '''Manages the card deck: creating shuffing and drawing'''
    def __init__(self):
        '''initalize a new card with 52 cards, 4 copies each'''
        self.all_cards=[]
        self.remaining_cards=[]
        self.create_deck()   #start the game (turn1) and every turn need to create a new deck

    def create_deck(self):
        '''create a new deck of 52 cards'''
        self.all_cards=[]    #each turn the hand will return to the deck
        for number in range(1,14):#from A~K
            for copy in range(4): #4copy
                self.all_cards.append(number)
        self.remaining_cards=self.all_cards.copy()   #so it wont affect the original one 
        self.shuffle_deck()
    
    def shuffle_deck(self):
        '''Randomly shuffle the remaining cards'''
        random.shuffle(self.remaining_cards)       #random.shuffle()
    
    def draw_cards(self,count):
        '''draw the card from deck'''
        drawn=[]
        for i in range(count):
            if len(self.remaining_cards)>0:
                card=self.remaining_cards.pop(0)    #get the 1st card in card pile
                drawn.append(card)      #the deleted card becomes the drawn card
            else:           #if no card in deck
                self.create_deck()
                card=self.remaining_cards.pop(0)
                drawn.append(card)
        return drawn
        
    def show_deck(self):
        '''display remain cards in deck'''
        print("\n" + "="*50)
        print(f"📦 Deck: {len(self.remaining_cards)} cards remaining")
        counts = {}        #dictionary to match the cards and the remain counts, like A(key):4(valuie)
        for card in self.remaining_cards:
            counts[card] = counts.get(card, 0) + 1        #get the value and +1 each time
        for num in sorted(counts.keys()):       #use sorted()
            print(f"  {format_card(num)}: {counts[num]}")     
        print("="*50)        

        

#=========================================
# player class
#=========================================

class Player:
    """manages player state : hand, score, and bonuses"""

    def __init__(self):
        """initialize player with default values"""
        self.hand = []
        self.current_round = 1
        self.target_score = 150
        self.round_score = 0
        self.plays_left = 4
        self.discards_left = 3
        self.global_bonus = 0  # Permanent bonus to all scores
        self.hand_type_bonus = {}  # store multiplier bonuses for specific hand types, dictionary, to get buffs
        self.bonus_start_score = 0  # bonus points to start next round with

    def reset_round(self):
        """start a new round with increased difficulty"""
        # Save any extra actions from rewards (before reset)
        extra_plays = max(0, self.plays_left - 4)  # calculate extra
        extra_discards = max(0, self.discards_left - 3)
        
        self.current_round += 1
        self.target_score = 150 + (self.current_round - 1) * 60
        self.round_score = self.bonus_start_score  # apply bonus from previous round
        self.bonus_start_score = 0  # reset for next time
        self.plays_left = 4 + extra_plays  # restore base + extra
        self.discards_left = 3 + extra_discards

    def show_hand(self):
        """display the player's current hand"""
        print("\n🎴 Your Hand: ", end="")
        cards_display = []
        for card in sorted(self.hand):
            cards_display.append(format_card(card))
        print(", ".join(cards_display))         #"A, 5, 5, 7, 9, J, K", without'[]'

    def show_status(self):
        """display current game status"""
        print("\n" + "="*50)
        print(f"🎯 Round {self.current_round}/5")
        print(f"📊 Target: {self.target_score} | Current: {self.round_score}")
        print(f"🎴 Plays: {self.plays_left} | ♻️  Discards: {self.discards_left}")
        print("="*50)



#=========================================
# Basic function
#=========================================

def format_card(card):
    """convert card number to display format (A, J, Q, K)"""
    if card == 1:
        return "A"
    elif card == 11:
        return "J"
    elif card == 12:
        return "Q"
    elif card == 13:
        return "K"
    else:
        return str(card)
    
def parse_card(card_string):
    """convert card string input to number"""
    card_string = card_string.strip().upper()
    if card_string == "A":
        return 1
    elif card_string == "J":
        return 11
    elif card_string == "Q":
        return 12
    elif card_string == "K":
        return 13
    else:
        try:
            return int(card_string)
        except:
            return None
        
def evaluate_hand(cards):
    """determine hand type and calculate score"""
    if len(cards) == 0:         #no input
        return {"type": "nothing", "sum": 0, "mult": 1}
    
    # count occurrences of each card value
    counts = {}         #counts = {A: 3, K: 2}
    for card in cards:
        counts[card] = counts.get(card, 0) + 1
    
    # get counts in descending order
    count_values = sorted(counts.values(), reverse=True)        #cards = [7, 7, 7, 7, 5], counts = {7: 4, 5: 1}, count_values = [4, 1]
    cards_sum = sum(cards)  #sum([7, 7, 7]) = 21
    
    # Determine hand type
    hand_type = "nothing"
    multiplier = 1
    
    # Four of a kind
    if len(count_values) >= 1 and count_values[0] >= 4:
        hand_type = "four_kind"
        multiplier = 7
    # Full house (3+2)
    elif len(count_values) >= 2 and count_values[0] >= 3 and count_values[1] >= 2:
        hand_type = "full_house"
        multiplier = 6
    # Three of a kind
    elif len(count_values) >= 1 and count_values[0] >= 3:
        hand_type = "three_kind"
        multiplier = 4
    # Two pairs
    elif len(count_values) >= 2 and count_values[0] >= 2 and count_values[1] >= 2:
        hand_type = "two_pairs"
        multiplier = 3
    # One pair
    elif len(count_values) >= 1 and count_values[0] >= 2:
        hand_type = "pair"
        multiplier = 2
    # Check for straight (5 consecutive cards)
    elif len(cards) == 5:
        sorted_cards = sorted(cards)
        is_straight = True
        # Special case: A-10-J-Q-K
        if sorted_cards == [1, 10, 11, 12, 13]:
            is_straight = True
        else:
            for i in range(len(sorted_cards) - 1):
                if sorted_cards[i+1] - sorted_cards[i] != 1:
                    is_straight = False
                    break
        if is_straight:
            hand_type = "straight"
            multiplier = 5
    
    return {"type": hand_type, "sum": cards_sum, "mult": multiplier}


#=========================================
# Reward
#=========================================


def generate_reward(round_num):
    """generate reward with rarity tiers: Legendary, Rare, Common"""
    chance = random.random() * 100          #0%～100%
    
    if chance < 5:  # 5% Legendary - Double multipliers
        hand_types = ["pair", "three_kind", "straight", "full_house"]
        selected = random.choice(hand_types)        #random hand_type
        return {"tier": "Legendary", "name": f"double_{selected}",
                "desc": f"✨ Double multiplier for {selected} (permanent)"}
    
    elif chance < 35:  # 30% Rare
        rare_type = random.randint(1, 3)        #3 types
        if rare_type == 1:
            return {"tier": "Rare", "name": "global_mult", 
                    "desc": "⭐ +1 to all hand multipliers (permanent)"}
        elif rare_type == 2:
            return {"tier": "Rare", "name": "score_triple", 
                    "desc": "💎 Start next round with +100 points"}
        else:
            return {"tier": "Rare", "name": "extra_actions",
                    "desc": "⚡ +2 plays and +1 discard this round"}
    
    else:  # 65% Common
        return {"tier": "Common", "name": "score_boost",
                "desc": "💯 Start next round with +30 points"}
        

def choose_and_apply_reward(player, deck, round_num):
    """let player choose from 3 reward options"""
    print("\n" + "="*50)
    print("🎁 Choose Your Reward:")
    print("="*50)
    
    # generate 3 options
    options = []
    for i in range(3):
        reward = generate_reward(round_num)
        options.append(reward)
        print(f"\n[{i+1}] {reward['tier']} - {reward['desc']}")     #start from 1
    
    print("\n" + "="*50)
    
    # Get player choice
    while True:
        try:
            choice = input("Choose (1, 2, or 3): ").strip()
            num = int(choice)
            if 1 <= num <= 3:
                selected = options[num - 1] #index 
                break
            print("❌ Enter 1, 2, or 3")
        except:
            print("❌ Enter 1, 2, or 3")
    
    apply_reward(selected, player, deck)


def apply_reward(reward, player, deck):
    """apply selected reward to game state"""
    print(f"\n✅ Applied: {reward['desc']}")
    
    name = reward["name"]
    
    if name == "score_triple":
        player.bonus_start_score += 100  # for next round
        print(f"  Next round starts with +100 points!")
    
    elif name == "global_mult":
        player.global_bonus += 1.0
        print("  All hand types boosted!")
    
    elif name.startswith("double_"):    #start with
        hand_type = name.replace("double_", "")   #replace
        current_mult = player.hand_type_bonus.get(hand_type, 1)
        player.hand_type_bonus[hand_type] = current_mult * 2
        print(f"  {hand_type} multiplier doubled! (now ×{player.hand_type_bonus[hand_type]})")
    
    elif name == "extra_actions":
        player.plays_left += 2  # will be preserved by reset_round
        player.discards_left += 1
        print("  Extra actions granted!")
    
    elif name == "score_boost":
        player.bonus_start_score += 30  # for next round
        print(f"  Next round starts with +30 points!")


#=========================================
# Help function
#=========================================

def show_help():
    """Display game rules and scoring information"""
    print("\n" + "="*50)
    print("📖 GAME HELP")
    print("="*50)
    
    print("\n🎯 OBJECTIVE:")
    print("  Complete 5 rounds by reaching target scores")
    print("  Target increases each round: 150, 210, 270...")
    
    print("\n🎴 HAND TYPES & SCORING:")
    print("  Score = Card Sum × Multiplier")
    print("  ─────────────────────────────────────────")
    print("  Straight (5 cards)    → ×5  (e.g. 5-6-7-8-9)")
    print("  Four of a kind        → ×7  (e.g. 7-7-7-7)")
    print("  Full House (3+2)      → ×6  (e.g. 5-5-5-9-9)")
    print("  Three of a kind       → ×4  (e.g. 8-8-8)")
    print("  Two Pairs             → ×3  (e.g. 3-3-7-7)")
    print("  One Pair              → ×2  (e.g. K-K)")
    print("  Single Cards          → ×1")
    
    print("\n💬 COMMANDS:")
    print("  play [cards]     - Play cards (e.g. 'play 7 7 8')")
    print("  discard [cards]  - Discard and draw new (e.g. 'discard 2 K')")
    print("  deck             - View remaining cards in deck")
    print("  end              - End current round")
    print("  save             - Save game progress")
    print("  help             - Show this help message")
    
    print("\n⚠️  INPUT FORMAT:")
    print("  • Use SPACES between cards: 'play 7 7 8' ✅")
    print("  • NOT: 'play 778' ❌")
    print("  • Card names: A, 2-10, J, Q, K")
    print("  • Maximum 5 cards per play/discard ⚠️")
    print("  • Examples:")
    print("    play A A      → Play two Aces")
    print("    discard 2 5 K → Discard 2, 5, and King")
    print("    play 5 6 7 8 9 → Play a straight (5 cards max)")
    
    print("\n" + "="*50)
    input("Press Enter to continue...")


#=========================================
# load function
#=========================================

def save_game(player, deck):
    """save current game state to a file"""
    try:
        with open("poker_save.txt", "w") as file:
            file.write(f"round={player.current_round}\n")
            file.write(f"target={player.target_score}\n")
            file.write(f"score={player.round_score}\n")
            file.write(f"plays={player.plays_left}\n")
            file.write(f"discards={player.discards_left}\n")
            file.write(f"bonus={player.global_bonus}\n")
            hand_str = ",".join([str(c) for c in player.hand])
            file.write(f"hand={hand_str}\n")
        print("\n💾 Game saved!")
    except Exception as e:
        print(f"\n❌ Save failed: {e}")

def load_game(player, deck):
    """load game state from a file"""
    try:
        with open("poker_save.txt", "r") as file:
            for line in file:
                line = line.strip()
                if "=" in line:
                    key, value = line.split("=", 1)
                    if key == "round":
                        player.current_round = int(value)
                    elif key == "target":
                        player.target_score = int(value)
                    elif key == "score":
                        player.round_score = int(value)
                    elif key == "plays":
                        player.plays_left = int(value)
                    elif key == "discards":
                        player.discards_left = int(value)
                    elif key == "bonus":
                        player.global_bonus = float(value)
                    elif key == "hand" and value:
                        player.hand = [int(c) for c in value.split(",")]
        print("\n💾 Game loaded!")
        return True
    except FileNotFoundError:
        print("\n❌ No save file found.")
        return False
    except Exception as e:
        print(f"\n❌ Load failed: {e}")
        return False
    

#=========================================
# main loop
#=========================================


def main():
    """Main game function"""
    print("="*50)
    print("🎴  Simplified Poker Card Game  🎴")
    print("="*50)
    print("\n🎯 Goal: Complete 5 rounds!")
    print("Commands: play, discard, deck, end, save, help")
    
    deck = CardDeck()
    player = Player()
    
    choice = input("Load saved game? (y/n): ")
    if choice.lower() == "y":
        if not load_game(player, deck):  # if load fails, draw new hand
            player.hand = deck.draw_cards(7)
    else:
        player.hand = deck.draw_cards(7)  # start fresh
    
    game_running = True
    while game_running:
        player.show_status()
        player.show_hand()
        
        # Check if no plays left and score not reached
        if player.plays_left == 0 and player.round_score < player.target_score:
            print(f"\n😢 Game Over! No plays left!")
            print(f"📊 Final: {player.round_score}/{player.target_score}")
            print(f"🎯 Reached round {player.current_round}")
            game_running = False
            break
        
        print("\n💬 Commands: play [cards] | discard [cards] | deck | end | save | help")
        command = input("> ").strip()
        
        # Save command
        if command == "save":
            save_game(player, deck)
            continue
        
        # Skip command (hidden cheat for demonstration)
        if command == "skip":
            player.round_score = player.target_score  # auto complete
            print("\n🎪 [CHEAT] Auto-completed current round!")
            print(f"📊 Score: {player.round_score}/{player.target_score}")
            print(f"🎉 Round {player.current_round} Complete!")
            
            # Check if game won
            if player.current_round >= 5:  # last round
                print("\n" + "="*50)
                print("🏆 VICTORY! You completed all 5 rounds! 🏆")
                print("="*50)
                game_running = False
                continue
            
            # Choose reward and reset
            choose_and_apply_reward(player, deck, player.current_round)  # apply reward first
            player.reset_round()  # then reset (will preserve extra actions)
            deck.create_deck()  # fresh deck
            player.hand = deck.draw_cards(7)  # new hand
            input("\n⏩ Press Enter for next round...")
            continue
        
        # Help command
        if command == "help":
            show_help()
            continue
        
        # Deck command
        if command == "deck":
            deck.show_deck()
            continue
        
        # End round command
        if command == "end":
            if player.round_score >= player.target_score:  # reached target score
                print(f"\n🎉 Round {player.current_round} Complete!")
                print(f"📊 Score: {player.round_score}/{player.target_score}")
                
                if player.current_round >= 5:  # completed all rounds
                    print("\n" + "="*50)
                    print("🏆 VICTORY! You completed all 5 rounds! 🏆")
                    print("="*50)
                    game_running = False
                    continue
                
                choose_and_apply_reward(player, deck, player.current_round)  # apply reward first
                player.reset_round()  # go to next round (will preserve extra actions)
                deck.create_deck()  # reset deck
                player.hand = deck.draw_cards(7)  # new hand
                input("\n⏩ Press Enter for next round...")
            else:
                print(f"\n😢 Game Over!")
                print(f"📊 Score: {player.round_score}/{player.target_score}")
                print(f"🎯 Reached round {player.current_round}")
                game_running = False
            continue
        
        # Discard command
        if command.startswith("discard"):
            if player.discards_left <= 0:
                print("\n❌ No discards left!")
                continue
            
            parts = command.split()
            if len(parts) < 2:
                print("\n❌ Specify cards to discard!")
                continue
            
            # Check maximum 5 cards
            if len(parts) - 1 > 5:  # parts[0] is "discard", so -1
                print("\n❌ You can only discard up to 5 cards at once!")
                continue
            
            # First, validate ALL cards before discarding any
            temp_hand = player.hand.copy()  # make a copy to check availability
            cards_to_discard = []
            has_invalid = False  # track if any card is invalid
            
            for part in parts[1:]:  # skip first part which is "discard"
                card = parse_card(part)
                if card and card in temp_hand:
                    cards_to_discard.append(card)
                    temp_hand.remove(card)  # remove from temp to prevent duplicates
                elif card:
                    if not has_invalid:  # first error, add blank line
                        print()
                    print(f"❌ {format_card(card)} not in your hand or already selected!")
                    has_invalid = True
                else:
                    if not has_invalid:  # first error, add blank line
                        print()
                    print(f"❌ Invalid card: {part}")
                    has_invalid = True
            
            # If any invalid card, cancel the entire discard
            if has_invalid:
                print("\n❌ Discard cancelled! All cards must be valid.\n")
                continue
            
            # Check if any valid cards to discard
            if len(cards_to_discard) == 0:
                print("\n❌ No valid cards to discard!")
                continue
            
            for card in cards_to_discard:
                player.hand.remove(card)  # remove from actual hand
            
            while len(player.hand) < 7:  # refill to 7 cards
                player.hand.extend(deck.draw_cards(1))
            
            player.discards_left -= 1
            print(f"\n♻️  Discarded {len(cards_to_discard)} cards")
            continue
        
        # Play command
        if command.startswith("play"):
            if player.plays_left <= 0:
                print("\n❌ No plays left!")
                continue
            
            try:
                parts = command.split()
                if len(parts) < 2:
                    print("\n❌ Specify cards to play!")
                    continue
                
                # Check maximum 5 cards
                if len(parts) - 1 > 5:  # parts[0] is "play", so -1
                    print("\n❌ You can only play up to 5 cards at once!")
                    continue
                
                # First, validate ALL cards before playing any
                selected = []
                temp_hand = player.hand.copy()  # make a copy to track availability
                has_invalid = False  # flag to check if any card is invalid
                
                for part in parts[1:]:  # skip "play" command itself
                    card = parse_card(part)
                    if card and card in temp_hand:
                        selected.append(card)
                        temp_hand.remove(card)  # remove to prevent duplicate selection
                    elif card:
                        if not has_invalid:  # first error, add blank line
                            print()
                        print(f"❌ {format_card(card)} not in your hand!")
                        has_invalid = True
                    else:
                        if not has_invalid:  # first error, add blank line
                            print()
                        print(f"❌ Invalid card: {part}")
                        has_invalid = True
                
                # If any invalid card, cancel the entire play
                if has_invalid:
                    print("\n❌ Play cancelled! All cards must be valid.\n")
                    continue
                
                if len(selected) == 0:
                    print("\n❌ No valid cards!")
                    continue
                
                for card in selected:
                    player.hand.remove(card)  # remove cards from hand
                
                result = evaluate_hand(selected)  # check what hand type
                # Apply hand type bonus if exists
                hand_type_mult = player.hand_type_bonus.get(result["type"], 1)  # default 1 if no bonus
                base_score = int(result["sum"] * result["mult"] * hand_type_mult)
                final_score = int(base_score * (1 + player.global_bonus))  # apply global multiplier
                
                player.round_score += final_score
                player.plays_left -= 1
                
                while len(player.hand) < 7:  # refill hand to 7 cards
                    player.hand.extend(deck.draw_cards(1))
                
                print(f"\n✅ Hand: {result['type']}")
                if hand_type_mult > 1:  # show extra multiplier if exists
                    print(f"💎 Cards: {result['sum']} × {result['mult']} × {hand_type_mult} = {base_score}")
                else:
                    print(f"💎 Cards: {result['sum']} × {result['mult']} = {base_score}")
                
                # Show global bonus if active
                if player.global_bonus > 0:  # show global multiplier
                    global_mult_display = 1 + player.global_bonus
                    print(f"⭐ Global: {base_score} × {global_mult_display} = {final_score}")
                else:
                    print(f"🎯 Final: {final_score}")
                
                print(f"💯 Total: {player.round_score}/{player.target_score}")
                
                # Auto-advance if target reached
                if player.round_score >= player.target_score:  # check if won this round
                    print(f"\n🎉 Round {player.current_round} Complete!")
                    
                    if player.current_round >= 5:  
                        print("\n🏆 VICTORY! You completed all 5 rounds! 🏆")
                        game_running = False
                        continue
                    
                    choose_and_apply_reward(player, deck, player.current_round)  # apply reward first
                    player.reset_round()  # then reset (will preserve extra actions)
                    deck.create_deck() 
                    player.hand = deck.draw_cards(7)  
                    input("\n⏩ Press Enter for next round...")
                # Auto-fail if no plays left
                elif player.plays_left == 0:  # no plays left to score
                    print(f"\n😢 Game Over! No plays left!")
                    print(f"📊 Final: {player.round_score}/{player.target_score}")
                    print(f"🎯 Reached round {player.current_round}")
                    game_running = False
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again!")
            continue
        
        print("\nUnknown command!")
    
    print("\nThanks for playing!")


#=========================================
# entry point
#=========================================


if __name__ == "__main__":
    main()
