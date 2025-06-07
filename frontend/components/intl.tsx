import { plPL } from '@mui/x-date-pickers/locales';
import { enUS } from '@mui/x-date-pickers/locales';
import { esES } from '@mui/x-date-pickers/locales';


export type Locale = "pl" | "en" | "es";

export const META_DESCRIPTION: {
	pl: string;
	en: string;
	es: string;
} = {
	"pl": "Mszał Rzymski zawierający kalendarz liturgiczny i czytania wg układu z 1962 r. dla Mszy św. w nadzwyczajnej formie rytu rzymskiego (Msza Trydencka, NFRR).",
	"en": "The 1962 Roman Missal containing the liturgical calendar and the readings for Traditional Latin Mass (Extraordinary form of the Roman Rite, Tridentine Mass, TLM)",
	"es": "El Misal Romano de 1962 que contiene el calendario litúrgico y las lecturas para la Misa Tradicional en Latín (forma extraordinaria del Rito Romano, Misa Tridentina, TLM).",
}

export const SEARCH_PLACEHOLDER = { "en": "Search", "pl": "Szukaj", "es": "Buscar" }
export const IN = { "en": "in", "pl": "w", "es": "en" }
export const RANK_NAMES = {
	"en": [null, "1st class", "2nd class", "3rd class", "4th class"],
	"pl": [null, "1 kl.", "2 kl.", "3 kl.", "4 kl."],
	"es": [null, "Iª Clase", "IIª Clase", "IIIª Clase", "IVª Clase"]
}
export const COMMEMORATION = { "en": "Commemoration", "pl": "Wsp.", "es": "Conmemoración" }
export const VESTMENTS_RED = { "en": "Red vestments", "pl": "Szaty czerwone", "es": "Ornamentos rojos" }
export const VESTMENTS_GREEN = { "en": "Green vestments", "pl": "Szaty zielone", "es": "Ornamentos verdes" }
export const VESTMENTS_WHITE = { "en": "White vestments", "pl": "Szaty białe", "es": "Ornamentos blancos" }
export const VESTMENTS_VIOLET = { "en": "Violet vestments", "pl": "Szaty fioletowe", "es": "Ornamentos morados" }
export const VESTMENTS_BLACK = { "en": "Black vestments", "pl": "Szaty czarne", "es": "Ornamentos negros" }
export const VESTMENTS_PINK = { "en": "Pink vestments", "pl": "Szaty różowe", "es": "Ornamentos rosados" }
export const MENUITEM_PROPER = { "en": "Proprium", "pl": "Proprium", "es": "Propio" }
export const MENUITEM_ORDO = { "en": "Ordo", "pl": "Ordo", "es": "Ordo" }
export const MENUITEM_VOTIVE = { "en": "Votive Masses", "pl": "Msze wotywne", "es": "Misas votivas" }
export const MENUITEM_ORATIO = { "en": "Prayers", "pl": "Modlitwy", "es": "Oraciones" }
export const MENUITEM_CANTICUM = { "en": "Chants", "pl": "Pieśni", "es": "Canticos" }
export const MENUITEM_SUPPLEMENT = { "en": "Supplement", "pl": "Suplement", "es": "Suplemento" }
export const MENUITEM_INFO = { "en": "About", "pl": "Informacje", "es": "Acerca de" }
export const MENUITEM_ANNOUNCEMENTS = { "en": "Announcements", "pl": "Ogłoszenia", "es": "Avisos" }
export const MSG_ADDRESS_COPIED = { "en": "Address copied to clipboard", "pl": "Adres skopiowany do schowka", "es": "Dirección copiada al portapapeles" }
export const MSG_COOKIES = {
	"en": "This website uses cookies. ",
	"pl": "Ta strona wykorzystuje ciasteczka (cookies). ",
	"es": "Este sitio web utiliza cookies. "
}
export const MSG_POLICY_LINK = {
	"en": "Privacy Policy.",
	"pl": "Polityka Prywatności",
	"es": "Politica de privacidad"
}
export const MSG_POLICY_DECLINE_BUTTON: { [key in Locale]: string } = {
	"en": "No, thanks",
	"pl": "Nie, dziękuję",
	"es": "No, gracias"
}
export const TODAY = { "en": "Today", "pl": "Dzisiaj", "es": "Hoy" }
export const POWERED_BY = { "en": "Powered by", "pl": "Treści dostarcza", "es": "Impulsado por" }
export const SEARCH_SUGGESTIONS_PROPER: {
	pl: string[];
	en: string[];
	es: string[];
} = {
	"pl": ["Niedziela", "Niedziela Adwentu", "Boże Narodzenie", "Objawienie Pańskie", "Środa Popielcowa",
		"Niedziela Palmowa", "Niedziela Zmartwychwstania", "Wniebowstąpienie Pańskie",
		"Niedziela Zesłania Ducha Świętego", "Uroczystość Bożego Ciała", "Wniebowzięcie N. M. P.",
		"Wszystkich Świętych", "Suchych Dni"],
	"en": ["Sunday of Advent", "The Nativity of Our Lord", "Epiphany of the Lord", "Ash Wednesday", "Palm Sunday",
		"Easter Sunday", "Ascension of the Lord", "Pentecost Sunday", "Corpus Christi",
		"Assumption of the Blessed Virgin Mary", "All Saints", "Ember"],
	"es": ["Domingo de Adviento", "La Natividad de Nuestro Señor", "Epifanía del Señor", "Miércoles de Ceniza",
		"Domingo de Ramos", "Domingo de Resurrección", "Ascensión del Señor",
		"Domingo de Pentecostés", "Corpus Christi", "Asunción de la Santísima Virgen María",
		"Todos los Santos", "Témporas"]
}
export const SEARCH_SUGGESTIONS_CANTICUM: {
	pl: string[];
	en: string[];
	es: string[];
} = {
	"pl": ["Adwent", "Boże Narodzenie", "Wielki Post", "Wielkanoc", "Przygodne", "Eucharystyczne", "Jezus", "Maryja"],
	"en": [],
	"es": []
}
export const SEARCH_SUGGESTIONS_ORATIO: {
	pl: string[];
	en: string[];
	es: string[];
} = {
	"pl": ["Eucharystyczne", "Wielki Post", "Maryja", "Poranne", "Wieczorne"],
	"en": [],
	"es": [],
}

export const MUI_DATEPICKER_LOCALE_TEXT: {
	pl: any;
	en: any;
	es: any;
} = {
	"pl": plPL.components.MuiLocalizationProvider.defaultProps.localeText,
	"en": enUS.components.MuiLocalizationProvider.defaultProps.localeText,
	"es": esES.components.MuiLocalizationProvider.defaultProps.localeText,
}
