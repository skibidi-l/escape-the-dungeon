import game
import random

class GameState:
    NOT_STARTED = "not_started"
    CHAR_CREATION = "character_creation"
    EXPLORATION = "exploration"
    COMBAT = "combat"
    COMPLETED = "completed"
    GAME_OVER = "game_over"

    def get_available_actions(self):
        pass

    def reponse_to_command(self, command: str):
        pass
class LetStartState(GameState):
    def __init__(self):
        self.available_actions = ["start"]

    def get_available_actions(self) -> dict:
        return f"Available actions: {', '.join(self.available_actions)}"
    
    def reponse_to_command(self, command: str) -> dict:
        if command == "start":
            return {"game_response": "welcome to Escape the Dungeon! Your adventure begins now."}
        else:
            return {"game_response": "Please type 'start' to begin your adventure!"}

class GameEngine:
    NOT_STARTED = "not_started"
    CHAR_CREATION = "character_creation"
    EXPLORATION = "exploration"
    COMBAT = "combat"
    COMPLETED = "completed"
    GAME_OVER = "game_over"


    def __init__(self):
        self.player = None
        self.current_room = "Cell"
        self.rooms = {
            'Cell': {
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

        self.monsters = [skeleton_monster,goblin_monster,zombie_monster,DRAGON_monster]
        self.state = self.NOT_STARTED
        self.enemy = None

    def response_to_command(self,command: str) -> str:
        command = command.strip().lower()

        
        if self.state == self.NOT_STARTED:
            if command == "start":
                self.state = self.CHAR_CREATION
                self.player = game.PlayerCharacter("Hero", "Warrior", game.Attributes(8, 4, 2))
                self.player.equip_armor(game.Armor("chainmail","chainmail"))
                self.player.equip_weapon(game.Weapon("longsword","1d8"))

                power_strike_skill = game.Skill("Power Strike", "4d6", 150)
                self.player.learn_skill(power_strike_skill)

                self.state = self.EXPLORATION
                response = "welcome to Escape the Dungeon! Your adventure begins now."

                room_status = f"You are in the {self.current_room}. \n\n{self.rooms[self.current_room]['description']}"
                if "item" in self.rooms[self.current_room]:
                    room_status += f"\n\nwhere would you like to go?"

                response += "\n\navailable commands : go [direction] / take [item] / use [item] / stats / exit / inventory / equip [weapon/armor]"
                response += "\n\nwhat would you like to do?"

                return {
                    "game_response": response,
                    "status_update": room_status,
                    "character_update": self.player.get_status()
                }
            else:
                return {"game_response": "Please type 'start' to begin your adventure!"}
        elif self.state == self.EXPLORATION:
            if command.startswith("go"):
                direction = command.split()[1]
                if direction in self.rooms[self.current_room]:
                    if self.rooms[self.current_room][direction].lower().endswith("(locked)"):
                        return {"game_response": "The door is locked. You need a key to proceed."}
                    else:
                        self.current_room = self.rooms[self.current_room][direction]
                        response = f"You move {direction} and enter the {self.current_room}."

                        room_status = f"You are in the {self.current_room}. \n\n{self.rooms[self.current_room]['description']}"


                        
                        if 'encounter' in self.rooms[self.current_room] and self.rooms[self.current_room]['encounter'] == True:
                            self.state = self.COMBAT
                            self.enemy = random.choice(self.monsters)
                            response += f"\n\nAs you enter the {self.current_room}, a {self.enemy.name} appears!"
                            return{
                                "game_response": response,
                                "status_update": room_status,
                            }

                        if self.current_room == "Exit":
                            self.state = self.COMPLETED
                            response += "\n\nCongratulations! You've escaped the dungeon!"
                            return {"game_response": response}
                        
                        
                        if "item" in self.rooms[self.current_room]:
                            room_status = f"You see a {self.rooms[self.current_room]['item']} here."
                            

                        response += "\n\navailable commands : go [direction] / take [item] / use [item] / stats / exit / inventory / equip [weapon/armor]"
                        response += "\n\nwhat would you like to do?"

                        return {
                            "game_response": response,
                            "status_update": room_status,
                        }
                    
            elif command.startswith("take"):
                item = command.removeprefix("take ").lower()
                if "item" in self.rooms[self.current_room] and item == self.rooms[self.current_room]['item']:
                    self.player.inventory.append(game.QuestItem(self.rooms[self.current_room].pop('item')))
                    return {
                        "game_response": f"You picked up the {item}.",
                        "character_update": self.player.get_status()
                    }
                else:
                    return {"game_response": "No such item is here."}
            elif command.startswith("use "):
                item = command.removeprefix("use ")
                if self.player.is_in_inventory(item):
                    if item.lower() == 'key' and self.current_room == 'Cell':
                        self.player.use_item('key')
                        self.rooms['Cell']['east'] = 'Hallway'
                        self.rooms['Cell']['description'] = self.rooms['Cell']['description'].replace("The door is locked.","The door is now unlocked.")
                        return {
                            "game_response": "You used the key to unlock the gate to a dilapidated hallway.",
                            "status_update": f"You are in the {self.current_room}. \n\n{self.rooms[self.current_room]['description']}",
                            "character_update": self.player.get_status(),
                        }
                    else:
                        self.player.use_item(item)
                        return {
                            "game_response": f"You used the {item}.",
                            "character_update": self.player.get_status()
                        }
                else:
                    return {"game_response": f"you don't have the {item} in your inventory."}
            elif command == "inventory":
                if self.player.inventory:
                    inventory_list = "\n".join([f"- {item.name}" for item in self.player.inventory])
                    return {"game_response": f"Your inventory contains:\n{inventory_list}"}
                else:
                    return {"game_response": "Your inventory is empty."}
            elif command.startswith("equip "):
                equip_item = command.removeprefix("equip ").lower()
                if self.player.is_in_inventory(equip_item):
                    is_equip_successful = self.player.equip(equip_item)
                    if is_equip_successful:
                        return {
                            "game_response": f"You equipped the {equip_item}.",
                            "character_update": self.player.get_status()
                        }
                    else:
                        return {"game_response": f"You cannot equip the {equip_item}."}
                else:
                    return {"game_response": f"you don't have the {equip_item} in your inventory."}
                    