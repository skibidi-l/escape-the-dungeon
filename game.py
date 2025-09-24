import random

armor_value = {
    "none": 0,
    "cloth armor": 1,
    "leather armor": 2,
    "chainmail armor": 3,
    "plate armor": 4,
    "dragon scale": 5,
}

class weapon:
     def __init__(self, name, damage):  
            self.name = name
            self.damage = damage
     def   get_damage(self):   
        result = self.damage_dice.split('d')
        num_dice = int(result[0])
        sides = int(result[1])
        return roll_dice(sides_per_die=sides, number_of_dice=num_dice)

class armor:
    def __init__(self, name, damage_dice):
        self.name = name
        self.damage_dice = damage_dice

    def get_damage(self):
        result = self.damage_dice.split('d')
        num_dice = int(result[0])
        sides = int
        

    def get_defense(self):
        return armor_value[self.name]
    
class Equipment:
    def __init__(self, weapon, armor):
        self.weapon = weapon
        self.armor = armor

class Attributes:
    def __init__(self, strength, agility, mind):
        self.strength = strength
        self.agility = agility
        self.mind = mind

class Character:
    def __init__(self, name, character_class , attributes):
        self.name = name
        self.character_class = character_class
        self.max_health = attributes.strength * 5
        self.current_health = self.max_health
        self.attributes = attributes    
        self.equipments = Equipment(None,None)
        self.is_in_combat = False
    
    def equip(self, equipment):
        if isinstance(equipment, weapon):
            self.equipments = equipment

    def equip_armor(self, armor):
        self.equipments.armor = armor

    def equip_weapon(self, weapon):
        self.equipments.weapon = weapon

    
    def get_armor_value(self):
        if self.equipments != None:
            return self.equipments.armor.get_defense()
        return 0
    
    def attack(self, target):
        damage = self.attributes.strength + roll_dice(sides_per_die=6)
        damage = damage - target.get_armor_value()
        target.current_health = target.current_health - damage
        return damage
    def dodge(self):
        dodge_chance = self.attributes.agility * 5
        if roll_dice(sides_per_die=100) <= dodge_chance:
            has_dodged = True
        else:
            has_dodged = False
        return has_dodged

    def show_stats(self):
        if self.is_in_combat == False:
            print("=======Character Stats=======")
            print(f"Name: {self.name}")
            print(f"Class: {self.character_class}")
            print(f"Health: {self.current_health}/{self.max_health}")
            print(f"Strength: {self.attributes.strength}")
            print(f"Agility: {self.attributes.agility}")
            print(f"Mind: {self.attributes.mind}")
        if self.equipments.weapon != None:
            print(f"Weapon: {self.equipments.weapon.name} (Damage: {self.equipments.weapon.damage})")
        else:
            print("Weapon: None")
        if self.equipments.armor != None:
            print(f"Armor: {self.equipments.armor.name} (Defense: {self.get_armor_value()})")
        else:
            print("Armor: None")

    def start_combat(self):
        self.is_in_combat = True

class PlayerCharacter(Character):
    def __init__(self, name, character_class, attributes):
        super().__init__(name, character_class, attributes)
        self.gold = 0
        self.inventory = []

class NonPlayerCharacter(Character):
    def __init__(self, name, character_class, attributes):
        super().__init__(name, character_class, attributes)

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