import type { ReactNode } from "react";
import Image from "next/image";
import Link from "next/link";
import Script from "next/script";
import { Roboto } from "next/font/google";
import { generateLocalisedMetadata } from "@/components/utils";
import { Locale } from "@/components/intl";
import Logo from "@/components/Logo";
import styles from "@/app/landing.module.css";

const roboto = Roboto({
  subsets: ["latin"],
  weight: ["400", "500", "700"],
  variable: "--font-landing-roboto",
});

const SITE_BASE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? "https://www.missalemeum.com";

const ABOUT_SECTION_ID = "about-missal";
const STRUCTURE_SECTION_ID = "missal-structure";
const FEATURES_SECTION_ID = "missal-features";
const USAGE_SECTION_ID = "living-tradition";
const RESOURCES_SECTION_ID = "resources";
const SUPPORT_SECTION_ID = "support";
const TRUST_SECTION_ID = "credibility";
const FAQ_SECTION_ID = "faq";

const DONATION_CONFIG: Record<Locale, { buyButtonId: string; publishableKey: string }> = {
  en: {
    buyButtonId: "buy_btn_1SA6zyASmawTdJcy077G1ZOj",
    publishableKey: "pk_live_51S9B6GASmawTdJcyQ1lrfyFvuGfciQ7Kci0Sw11AGBGjg7dbH0KlbFUOjpcD96LtyWT3JGhpS4oWfIjtHAoCFbo500O7bzQ4Nr",
  },
  pl: {
    buyButtonId: "buy_btn_1SA6NzASmawTdJcyyd6YboOh",
    publishableKey: "pk_live_51S9B6GASmawTdJcyQ1lrfyFvuGfciQ7Kci0Sw11AGBGjg7dbH0KlbFUOjpcD96LtyWT3JGhpS4oWfIjtHAoCFbo500O7bzQ4Nr",
  },
};

type InternalNavItem = {
  label: string;
  targetId: string;
};

type FaqItem = {
  question: string;
  answer?: ReactNode;
  renderAnswer?: (lang: Locale) => ReactNode;
  schemaAnswer?: string;
};

type LandingCopy = {
  metaTitle: string;
  metaDescription: string;
  heroTag: string;
  heroHeading: string;
  heroSubheading?: string;
  heroIntro: string;
  primaryCtaLabel: string;
  secondaryCtaLabel: string;
  todayCtaLabel: string;
  internalNav: InternalNavItem[];
  featuresHeading: string;
  featuresIntro: string;
  features: Array<{ title: string; description: string }>;
  calendarCaption: string;
  properCaption: string;
  usageHeading: string;
  resourcesHeading: string;
  supportHeading: string;
  trustHeading: string;
  trustSignature: string;
  faqHeading: string;
  faq: FaqItem[];
  metaNote: string;
};

const LANDING_COPY: Record<Locale, LandingCopy> = {
  en: {
    metaTitle: "Missale Meum – Latin Mass readings and resources made simple",
    metaDescription:
      "Missale Meum provides complete daily Latin Mass readings and resources, accessible and simple to use.",
    heroTag: "1962 Roman Missal",
    heroHeading: "Missale Meum",
    heroSubheading: "Complete resources for the Latin Mass (1962 Missal)",
    heroIntro:
      "A bilingual edition of the 1962 Roman Missal. Follow the liturgical year, study the daily propers, and keep trusted devotions close—wherever you pray.",
    primaryCtaLabel: "Learn more about Missale Meum",
    secondaryCtaLabel: "Browse the calendar",
    todayCtaLabel: "Open today's proper",
    internalNav: [
      { label: "Overview", targetId: ABOUT_SECTION_ID },
      { label: "Missal structure", targetId: STRUCTURE_SECTION_ID },
      { label: "Digital features", targetId: FEATURES_SECTION_ID },
      { label: "How the faithful use it", targetId: USAGE_SECTION_ID },
      { label: "Tools & resources", targetId: RESOURCES_SECTION_ID },
      { label: "How you can help", targetId: SUPPORT_SECTION_ID },
      { label: "Trust & provenance", targetId: TRUST_SECTION_ID },
      { label: "FAQ", targetId: FAQ_SECTION_ID },
    ],
    featuresHeading: "Everything you need for the Extraordinary Form",
    featuresIntro:
      "Missale Meum is more than a calendar. It is a study companion, a travel missal, and a reliable reference for clergy and laity alike.",
    features: [
      {
        title: "Daily propers in context",
        description:
          "View complete Mass formularies in Latin with a parallel vernacular translation. Introits, collects, lessons, graduals, and rubrical notes appear together so nothing is lost between books.",
      },
      {
        title: "Traditional calendar intelligence",
        description:
          "Ranks, vestment colours, commemorations, ember days, and octaves are displayed at a glance. Quickly move through years to study how the temporale and sanctorale intersect.",
      },
      {
        title: "Reference library included",
        description:
          "From votive Masses and Commons to seasonal chants and devotional prayers, Missale Meum gathers the texts most often needed by families, choirs, and altar servers.",
      },
    ],
    calendarCaption: "Traditional liturgical calendar with feasts and commemorations.",
    properCaption: "Full daily propers in Latin and vernacular.",
    usageHeading: "How the faithful live with the missal",
    resourcesHeading: "Tools, feeds, and embeds",
    supportHeading: "How you can help",
    trustHeading: "Prepared with reverence and scholarship",
    trustSignature: "The Missale Meum team — traditional Catholics in Poland",
    faqHeading: "Frequently asked questions",
    faq: [
      {
        question: "Is Missale Meum free to use?",
        answer:
          "Yes. Missale Meum is a volunteer-maintained project and will always remain free for personal use. You can install it as a web app or use it from any modern browser without payment or registration. If you wish, optional donations help cover hosting and support Catholic education in Poland.",
      },
      {
        question: "Which edition of the Missal does it follow?",
        answer:
          "The texts follow the 1962 editio typica of the Roman Missal (Extraordinary Form). Propers, commemorations, and rubrics reflect the legislation issued after the 1960 code of rubrics.",
      },
      {
        question: "Where do Missale Meum's texts come from?",
        renderAnswer: renderProjectInfoSection,
        schemaAnswer:
          "Latin texts come from Divinum Officium, English translations are checked against the same sources, and the project remains a private open initiative with code on GitHub.",
      },
      {
        question: "How often are texts reviewed and updated?",
        answer:
          "Editorial changes are logged publicly. Corrections from priests, translators, and readers are reviewed, documented, and merged once they are verified against the 1962 sources.",
      },
    ],
    metaNote: "Content sourced from the 1962 Roman Missal and traditional liturgical books.",
  },
  pl: {
    metaTitle: "Missale Meum – Teksty i czytania do mszy trydenckiej",
    metaDescription:
      "Missale Meum udostępnia codzienne teksty i czytania do mszy trydenckiej, wraz z kalendarzem liturgicznym i proprium – wszystko w prosty i przejrzysty sposób.",
    heroTag: "Msza Trydencka",
    heroHeading: "Missale Meum",
    heroSubheading: "Teksty i czytania do Mszy trydenckiej",
    heroIntro:
      "Dwujęzyczne wydanie Mszału Rzymskiego z 1962 roku. Śledź rok liturgiczny, czytaj codzienne proprium i miej sprawdzone modlitwy zawsze pod ręką.",
    primaryCtaLabel: "Poznaj Missale Meum",
    secondaryCtaLabel: "Kalendarz liturgiczny",
    todayCtaLabel: "Dzisiejsze proprium",
    internalNav: [
      { label: "Wprowadzenie", targetId: ABOUT_SECTION_ID },
      { label: "Struktura mszału", targetId: STRUCTURE_SECTION_ID },
      { label: "Funkcje cyfrowe", targetId: FEATURES_SECTION_ID },
      { label: "Jak korzystają wierni", targetId: USAGE_SECTION_ID },
      { label: "Narzędzia", targetId: RESOURCES_SECTION_ID },
      { label: "Wsparcie projektu", targetId: SUPPORT_SECTION_ID },
      { label: "Wiarygodność", targetId: TRUST_SECTION_ID },
      { label: "FAQ", targetId: FAQ_SECTION_ID },
    ],
    featuresHeading: "Wszystko dla Mszy w nadzwyczajnej formie",
    featuresIntro:
      "Missale Meum to coś więcej niż kalendarz — to narzędzie do modlitwy, nauki i przygotowania do liturgii w klasycznym rycie rzymskim.",
    features: [
      {
        title: "Pełne proprium w kontekście",
        description:
          "Kompletne formularze Mszy świętej z tekstem łacińskim i polskim obok siebie. Modlitwy, czytania, antyfony i wskazówki rubrycystyczne są zawsze w jednym miejscu.",
      },
      {
        title: "Inteligentny kalendarz tradycyjny",
        description:
          "Od razu widać klasę obchodu, kolor szat i wspomnienia. Można łatwo przeskakiwać między latami i śledzić układ temporale i sanctorale.",
      },
      {
        title: "Biblioteka odniesień",
        description:
          "Wotywy i formularze wspólne, śpiewy sezonowe, modlitwy codzienne — Missale Meum gromadzi teksty najczęściej potrzebne rodzinom, scholii i ministrantom.",
      },
    ],
    calendarCaption: "Tradycyjny kalendarz liturgiczny z obchodami i wspomnieniami.",
    properCaption: "Pełne proprium dnia w łacinie i przekładzie.",
    usageHeading: "Jak wierni żyją z mszałem",
    resourcesHeading: "Narzędzia i materiały dodatkowe",
    supportHeading: "Wsparcie projektu",
    trustHeading: "Przygotowane z pietyzmem i wiedzą",
    trustSignature: "Zespół Missale Meum — tradycyjni katolicy z Polski",
    faqHeading: "Najczęstsze pytania",
    faq: [
      {
        question: "Czy Missale Meum jest płatne?",
        answer:
          "Nie. Missale Meum to projekt społeczny i pozostaje bezpłatny do prywatnego użytku. Można z niego korzystać w przeglądarce lub dodać jako aplikację webową na telefonie. Dobrowolne darowizny pomagają pokryć koszty utrzymania i wspierają edukację katolicką w Polsce.",
      },
      {
        question: "Na jakim wydaniu mszału bazuje serwis?",
        answer:
          "Teksty pochodzą z wydania typicznego z 1962 r. (forma nadzwyczajna). Uwzględniono rubryki wprowadzone reformą z 1960 r. oraz wspomnienia właściwe temu kalendarzowi.",
      },
      {
        question: "Skąd pochodzą teksty Missale Meum?",
        renderAnswer: renderProjectInfoSection,
        schemaAnswer:
          "Łacińskie teksty pochodzą z serwisu Divinum Officium, tłumaczenia z Mszału Rzymskiego Pallottinum 1963, a projekt jest prywatną inicjatywą z otwartym kodem na GitHubie.",
      },
      {
        question: "Jak często wprowadzane są poprawki?",
        answer:
          "Zmiany redakcyjne są dokumentowane publicznie. Sugestie kapłanów, tłumaczy i czytelników są weryfikowane i wdrażane po porównaniu ze źródłami z 1962 r.",
      },
    ],
    metaNote: "Treści zaczerpnięte z Mszału Rzymskiego z 1962 r. i tradycyjnych ksiąg liturgicznych.",
  },
};

const PHOTO_CREDIT: Record<Locale, string> = {
  en: 'Photography courtesy of "Jerzy Szałaciński | key4"',
  pl: 'Fotografie dzięki uprzejmości „Jerzego Szałacińskiego | key4”',
};

const renderIntro = (lang: Locale) => {
  if (lang === "pl") {
    return (
      <>
        <p>
          Missale Meum powstało, aby wiernym przywiązanym do klasycznej liturgii dać wygodny dostęp do Mszału Rzymskiego z 1962 r. Każdy formularz został wiernie przepisany,
          a łacińskie teksty zestawiono z przekładem polskim, aby zawsze można było korzystać z obu wersji równolegle.
        </p>
        <p>
          Serwis obejmuje rok liturgiczny w całości: od Adwentu aż po ostatnią niedzielę po Zesłaniu Ducha Świętego, z uwzględnieniem Suchych Dni, oktaw i wigilii. Dodatkowe komentarze pomagają 
          zrozumieć rubryki i okresy liturgiczne. Wyszukiwarka prowadzi do konkretnych świąt, a <Link href="/pl/calendar">kalendarz</Link> pozwala przechodzić pomiędzy cyklami bez utraty kontekstu.
        </p>
        <p>
          Missale Meum wspiera codzienną modlitwę. W jednym miejscu otworzysz <Link href="/pl/votive">msze wotywne</Link>, <Link href="/pl/oratio">modlitwy codzienne</Link>, <Link href="/pl/canticum">śpiewy na dany okres</Link> oraz obszerny <Link href="/pl/supplement/index">suplement</Link> rubryk i komentarzy.
          Wierni sięgają po Missale Meum jako prosty i przejrzysty mszalik online, pomocny w przygotowaniu do Mszy, modlitwie osobistej i zawsze pod
          ręką, gdy papierowy egzemplarz jest poza zasięgiem.
        </p>
      </>
    );
  }

  return (
    <>
      <p>
        Missale Meum was created so Catholics devoted to the classical Roman Rite can pray with the 1962 Missal without compromise. Each Mass formulary is faithfully transcribed,
        pairing the authoritative Latin with a carefully checked vernacular translation so families, choirs, and servers can meditate on every proper together.
      </p>
      <p>
        The site spans the entire liturgical year—from the purple of Advent to the final green Sundays after Pentecost. Rubrical notes explain ember weeks, octaves, and commemorations,
        while the calendar for the <Link href="/en/calendar">Proper of Time</Link> and the <Link href="/en/calendar#sanctorale">Proper of Saints</Link> keeps both cycles within reach.
        A focused search helps you find major feasts, votives, and commemorations in seconds.
      </p>
      <p>
        Missale Meum supports personal prayer throughout the week. Within a single resource you can open <Link href="/en/votive">votive Mass formularies</Link>,
        <Link href="/en/oratio">beloved prayers</Link>, <Link href="/en/canticum">seasonal chants</Link>, and an extensive <Link href="/en/supplement/index">supplement</Link> of rubrics and devotions.
        Many readers consult the propers at home before Mass, review them during study, or revisit them afterwards; the project is not meant to replace the printed hand missal in church,
        but it remains a dependable fallback while travelling or away from a liturgical library.
      </p>
    </>
  );
};

const renderStructureSection = (lang: Locale) => {
  const internalLinks = [
    { href: `/${lang}/calendar#temporale`, label: lang === "pl" ? "Proprium de Tempore (Temporale)" : "Proper of Time (Temporale)" },
    { href: `/${lang}/calendar#sanctorale`, label: lang === "pl" ? "Proprium Sanctorum (Sanctorale)" : "Proper of Saints (Sanctorale)" },
    { href: `/${lang}/votive`, label: lang === "pl" ? "Msze wotywne" : "Votive Masses" },
    { href: `/${lang}/supplement/index`, label: lang === "pl" ? "Commons i rytuały" : "Commons and Rituals" },
    { href: `/${lang}/oratio`, label: lang === "pl" ? "Modlitwy i nabożeństwa" : "Prayers and Devotions" },
    { href: `/${lang}/canticum`, label: lang === "pl" ? "Śpiewy i hymnaria" : "Chants and hymnody" },
    { href: `/${lang}/supplement/info`, label: lang === "pl" ? "Informacje o projekcie" : "Project notes" },
  ];

  if (lang === "pl") {
    return (
      <>
        <p>
          Missale Meum wiernie odzwierciedla układ drukowanego mszału z 1962 roku. W serwisie znajdują się zarówno części stałe (Ordo Missae), jak i proprium każdego dnia roku
          liturgicznego – czytania, modlitwy i antyfony.
        </p>
        <p>
          Tekst łaciński został zestawiony z polskim tłumaczeniem, co ułatwia śledzenie liturgii, naukę łaciny oraz przygotowanie do katechezy czy homilii. Dodatkowe 
          informacje – jak klasa obchodu, kolor szat liturgicznych czy wspomnienia świętych – tworzą spójny przewodnik po formularzach i całym roku kościelnym.
        </p>
        <ul className={styles.articleList}>
          {internalLinks.map(({ href, label }) => (
            <li key={href}>
              <Link href={href}>{label}</Link>
            </li>
          ))}
        </ul>
      </>
    );
  }

  return (
    <>
      <p>
        Missale Meum mirrors the structure of a printed hand missal. Each liturgical day gathers the variable propers with the fixed Ordinary so readers can move seamlessly from
        preparation at the foot of the altar to the Last Gospel without juggling multiple books.
      </p>
      <p>
        Parallel translations make it easier to teach newcomers the language of the Roman Rite. Commentary notes draw attention to rank, commemorations, and vesture, while links to
        supplements and chants place every rubric in its wider context.
      </p>
      <ul className={styles.articleList}>
        {internalLinks.map(({ href, label }) => (
          <li key={href}>
            <Link href={href}>{label}</Link>
          </li>
        ))}
      </ul>
    </>
  );
};

const renderFeaturesIntro = (lang: Locale) => {
  if (lang === "pl") {
    return (
      <p>
        Serwis rozwija się zgodnie z potrzebami wspólnot korzystających z Mszału Rzymskiego z 1962 r. Najczęściej używane widoki to kalendarz liturgiczny oraz
        pełne proprium dnia, dostępne zarówno na komputerach, jak i na telefonach.
      </p>
    );
  }

  return (
    <p>
      Missale Meum grows with the communities that celebrate the Extraordinary Form. The screenshots below present the views most people keep open: the liturgical calendar with its
      feast ranks and the full proper text. Both layouts adapt gracefully to desktop and mobile screens.
    </p>
  );
};

const renderUsageSection = (lang: Locale) => {
  if (lang === "pl") {
    return (
      <>
        <p>
          Missale Meum pomaga rodzinom żyć rytmem roku liturgicznego. Rodziny czytają proprium prywatnie w domu i uczą dzieci modlitw rytu rzymskiego. 
          Wielu użytkowników podkreśla prostotę i przejrzystość strony—codzienne teksty są zawsze pod ręką, a łacina i polski obok siebie ułatwiają 
          przygotowanie do Mszy i medytację nad Ewangelią.
        </p>
        <p>
          Dla jednych staje się częścią lectio divina i modlitwy osobistej, dla innych najwygodniejszym sposobem, by sprawdzić jaki formularz 
          przypada danego dnia. Strona jest dobrze dostosowana do urządzeń mobilnych i często określana jako najłatwiejszy sposób dostępu do Mszału 
          Rzymskiego — darmowy, intuicyjny i zawsze dostępny. Ułatwia przygotowanie zanim wyjdzie się do kościoła i stanowi pewne oparcie zawsze wtedy, 
          gdy tradycyjny mszalik nie jest pod ręką.
        </p>
      </>
    );
  }

  return (
    <>
      <p>
        Missale Meum helps households keep pace with the liturgical year. Families read the propers privately at home and teach children the prayers of the 
        Roman Rite. Many users appreciate the simplicity and clarity of the site — daily texts are always at hand, with Latin and English side by side, making 
        preparation for Mass and Gospel meditation easier.
      </p>
      <p>
        For some it becomes part of lectio divina and private prayer, for others the most convenient 
        way to check which Mass is celebrated today. Designed to work smoothly on mobile devices, it is often described as the easiest way to access the 
        Roman Missal — free, intuitive, and always available. It keeps you informed before you leave for church and offers a trustworthy fallback whenever 
        a printed hand missal is out of reach.
      </p>
    </>
  );
};

function renderProjectInfoSection(lang: Locale): ReactNode {
  if (lang === "pl") {
    return (
      <>
        <p>
          Teksty łacińskie zaczerpnięto głównie z czcigodnej strony <a href="https://www.divinumofficium.com/" target="_blank" rel="noopener noreferrer">Divinum Officium</a>, a przekłady polskie z
          "Mszału Rzymskiego" (Pallottinum 1963) udostępnionego za zgodą wydawnictwa. Wybrane fragmenty Ordo pochodzą z serwisu <a href="https://www.fisheaters.com/" target="_blank" rel="noopener noreferrer">Fish Eaters</a>.
        </p>
        <p>
          Projekt Missale Meum jest otwarty: kod źródłowy znajduje się w <a href="https://github.com/mmolenda/missalemeum" target="_blank" rel="noopener noreferrer">repozytorium GitHub</a>, a strona ma charakter prywatny i nie reprezentuje żadnej instytucji.
        </p>
        <p>
          Kontakt: <a href="mailto:marcin@missalemeum.com">marcin@missalemeum.com</a>. Aktualności publikujemy także na Facebooku: <a href="https://www.facebook.com/missalemeum" target="_blank" rel="noopener noreferrer">facebook.com/missalemeum</a>.
        </p>
        <p>
          Msze własne dla diecezji polskich zachowują układ z <em>Calendarium Perpetuum pro Diœcesium Poloniæ</em> (1964). W serwisie pozostają jednak formularze z wcześniejszych wydań mszalika, z dodaniem nowych formularzy z 1965 roku w miejscach, gdzie brakowało odpowiednich tekstów.
        </p>
        <p>
          <Link href={`/${lang}/supplement/privacy-policy?ref=landing`}>Polityka prywatności</Link>.
        </p>
      </>
    );
  }

  return (
    <>
      <p>
        Latin texts largely come from the venerable <a href="https://www.divinumofficium.com/" target="_blank" rel="noopener noreferrer">Divinum Officium</a>, while parallel English passages draw on carefully reviewed translations of the same sources. Elements of the Ordo borrow from <a href="https://www.fisheaters.com/" target="_blank" rel="noopener noreferrer">Fish Eaters</a>.
      </p>
      <p>
        Missale Meum is an open project; the code is available on <a href="https://github.com/mmolenda/missalemeum" target="_blank" rel="noopener noreferrer">GitHub</a>. It remains a private initiative and speaks only for its maintainers.
      </p>
      <p>
        Contact us at <a href="mailto:marcin@missalemeum.com">marcin@missalemeum.com</a> or follow updates on <a href="https://www.facebook.com/missalemeum" target="_blank" rel="noopener noreferrer">facebook.com/missalemeum</a>.
      </p>
      <p>
        Polish diocesan propers follow the <em>Calendarium Perpetuum pro Diœcesium Poloniæ</em> (1964); for older formularies we reference the Pallottinum 1963 hand missal, adding the newer formularies where they were absent.
      </p>
      <p>
        <Link href={`/${lang}/supplement/privacy-policy?ref=landing`}>Privacy policy</Link>.
      </p>
    </>
  );
}

const renderSupportSection = (lang: Locale) => {
  const donationDetails = DONATION_CONFIG[lang];

  if (lang === "pl") {
    return (
      <>
        <p>
          Missale Meum jest i pozostanie bezpłatne do osobistego użytku. Jeśli chcesz wesprzeć rozwój projektu, rozważ następujące formy pomocy:
        </p>
        <ul className={styles.articleList}>
          <li>modlitwa w intencji autorów i użytkowników;</li>
          <li>przekazywanie sugestii oraz poprawek merytorycznych;</li>
          <li>dzielenie się serwisem z rodziną, przyjaciółmi i wspólnotą parafialną;</li>
          <li>udostępnianie brakujących tekstów i komentarzy biblijnych;</li>
          <li>
            dobrowolna darowizna — Missale Meum jest i pozostanie bezpłatne.
            Twoja darowizna w pierwszej kolejności pokrywa podstawowe koszty działania serwisu – domenę, serwer i usługi pomocnicze.
            Pozostałe środki kierujemy na wsparcie edukacji katolickiej w Polsce.
          </li>
        </ul>
        <div className={styles.donateCta}>
          <stripe-buy-button
            buy-button-id={donationDetails.buyButtonId}
            publishable-key={donationDetails.publishableKey}
          />
        </div>
      </>
    );
  }

  return (
    <>
      <p>
        Missale Meum will always remain free to use. If you would like to help sustain the project, you can:
      </p>
      <ul className={styles.articleList}>
        <li>remember Missale Meum in your prayers;</li>
        <li>send feedback and corrections—it helps us improve;</li>
        <li>share the project with friends, families, and parish groups;</li>
        <li>contribute missing texts or trusted commentaries;</li>
        <li>
          make a one-time or recurring donation — Missale Meum remains free to use. Your donation is used first to cover the essential costs of running Missale Meum – the domain, server, and auxiliary services.
          Any remainder is directed to supporting Catholic education in Poland.
        </li>
      </ul>
      <div className={styles.donateCta}>
        <stripe-buy-button
          buy-button-id={donationDetails.buyButtonId}
          publishable-key={donationDetails.publishableKey}
        />
      </div>
    </>
  );
};

const renderResourcesSection = (lang: Locale) => {
  if (lang === "pl") {
    return (
      <>
        <p>
          Suplement Missale Meum zawiera rozbudowane opracowania okresów liturgicznych, sakramentów oraz materiały pomocnicze dla wiernych i katechistów.
        </p>
        <ul className={styles.articleList}>
          <li><strong>Okresy liturgiczne</strong> – komentarze i przepisy: <Link href="/pl/supplement/1-wprowadzenie?ref=landing">Wprowadzenie</Link>, <Link href="/pl/supplement/2-adwent?ref=landing">Adwent</Link>, <Link href="/pl/supplement/3-boze-narodzenie?ref=landing">Boże Narodzenie</Link>, <Link href="/pl/supplement/6-wielki-post?ref=landing">Wielki Post</Link> i kolejne aż po okres po Zesłaniu Ducha Świętego.</li>
          <li><strong>Sakramenty</strong> – praktyczne przewodniki: <Link href="/pl/supplement/20-chrzest?ref=landing">Chrzest</Link>, <Link href="/pl/supplement/21-pokuta?ref=landing">Pokuta</Link>, <Link href="/pl/supplement/22-malzenstwo?ref=landing">Małżeństwo</Link>.</li>
          <li><strong>Ebook</strong> – mszalik na czytniki: <a href="https://www.dropbox.com/s/88z242hgr0q6e2e/mszalik.epub?dl=0" target="_blank" rel="noopener noreferrer">pobierz epuba</a>.</li>
          <li><strong>Msza dla początkujących</strong> – przewodnik PDF: <a href="https://www.dropbox.com/s/a94bingl33xlirx/msza-dla-pocz%C4%85tkuj%C4%85cych.pdf?dl=0" target="_blank" rel="noopener noreferrer">msza-dla-początkujących.pdf</a>.</li>
        </ul>
        <p>
          Strona działa jako aplikacja <abbr title="Progressive Web App">PWA</abbr>. Dodaj ją do ekranu startowego na Androidzie (Chrome → „Dodaj do ekranu startowego”) lub na iPhonie (Safari → Udostępnij → „Dodaj do ekranu głównego”).
        </p>
        <p>
          Kalendarz liturgiczny dostępny jest w formacie iCalendar: <a href="https://www.missalemeum.com/pl/api/v3/icalendar" target="_blank" rel="noopener noreferrer">pełny feed</a>. Możesz wczytać go w Google Calendar lub Outlooku.
        </p>
        <p>
          Udostępniamy również widżet propriów do osadzenia na stronie: <code>&lt;iframe src="https://www.missalemeum.com/pl/widgets/propers?theme=light" height=300 style="width: 100%;"&gt;&lt;/iframe&gt;</code> (parametr <code>theme</code> przyjmuje wartości <code>light</code> lub <code>dark</code>).
        </p>
      </>
    );
  }

  return (
    <>
      <p>Missale Meum provides practical tools that extend beyond the website itself.</p>
      <ul className={styles.articleList}>
        <li><strong>Install as a PWA:</strong> on Android open the site in Chrome and choose “Add to Home screen”; on iPhone use Safari → Share → “Add to Home Screen”.</li>
        <li><strong>Liturgical calendar feeds:</strong> subscribe via iCalendar – <a href="https://www.missalemeum.com/en/api/v3/icalendar" target="_blank" rel="noopener noreferrer">all feasts</a>, or limit to <a href="https://www.missalemeum.com/en/api/v3/icalendar/1" target="_blank" rel="noopener noreferrer">first class</a>, <a href="https://www.missalemeum.com/en/api/v3/icalendar/2" target="_blank" rel="noopener noreferrer">first &amp; second class</a>, and <a href="https://www.missalemeum.com/en/api/v3/icalendar/3" target="_blank" rel="noopener noreferrer">through third class</a>.</li>
        <li><strong>Embeddable widget:</strong> place Missale Meum propers on your site with <code>&lt;iframe src="https://www.missalemeum.com/en/widgets/propers?theme=light" height=300 style="width: 100%;"&gt;&lt;/iframe&gt;</code> (use <code>theme=dark</code> for the dark variant).</li>
      </ul>
      <p>Browse the full supplement for chants, seasonal meditations, and more: <Link href="/en/supplement/index?ref=landing">Supplement index</Link>.</p>
    </>
  );
};

const renderTrustSection = (lang: Locale) => {
  if (lang === "pl") {
    return (
      <>
        <p>
          Missale Meum to osobisty projekt Marcina Molendy — męża i ojca, który z pasją łączy liturgię i technologię. Serwis działa w sieci od 2018 roku, a przez lata rozwinął się dzięki
          wiernym korzystającym z tradycyjnej liturgii w Polsce i na świecie.
        </p>
        <p>
          Marcin współpracuje z kapłanami celebrującymi w nadzwyczajnej formie rytu rzymskiego oraz z redaktorami świeckimi. Każda aktualizacja jest publicznie dokumentowana, a
          zgłoszenia użytkowników trafiają do repozytorium GitHub, gdzie przechodzą weryfikację przed publikacją.
        </p>
        <p>
          Teksty zachowują ortografię kościelną, a przypisy wyjaśniają różnice wobec starszych wydań mszału i zwyczajów lokalnych. Dzięki przejrzystości źródeł i korekt Missale Meum
          pozostaje wiarygodnym narzędziem do modlitwy i studium.
        </p>
      </>
    );
  }

  return (
    <>
      <p>
        Missale Meum is the personal project of Marcin Molenda—a husband, father, and developer who loves bringing liturgy and technology together. Online since 2018, it has grown
        alongside the faithful who rely on the Traditional Latin Mass across the world.
      </p>
      <p>
        Marcin collaborates with clergy experienced in the Extraordinary Form and with lay editors. Updates are logged publicly and community suggestions flow through the GitHub
        repository, where they are reviewed before publication.
      </p>
      <p>
        Sources, translations, and editorial choices are carefully documented. Rubrical notes highlight differences from earlier hand missals or local customs so Missale Meum remains
        a trustworthy companion for prayer, study, and parish life.
      </p>
    </>
  );
};

const renderClosing = (lang: Locale) => {
  if (lang === "pl") {
    return (
      <>
        <p>
          Zapraszamy do codziennego korzystania z Missale Meum, udostępniania go znajomym oraz zgłaszania uwag. Wspólna troska o dziedzictwo liturgiczne sprawia, że tradycyjna Msza
          święta pozostaje żywa w parafiach i wspólnotach na całym świecie.
        </p>
      </>
    );
  }

  return (
    <>
      <p>
        Explore Missale Meum, bookmark the sections you use most, and share it with others who cherish the Traditional Latin Mass. Preserving the liturgical heritage of the Church is
        a shared work; this digital missal is one small contribution placed at the service of that mission.
      </p>
    </>
  );
};

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const lang = (locale === "pl" ? "pl" : "en") as Locale;
  const copy = LANDING_COPY[lang];

  return generateLocalisedMetadata(locale, {
    titleFragment: copy.metaTitle,
    description: copy.metaDescription,
    pathSuffix: "",
  });
}

export default async function LandingPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const lang = (locale === "pl" ? "pl" : "en") as Locale;
  const copy = LANDING_COPY[lang];
  const photoCredit = PHOTO_CREDIT[lang];
  const authorAlt = lang === "pl" ? "Portret Marcina Molendy" : "Portrait of Marcin Molenda";

  const calendarUrl = `/${lang}/calendar`;
  const today = new Date();
  const isoToday = today.toISOString().slice(0, 10);
  const todayUrl = `${calendarUrl}/${isoToday}`;
  const websiteSchema = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: "Missale Meum",
    url: SITE_BASE_URL,
    inLanguage: lang === "pl" ? "pl-PL" : "en-US",
    description: copy.metaDescription,
    potentialAction: {
      "@type": "ViewAction",
      target: `${SITE_BASE_URL}${calendarUrl}`,
    },
  };

  const faqSchema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: copy.faq.reduce((entities, item) => {
      const schemaText = item.schemaAnswer ?? (typeof item.answer === "string" ? item.answer : undefined);

      if (!schemaText) {
        return entities;
      }

      entities.push({
        "@type": "Question",
        name: item.question,
        acceptedAnswer: {
          "@type": "Answer",
          text: schemaText,
        },
      });

      return entities;
    }, [] as Array<{ "@type": string; name: string; acceptedAnswer: { "@type": string; text: string } }>),
  };

  const structuredData = JSON.stringify([websiteSchema, faqSchema]);

  return (
    <>
      <Script strategy="afterInteractive" src="https://js.stripe.com/v3/buy-button.js" />
      <div className={roboto.variable}>
        <section className={styles.heroSection}>
          <div className={styles.heroMedia}>
            <picture>
              <source srcSet="/images/hero.webp" type="image/webp" />
              <img src="/images/hero.jpg" alt="Open Roman Missal on altar during Traditional Latin Mass (1962 Missal)" />
            </picture>
          </div>
          <div className={styles.heroContent}>
          <div className={styles.heroIdentity}>
            <Logo width={64} height={64} />
            <span className={styles.heroTag}>{copy.heroTag}</span>
          </div>
          <h1 className={styles.heroHeading}>{copy.heroHeading}</h1>
          {copy.heroSubheading ? <h2 className={styles.heroSubheading}>{copy.heroSubheading}</h2> : null}
          <p className={styles.heroIntro}>{copy.heroIntro}</p>
          <div className={styles.ctaGroup}>
            <Link href={todayUrl} className={`${styles.ctaButton} ${styles.secondaryCta}`}>
              {copy.todayCtaLabel}
            </Link>
            <Link href={calendarUrl} className={`${styles.ctaButton} ${styles.primaryCta}`}>
              {copy.secondaryCtaLabel}
            </Link>
            <Link href={`#${ABOUT_SECTION_ID}`} className={`${styles.ctaButton} ${styles.tertiaryCta}`}>
              {copy.primaryCtaLabel}
            </Link>
          </div>
        </div>
        </section>


        <main className={styles.page}>
        <nav className={styles.internalNav}>
          {copy.internalNav.map((item) => (
            <Link key={item.targetId} href={`#${item.targetId}`}>
              {item.label}
            </Link>
          ))}
        </nav>

        <section id={ABOUT_SECTION_ID} className={styles.section}>
          <h2 className={styles.sectionHeading}>{lang === "pl" ? "Mszalik online" : "Roman Missal Online"}</h2>
          <div className={styles.longForm}>{renderIntro(lang)}</div>
        </section>

        <section id={STRUCTURE_SECTION_ID} className={styles.section}>
          <h2 className={styles.sectionHeading}>{lang === "pl" ? "Pełna struktura klasycznego mszału" : "The full structure of the classical missal"}</h2>
          <div className={styles.longForm}>{renderStructureSection(lang)}</div>
        </section>

        <section id={FEATURES_SECTION_ID} className={styles.section}>
          <h2 className={styles.sectionHeading}>{copy.featuresHeading}</h2>
          <div className={styles.longForm}>
            <p>{copy.featuresIntro}</p>
            {renderFeaturesIntro(lang)}
          </div>
          <div className={styles.mockupGrid}>
            <figure className={styles.mockup}>
              <picture>
                <source srcSet="/images/mock-calendar.png" type="image/png" />
                <img src="/images/mock-calendar.png" alt="Liturgical calendar view in Missale Meum app" loading="lazy" />
              </picture>
              <figcaption className={styles.caption}>{copy.calendarCaption}</figcaption>
            </figure>
            <figure className={styles.mockup}>
              <picture>
                <source srcSet="/images/mock-proper.png" type="image/png" />
                <img src="/images/mock-proper.png" alt="Daily Mass proper text view in Missale Meum app" loading="lazy" />
              </picture>
              <figcaption className={styles.caption}>{copy.properCaption}</figcaption>
            </figure>
          </div>
          <div className={styles.featureGrid}>
            {copy.features.map((item) => (
              <article key={item.title} className={styles.card}>
                <h3 className={styles.cardTitle}>{item.title}</h3>
                <p className={styles.cardText}>{item.description}</p>
              </article>
            ))}
          </div>
        </section>

        <section id={USAGE_SECTION_ID} className={styles.section}>
          <h2 className={styles.sectionHeading}>{copy.usageHeading}</h2>
          <div className={styles.twoColumn}>
            <div className={styles.longForm}>{renderUsageSection(lang)}</div>
            <div className={styles.twoColumnMedia}>
              <picture>
                <source srcSet="/images/secondary.webp" type="image/webp" />
                <img
                  src="/images/secondary.jpg"
                  alt="Young Catholic holding hand missal during Mass"
                  loading="lazy"
                />
              </picture>
            </div>
          </div>
        </section>

        <section id={RESOURCES_SECTION_ID} className={styles.section}>
          <h2 className={styles.sectionHeading}>{copy.resourcesHeading}</h2>
          <div className={styles.longForm}>{renderResourcesSection(lang)}</div>
        </section>

        <section id={SUPPORT_SECTION_ID} className={styles.section}>
          <h2 className={styles.sectionHeading}>{copy.supportHeading}</h2>
          <div className={styles.longForm}>{renderSupportSection(lang)}</div>
        </section>

        <section id={TRUST_SECTION_ID} className={styles.section}>
          <h2 className={styles.sectionHeading}>{copy.trustHeading}</h2>
          <div className={styles.trustCard}>
            <div className={styles.trustBody}>
              <Image
                src="/images/author.webp"
                alt={authorAlt}
                width={112}
                height={112}
                className={styles.trustAvatar}
                sizes="112px"
              />
              <div className={styles.longForm}>{renderTrustSection(lang)}</div>
            </div>
            <p className={styles.trustSignature}>{copy.trustSignature}</p>
          </div>
        </section>

        <section id={FAQ_SECTION_ID} className={styles.section}>
          <h2 className={styles.sectionHeading}>{copy.faqHeading}</h2>
          <div className={styles.faqList}>
            {copy.faq.map((item) => {
              const answerContent = item.renderAnswer
                ? <div className={styles.longForm}>{item.renderAnswer(lang)}</div>
                : <p className={styles.cardText}>{item.answer}</p>;

              return (
                <details key={item.question}>
                  <summary>
                    <span>{item.question}</span>
                  </summary>
                  {answerContent}
                </details>
              );
            })}
          </div>
        </section>

        <section className={styles.section}>
          <div className={styles.longForm}>{renderClosing(lang)}</div>
          <p className={styles.meta}>{copy.metaNote}</p>
        </section>
        </main>

        <footer className={styles.footer}>
          <p className={styles.photoCredit}>{photoCredit}</p>
        </footer>
      </div>

      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: structuredData }} />
    </>
  );
}
