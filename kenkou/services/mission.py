import random
from kenkou.models import Mission
from datetime import date

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
        "description": "4秒吸って7秒止めて8秒かけて吐き出します。これを3回繰り返すだけで、副交感神経が優位になりリラックス状態に入れます。", 
        "reward_damage": 15,
    }, 
    {
        "title": "デジタル・デトックス", 
        "description": "スマホを家においたまま、近所を5分だけ歩きます。視界情報を制限することで、脳の疲れがおどろくほど取れます。", 
        "reward_damage": 15, 
    }, 
    {
        "title": "「白湯」一杯", 
        "description": "何も入れないお湯をゆっくり飲みます。内臓が高まり、代謝のスイッチが入ります。", 
        "reward_damage": 15, 
    }, 
    {
        "title": "「非利き手」で食べる", 
        "description": "あえて食べくい方の手を使うことで、強制的にゆっくり噛むことになり、満腹中枢が刺激されます。", 
        "reward_damage": 20, 
    }, 
    {
        "title": "「肩甲骨はがし」ストレッチ", 
        "description": "両手を肩に乗せ、肘で大きな円を描くように回します。後ろに回す時に「肩甲骨を寄せて下げる」を意識すると猫背解消に効果的です", 
        "reward_damage": 20, 
    }, 
    {
        "title": "「ドローイン」デスクワーク", 
        "description": "座ったままお腹を極限まで凹ませ、そのまま30秒キープ。呼吸は止めないのがコツです。これだけでインナーマッスルが鍛えられます。", 
        "reward_damage": 20, 
    }, 
    {
        "title": "遠くの緑", 
        "description": "外にある一番遠くの緑を10秒間じっと見つめます。その後、手元の指先を10秒見ます。目のピント調整機能をリセットしましょう。", 
        "reward_damage": 20, 
    }, 
    {
        "title": "ゴキブリ体操", 
        "description": "仰向けに寝て、両手両足を天井に向けてあげます。そのまま手足を1分間ブルブルと細かく震わせるだけ。手足の端末の血流が戻り、冷え性改善やむくみ取りに最強です。", 
        "reward_damage": 20, 
    }, 
    {
        "title": "足指グーパー", 
        "description": "布団の中で足の指を思い切り「ぐー」で縮め、「パー」で開きます。現代人は足指が固まりがちなので、これで愛の疲れが取れやすくなります。", 
        "reward_damage": 15, 
    }, 
    {
        "title": "3つの感謝", 
        "description": "目をつぶって今日あった「良かったこと」を3つだけ思い出します。「コーヒーが美味しかった」レベルでオッケーです。脳がポジティブな状態で入眠できます。", 
        "reward_damage": 20,
    }
]

def save_ai_missions():
    """AIが考えたミッションをDBに保存"""
    for m in AI_missions:
        Mission.objects.get_or_create(
            title=m["title"],
            defaults={
                "description": m["description"],
                "reward_damage": m["reward_damage"],
            }
        )

from datetime import date

def get_today_missions(count=3):
    missions = list(Mission.objects.all())
    if not missions:
        return []

    # 日付ベースでシードを固定
    today = date.today()
    seed = int(today.strftime("%Y%m%d"))  # 例: 20260204
    random.seed(seed)

    selected = random.sample(missions, min(count, len(missions)))

    # シードを戻して他のランダム処理に影響を与えないようにする
    random.seed()
    return selected
