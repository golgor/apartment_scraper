from enum import Enum


class _Wien(Enum):
    ALL = "wien"
    INNERESTADT = "wien/wien-1010-innere-stadt"
    LEOPOLDSTADT = "wien/wien-1020-leopoldstadt"
    LANDSTRASSE = "wien/wien-1030-landstrasse"
    WIEDEN = "wien/wien-1040-wieden"
    MARGARETEN = "wien/wien-1050-margareten"
    MARIAHILF = "wien/wien-1060-mariahilf"
    NEUBAU = "wien/wien-1070-neubau"
    JOSEFSTADT = "wien/wien-1080-josefstadt"
    ALSERGRUND = "wien/wien-1090-alsergrund"
    FAVORITEN = "wien/wien-1100-favoriten"
    SIMMERING = "wien/wien-1110-simmering"
    MEIDLING = "wien/wien-1120-meidling"
    HIETZING = "wien/wien-1130-hietzing"
    PENZING = "wien/wien-1140-penzing"
    RUDOLFSHEIM_FUNFHAUS = "wien/wien-1150-rudolfsheim-fuenfhaus"
    OTTAKRING = "wien/wien-1160-ottakring"
    HERNALS = "wien/wien-1170-hernals"
    WÄHRING = "wien/wien-1180-währing"
    DÖBLING = "wien/wien-1190-döbling"
    BRIGITTENAU = "wien/wien-1200-brigittenau"
    FLORIDSDORF = "wien/wien-1210-floridsdorf"
    DONAUSTADT = "wien/wien-1220-donaustadt"
    LIESING = "wien/wien-1230-liesing"


class _Niederösterreich(Enum):
    ALL = 3
    AMSTETTEN = 305
    BADEN = 306
    BRUCK_AN_DER_LEITHA = 307
    GÄNSERNDORF = 308
    GMÜND = 309
    HOLLABRUNN = 310
    HORN = 311
    KORNEUBURG = 312
    KREMS_AN_DER_DONAU = 301
    KREMS_LAND = 313
    LILIENFELD = 314
    MELK = 315
    MISTELBACH = 316
    MÖDLING = 317
    NEUNKIRCHEN = 318
    SANKT_PÖLTEN = 302
    SANKT_PÖLTEN_LAND = 319
    SCHEIBBS = 320
    TULLN = 321
    WAIDHOFEN_AN_DER_THAYA = 322
    WAIDHOFEN_AN_DER_YBBS = 303
    WIENER_NEUSTADT = 304
    WIENER_NEUSTADT_LAND = 323
    ZWETTL = 325


class AreaId:
    """AreaId to wrap the area enumerators of different states."""

    WIEN = _Wien
    NIEDERÖSTERREICH = _Niederösterreich
    BURGENLAND = 1
    KÄRNTEN = 2
    OBERÖSTERREICH = 4
    SALZBURG = 5
    STEIERMARK = 6
    TIROL = 7
    VORARLBERG = 8
