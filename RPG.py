import random
import copy 
player = {
    "name": "",
    "hp": 150,
    "max_hp": 150,
    "attack": 15,
    "defense": 5,
    "gold": 0,
    "level": 1,
    "xp": 0
}

inventory = []

foes = [
    {"name": "Snake", "hp": 10,"atk": 10, "gold": 10,"xp": 10},
    {"name": "Wolf", "hp": 25,"atk": 5, "gold": 5,"xp": 10},
    {"name": "Rat", "hp": 10,"atk": 2, "gold": 5,"xp": 5},
    {"name": "Bandit", "hp": 50,"atk": 5, "gold": 10,"xp": 20},
    {"name": "Goblin", "hp": 30, "atk": 8,  "gold": 10, "xp": 15},
    {"name": "Cursed Plant", "hp": 50,"atk": 20, "gold": 35,"xp": 45},
    {"name": "Skeleton", "hp": 70,"atk": 10, "gold": 20,"xp": 35},
    {"name": "Mage", "hp": 20,"atk": 20, "gold": 30,"xp": 40},
    {"name": "Orc", "hp": 60, "atk": 14, "gold": 25, "xp": 30},
    {"name": "Ghoul", "hp": 100,"atk": 15, "gold": 30,"xp": 40},
    {"name": "Dragon", "hp": 350,"atk": 30, "gold": 250,"xp": 150},    
]

shop = {
    "Health Potion": {"cost": 20, "hp": 30},
    "Sword": {"cost": 40, "attack": 10},
    "Shield": {"cost": 50, "defense": 8}
}

locations = [
    ("Forêt des pleurs touffus", "A wide forest, with dangers within it"),
    ("Sous le manteau de la Seine", "A little town with a shop and a pub"),
    ("Le château de New Meaux", "The home of the greatest of horrors")
]

speeches = {
    "shopkeeper": {
        "1": "Life's getting harder and harder, isn't it? I don't know how much longer I can keep this shop running.\n (Idk i didn't put any effort in the worldbuilding or lore of this game, leave alone).",
        "2": "My opinion about the english? Who cares? Oasis won the britpop battle, Blur overrated asf.",
        "3": "what is inside that castle? well, some say that a giant dragon lives there, it scares me :("
        }
}

def show_stats(player):
    for stat, num in player.items():
        print(f" {stat} - {num}")

def show_inventory(inventory):
    if not inventory:
        print("vide comme ton crâne (empty as your cranium)")
        return
    for i, item in enumerate(inventory, start=1):
        print(f"{i}. {item}")

def buy_item(inventory, item):
    gold_cost = shop[item]["cost"]
    if player["gold"] >= gold_cost:
        player["gold"] -= gold_cost
        if "hp" in shop[item]:      # solo pociones van al inventario
            inventory.append(item)
        print(f"You bought {item}!")
    else:
        print("Not enough gold!")

def use_item(inventory, player):
    if not inventory:
        print("Your inventory is empty.")
        return
    show_inventory(inventory)
    use_choice = int(input("Select item number: ")) - 1
    if 0 <= use_choice < len(inventory):
        item = inventory[use_choice]
        if "hp" in shop.get(item, {}):
            player["hp"] = min(player["max_hp"], player["hp"] + shop[item]["hp"])
            inventory.remove(item)
            print(f"You used {item}. HP: {player['hp']}")
        else:
            print("Can't use that here.")
    else:
        print("Invalid choice.")

def levelup(player):
    while player["xp"] >= 100:   # while en vez de if
        player["level"] += 1
        player["xp"] -= 100      # resta 100 en vez de resetear a 0
        player["max_hp"] += 10
        player["attack"] += 5
        player["defense"] += 1
        player["hp"] = player["max_hp"]
        print(f"Level up! Now level {player['level']}")
        print(f"Max HP: {player['max_hp']}, Attack: {player['attack']}, Defense: {player['defense']}")

def speech(npc, topic):
    if npc in speeches and topic in speeches[npc]:
        print(f'\n{npc.capitalize()}: "{speeches[npc][topic]}"')
    else:
        print(f"{npc}: ...")

def fight(player, foe):
    print(f"It has appeared a {foe["name"]}!")
    print(" ")
    while player["hp"] > 0 and foe["hp"] > 0:
        print(f"{player['name']}'s HP: {player["hp"]}\n - ENEMY - \n{foe["name"]} HP: {foe["hp"]}")
        print("-"*10+" En Garde! "+"-"*10)
        print(f"[1] Fight!\n[2] Use Item \n[3] Flee" )
        choice = int(input("> "))
        if choice == 1:
            print("You battled")
            crit_chance = random.randint(1, 6)
            if crit_chance == 6:
                print(" ")
                print("     =-- <(- Critical hit! - Coup critique! -)> --=   ")
                print(" ")
                damage = max(1, player["attack"]*2) # critical hit ignores all defense and doubles the attack, but it still has a minimum of 1 damage
            else:
                damage = max(1, player["attack"]-(foe["atk"]*0.5))
            foe["hp"] -= damage
            print(f"You dealt {damage} damage to the {foe["name"]}!")
            print(" ")
            print("-=-"*5)
            print("tour de l'adversaire")
            print("-=-"*5)
            print(" ")
            crit_chance_foe = random.randint(1, 6)
            if crit_chance_foe == 6:
                print(" ")
                print(f"     =-- <(- The {foe['name']} landed a critical hit! - Le {foe['name']} a porté un coup critique! -)> --=   ")
                print(" ")
                damage_foe = max(1, (foe["atk"]*2)-player["defense"])
            else:
                damage_foe = max(1, foe["atk"]-player["defense"])
            player["hp"] -= damage_foe
            print(f"The {foe["name"]} dealt {damage_foe} damage to {player['name']}!")

        elif choice == 2:
            print(f"{player["name"]}... let's take a look")
            use_item(inventory, player)
        elif choice == 3:
            escape_ch = random.randint(1, 6)
            if escape_ch > 4:
                print(f"{player["name"]}. Lâche! tu l'as fait! (you coward! you did it!)")
                print("You won't get any reward, lame ass, but at least you are alive... for now.")
                break
            else: 
                print(f"{player["name"]} tu as échoué, prépare-toi pour ta finalel (you failed, prepare for your death)")
            print("-=-"*5)
            print("tour de l'adversaire")
            print("-=-"*5)
            damage_foe = max(1, foe["atk"]-player["defense"])
            player["hp"] -= damage_foe

            
        else: print("Select only 1, 2 or 3 you crétin!")
    
    if player["hp"] <= 0:
        print("-="*20)
        print("GAME OVER\nEnterré comme tout le monde.")
        print("-="*20)
        print("Start over again?")
        choice = input("[1] Yes\n[2] No\n> ")
        if choice == "1":
            print("In another life...")
            #restart the values
            player["name"] = ""
            player["max_hp"] = 100
            player["hp"] = 100
            player["attack"] = 15
            player["defense"] = 5
            player["gold"] = 0
            player["xp"] = 0
            player["level"] = 1
            inventory.clear()
            shop["Health Potion"] = {"cost": 20, "hp": 30}
            shop["Sword"] = {"cost": 40, "attack": 10}
            shop["Shield"] = {"cost": 50, "defense": 8}
            main()
        else:
            print("personne ne se souviendra de toi (nobody will remember you)")
            exit()

    else: 
        print(" ")
        print("Thus shalt open your eyes once more.")
        print(" ")
        print(f"You've got {foe["gold"]} gold and {foe["xp"]} xp!")
        player["gold"] += foe["gold"]
        player["xp"] += foe["xp"]
        levelup(player)

def explore(player, inventory):
    print(" ")
    print("Let's travel to...")
    print(" ")
    for i, lugar in enumerate(locations, start=1):
        nombre, summary = lugar
        print(f"{i}. {nombre}... {summary}")
        print(" ")
    travel = int(input("Choose: "))
    if travel in [1, 2, 3]:
        if travel == 1:
            print(" ")
            forest_foes = foes[:9] # the first 9 foes are the ones that can be found in the forest
            enemy = copy.deepcopy(random.choice(forest_foes)) # we use deepcopy to avoid modifying the original foe in the list
            print("You ventured into the forest...")
            fight(player, enemy)
        elif travel == 2:
            print("You went to the ville...")
            shoping(player, inventory)
        elif travel == 3:
            if player["level"] < 5:
                print(" ")
                print("Quelque chose punit ton âme, tu ne te sens pas bien de prendre cette décision (at least level 5 to enter this place)")
            else:
                print("You entered the castle...")
                dragon = copy.deepcopy(foes[-1])
                fight(player, dragon)
                if dragon["hp"] <= 0:
                    print(" ")
                    print(" (--> Tu as sauvé Troyes, ton nom sera retenu comme le héros qui a vaincu le dragon <--) ")
                    print(" ")
                    print("     Congratulations, you defeated the dragon and won the game! Thanks for playing :)")
                    print(" ")
                    print(" (--> You've saved Troyes, your name will be remembered as the hero who defeated the dragon <--) ")
                    print(" ")
                    print(f"    -    '{player['name']}' l'élu de Dieu (the chosen of God)   -   ")
                    exit()
    else: 
        print(" ")
        print("Select only 1, 2 or 3 you crétin!")

def shoping(player, inventory):
    print("Welcome traveler")
    print("We've got...")
    if not shop:
        print("(The shelves are empty...)")
    else:
        for item, pay in shop.items():
            print(f"{item} - {pay['cost']} gold")
    while True:
        print(f"\n[1] Buy\n[2] Talk\n[3] Leave")
        choice_shop = int(input("> "))
        if choice_shop == 1:
            if not shop:
                print("Nothing left to sell.")
            else:
                print("What would you like to buy?")
                items_list = list(shop.keys())
                for i, item in enumerate(items_list, start=1):
                    print(f"{i}. {item} - {shop[item]['cost']} gold")
                while True:
                    item_choice = int(input("Select: "))
                    if 1 <= item_choice <= len(items_list):
                        chosen = items_list[item_choice - 1]
                        buy_item(inventory, chosen)
                        if "attack" in shop.get(chosen, {}):
                            player["attack"] += shop[chosen]["attack"]
                            shop.pop(chosen)
                        elif "defense" in shop.get(chosen, {}):
                            player["defense"] += shop[chosen]["defense"]
                            shop.pop(chosen)
                        break
                    else:
                        print("Invalid choice.")
        elif choice_shop == 2:
            print("About what?")
            print("[1] Life\n[2] The English\n[3] The Castle")
            topic = input("> ")
            speech("shopkeeper", topic)
        elif choice_shop == 3:
            print('\nShopkeeper: "Au revoir, et que Dieu ait pitié de vous."')
            return
        else:
            print("Please type only 1, 2 or 3")

def main():
    print(" ")
    print(" - Little RPG ^u^ - ")
    print(" ")
    print('''  1. Start
  2. Tutorial
  3. Exit    ''')
    print(" ")
    print(" - Copyright None lol - ")
    print(" ")
    while True:
        menu_choice = int(input("Veuillez sélectionner une option >  "))
        if menu_choice in [1, 2, 3]:
            break
        else: print("1, 2 or 3 only.")
    if menu_choice == 1:
        print(" ")
        name = input("What is your name?: ")
        name = name.capitalize()
        player["name"] = name
        print(" ")
        print("="*15 + " Troyes, France " + "="*15)
        print(" ")
        print("Prologue...")
        print(" ")
        print(f'''    The hope of this world has vanished trough the millenia, turning the wealthy earth we knew 
    into a wasteland of woe and illness, you... {name} are just a nobody, trying to survive in this place.
    fiends lurk over Europe, good luck... \n(This has no OOP, 0 AI involved, i practiced french in this project) \n(my french is disgusting and im barely starting, excuse any typo or something like that)''')
        
        
        while True:
            print(" ")
            print("\nTu vas faire quoi ? (What will you do?)\n")
            print("1. Explore")
            print("2. See stats")
            print("3. See inventory")
            print("4. Exit")
            print(" ")
            
            accion = input("> ")
            
            if accion == "1":
                explore(player, inventory)
            elif accion == "2":
                print(" ")
                show_stats(player)
            elif accion == "3":
                print(" ")
                show_inventory(inventory)
            elif accion == "4":
                print(" ")
                print("Au revoir.")
                print(" ")
                break
    elif menu_choice == 2:
        print(''' This is a role playing game, situaded in a re-imagined medieval france\nactions: explore, see stats, see inventory and ran away like a moron (exit)\nIn the explore tab, you'll choose a location to go, between the: forest, ville and castle\nOnce you've stablished combat with an enemy, you can choose between fight, use item or flee\n in the fight option, you'll deal damage to the enemy and receive damage from it \n(either the enemy and you can miss the attack)\nUntil one of you dies, then if you won, you'll get a reward\n in the use item option, you'll be able to use a potion or something like that\n in the flee option you'll roll a dice, and if you are lucky enoguh, you'll escape \n good luck...''')
        print(" ")
        main()
    elif menu_choice == 3:
        print(" ")
        print("Au revoir.")
        print(" ")
        exit()

main()
            