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
    strength, agility, mind = 8, 4, 2
    print("yes... a gruelsome fighter who shows NO mercy to his enemies!")
elif class_choice == "2":
    player_class = "Rogue"
    strength, agility, mind = 4, 8, 2
    print("yes...a sneaky assasin that punishes foes for stepping on his shadow!")
elif class_choice == "3":
    player_class = "Mage"
    strength, agility, mind = 2, 4, 8
    print
else:
    print("you made a wrong move lul, idc if u made it by mistake but since you thought smashing your head on the keyboard was a option your getting the WOMP WOMP class, try not to die!!!")
    player_class = "WOMP WOMP"
    strength, agility, mind = 1, 1, 1
player = {
    "name":character_name,
    "class": player_class,
    "attributes":{
        "strength": strength,
        "agility": agility,
        "mind": mind,
    },
    "max_health": 5 * strength,
    "current_health": 5 * strength,
    "gold": 5,
    "inventory": []
}


skeleton_monster = ("skeleton",30,4)
goblin_monster = ("goblin",35,5)
zombie_monster = ("zombie",20,6)
DRAGON_monster= ("DRAGON",100,10)
monster_list = [skeleton_monster,goblin_monster,zombie_monster,DRAGON_monster]
monster_index = random.randint(0,len(monster_list) - 1)
monster_name,monster_health,monster_damage = monster_list[monster_index]
print(f"welcome to the dungeon dungeoneer, to test your might, you will have to duel...a good ole {monster_name,monster_health,monster_damage}!")
print(f"You have encountered a {monster_name}!")   
print(f"⚠️ The {monster_name} attacks you!⚠️")
loot_list = ["armor","sword","dagger","staff","mace","axe","armor"]
while True:
    if player["current_health"] <= 0:
        break
    action = input("Choose action: attack / dodge / spell: ").lower()
    is_dodged = False
    
    if action == 'attack':
        damage = strength + random.randint(1, 6)
        monster_health -= damage
        print(f"You swing your weapon and deal {damage} damage!")
        print(f"the Monster is{monster_health}")
    elif action == "dodge":
        dodge_chance = agility * 5
        if random.randint(1,100)<= dodge_chance:
            is_dodged = True
            print("ya dodged the attack, well played...")
        else:
            is_dodged = False
            print("ya tried to dodge but had a skill issue,lul")
            player["current_health"] -= 5
            print(f"ya got hit, HP remaining:{player["current_health"]}")
    elif action == "spell":
        if mind>=6:
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
        player["inventory"].append(loot_list[loot_index])
        player["gold"] += loot_gold
        break
    else:
        if is_dodged == False:
            hit = random.randint(1,6) + 2
            player["current_health"] -= hit
            print(f"The {monster_name} brandishes a knife, hitting a mighty swing dealing {hit} your player health depleted to {player["current_health"]}")
if player["current_health"] <= 0:
    print("GAME OVER!")
    print("LOL WOMP WOMP")
else:
    print("hey man, this game is made as a draft for me coding class so tysm for playin, hope to see ya again!!!😊")
    print(f" you now have {player["inventory"]} in your inventory and {player["gold"]} gold")
