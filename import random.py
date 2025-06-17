import random

# --- Create Character ---
print("Welcome to Escape the Dungeon!")
character_name = input("What is your name, BRAVE adventurer??? ")

# --- Class Selection ---
print("Choose your class:")
print("1. Warrior (High Strength)")
print("2. Rogue (High Agility)")
print("3. Mage (High Magic)")

class_choice = input("Enter 1, 2, or 3: ")

if class_choice == "1":
    player_class = "Warrior"
    strength, agility, magic = 8, 4, 2
    print("yes... a gruelsome fighter who shows NO mercy to his enemies!")
elif class_choice == "2":
    player_class = "Rogue"
    strength, agility, magic = 4, 8, 2
    print("yes...a sneaky assasin that punishes foes for stepping on his shadow!")
elif class_choice == "3":
    player_class = "Mage"
    strength, agility, magic = 2, 4, 8
    print
else:
    print("you made a wrong move lul, idc if u made it by mistake but since you thought smashing your head on the keyboard was a option your getting the WOMP WOMP class, try not to die!!!")
    player_class = "WOMP WOMP"
    strength, agility, magic = 1, 1, 1

health = 100
gold = 5
inventory = []

monster_list = ["skeleton","goblin","zombie"]
monster_health_list = [30,35,20]
monster_index = random.randint(0,len(monster_list) - 1)
monster = monster_list[monster_index]
print(f"welcome to the dungeon dungeoneer, to test your might, you will have to duel...a good ole {monster}!")
print(f"You have encountered a {monster}!")   
print(f"⚠️ The {monster} attacks you!⚠️")
monster_health = 30
loot_list = ["armor","sword","dagger","staff","mace","axe","armor"]
while True:
    action = input("Choose action: attack / dodge / spell: ").lower()
    is_dodged = False
    
    if action == 'attack':
        damage = strength + random.randint(1, 6)
        monster_health -= damage
        print(f"You swing your weapon and deal {damage} damage!")
        print(f"the monster is{monster_health}")
    elif action == "dodge":
        dodge_chance = agility * 5
        if random.randint(1,100)<= dodge_chance:
            is_dodged = True
            print("ya dodged the attack, well played...")
        else:
            is_dodged = False
            print("ya tried to dodge but had a skill issue,lul")
            health -= 5
            print(f"ya got hit, HP remaining:{health}")
    elif action == "spell":
        if magic>=6:
            print("ya cast a powerful fireball")
            monster_health =0
            print("well done ")
        else:
            print("ya fail to cast the spell.")
    else:
        print("dumdass dont smash your keyboard!!!")
    if monster_health <= 0:
        print("congrats,your SOOOO good, well this is only thy beginning")
        print("you may earn these items:")
        for loot in loot_list:
            print(loot)
        print("LET'S GO GAMBLINGGG!!! picking your rewards...")
        loot_index = random.randint(0,len(loot_list) - 1)
        loot_gold = random.randint(5,20)
        print(f"you found one {loot_list[loot_index]} and {loot_gold} gold, u RICH now")
        inventory.append(loot_list[loot_index])
        gold += loot_gold
        break
    else:
        if is_dodged == False:
            hit = random.randint(1,6) + 2
            health -= hit
            print(f"The {monster} brandishes a knife, hitting a mighty swing dealing {hit} your health depleted to {health}")
print("hey man, this game is made as a draft for me coding class so tysm for playin, hope to see ya again!!!😊")
print(f" you now have {inventory} in your inventory and {gold} gold")
