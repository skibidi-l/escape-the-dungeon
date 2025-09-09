import game
import random



# npc = Character("smily", "npc", Attributes(5, 3, 2))
# print(f"NPC Name: {npc.name}")
# print(f"NPC Max Health: {npc.max_health}")
# print(f"NPC Current Health: {npc.current_health}")

# hero = PlayerCharacter("hero","warrior", Attributes(6,4,3))
# iron_sword = weapon("iron sword", "1d6")
# dagger = weapon("dagger", "1d4")
# magic_sword = weapon("magic sword", "2d6")
# hero.equip(Equipment("sword","leather armor"))





    
# def attack(attacker, defender):
#     damage = attacker["attributes"]["strength"]+ roll_dice(sides_per_die=6)
#     damage = damage - get_armor_value(defender)
#     defender["current_health"] = defender["current_health"] - damage
#     return damage

# def get_armor_value(character):
#     return armor_value[character["equipments"]["armor"]]

    
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
    attr = game.Attributes(8, 4, 2)
    print("yes... a gruelsome fighter who shows NO mercy to his enemies!")
elif class_choice == "2":
    player_class = "Rogue"
    attr = game.Attributes(4, 8, 2)
    print("yes...a sneaky assasin that punishes foes for stepping on his shadow!")
elif class_choice == "3":
    player_class = "Mage"
    attr = game.Attributes(8,4,2)
    print("yes...a mystical wizard who bends the very fabric of reality to his will!")
else:
    print("you made a wrong move lul, idc if u made it by mistake but since you thought smashing your head on the keyboard was a option your getting the WOMP WOMP class, try not to die!!!")
    player_class = "WOMP WOMP"
    attr = game.Attributes(3,3,3)

player = game.PlayerCharacter(character_name, player_class, attr)

print(game.player["attributes"]["strength"])


skeleton_monster = game.NonPlayerCharacter("skeleton","undead",game.Attributes(4, 2, 0))
goblin_monster = game.NonPlayerCharacter("goblin","goblin",game.Attributes(3, 4, 0))
zombie_monster = game.NonPlayerCharacter("zombie","undead",game.Attributes(5, 1, 0))
DRAGON_monster= game.NonPlayerCharacter("DRAGON","dragon",game.Attributes(20,10,5))

monster_list = [skeleton_monster,goblin_monster,zombie_monster,DRAGON_monster]
monster = random.choice(monster_list)
print(f"welcome to the dungeon dungeoneer, to test your might, you will have to duel...a good ole {monster["name"]}!")
print(f"You have encountered a {monster["name"]}!")   
print(f"⚠️ The {monster["name"]} attacks you!⚠️")


loot_list = ["cloth armor","leather armor","chainmail armor","plate armor","dragon scale","sword","dagger","staff","mace","axe"]
while True:
    if player.current_health <= 0:
        break
    action = input("Choose action: attack / dodge / spell: ").lower()
    is_dodged = False
    
    if action == 'attack':
        damage = player.attack(player,monster)
        print(f"You swing your weapon and deal {damage} damage!")

        print(f"the Monster's health is {monster['current_health']}")

    elif action == "dodge":
        has_dodged = player.dodge()
        if has_dodged:
            print("ya dodged the attack, well played...")
        else:
            print("ya tried to dodge but had a skill issue,lul")
    elif action == "spell":
        if attr.mind>=6:
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
        number_of_loot_items = game.roll_dice
        looted_items = game.loot_roll(loot_list)
        loot_gold = game.roll_dice(number_of_dice=5, sides_per_die=4)
        print(f"you found {looted_items} and {loot_gold} gold from the {monster["name"]}, u RICH now")
        player["inventory"].extend(looted_items)
        player["gold"] += loot_gold
        break
    else:
        if not has_dodged:
            hit = monster.attack(player)
            print(f"The {monster["name"]} brandishes a knife, hitting a mighty swing dealing {damage} your player health depleted to {player["current_health"]}")
if player["current_health"] <= 0:
    print("GAME OVER!")
    print("LOL WOMP WOMP")
else:
    print("hey man, this game is made as a draft for me coding class so tysm for playin, hope to see ya again!!!😊")
    print(f" you now have {player["inventory"]} in your inventory and {player["gold"]} gold")
