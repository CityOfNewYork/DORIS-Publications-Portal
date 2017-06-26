from collections import namedtuple

LanguagePair = namedtuple("Language", ["value", "text"])

ENGLISH = "english"
SPANISH = "spanish"
CHINESE = "chinese"
RUSSIAN = "russian"
ARABIC = "arabic"
BENGALI = "bengali"
FRENCH = "french"
HAITIAN_CREOLE = "haitian_creole"
ITALIAN = "italian"
KOREAN = "korean"
POLISH = "polish"
URDU = "urdu"
YIDDISH = "yiddish"

ALL = [
    LanguagePair(ENGLISH, "English"),
    LanguagePair(SPANISH, "Spanish"),
    LanguagePair(CHINESE, "Chinese"),
    LanguagePair(RUSSIAN, "Russian"),
    LanguagePair(ARABIC, "Arabic"),
    LanguagePair(BENGALI, "Bengali"),
    LanguagePair(FRENCH, "French"),
    LanguagePair(HAITIAN_CREOLE, "Haitian Creole"),
    LanguagePair(ITALIAN, "Italian"),
    LanguagePair(KOREAN, "Korean"),
    LanguagePair(POLISH, "Polish"),
    LanguagePair(URDU, "Urdu"),
    LanguagePair(YIDDISH, "Yiddish")
]
