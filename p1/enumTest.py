from enum import Enum, unique


@unique
class WeekDay(Enum):
    SUN = 0
    MON = 1
    TUE = 2
    WED = 3
    THU = 4
    Fir = 5
    SAT = 6


print(WeekDay.SUN)
for position, i in enumerate(WeekDay):
    print("%s      …… %s" % (i, WeekDay(position)))
