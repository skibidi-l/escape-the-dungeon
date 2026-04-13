
from textual import on

import game
import random

from textual.app  import App, ComposeResult, on
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.widgets import Header, Footer, Input, Markdown

class TextAdventureApp(App):

    def __init__(self):
        super().__init__()
        self.command_history = []   
        self.game_engine = GameEngine()
    def compose(self) -> ComposeResult:
        yield Header()
        yield HorizontalGroup(
            RecentHistoryWindow(),
            SidebarWindow(),
        )
            
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#command-input").focus()

    @on(Input.Submitted, "#command-input")
    def handle_command(self, event: Input.Submitted) -> None:
        command = event.value.strip()
        if not command:
            return
        
        event.input.value = ""

        command_text = f"> **{command}**\n\n"
        self.command_history.append(f"> **{command}**\n\n")
        


        response = self.game_engine.response_to_command(command)
        self.command_history.append(response["game_response"])



        self.update_history(command_text, response["game_response"])

        if "status_update" in response:
            status_window = self.query_one("#status")
            status_window.update(response["status_update"])

        if "character_update" in response:
            character_sheet_window = self.query_one("#character-sheet")
            character_sheet_window.update(response["character_update"])


    def update_history(self, command_text: str, response: str) -> None:
        history_scroll = self.query_one("#history-scroll")
        history_scroll.mount(Response(command_text + response))
        history_scroll.scroll_end(animate=False)

class RecentHistoryWindow(VerticalGroup):

    DEFAULT_CSS = """
    RecentHistoryWindow {
        width: 70%;
        border: round $accent;
        padding: 1;
        dock: left;
    }
    """
    def compose(self) -> ComposeResult:
        yield VerticalScroll(id="history-scroll")
        yield Input(placeholder="Type your command here...", id="command-input")

    def _on_mount(self) -> None:
        self.border_title = "escape the dungeon"


class SidebarWindow(VerticalGroup):

    DEFAULT_CSS = """
    SidebarWindow {
        width: 30%;
        height: 100%;
        dock: right;
    }
    """
    def compose(self) -> ComposeResult:
        yield StatusWindow()
        yield CharacterSheetWindow()

class Response(Markdown):
   """Markdown widget for displaying game Responses"""

class StatusWindow(VerticalScroll):
    DEFAULT_CSS = """
    StatusWindow {
        height: 40%;
        border: round $accent;
        padding: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Response("Room Status\n\n ", id="status")

    def _on_mount(self):
        self.border_title = "status"
class CharacterSheetWindow(VerticalScroll):
    DEFAULT_CSS = """
    CharacterSheetWindow {
        height: 60%;
        border: round $accent;
        padding: 1;
    }
    """
    def compose(self) -> ComposeResult:
        yield Response("Character Sheet\n\n ", id="character-sheet")

    def _on_mount(self):
        self.border_title = "character sheet"

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
        self.player = None

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

                        if self.current_room == "Exit":
                            self.state = self.COMPLETED
                            response += "\n\nCongratulations! You've escaped the dungeon!"
                            return {"game_response": response}
                        
                        room_status = f"You are in the {self.current_room}. \n\n{self.rooms[self.current_room]['description']}"
                        if "item" in self.rooms[self.current_room]:
                            room_status += f"\n\nwhere would you like to go?"

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
                    self.player.equip(equip_item)
                    return {
                        "game_response": f"You equipped the {equip_item}.",
                        "character_update": self.player.get_status()
                    }
                else:
                    return {"game_response": f"you don't have the {equip_item} in your inventory."}
                    





def game_loop():

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

    skeleton_monster = game.NonPlayerCharacter("skeleton","undead",game.Attributes(4, 2, 0))

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
    if player_class == "Warrior":
        player.equip_armor(game.Armor("chainmail","chainmail"))
        player.equip_weapon(game.Weapon("longsword","1d8"))

        power_strike_skill = game.Skill("Power Strike", "4d6", 150)
        player.learn_skill(power_strike_skill)
    elif player_class == "Rogue":
        player.equip_armor(game.Armor("leather armor","leather armor"))
        player.equip_weapon(game.Weapon("dagger","1d4"))

        backstab_skill = game.Skill("Backstab", "3d8", 200)
        player.learn_skill(backstab_skill)
    elif player_class == "Mage":
        player.equip_armor(game.Armor("cloth armor","cloth armor"))
        player.equip_weapon(game.Weapon("staff","1d6"))

        fireball_spell = game.Spell("Fireball", "2d10", 120)
        player.learn_spell(fireball_spell)
    else:
        player.equip_armor(game.Armor("cloth armor","cloth armor"))
        player.equip_weapon(game.Weapon("sword","1d6"))

    player.inventory.append(game.HealthPotion("Small Health Potion", 10))
    player.inventory.append(game.ThrowingKnife("throwing knife", "2d4"))
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
        print("actions available : go [direction] / take [item] / use [item] / stats / exit / inventory / equip [weapon/armor]")
        action = input("What would you like to do? ").strip().lower()
        
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
            item = action.removeprefix('take ')
            if 'item' in rooms[current_room] and item == rooms[current_room]['item']:
                player.inventory.append(game.QuestItem(rooms[current_room].pop('item')))
                print(f"You picked up the {item}.")
            else:
                print("No such item is here.")
        elif action.startswith('use '):
            item = action.removeprefix('use ')
            if player.is_in_inventory(item):
                if item.lower() == 'key' and current_room == 'cell':
                    player.use_item('key')
                    print("You used the key to unlock the gate to a dilapidated hallway.")
                    rooms['cell']['east'] = 'Hallway'
                    rooms['cell']['description'] = rooms['cell']['description'].replace("The door is locked.","The door is now unlocked.")
                    #player.inventory.remove('key')
                else:
                    player.use_item(item)
    
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

if __name__ == "__main__":
    #game_loop()
    app = TextAdventureApp()
    app.run()
    