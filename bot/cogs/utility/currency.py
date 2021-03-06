from bot.db import db


class Currency:
    def __init__(self, bga, neg):
        number = int(bga[0]) + int(bga[1]) * 100 + int(bga[2]) * 10000
        number = str(number).zfill(6)

        self.bakir = int(number[-2:])
        self.gumus = int(number[-4:-2])
        self.altin = int(number[:-4])
        self.is_negative = neg

    def __add__(self, other):
        int_self = await bga_to_integer(self)

        if isinstance(other, Currency) or isinstance(other, list):
            int_other = await bga_to_integer(other)
        elif isinstance(other, int):
            int_other = other
        else:
            raise TypeError

        return await integer_to_bga(int_self + int_other)

    def __iadd__(self, other):
        int_self = await bga_to_integer(self)

        if isinstance(other, Currency) or isinstance(other, list):
            int_other = await bga_to_integer(other)
        elif isinstance(other, int):
            int_other = other
        else:
            raise TypeError

        return await integer_to_bga(int_self + int_other)

    def __sub__(self, other):
        int_self = await bga_to_integer(self)

        if isinstance(other, Currency) or isinstance(other, list):
            int_other = await bga_to_integer(other)
        elif isinstance(other, int):
            int_other = other
        else:
            raise TypeError

        return await integer_to_bga(int_self - int_other)

    def __isub__(self, other):
        int_self = await bga_to_integer(self)

        if isinstance(other, Currency) or isinstance(other, list):
            int_other = await bga_to_integer(other)
        elif isinstance(other, int):
            int_other = other
        else:
            raise TypeError

        return await integer_to_bga(int_self - int_other)

    def __truediv__(self, other):
        int_self = await bga_to_integer(self)

        if isinstance(other, Currency) or isinstance(other, list):
            int_other = await bga_to_integer(other)
        elif isinstance(other, int):
            int_other = other
        else:
            raise TypeError

        return await integer_to_bga(int_self // int_other)

    def __itruediv__(self, other):
        int_self = await bga_to_integer(self)

        if isinstance(other, Currency) or isinstance(other, list):
            int_other = await bga_to_integer(other)
        elif isinstance(other, int):
            int_other = other
        else:
            raise TypeError

        return await integer_to_bga(int_self // int_other)

    def __floordiv__(self, other):
        int_self = await bga_to_integer(self)

        if isinstance(other, Currency) or isinstance(other, list):
            int_other = await bga_to_integer(other)
        elif isinstance(other, int):
            int_other = other
        else:
            raise TypeError

        return await integer_to_bga(int_self // int_other)

    def __ifloordiv__(self, other):
        int_self = await bga_to_integer(self)

        if isinstance(other, Currency) or isinstance(other, list):
            int_other = await bga_to_integer(other)
        elif isinstance(other, int):
            int_other = other
        else:
            raise TypeError

        return await integer_to_bga(int_self // int_other)

    def __eq__(self, other):
        int_self = await bga_to_integer(self)

        if isinstance(other, Currency) or isinstance(other, list):
            int_other = await bga_to_integer(other)
        elif isinstance(other, int):
            int_other = other
        else:
            raise TypeError

        return int_self == int_other

    def __ne__(self, other):
        int_self = await bga_to_integer(self)

        if isinstance(other, Currency) or isinstance(other, list):
            int_other = await bga_to_integer(other)
        elif isinstance(other, int):
            int_other = other
        else:
            raise TypeError

        return int_self != int_other

    def __lt__(self, other):
        int_self = await bga_to_integer(self)

        if isinstance(other, Currency) or isinstance(other, list):
            int_other = await bga_to_integer(other)
        elif isinstance(other, int):
            int_other = other
        else:
            raise TypeError

        return int_self < int_other

    def __gt__(self, other):
        int_self = await bga_to_integer(self)

        if isinstance(other, Currency) or isinstance(other, list):
            int_other = await bga_to_integer(other)
        elif isinstance(other, int):
            int_other = other
        else:
            raise TypeError

        return int_self > int_other

    def __le__(self, other):
        int_self = await bga_to_integer(self)

        if isinstance(other, Currency) or isinstance(other, list):
            int_other = await bga_to_integer(other)
        elif isinstance(other, int):
            int_other = other
        else:
            raise TypeError

        return int_self <= int_other

    def __ge__(self, other):
        int_self = await bga_to_integer(self)

        if isinstance(other, Currency) or isinstance(other, list):
            int_other = await bga_to_integer(other)
        elif isinstance(other, int):
            int_other = other
        else:
            raise TypeError

        return int_self >= int_other

    def __neg__(self):
        if self.is_negative:
            self.is_negative = False
        else:
            self.is_negative = True

    def __int__(self):
        return await bga_to_integer(self)

    def __float__(self):
        return float(await bga_to_integer(self))

    @property
    async def as_list(self):
        return [self.bakir, self.gumus, self.altin]

    @property
    async def simplified(self):
        return await integer_to_bga(await bga_to_integer(self))


# Para birimini basitle??tirir (??rn. 150 g??m???? -> 1 alt??n 50 g??m????)
async def bga_simplify(currency) -> Currency:
    if isinstance(currency, list) or isinstance(currency, Currency):
        number = await bga_to_integer(currency)
    else:
        raise TypeError
    return await integer_to_bga(number)


# Para biriminin hepsini depolama ya da aritmetik i??lemler i??in bak??ra ??evirir.
async def bga_to_integer(currency) -> int:
    if isinstance(currency, Currency):
        number = int(currency.bakir) + int(currency.gumus) * 100 + int(currency.altin) * 10000
        if currency.is_negative:
            number *= -1
    elif isinstance(currency, list):
        number = int(currency[0]) + int(currency[1]) * 100 + int(currency[2]) * 10000
    else:
        raise TypeError
    return number


# Bak??ra ??evirilmi?? paray?? geri Para() s??n??f??na ??evirir.
async def integer_to_bga(number: int) -> Currency:
    if number < 0:
        is_negative = True
        number = str(number)[1:]
        number = number.zfill(6)
    else:
        is_negative = False
        number = str(number).zfill(6)
    bga = [int(number[-2:]), int(number[-4:-2]), int(number[:-4])]
    return Currency(bga, is_negative)


# DB'den ki??inin paras??n?? al??r.
async def get_money(member_id):
    money = db.record("SELECT money FROM player WHERE UserID = ?", member_id)
    return money


# DB'ye ki??inin paras??n?? ayarlar.
async def set_money(member_id, balance):
    db.execute("UPDATE player SET money = ? WHERE UserId = ?", balance, member_id)
    db.commit()


# DB'deki ki??inin paras??n?? verilen miktarda de??i??tirir.
async def add_money(member_id, balance):
    db.execute("UPDATE player SET money = money + ? WHERE UserId = ?", balance, member_id)
    db.commit()


# DB'deki herkesin paras??n?? verilen miktara ayarlar.
async def set_all_money(balance):
    members = db.column("SELECT UserID FROM player")

    db.multiexec(f"UPDATE player SET money = {balance} WHERE UserID = ?", ((user_id,) for user_id in members))
    db.commit()


# DB'deki herkesin paras??n?? verilen miktarda de??i??tirir.
async def change_all_money(balance):
    members = db.column("SELECT UserID FROM player")

    db.multiexec(f"UPDATE player SET money = money + {balance} WHERE UserID = ?", ((user_id,) for user_id in members))
    db.commit()
