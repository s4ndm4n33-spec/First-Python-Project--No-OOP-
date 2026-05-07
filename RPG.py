import random
import sys
import copy

# =================================================================
# SOVEREIGN ENGINE: P.D.M. CORE (SEAM PROTOCOL V2.1)
# =================================================================
class SovereignEngine:
    def __init__(self):
        # The P.D.M. Governor tracks the global state of the adventure[cite: 1]
        self.pdm = {
            "world_tension": 0,
            "narrative_phase": 1,
            "current_location": "Cathedral Ruins",
            "momentum": 0,
            "active": True
        }
        self.player = {
            "name": "Mike", 
            "hp": 150, 
            "max_hp": 150,
            "atk": 15, 
            "def": 5, 
            "xp": 0, 
            "inv": ["Rusted Key"]
        }
        # SEAM Protocol: Decoupled Map Architecture[cite: 1]
        self.world_map = {
            "ACT_1": {
                "Cathedral Ruins": {
                    "desc": "Ash falls like snow. The altar hums with dying power.",
                    "actions": {
                        "Search Altar": {"type": "item", "stat": "atk"},
                        "Inspect Crypts": {"type": "lore", "stat": "atk"},
                        "Exit": {"type": "move", "stat": "atk"}
                    }
                },
                "Shattered Bridge": {
                    "desc": "A precarious path over the gorge toward New Meaux.",
                    "actions": {
                        "Scout Underpass": {"type": "combat", "stat": "atk"},
                        "Repair Gap": {"type": "skill", "stat": "def"},
                        "Cross": {"type": "move", "stat": "atk"}
                    }
                }
            },
            "ACT_2": {
                "New Meaux Gates": {
                    "desc": "The barricades are high. Sentinels eye you warily.",
                    "actions": {
                        "Negotiate Entry": {"type": "skill", "stat": "atk"},
                        "Storm Gates": {"type": "combat", "stat": "atk"}
                    }
                }
            }
        }

    def resolve_fate(self, bonus=0):
        """ The Fate Resolver ($d20$)[cite: 1] """
        roll = random.randint(1, 20)
        total = roll + (bonus // 5)
        print(f"\n[P.D.M.]: Fate Roll: {roll} (Total: {total})")
        if roll == 20: return "CRIT"
        if total >= 14: return "SUCCESS"
        if total <= 6: return "FUMBLE"
        return "FAIL"

    def combat(self, enemy_name, hp, atk):
        """ Rigorous Combat Resolver using Five Masters principles[cite: 1] """
        print(f"\n--- ENCOUNTER: {enemy_name} ---")
        # Enemy health scales with world tension[cite: 1]
        e_hp = hp * (1 + (self.pdm["world_tension"] / 100))
        while e_hp > 0 and self.player["hp"] > 0:
            print(f"{self.player['name']}: {self.player['hp']}HP | {enemy_name}: {int(e_hp)}HP")
            cmd = input("[1] Strike [2] Potion\n> ")
            if cmd == "1":
                dmg = self.player["atk"] + random.randint(1, 5)
                e_hp -= dmg
                print(f"You deal {dmg} damage.")
                if e_hp > 0:
                    taken = max(1, (atk - self.player["def"]))
                    self.player["hp"] -= taken
                    print(f"The {enemy_name} strikes for {taken} damage.")
            elif cmd == "2" and "Potion" in self.player["inv"]:
                self.player["hp"] = min(self.player["max_hp"], self.player["hp"] + 50)
                print("Healed for 50 HP.")
        
        if self.player["hp"] > 0:
            print(f"Victory! {enemy_name} neutralized.")
            self.pdm["world_tension"] += 10
            return True
        return False

    def game_loop(self):
        print(f"=== B.L.U.E.-J. SOVEREIGN ENGINE v2.1 ===")
        print("Protocol: SEAM Implementation | Node Purge: ENABLED")
        
        while self.pdm["active"]:
            act_key = f"ACT_{self.pdm['narrative_phase']}"
            loc_key = self.pdm["current_location"]
            
            # ACT TRANSITION LOGIC[cite: 1]
            if self.pdm["world_tension"] >= 50 and self.pdm["narrative_phase"] == 1:
                print("\n>>> NARRATIVE SHIFT: You have reached the outskirts of Troyes.")
                self.pdm["narrative_phase"] = 2
                self.pdm["current_location"] = "New Meaux Gates"
                continue

            node = self.world_map[act_key][loc_key]
            print(f"\n[{loc_key.upper()}]")
            print(node["desc"])
            
            options = list(node["actions"].keys())
            for i, opt in enumerate(options, 1):
                print(f"[{i}] {opt}")

            try:
                idx = int(input("> ")) - 1
                action_name = options[idx]
                action_data = node["actions"][action_name]
            except (ValueError, IndexError):
                print("Invalid input. Maintain Rigor.")
                continue

            # Resolve Outcome[cite: 1]
            outcome = self.resolve_fate(self.player[action_data["stat"]])

            # DYNAMIC BRANCHING & PURGING[cite: 1]
            if action_data["type"] == "move":
                if outcome != "FUMBLE":
                    others = [k for k in self.world_map[act_key].keys() if k != loc_key]
                    if others:
                        self.pdm["current_location"] = others[0]
                        print(f"\n>>> ADVANCING: Moving to {others[0]}...")
                    else:
                        print("\n>>> No other paths visible yet. Increase Tension.")
                else:
                    print("\n>>> INTERDICTION: You tripped an alarm!")
                    self.combat("Patrol Drone", 30, 10)

            elif action_data["type"] == "item" or action_data["type"] == "lore":
                if outcome in ["SUCCESS", "CRIT"]:
                    if action_data["type"] == "item":
                        print("\n>>> DATA RETRIEVED: Found a Sovereign Core. Atk UP.")
                        self.player["atk"] += 5
                    else:
                        print("\n>>> INTEL GAINED: Area mapped. Tension UP.")
                    
                    self.pdm["world_tension"] += 20 # High velocity progress[cite: 1]
                    # THE PURGE: Deletes the action so it cannot be repeated[cite: 1]
                    del node["actions"][action_name] 
                else:
                    print("\n>>> FAILURE: The environment remains stubborn. Try another path.")

            elif action_data["type"] == "combat":
                if self.combat("Wasteland Scavenger", 40, 12):
                    del node["actions"][action_name]

            if self.player["hp"] <= 0:
                print("\nFATAL ERROR: Legend Terminated.")
                self.pdm["active"] = False

# =================================================================
# INITIALIZATION
# =================================================================
if __name__ == "__main__":
    Engine = SovereignEngine()
    Engine.game_loop()
