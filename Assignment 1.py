# Task 12 - seasonal rate cards + bonus, two-decimal analyser readings

from decimal import Decimal as D, ROUND_HALF_UP

RATE_CARDS = {

    "normal": {

        "base": D("30.00"),

        "fat_step": D("0.40"),

        "snf_step": D("0.30")

    },

    "apr_jun": {

        "base": D("32.00"),

        "fat_step": D("0.45"),

        "snf_step": D("0.30")

    },

}

BONUS_LIMIT_LITRES = D("500")

BONUS_PER_LITRE = D("0.50")

STD_FAT, STD_SNF, STEP = D("3.5"), D("8.5"), D("0.1")

def money(x):

    return x.quantize(D("0.01"), rounding=ROUND_HALF_UP)

def get_card(season):

    """Select the rate card for a season."""

    return RATE_CARDS[season]

def rate_per_litre(fat, snf, season="normal"):

    """Calculate rate per litre using fractional steps."""

    c = get_card(season)

    fs = (D(str(fat)) - STD_FAT) / STEP

    ss = (D(str(snf)) - STD_SNF) / STEP

    return money(c["base"] + fs * c["fat_step"] + ss * c["snf_step"])

def payout(litres, fat, snf, season="normal"):

    """Amount for one entry (no bonus)."""

    return money(D(str(litres)) * rate_per_litre(fat, snf, season))

def bonus(total_litres):

    """Bonus applies when ten-day volume exceeds 500 litres."""

    total = D(str(total_litres))

    return money(total * BONUS_PER_LITRE) if total > BONUS_LIMIT_LITRES else D("0.00")

def ten_day_total(entries, season="normal"):

    """Calculate total litres, payment, bonus and grand total."""

    litres = sum(D(str(e[0])) for e in entries)

    pay = sum(

        (payout(l, f, s, season) for l, f, s in entries),

        D("0")

    )

    b = bonus(litres)

    return litres, pay, b, pay + b

# Tests

print("normal  3.5/8.5 :", rate_per_litre(3.5, 8.5))

print("normal  4.2/8.7 :", rate_per_litre(4.2, 8.7))

print("apr_jun 4.2/8.7 :", rate_per_litre(4.2, 8.7, "apr_jun"))

print("apr_jun 3.57/8.43:", rate_per_litre(3.57, 8.43, "apr_jun"))

whole = round((D("3.57") - STD_FAT) / STEP)

print("whole-step fat 3.57 ->", whole, "steps")

print("pay 480 L, 4.2/8.7, apr_jun:",

      ten_day_total([(480, 4.2, 8.7)], "apr_jun"))

print("pay 500 L (no bonus):",

      ten_day_total([(500, 4.2, 8.7)], "apr_jun"))

print("pay 500.5 L (bonus):",

      ten_day_total([(500.5, 4.2, 8.7)], "apr_jun"))

assert rate_per_litre(4.2, 8.7) == D("33.40")

assert bonus(500) == D("0.00")

assert bonus(501) == D("250.50")

print("All Task 12 tests passed")
