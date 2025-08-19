import random
class Character:
    name = ""
    max_health = 0
    current_health = 0

npc = Character()
npc.name = "smily"
npc.max_health = 30
npc.current_health = 30

print(f"NPC Name: {npc.name}")
print(f"NPC Max Health: {npc.max_health}")
print(f"NPC Current Health: {npc.current_health}")

def roll_dice( sides_per_die, number_of_dice=1):
    total = 0
    for _ in range(number_of_dice):
        total += random.randint(1, sides_per_die)
    return total

def loot_roll(loot_list):
    number_of_loot_items = roll_dice(sides_per_die=3)
    looted_items = []
    for _ in range(number_of_loot_items):
        loot_item = random.choice(loot_list)
        looted_items.append(loot_item)
    return looted_items
    
def attack(attacker, defender):
    damage = attacker["attributes"]["strength"]+ roll_dice(sides_per_die=6)
    damage = damage - get_armor_value(defender)
    defender["current_health"] = defender["current_health"] - damage
    return damage

def get_armor_value(character):
    return armor_value[character["equipments"]["armor"]]

    
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
    "equipments": {
        "armor": "leather armor",  # Default armor
    },
    # Health is calculated based on strength
    "max_health": 5 * strength,
    "current_health": 5 * strength,
    "gold": 5,
    "inventory": []
}

print(player["attributes"]["strength"])


skeleton_monster = {
    "name": "skeleton",
    "attributes":{
        "strength": 4,
        "agility": 2,
        "mind": 0,
    },
    "equipments": {
        "armor": "cloth armor",
    },
    "max_health": 20,
    "current_health": 20,
}
goblin_monster = {
    "name": "goblin",
    "attributes":{
        "strength": 3,
        "agility": 4,
        "mind": 0,
    },
    "equipments": {
        "armor": "leather armor",
    },
    "max_health": 20,
    "current_health": 20,
}
zombie_monster = {
    "name": "zombie",
    "attributes":{
        "strength": 5,
        "agility": 1,
        "mind": 0,
    },
    "equipments": {
        "armor": "cloth armor",
    },
    "max_health": 35,
    "current_health": 35,
}
DRAGON_monster= {
    "name": "DRAGON",
    "attributes":{
        "strength": 20,
        "agility": 10,
        "mind": 5,   
    },
    "equipments": {
        "armor": "dragon scale",
    },
    "max_health": 100,
    "current_health": 100,
}

monster_list = [skeleton_monster,goblin_monster,zombie_monster,DRAGON_monster]
monster = random.choice(monster_list)
print(f"welcome to the dungeon dungeoneer, to test your might, you will have to duel...a good ole {monster["name"]}!")
print(f"You have encountered a {monster["name"]}!")   
print(f"⚠️ The {monster["name"]} attacks you!⚠️")
armor_value = {
    "none": 0,
    "cloth armor": 1,
    "leather armor": 2,
    "chainmail armor": 3,
    "plate armor": 4,
    "dragon scale": 5,
}

loot_list = ["cloth armor","leather armor","chainmail armor","plate armor","dragon scale","sword","dagger","staff","mace","axe"]
while True:
    if player["current_health"] <= 0:
        break
    action = input("Choose action: attack / dodge / spell: ").lower()
    is_dodged = False
    
    if action == 'attack':
        damage = attack(player,monster)
        print(f"You swing your weapon and deal {damage} damage!")

        print(f"the Monster's health is {monster['current_health']}")

    elif action == "dodge":
        dodge_chance = agility * 5
        if roll_dice(sides_per_die=100) <= dodge_chance:
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
            monster["current_health"] <= 0
            print("well done ")
        else:
            print("ya fail to cast the spell.")
    else:
        print("dumdass dont smash your keyboard!!!")
    if monster["current_health"] <= 0:
        print(f"congrats,your SOOOO good, well this is only thy beginning, you have slain a {monster["name"]}!")
        print("you may earn these items:")
        for loot in loot_list:
            print(loot)
        print("LET'S GO GAMBLINGGG!!! picking your rewards...")
        number_of_loot_items = roll_dice
        looted_items = loot_roll(loot_list)
        loot_gold = roll_dice(number_of_dice=5, sides_per_die=4)
        print(f"you found {looted_items} and {loot_gold} gold from the {monster["name"]}, u RICH now")
        player["inventory"].extend(looted_items)
        player["gold"] += loot_gold
        break
    else:
        if is_dodged == False:
            damage = attack(monster,player)
            print(f"The {monster["name"]} brandishes a knife, hitting a mighty swing dealing {damage} your player health depleted to {player["current_health"]}")
if player["current_health"] <= 0:
    print("GAME OVER!")
    print("LOL WOMP WOMP")
else:
    print("hey man, this game is made as a draft for me coding class so tysm for playin, hope to see ya again!!!😊")
    print(f" you now have {player["inventory"]} in your inventory and {player["gold"]} gold")
