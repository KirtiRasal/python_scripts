import random
from random import shuffle 

Playerchar = [{"name": "Ronaldo", "Shoot" : 9.5, "Passing": 6.0, "Speed": 9.0},
        {"name": "Messi", "Shoot" : 9.0, "Passing": 9.5, "Speed": 7.0},
        {"name": "Ramos", "Shoot" : 7.0, "Passing": 7.0, "Speed": 5.0},
        {"name": "Buffon", "Shoot" : 6.0, "Passing": 4.0, "Speed": 3.0},
        {"name": "Neymar", "Shoot" : 8.5, "Passing": 9.0, "Speed": 9.5},
        {"name": "Iniesta", "Shoot" : 7.5, "Passing": 10.0, "Speed": 5.5},
        {"name": "Pele", "Shoot" : 9.8, "Passing": 9.7, "Speed": 9.8},
        {"name": "Maradona", "Shoot" : 10.0, "Passing": 9.9, "Speed": 10.0},
        {"name": "Mbappe", "Shoot" : 8.4, "Passing": 9.1, "Speed": 9.9},
        {"name": "Suarez", "Shoot" : 9.2, "Passing": 7.5, "Speed": 7.5}]

class Deck :
        
    def __init__(self) :
        print("Creating New Ordered Deck")
        self.allcards = [(key)for key in Playerchar]

    def shuffle(self):
        print("Shuffling Deck")
        shuffle(self.allcards)

    def split_in_half(self):
        return (self.allcards[:5],self.allcards[5:])

class Hand:
    """
    This is for the players. Each player has a Hand and can add or remove cards from that hand.
    So we will perform the add and remove operation here.
    """
    def __init__(self,cards):
        self.cards = cards

    def __str__(self):
        return "Contains {} cards".format(len(self.cards))

    def add(self,added_cards):
        self.cards.extend(added_cards)

    def remove_card(self):
        return self.cards.pop()


class Player:
    """
    This class will has the name of the player.
    It will also has the instance of Hand class object.
    """

    def __init__(self,name,hand):
        self.name = name
        self.hand = hand

    def play_card(self):
        drawn_card = self.hand.remove_card()
        print("{} has placed: {}".format(self.name,drawn_card))
        print('\n')
        return drawn_card

    def still_has_cards(self):
        """
        Returns True if player still has cards
        """
        return len(self.hand.cards) != 0

print ("Let's start the game")

# Create New Deck and split in half
d = Deck()
d.shuffle()
half1,half2 = d.split_in_half()

# Create Both Players
name1 = input("What is your name player1? ")
user1 = Player(name1,Hand(half1))    
name2 = input("What is your name player2? ")
user2 = Player(name2,Hand(half2))

# Set Counters
total_rounds = 0
User1_score = 0
User2_score = 0
Outdated = []

#Dice roll for the two players
user1_roll = random.randint(1,6)
user2_roll = random.randint(1,6)

#Dice roll winner will specify the characteristic choice : This applies only for the first round.
if user1_roll == user2_roll :
    print ("Rolling the dice again")
    user1_roll = random.randint(1,6)
    user2_roll = random.randint(1,6)

if user1_roll > user2_roll :
    print( user1.name + " will start ")
    StartingPlayer = (user1)
      
else :
    print( user2.name + " will start ")
    StartingPlayer = (user2)

while user1.still_has_cards() and user2.still_has_cards():
    total_rounds += 1
    print("It is time for a new round!")
    print("Here are the current standings: ")
    print(user1.name+" card count: "+str(len(user1.hand.cards)))
    print(user2.name+" card count: "+str(len(user2.hand.cards)))
    print("Both players play a card!")
    print('\n')
   
    #Spells counter 
    Godspell_counter = [0,0]
    Resurrectspell_counter = [0,0]
    
    if total_rounds <= 1 :
        
        if StartingPlayer == (user1) :
            first_user = user1.play_card()

            choice = input(user1.name + " what is your choice for characteristics of players?(Shoot, Passing, Speed) ")

            second_user = user2.play_card()
    
        if StartingPlayer == (user2) :
            second_user = user2.play_card()

            choice = input(user2.name + " what is your choice for characteristics of players?(Shoot, Passing, Speed) ")

            first_user = user1.play_card()
        
        if choice == 'Shoot' :
            var1 = first_user['Shoot']
            print("The card value of " +  user1.name + " is " , var1)
    
        if choice == 'Passing' :
            var1 = first_user['Passing']
            print("The card value of " +  user1.name + " is " , var1)
    
        if choice == 'Speed' :
            var1 = first_user['Speed']
            print("The card value of " +  user1.name + " is " , var1)
     

        if choice == 'Shoot' :
            var2 = second_user['Shoot']
            print("The card value of " +  user2.name + " is " , var2)
     
        if choice == 'Passing' :
            var2 = second_user['Passing']
            print("The card value of " +  user2.name + " is " , var2)
    
        if choice == 'Speed' :
            var2 = second_user['Speed']
            print("The card value of " +  user2.name + " is " , var2)

    #Points calculation
        if var1 > var2 :
            print( user1.name + " gets a point! ")
            StartingPlayer = (user1)
            User1_score = User1_score + 1

        if var2 > var1 :
            print( user2.name + " gets a point! " )
            StartingPlayer = (user2)
            User2_score = User2_score + 1
    
        print('\n')
          
        Outdated.append(first_user)
        Outdated.append(second_user)

        print(user1.name , " scored " , User1_score , " point! ")
        print(user2.name , " scored " , User2_score , " point! ")


    if Resurrectspell_counter[0] == 1 :
        print(user1.name + " : You have already used Resurrectspell. You cannot use again in this round! ")

    if Godspell_counter[0] == 1 :
        print (user1.name + " : You have already used Resurrectspell. You cannot use again in this round!")
    
    if Resurrectspell_counter[1] == 1 :
        print(user2.name + " : You have already used Resurrectspell. You cannot use again in this round! ")

    if Godspell_counter[1] == 1 :
        print (user1.name + " : You have already used Resurrectspell. You cannot use again in this round!")

    if total_rounds > 1 :

        if StartingPlayer == (user1) :
            spellchoice1 = input("Do you want to select any of Spells " + user1.name + " ? Y/N ")
            if spellchoice1 == "Y" :
                spellchoice_user1 = input ("Which spell do you want to use? (G, R) ")
                if spellchoice_user1 == "R" :
                    Resurrectspell_counter[0] =+ 1
                    random.choice(Outdated)  
                    user1.hand.cards[0] = random.choice(Outdated)                
                    first_user = user1.play_card()
                    choice = input(user1.name + " what is your choice for characteristics of players?(Shoot, Passing, Speed) ")
                    second_user = user2.play_card()       
                
                if spellchoice_user1 == "G" :
                    Godspell_counter[0] =+ 1
                    n = input("Please mention the card number you want to choose from 0 to" + str({len(user2.hand.cards)-1}))
                    n = int(n)
                    user2.hand.cards[n]
                    user2.hand.cards[0] = (user2.hand.cards[n])
                    first_user = user1.play_card()
                    choice = input(user1.name + " what is your choice for characteristics of players?(Shoot, Passing, Speed) ")
                    second_user = user2.play_card()
            
            else :
                first_user = user1.play_card()        
                choice = input(user1.name + " what is your choice for characteristics of players?(Shoot, Passing, Speed) ")
                second_user = user2.play_card()
        
        if StartingPlayer == (user2) :
            spellchoice2 = input("Do you want to select any of Spells " + user2.name + " ? Y/N ")
            if spellchoice2 == "Y" : 
                spellchoice_user2 = input ("Which spell do you want to use? (G, R) ")
                if spellchoice_user2 == "R" :
                    Resurrectspell_counter[1] =+ 1
                    random.choice(Outdated) 
                    user2.hand.cards[0] = random.choice(Outdated) 
                    second_user = user2.play_card()
                    choice = input(user1.name + " what is your choice for characteristics of players?(Shoot, Passing, Speed) ")
                    first_user = user1.play_card()
            
                if spellchoice_user2 == "G" :
                    Godspell_counter[1] =+ 1
                    n = input("Please mention the card number you want to choose from 0 to" + str({len(user1.hand.cards)-1}))
                    n = int(n)
                    user1.hand.cards[n]
                    user1.hand.cards[0] = (user1.hand.cards[n])
                    second_user = user2.play_card()
                    choice = input(user2.name + " what is your choice for characteristics of players?(Shoot, Passing, Speed) ")
                    first_user = user1.play_card()
                               
            else :
                first_user = user1.play_card()        
                choice = input(user1.name + " what is your choice for characteristics of players?(Shoot, Passing, Speed) ")
                second_user = user2.play_card() 
    
       

    # Check to see who had higher rank
    
        if choice == 'Shoot' :
            var1 = first_user['Shoot']
            print("The card value of " +  user1.name + " is " , var1)
    
        if choice == 'Passing' :
            var1 = first_user['Passing']
            print("The card value of " +  user1.name + " is " , var1)
    
        if choice == 'Speed' :
            var1 = first_user['Speed']
            print("The card value of " +  user1.name + " is " , var1)
     

        if choice == 'Shoot' :
            var2 = second_user['Shoot']
            print("The card value of " +  user2.name + " is " , var2)
     
        if choice == 'Passing' :
            var2 = second_user['Passing']
            print("The card value of " +  user2.name + " is " , var2)
    
        if choice == 'Speed' :
            var2 = second_user['Speed']
            print("The card value of " +  user2.name + " is " , var2)

    #Points calculation
        if var1 > var2 :
            print( user1.name + " gets a point! ")
            StartingPlayer = (user1)
            User1_score = User1_score + 1

        if var2 > var1 :
            print( user2.name + " gets a point! " )
            StartingPlayer = (user2)
            User2_score = User2_score + 1
    
        print('\n')
          
        Outdated.append(first_user)
        Outdated.append(second_user)

        print(user1.name , " scored " , User1_score , " point! ")
        print(user2.name , " scored " , User2_score , " point! ")

if User1_score > User2_score :
    print( user1.name + " is the winner! ")

else : 
    print( user2.name + " is the winner! ")