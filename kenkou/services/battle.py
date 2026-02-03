def calculate_damage(steps):
    return steps // 100

def attack_enemy(enemy, damage):
    enemy.current_hp = max(enemy.current_hp - damage, 0)
    enemy.save()