import enum


class AddExpenseState(enum.IntEnum):
    AMOUNT = 1
    CATEGORY = 2
    DESCRIPTION_CHOICE = 3
    DESCRIPTION_SET = 4


class AddIncomeState(enum.IntEnum):
    AMOUNT = 1
    DESCRIPTION_CHOICE = 2
    DESCRIPTION_SET = 3


class AddCategoryState(enum.IntEnum):
    NAME = 1
    LIMIT_CHOICE = 2
    LIMIT_SET = 3


class UpdateCategoryLimitState(enum.IntEnum):
    CATEGORY = 1
    LIMIT = 2


class UpdateUTCOffsetState(enum.IntEnum):
    REGION = 1
    UTC_OFFSET = 2


class UTCRegion(enum.Enum):
    AF = "африка"
    EU = "европа"
    AS = "азия"
    NA = "северная америка"
    SA = "южная америка"
    OC = "австралия и океания"
    AN = "антарктида"
    NO = "выбрать время вручную"

    def get_offsets(self) -> list[int]:
        regions_to_utc_offsets_map = {
            UTCRegion.AF: [-1, 0, 1, 2, 3, 4],
            UTCRegion.EU: [0, 1, 2, 3, 4],
            UTCRegion.AS: [4, 5, 6, 7, 8, 9, 10, 11, 12],
            UTCRegion.NA: [-11, -10, -9, -8, -7, -6, -5, -4],
            UTCRegion.SA: [-5, -4, -3, -2],
            UTCRegion.OC: [6, 7, 8, 9, 10, 11, 12],
            UTCRegion.AN: [-6, -3, 0, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13],
            UTCRegion.NO: list(range(-12, 14)),
        }
        return regions_to_utc_offsets_map[self]
