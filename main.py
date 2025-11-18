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
    print("yes...a sneaky assasin that punishes foes for DARING to step on his shadow!")
elif class_choice == "3":
    player_class = "Mage"
    attr = game.Attributes(8,4,2)
    print("yes...a mystical wizard who bends the very fabric of reality to his will!")
else:
    print("you made a wrong move lul, idc if u made it by mistake but since you thought smashing your head on the keyboard was a option your getting the WOMP WOMP class, try not to die!!!")
    player_class = "WOMP WOMP"
    attr = game.Attributes(3,3,3)

player = game.PlayerCharacter(character_name, player_class, attr)
player.equip_armor(game.Armor("leather armor","1d4"))
player.equip_weapon(game.Weapon("iron sword","1d6"))

player.show_stats()


skeleton_monster = game.NonPlayerCharacter("skeleton","undead",game.Attributes(4, 2, 0))
skeleton_monster.equip_armor(game.Armor("leather armor","leather armor"))
skeleton_monster.equip_weapon(game.Weapon("iron sword","1d6"))
goblin_monster = game.NonPlayerCharacter("goblin","goblin",game.Attributes(3, 4, 0))
goblin_monster.equip_armor(game.Armor("leather armor","leather armor"))
goblin_monster.equip_weapon(game.Weapon("club","1d6"))
zombie_monster = game.NonPlayerCharacter("zombie","undead",game.Attributes(5, 1, 0))
zombie_monster.equip_armor(game.Armor("cloth armor","cloth armor"))
zombie_monster.equip_weapon(game.Weapon("claws","1d4"))
DRAGON_monster= game.NonPlayerCharacter("DRAGON","dragon",game.Attributes(20,10,5))
DRAGON_monster.equip_armor(game.Armor("dragon scale","dragon scale"))
DRAGON_monster.equip_weapon(game.Weapon("fire breath","3d6"))

monster_list = [skeleton_monster,goblin_monster,zombie_monster,DRAGON_monster]

rooms = {
        'cell': {
        'description': 'A cold, dark cell. The door is locked.',
        'east': "Hallway (locked)",
        'item': "key",
        },
    "Hallway": {
        'description': "A dim hallway that leads to a heavy iron gate that acts as a roadblock to the northword path.",
        'west': 'cell',
        'encounter' : True,
        'north': 'Armory',
    },
    "Armory": {
        'description': "A room filled with rusty weapons were a glowing staff beckons you to grab it.",
        'south': 'Hallway',
        'item': "magic staff",
        'encounter' : True,
        'east': "Exit",
    },
    "Exit": {
        'description': "A ancient door that is riddled with arcane symbols, it seems to be locked with a magical seal.",
        'west': "Armory",
    }
}
current_room = 'cell'

print("You find yourself in a dungeon cell. Your goal is to escape and grasp freedom!")
print("type 'exit' to exit the game at any time.")
while True:
    print(f"\nYou are in the {current_room}.")
    print(rooms[current_room]['description'])

    if 'encounter' in rooms[current_room] and rooms[current_room]['encounter'] == True:
        monster = random.choice(monster_list)
        game.encounter(player, monster)
        rooms[current_room]['encounter'] = False
        if player.current_health <= 0:
            print("GAME OVER!")
            print("LOL WOMP WOMP")
            break
    
    if 'item' in rooms[current_room]:
        print(f"You see a {rooms[current_room]['item']} here.")
    
    print("")
    action = input("Where do you wish to go?(go [direction] / take [item] /use [item] / stats / exit / inventory / equip [weapon/armor]): ").strip().lower()
    
    if action == 'Exit':
        print("Exiting the game. Goodbye!")
        break
    elif action == 'stats':
        player.show_stats()
        continue
    elif action.startswith('go '):
        direction = action.split()[1].lower()
        if direction in rooms[current_room]:
            if rooms[current_room][direction].lower().endswith("(locked)"):
                print("The door is locked. You need a key to proceed.")
            else:
                current_room = rooms[current_room][direction]
                if current_room == "Exit":
                    print("Congratulations! You've escaped the dungeon!")
                    break
           
        else:
            print("Invalid direction, try again.")
    elif action.startswith('take '):
        item = action.removeprefix('take ').lower()
        if 'item' in rooms[current_room] and item == rooms[current_room]['item']:
            player.inventory.append(game.QuestItem(rooms[current_room].pop('item')))
            print(f"You picked up the {item}.")
        else:
             print("No such item is here.")
    elif action.startswith('use '):
        item = action.split()[1].lower()
        if player.is_in_inventory(item):
            if item == 'key' and current_room == 'cell':
                player.use_item('key')
                print("You used the key to unlock the gate to a dilapidated hallway.")
                rooms['cell']['east'] = 'Hallway'
                rooms['cell']['description'] = rooms['cell']['description'].replace("The door is locked.","The door is now unlocked.")
                #player.inventory.remove('key')
            else:
                print(f"You can't use the {item} here.")
        else:
            print(f"you don't have the {item} in your inventory.")
    elif action == 'inventory':
        if player.inventory:
            print("Your inventory contains:")
            for item in player.inventory:
                print(f"- {item.name}")
        else:
            print("Your inventory is empty.")

    elif action.startswith('equip '):
        equip_item = action.removeprefix('equip ').lower()
        if player.is_in_inventory(equip_item):
            player.equip(equip_item)

# monster = random.choice(monster_list)
# game.encounter(player, monster)


# if player.current_health <= 0:
#     print("GAME OVER!")
#     print("LOL WOMP WOMP")
# else:
#     print("hey man, this game is made as a draft for me coding class so tysm for playin, hope to see ya again!!!😊")
#     print(f" you now have {player.inventory} in your inventory and {player.gold} gold")
