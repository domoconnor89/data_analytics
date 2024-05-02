## Premise of the game is to find & buy a record.
## Start with 50€, with which you buy a coffe to exchange for advice, leading to target location to buy record.

## The variations in gameplay;
## * winning route = CAFE -> SSR -> CLK -> ST
## * losing route = visit CAFE more then once, leaving not enough money to buy the record.
## * other losing route = spend all money on coffees, leaving nothing for the record. 
## * unable to access ST if coffee has been collected but not exchanged / drunk (given option to drink in order to access).
## * if gameplay resolves to a loss, given the option to RESTART. Budget returns to 50€ and list cleared of collected items.

import time
items = [] #To be filled with "coffee" for each CAFE visit and "advice" when when rec. from CLK.
yn = ["YES", "NO"] #yes/no option for "user=" to restart.
budget = 50 #cash variable, reducing by 5 after each cafe visit.
advice = '"Ohhhh that coffee is goooood!\n But no Marv here for you, my friend. \n Go to Soul Trade and ask behind the counter. \n They\'d never keep a record like that on the shelf!"'
location = "start"

#Key = location options, Values = available paths.
options = {
    "start": ["CAFE", "SSR", "ST"],
    "restart": ["CAFE", "SSR", "ST"],
    "CAFE": ["ST", "SSR"],
    "SSR": ["CLK", "ST", "CAFE"],
    "ST": [],
    "CLK": [],
    "end": ["end"]}
#the values/paths for ST & CLK are left empty here, but will be...
#... populated differently depending on items collected once location reached.

print ("**** READY PLAYER 1 ****")
name = input("Please enter your name: ").upper()

print(f"\nWelcome {name}!\nYou\'re mission today: Find a copy of one of Marvin Gaye\'s most influential records... \nYou're journey begins at Schönleinstraße and you have {budget}€ in your pocket...\n\n! LET\'S GET IT ON !\n\nIf you would like to start the day with a caffeine boost, you can go to the Coffee Shop [CAFE]...\nOr if you want to get straight into searching, you can visit Static Shock Records[SSR] or Soul Trade Records[ST]...")
print("\ndestinations... ", options[location]) #next step option
location = input("input: ").upper() #next step player input
while location not in options["start"]: #select viable option prompt
    print("Sorry, that's not an option!Remember, you can only go to:", options["start"])
    location = input("where would you like to go? ").upper()

while location in options and location != "end":
        
# in Cafe
    if location == "CAFE":
        items.extend (["coffee"])
        budget = budget - 5
        if budget >= 1: ## You still have cash and can continue ##
            print (f"\nYou've decided to buy a coffee. This means you're down to {budget}€... be careful with your cash!\nAnyway... we're on this jouney to buy a record.\n\nThis coffee has been made to-go... but where shall we go?\n- Soul Trade[ST]\n- Static Shock Records[SSR]")
            # print(f"You have collected the item: {items}") # ITEM CHECK #
            print("\ndestinations... ", options[location]) #next location options
            location = input("input: ").upper() #user selection
            while location not in options["CAFE"]: #select viable option prompt
                print("Sorry, that's not an option! Remember, you can only go to:", options["CAFE"])
                location = input("where would you like to go? ").upper()
        else: ## LOSS - you have run out of money ##
            print("\n... ahhhhh you dufus! You've spent your last €5 on ANOTHER coffee!!!\nHow can you buy a record if you have no cash left!?!?!?\n\n!!GAME OVER!!\n\nYOU'VE SPENT ALL OF YOUR MONEY\nBut would you like to play again? ") 
            print("\nType... ", yn) # yes/no option list #
            user = input("input: ").upper() # next step input #
            while user not in yn: #select viable option prompt
                print("\nSorry, that's not an option! Remember, you can only pick:", yn)
                user = input("input: ").upper()
            if user == "NO": 
                location = "end" ## Send player to game_over ##
            if user == "YES": 
                location = "restart" ## Send player to Restart ##

# in SSR  
    elif location == "SSR":
        print(f"\nYou've made your way Static Shock... \nand what a shock... this place is a mess!\nThere's no way you'll find the record you need in here, {name}! \nMaybe talking to the clerk will help, or we can carry on over to Soul Trade or the Cafe.\n\nWhat do you want to do...\n- ask the clerk[CLK]?\n- go over to Soul Trade[ST]?\n- Go to the Coffee Shop[CAFE]?")
        print("\ndestinations... ", options[location]) #next step option
        location = input("input: ").upper() #next step option
        while location not in options["SSR"]:
            print("\nSorry, that's not an option! Remember, you can only go to:", options["SSR"])
            location = input("where would you like to go? ").upper()

# with clk: coffee not collected  
    elif location == "CLK" and "coffee" not in items:
        options["CLK"] = "ST", "CAFE"
        location == "CLK"
        print("\nYou try to speak with the clerk...\nBut wait... this guy is huuuuung-over. They're making no sense! Do you want to...\n- Try your luck at Soul Trade [ST]?\n- Or grab a coffee [CAFE]?")
        print("\ndestinations... ", options["CLK"]) #next step option
        location = input("input: ").upper() #next step option
        while location not in options["CLK"]: #select viable option prompt
            print("Sorry, that's not an option! Remember, you can only go to:", options["CLK"])
            # print("Remember, you can only go to:", options[location]) ## This feeds the location options back as empty, hence manual input
            location = input("where would you like to go? ").upper()

# with clk: coffee collected
    elif location == "CLK" and "coffee" in items:
        options["CLK"] = ["CAFE", "ST"]
        location == "CLK"
        print((f"\nYou want to speak with the clerk...\nBut wait... this guy is huuuuung-over. They're making no sense! \nThankfully, you have the power of caffiene in your hands! \n... you push the coffee under their nose aaaaaaand... \nYES! They take it, they drink it, they instantly perk-up! \nYou ask if they have Marvin Gaye's - Let's Get it On...\nThey don't... schade... but they do have a pearl of wisdom for you...\n\n {advice}\n"))
        # print(f"You currently have ... {items} ... items") ## ITEM CHECK ##
        items[:] = (value for value in items if value != "coffee") ## This removes all coffees, if multiple bought - found on stack overflow ##
        # print(f"You currently have ... {items} ... items") ## ITEM CHECK ##
        items.extend (["advice"])
        # print(f"You currently have ... {items} ... items") ## ITEM CHECK ##
        print(f"\nSo... what d'you wanna do, {name}?\n- Grab another coffee [CAFE]?\n- Or, follow the clerk's advice and hop over to Soul Trade [ST]?")
        print("\ndestinations... ", options["CLK"]) #next step option
        location = input("input: ").upper() #next step option
        while location not in options["CLK"]: #select viable option prompt
            print("Sorry, that's not an option! Remember, you can only go to:", options["CLK"])
            # print("Remember, you can only go to:", options[location]) ## This feeds the location options back as empty, hence manual input
            location = input("where would you like to go? ").upper()

# in Soul Trade: coffee collected
    elif location == "ST" and "coffee" in items:
        print("\nYou've entered Soul Trade Records... what a palace! \nEverything is categorised and alphabetised... Amazing!\n")
    # option to drink the coffee
        print("But wait... \nthe clerk spots the coffee in your hand... \nThat's not allowed in this store, friend! \n\nDo you want to drink the coffee and carry on shopping?",yn)      
        user = input("input: ").upper() # player restart input
        while user not in yn: #select viable option prompt
            print("\nSorry, that's not an option!")
            print("Remember, you can only pick:", yn)
            user = input("input: ").upper()
    # Deciding to drink coffee in order to access ST    
        if user == "YES":
            options["ST"] = ["SSR", "CAFE"] ## Populating dictionary... ST key with values ##
            items[:] = (value for value in items if value != "coffee") ## This removes all coffees, if multiple bought - found on stack overflow ##
            print("\nYou're in and you're shopping! But... \nIt doesn\'t take you very long to realise... there's no Marvin Gaye on these shelves!\nShall we go to the Cafe [CAFE]? or check-out Static Shock [SSR]?")
            print("\ndestinations... ", options[location]) #next step option
            location = input("input: ").upper() #player input
            while location not in options["ST"]: #select viable option prompt
                print("Sorry, that's not an option!")
                # print("Remember, you can only go to:", options[location]) ## This feeds the location options back as empty, hence manual input
                print("Remember, you can only go to:", options["ST"])
                location = input("where would you like to go? ").upper()
    # Deciding not to drink the coffee and search elsewhere
        if user == "NO":
            options["ST"] = ["SSR"] ## Populating dictionary... ST key with values ##
            print("\nYou're turned away but, no fear, the journey continues...\n\nMaybe we should search over at Static Shock Records[SSR]?")
            print("\ndestinations... ", options[location]) #next step option
            location = input("input: ").upper() #player input
            while location not in options["ST"]: #select viable option prompt
                print("Sorry, that's not an option!")
                # print("Remember, you can only go to:", options[location]) ## This feeds the location options back as empty, hence manual input
                print("Remember, you can only go to:", options["ST"])
                location = input("where would you like to go? ").upper()

# in Soul Trade: coffee + advice not collected
    elif location == "ST" and "coffee" not in items and "advice" not in items:
        options["ST"] = ["SSR", "CAFE"] ## Populating dictionary... ST key with values ##
        location == "ST"
        print("\nYou've entered Soul Trade Records... what a palace! \nEverything is categorised and alphabetised... Amazing!\nBut... it doesn\'t take you very long to realise... no Marvin Gaye on these shelves!\nShall we go to the Cafe [CAFE]? or check-out Static Shock [SSR]?")
        print("\ndestinations... ", options["ST"]) #next step option
        location = input("input: ").upper() #next step option
        while location not in options["ST"]: #select viable option prompt
            print("Sorry, that's not an option!")
            print("Remember, you can only go to:", options["ST"])
            location = input("where would you like to go? ").upper()

# LOSS in Soul Trade: advice is collected and Budget too low
    elif location == "ST" and "coffee" not in items and "advice" in items and budget <= 44:
        print("\nYou've entered Soul Trade Records... what a palace! \nEverything is categorised and alphabetised... Amazing!\nYou've spoken with our friend at Static and you follow their advice\nYou chat with the person behind the counter... and...\nSure enough, they have the record!!!\n\nBUT............... \nYou don't have enough cash\n\n !OHHH NOOO!\n!!GAME!OVER!!\n\n Would you like to play again? ")
        print("\nType... ", yn) # yes/no restart option
        user = input("input: ").upper() # player restart input
        while user not in yn: #select viable option prompt
            print("Sorry, that's not an option! Remember, you can only pick:", yn)
            user = input("input: ").upper()
        if user == "NO":
            location = "end" # move to gameover loss message
        if user == "YES":
            location = "restart" # move to play again
        

# WIN in Soul Trade: coffee not collected BUT advice is collected and Budget is good!
    elif location == "ST" and "coffee" not in items and "advice" in items and budget >= 45:
        options["ST"] = ["end"]
        print("\nYou've entered Soul Trade Records... what a palace! \nEverything is categorised and alphabetised... Amazing!\nYou've spoken with our friend at Static and you follow their advice \nYou chat with the person behind the counter...and...\n.......\n.........\n\nSure enough, they have the record!!!\nYou hand over all of your money and yesssss... YOU WIN!!!!")
        location = "end"

## RESTART ##    
    elif location == "restart":
        items = []
        budget = 50
        print(f"\n\n*+*+*+*+*+*+*+*+*+*+*+*+\n\n*+*+*+*+*+*+*+*+*+*+*+*+\n\nOK... let's go again!!!\n\nYou\'re mission remains the same {name}: Find a copy of one of Marvin Gaye\'s most influential records... \nYou're back at Schönleinstraße and once again you have {budget}€ in your pocket...\n\n! LET\'S GET IT ON !\n\nIf you would like to start off with a caffeine boost, you can go to the Coffee Shop [CAFE]...\nOr if you want to jump straight into searching, you can visit Static Shock Records[SSR] or Soul Trade Records[ST]...")
        print("destinations... ", options[location]) #next step option
        location = input("input: ").upper() #next step option
        while location not in options["start"]: #select viable option prompt
            print("Sorry, that's not an option! Remember, you can only go to:", options["start"])
            location = input("where would you like to go? ").upper() 

## WINNER END GAME ##
if location == "end" and budget >= 44:
    print("")
    for i in range(15):
        print(".: !WINNER! :.:.: !WINNER! :.:.: !WINNER! :.")
        time.sleep(0.25)
    print("")

## CAN'T AFFORD RECORD END GAME ##
elif location == "end" and budget <= 44 and "advice" in items:
    print("")
    for i in range(15):
        print("(-_- ) .:YOU LOSE:. ( -_-)")
        time.sleep(0.25)
    print("\n!PLAY AGAIN SOON!")

## NO CASH GAME END ##    
if budget == 0:
    print("")
    for i in range(15):
        print("(╥﹏╥) .:YOU LOSE:. (╥﹏╥)")
        time.sleep(0.25)
    print("\n!PLAY AGAIN SOON!\n")