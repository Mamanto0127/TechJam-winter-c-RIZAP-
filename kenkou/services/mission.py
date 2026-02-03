import random
from kenkou.models import Mission

def get_today_missions(count=1):
    missions = list(Mission.objects.all())
    return random.sample(missions, count)

AI_missions = [
    {
        "title": "「忍び足」階段登り", 
        "description": "階段を使う際、音を立てないようにゆっくり、つま先に力を入れて登ります。これだけでふくらはぎとお尻への刺激が倍増します。", 
        "reward_damage": 10,
    }, 
    {
        "title": "「かかとあげ」歯磨き", 
        "description": "歯を磨いている間だけ、かかとの上げ下げを繰り返します。第二の心臓と呼ばれるふくらはぎを鍛えて血流をアップしましょう。", 
        "reward_damage": 10,
    },
    {
        "title": "「空気椅子」スマホ", 
        "description": "壁に背中をつけて膝を90度に曲げてキープ。SNSを1件チェックする間だけ耐えてみましょう。",
        "reward_damage": 10, 
    }, 
    {
        "title": "「4-7-8」呼吸法", 
        "description": "4秒吸って7秒止めて8秒かけて吐き出します。これを3回繰り返すだけで、副交感神経が優位になり"
    }
]