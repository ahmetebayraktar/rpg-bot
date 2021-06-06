from bot.db import db
import json
from pathlib import Path


class Item:
    def __init__(self, item):
        self.id = item[0]


class Armor(Item):
    def __init__(self, item, stats):
        super().__init__(item[0])

        self.armor = stats[3]
        self.health = stats[8]
        self.healthregeneration = stats[9]
        self.magicresistance = stats[12]

        for i in item:
            if i.startswith("AR"):
                self.bonusarmor = int(i[3:])
            elif i.startswith("HP"):
                self.bonushealth = int(i[3:])
            elif i.startswith("MR"):
                self.bonusmagicresistance = int(i[3:])
            else:
                pass


class Weapon(Item):
    def __init__(self, item, stats):
        super().__init__(item[0])

        self.abiltypower = stats[2]
        self.armorpenetration = stats[4]
        self.attackdamage = stats[5]
        self.criticalstrikechance = stats[6]
        self.criticalstrikedamage = stats[7]
        self.lifesteal = stats[10]
        self.magicpenetration = stats[11]
        self.spellvamp = stats[15]

        for i in item:
            if i.startswith("AP"):
                self.bonusabilitypower = int(i[3:])
            elif i.startswith("AD"):
                self.bonusattackdamage = int(i[3:])
            elif i.startswith("CD"):
                self.bonuscriticalstrikedamage = int(i[3:])
            elif i.startswith("LS"):
                self.bonuslifesteal = int(i[3:])
            elif i.startswith("SV"):
                self.bonusspellvamp = int(i[3:])
            else:
                pass


class Pendant(Item):
    def __init__(self, item, stats):
        super().__init__(item[0])

        self.armorpenetration = stats[4]
        self.criticalstrikechance = stats[6]
        self.criticalstrikedamage = stats[7]
        self.healthregeneration = stats[9]
        self.lifesteal = stats[10]
        self.magicpenetration = stats[11]
        self.mana = stats[13]
        self.manaregeneration = stats[14]
        self.spellvamp = stats[15]

        for i in item:
            if i.startswith("CD"):
                self.bonuscriticalstrikedamage = int(i[3:])
            elif i.startswith("LS"):
                self.bonuslifesteal = int(i[3:])
            elif i.startswith("SV"):
                self.bonusspellvamp = int(i[3:])
            else:
                pass


class Potion(Item):
    def __init__(self, item_id, stats):
        super().__init__(item_id)

        # PyCharm neden stats değişkenini kullanmadığımı sorgulamasın diye yazdım.
        print(stats)


async def get_item(item):
    itemlist = item.split("+")
    itemstats = db.records("SELECT * FROM items WHERE ItemID = ?", itemlist[0])

    if itemstats[1] == "weapon":
        Weapon(itemlist, itemstats)
    elif itemstats[1] == "armor":
        Armor(itemlist, itemstats)
    elif itemstats[1] == "pendant":
        Pendant(itemlist, itemstats)
    elif itemstats[1] == "potion":
        Potion(itemlist, itemstats)
    else:
        Item(itemlist)

    # 0 -> ItemID
    # 1 -> ItemType
    # 2 -> AbilityPower
    # 3 -> Armor
    # 4 -> ArmorPenetration
    # 5 -> AttackDamage
    # 6 -> CriticalStrikeChance
    # 7 -> CriticalStrikeDamage
    # 8 -> Health
    # 9 -> HealthRegeneration
    # 10 -> Lifesteal
    # 11 -> MagicPenetration
    # 12 -> MagicResistance
    # 13 -> Mana
    # 14 -> ManaRegeneration
    # 15 -> SpellVamp
    # 16 -> BonusAbilityPower
    # 17 -> BonusArmor
    # 18 -> BonusAttackDamage
    # 19 -> BonusCriticalStrikeDamage
    # 20 -> BonusHealth
    # 21 -> BonusLifesteal
    # 22 -> BonusMagicResistance
    # 23 -> BonusSpellVamp


# DB'den depolama formatından (item_id;diğer_item_id) hepsini olması gereken iteme çevirir.
async def read_user_items(user_id):
    item = db.record("SELECT playeritems FROM player WHERE UserId = ?", user_id)
    return [get_item(i) for i in item.split(";")]


# Bitmedi bonusları kaydetme özelliğini eklemedim daha.
async def set_user_items(user_id, items: list):
    itemstring = ""
    for i in items:
        itemstring += f"{i};"
    db.execute("UPDATE player SET playeritems = ? WHERE UserID = ?", itemstring, user_id)


# JSON dosyasından eşyaların değerlerini alır ve SQL'e kaydeder.
async def update_itemstats_from_json():
    with open(Path("./data/itemstats.json"), "r") as f:
        data = json.load(f)
    for item in data:
        item_id = item[0]
        db.execute("UPDATE items SET AbilityPower = ? WHERE ItemID = ?", item[2], item_id)
        db.execute("UPDATE items SET Armor = ? WHERE ItemID = ?", item[3], item_id)
        db.execute("UPDATE items SET ArmorPenetration = ? WHERE ItemID = ?", item[4], item_id)
        db.execute("UPDATE items SET AttackDamage = ? WHERE ItemID = ?", item[5], item_id)
        db.execute("UPDATE items SET CriticalStrikeChance = ? WHERE ItemID = ?", item[6], item_id)
        db.execute("UPDATE items SET CriticalStrikeDamage = ? WHERE ItemID = ?", item[7], item_id)
        db.execute("UPDATE items SET Health = ? WHERE ItemID = ?", item[8], item_id)
        db.execute("UPDATE items SET HealthRegeneration = ? WHERE ItemID = ?", item[9], item_id)
        db.execute("UPDATE items SET LifeSteal = ? WHERE ItemID = ?", item[10], item_id)
        db.execute("UPDATE items SET MagicResistance = ? WHERE ItemID = ?", item[11], item_id)
        db.execute("UPDATE items SET Mana = ? WHERE ItemID = ?", item[12], item_id)
        db.execute("UPDATE items SET ManaRegeneration = ? WHERE ItemID = ?", item[13], item_id)
        db.execute("UPDATE items SET SpellVamp = ? WHERE ItemID = ?", item[14], item_id)
        db.commit()
