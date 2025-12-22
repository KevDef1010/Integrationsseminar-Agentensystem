# Battle System - Manuell korrigiert
# Zeigt wie der korrekte Code aussehen sollte
# Original war durch LLM-Limitationen fehlerhaft

class Attack:
    """Eine Attacke mit Name, Schaden und Typ."""
    
    def __init__(self, name: str, damage: int, typ: str):
        self.name = name
        self.damage = damage
        self.typ = typ
    
    def __repr__(self):
        return f"Attack({self.name}, {self.damage}, {self.typ})"


class Pokemon:
    """Ein Pokemon mit Kampf-Attributen."""
    
    def __init__(self, name: str, typ: str, level: int, max_hp: int, attacks: list):
        self.name = name
        self.typ = typ
        self.level = level
        self.max_hp = max_hp
        self.hp = max_hp  # HP startet bei max
        self.attacks = attacks  # Liste von Attack-Objekten
    
    def take_damage(self, amount: int) -> int:
        """Nimmt Schaden und gibt verbleibende HP zurück."""
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
        return self.hp
    
    def is_fainted(self) -> bool:
        """Gibt True zurück wenn Pokemon besiegt ist."""
        return self.hp <= 0
    
    def heal(self, amount: int) -> int:
        """Heilt Pokemon bis max_hp."""
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        return self.hp
    
    def __repr__(self):
        return f"{self.name} (Lv.{self.level}) HP: {self.hp}/{self.max_hp}"


class Battle:
    """Rundenbasiertes Kampfsystem für 2 Pokemon."""
    
    def __init__(self, pokemon1: Pokemon, pokemon2: Pokemon):
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2
        self.current_turn = 0  # 0 = pokemon1, 1 = pokemon2
        self.battle_log = []
    
    def execute_attack(self, attacker_index: int, attack_index: int) -> str:
        """
        Führt eine Attacke aus.
        
        Args:
            attacker_index: 0 für pokemon1, 1 für pokemon2
            attack_index: Index der Attacke in der attacks-Liste
            
        Returns:
            Log-String der Aktion
        """
        # Bestimme Angreifer und Verteidiger
        if attacker_index == 0:
            attacker = self.pokemon1
            defender = self.pokemon2
        else:
            attacker = self.pokemon2
            defender = self.pokemon1
        
        # Prüfe ob Angreifer noch kämpfen kann
        if attacker.is_fainted():
            log = f"{attacker.name} ist besiegt und kann nicht angreifen!"
            self.battle_log.append(log)
            return log
        
        # Prüfe ob Attacke existiert
        if attack_index >= len(attacker.attacks):
            log = f"Ungültiger Attacken-Index: {attack_index}"
            self.battle_log.append(log)
            return log
        
        attack = attacker.attacks[attack_index]
        
        # Berechne Schaden (mit einfacher Typen-Effektivität)
        damage = attack.damage
        effectiveness = ""
        
        # Feuer > Pflanze > Wasser > Feuer
        type_chart = {
            ("Feuer", "Pflanze"): 1.5,
            ("Pflanze", "Wasser"): 1.5,
            ("Wasser", "Feuer"): 1.5,
            ("Pflanze", "Feuer"): 0.5,
            ("Wasser", "Pflanze"): 0.5,
            ("Feuer", "Wasser"): 0.5,
        }
        
        multiplier = type_chart.get((attack.typ, defender.typ), 1.0)
        if multiplier > 1:
            effectiveness = " Es ist sehr effektiv!"
            damage = int(damage * multiplier)
        elif multiplier < 1:
            effectiveness = " Es ist nicht sehr effektiv..."
            damage = int(damage * multiplier)
        
        # Schaden zufügen
        remaining_hp = defender.take_damage(damage)
        
        # Log erstellen
        if defender.is_fainted():
            log = f"{attacker.name} setzt {attack.name} ein! {defender.name} nimmt {damage} Schaden.{effectiveness} {defender.name} ist besiegt!"
        else:
            log = f"{attacker.name} setzt {attack.name} ein! {defender.name} nimmt {damage} Schaden.{effectiveness} (HP: {remaining_hp}/{defender.max_hp})"
        
        self.battle_log.append(log)
        return log
    
    def get_winner(self) -> Pokemon:
        """Gibt den Gewinner zurück, oder None wenn Kampf noch läuft."""
        if self.pokemon1.is_fainted():
            return self.pokemon2
        elif self.pokemon2.is_fainted():
            return self.pokemon1
        else:
            return None
    
    def switch_turn(self):
        """Wechselt den aktuellen Zug."""
        self.current_turn = 1 - self.current_turn  # 0 -> 1 oder 1 -> 0
    
    def get_current_attacker(self) -> Pokemon:
        """Gibt das Pokemon zurück das gerade am Zug ist."""
        return self.pokemon1 if self.current_turn == 0 else self.pokemon2
    
    def is_battle_over(self) -> bool:
        """Prüft ob der Kampf vorbei ist."""
        return self.get_winner() is not None


if __name__ == "__main__":
    # Demo-Kampf
    print("=" * 50)
    print("POKEMON KAMPF DEMO")
    print("=" * 50)
    
    glumanda = Pokemon("Glumanda", "Feuer", 5, 39, [
        Attack("Glut", 40, "Feuer"),
        Attack("Kratzer", 40, "Normal")
    ])
    bisasam = Pokemon("Bisasam", "Pflanze", 5, 45, [
        Attack("Rankenhieb", 45, "Pflanze"),
        Attack("Tackle", 40, "Normal")
    ])
    
    battle = Battle(glumanda, bisasam)
    
    print(f"\n{glumanda}")
    print(f"{bisasam}\n")
    
    round_num = 1
    while not battle.is_battle_over():
        print(f"--- Runde {round_num} ---")
        attacker_idx = battle.current_turn
        log = battle.execute_attack(attacker_idx, 0)
        print(log)
        battle.switch_turn()
        round_num += 1
    
    print(f"\n{'='*50}")
    print(f"🏆 GEWINNER: {battle.get_winner().name}!")
    print(f"{'='*50}")
