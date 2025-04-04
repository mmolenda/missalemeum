import { plPL } from '@mui/x-date-pickers/locales';
import { enUS } from '@mui/x-date-pickers/locales';


export type Locale = "pl" | "en";

export const META_DESCRIPTION: {
  pl: string;
  en: string;
} = {
	"pl": "Mszał Rzymski zawierający kalendarz liturgiczny i czytania wg układu z 1962 r. dla Mszy św. w nadzwyczajnej formie rytu rzymskiego (Msza Trydencka, NFRR).",
	"en": "The 1962 Roman Missal containing the liturgical calendar and the readings for Traditional Latin Mass (Extraordinary form of the Roman Rite, Tridentine Mass, TLM)"
}

export const SEARCH_PLACEHOLDER = {"en": "Search", "pl": "Szukaj"}
export const IN = {"en": "in", "pl": "w"}
export const RANK_NAMES = {
	"en": [null, "1st class", "2nd class", "3rd class", "4th class"],
	"pl": [null, "1 kl.", "2 kl.", "3 kl.", "4 kl."]
}
export const COMMEMORATION = {"en": "Commemoration", "pl": "Wsp."}
export const VESTMENTS_RED = {"en": "Red vestments", "pl": "Szaty czerwone"}
export const VESTMENTS_GREEN = {"en": "Green vestments", "pl": "Szaty zielone"}
export const VESTMENTS_WHITE = {"en": "White vestments", "pl": "Szaty białe"}
export const VESTMENTS_VIOLET = {"en": "Violet vestments", "pl": "Szaty fioletowe"}
export const VESTMENTS_BLACK = {"en": "Black vestments", "pl": "Szaty czarne"}
export const VESTMENTS_PINK = {"en": "Pink vestments", "pl": "Szaty różowe"}
export const MENUITEM_PROPER = {"en": "Proprium", "pl": "Proprium"}
export const MENUITEM_ORDO = {"en": "Ordo", "pl": "Ordo"}
export const MENUITEM_VOTIVE = {"en": "Votive Masses", "pl": "Msze wotywne"}
export const MENUITEM_ORATIO = {"en": "Prayers", "pl": "Modlitwy"}
export const MENUITEM_CANTICUM = {"en": "Chants", "pl": "Pieśni"}
export const MENUITEM_SUPPLEMENT = {"en": "Supplement", "pl": "Suplement"}
export const MENUITEM_INFO = {"en": "About", "pl": "Informacje"}
export const MENUITEM_ANNOUNCEMENTS = {"en": "Announcements", "pl": "Ogłoszenia"}
export const MSG_ADDRESS_COPIED = {"en": "Address copied to clipboard", "pl": "Adres skopiowany do schowka"}
export const MSG_COOKIES = {"en": "This website uses cookies. ",
														"pl": "Ta strona wykorzystuje ciasteczka (cookies). "}
export const MSG_POLICY_LINK = {"en": "Privacy Policy.",
														    "pl": "Polityka Prywatności"}
export const MSG_POLICY_DECLINE_BUTTON: { [key in Locale]: string } = {"en": "No, thanks",
	"pl": "Nie, dziękuję"}
export const TODAY = {"en": "Today", "pl": "Dzisiaj"}
export const POWERED_BY = {"en": "Powered by", "pl": "Treści dostarcza"}
export const SEARCH_SUGGESTIONS_PROPER: {
  pl: string[];
  en: string[];
} = {
	"pl": ["Niedziela", "Niedziela Adwentu", "Boże Narodzenie", "Objawienie Pańskie", "Środa Popielcowa",
				 "Niedziela Palmowa", "Niedziela Zmartwychwstania", "Wniebowstąpienie Pańskie",
		     "Niedziela Zesłania Ducha Świętego", "Uroczystość Bożego Ciała", "Wniebowzięcie N. M. P.",
		     "Wszystkich Świętych", "Suchych Dni"],
	"en": ["Sunday of Advent", "The Nativity of Our Lord", "Epiphany of the Lord", "Ash Wednesday", "Palm Sunday",
				 "Easter Sunday", "Ascension of the Lord", "Pentecost Sunday", "Corpus Christi",
		     "Assumption of the Blessed Virgin Mary", "All Saints", "Ember"]
}
export const SEARCH_SUGGESTIONS_CANTICUM: {
  pl: string[];
  en: string[];
} = {
	"pl": ["Adwent", "Boże Narodzenie", "Wielki Post", "Wielkanoc", "Przygodne", "Eucharystyczne", "Jezus", "Maryja"],
	"en": [],
}
export const SEARCH_SUGGESTIONS_ORATIO: {
  pl: string[];
  en: string[];
} = {
	"pl": ["Eucharystyczne", "Wielki Post", "Maryja", "Poranne", "Wieczorne"],
	"en": []
}

export const MUI_DATEPICKER_LOCALE_TEXT: {
  pl: any;
  en: any;
} = {
	"pl": plPL.components.MuiLocalizationProvider.defaultProps.localeText,
	"en": enUS.components.MuiLocalizationProvider.defaultProps.localeText
}
