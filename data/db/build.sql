CREATE TABLE IF NOT EXISTS player(
    UserID integer PRIMARY KEY,
    xp integer default 1,
    money integer default 500
    playeritems text default "",
)

CREATE TABLE IF NOT EXISTS items(
    ItemID integer PRIMARY KEY,
    AbilityPower integer default 0,
    Armor integer default 0,
    ArmorPenetration integer default 0,
    AttackDamage integer default 0,
    CriticalStrikeChance integer default 0,
    CriticalStrikeDamage integer default 150,
    Health integer default 0,
    HealthRegeneration integer default 0,
    LifeSteal integer default 0,
    MagicPenetration integer default 0,
    MagicResistance integer default 0,
    Mana integer default 0,
    ManaRegeneration integer default 0,
    SpellVamp integer default 0,
    ItemType text default null,
)