import game
import random

class GameState:
    NOT_STARTED = "not_started"
    CHAR_CREATION = "character_creation"
    EXPLORATION = "exploration"
    COMBAT = "combat"
    COMPLETED = "completed"
    GAME_OVER = "game_over"

    def __init__(self, game_engine: 'GameEngine'):
        self.game_engine = game_engine
        self.available_actions = []

    def get_available_actions(self):
        return f"Available actions: {', '.join(self.available_actions)}"

    def response_to_command(self, command: str):
        pass


    def get_available_actions(self) -> dict:
        return f"Available actions: {', '.join(self.available_actions)}"
    

class NotStartedState(GameState):
    def __init__(self, game_engine: 'GameEngine'):
        super().__init__(game_engine)
        self.available_actions = ["start"]

    def response_to_command(self, command: str) -> dict:
        if command == "start":
            response = "Welcome to Escape the Dungeon! Your adventure begins now."
            next_state = CharacterCreationState(self.game_engine)
            self.game_engine.create_player()

            next_state = ExplorationState(self.game_engine)
            room_status = self.game_engine.get_room_status()
            response += "\n\n" + next_state.get_available_actions()
            response += "\n\nwhat do you want to do?"

            character_update = self.game_engine.player.get_stated()

            return {"game_response": "welcome to Escape the Dungeon! Your adventure begins now.",
                    "next_state": CharacterCreationState(self.game_engine)
                    }
        else:
            return {"game_response": "Please type 'start' to begin your adventure!"}
        
class CharacterCreationState(GameState):
    def __init__(self, game_engine: 'GameEngine'):
        super().__init__(game_engine)
        self.available_actions = []

    def get_available_actions(self) -> str:
        return f"Available actions: {', '.join(self.available_actions)}"
    
    def response_to_command(self, command: str) -> dict:
        pass

class ExplorationState(GameState):
    def __init__(self, game_engine: 'GameEngine'):
        super().__init__(game_engine)
        self.available_actions = ["go [direction]", "take [item]", "use [item]", "stats", "exit", "inventory", "equip [weapon/armor]"]

    def response_to_command(self, command: str) -> dict:

        if command.startswith("go"):
            direction = command.split()[1].lower()
            return self._go_to(direction)
        
        elif command.startswith("take"):
            item = command.removeprefix("take ").lower()
            return self._take(item)
        
        elif command.startswith("use "):
            item = command.removeprefix("use ").lower()
            return self._use(item)
        
        elif command == "inventory":
            return self._inventory()
        
        elif command.startswith("equip "):
            equip_item = command.removeprefix("equip ").lower()
            return self._equip(equip_item)

    def _go_to(self, direction: str) -> dict:
        pass
    
    def _take(self, item: str) -> dict:
        pass

    def _use(self, item: str) -> dict:
        pass

    def _inventory(self) -> dict:
        pass

    def _equip(self, equip_item: str) -> dict:
        pass


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
        self.state = NotStartedState(self)
        self.enemy = None

    def response_to_command(self,command: str) -> str:
        command = command.strip().lower()
        result = self.state.response_to_command(command)
        if "next_state" in result:
            self.state = result["next_state"]
        return result

    def create_player(self, name: str, char_class: str) -> game.PlayerCharacter:
        self.player = game.PlayerCharacter("Adventurer", "Warrior", game.Attributes(8, 4, 2))
        self.player.equip_armor(game.Armor("chainmail", "chainmail"))
        self.player.equip_weapon(game.Weapon("longsword", "1d8"))

        power_strike_skill =game.Skill("Power Stirke", "2d6", 150)
        self.player.learn_skill(power_strike_skill)

    def get_room_status(self) -> str:
        room_status = f"You are in the {self.current_room}. {self.rooms[self.current_room]['description']}"
        if "item" in self.rooms[self.current_room]:
            room_status += f" You see a {self.rooms[self.current_room]['item']} here."
        return room_status


                    