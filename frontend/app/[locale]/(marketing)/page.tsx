import type { ReactNode } from "react";
import Image from "next/image";
import Link from "next/link";
import Script from "next/script";
import { Icon } from "@iconify/react";
import { Roboto } from "next/font/google";
import BackToTopButton from "@/components/BackToTopButton";
import { DonationWidget } from "@/components/donations";
import {
  Locale,
  MENUITEM_PROPER,
  MENUITEM_ORDO,
  MENUITEM_VOTIVE,
  MENUITEM_ORATIO,
  MENUITEM_CANTICUM,
  MENUITEM_INFO,
  MENUITEM_SUPPLEMENT,
} from "@/components/intl";
import { generateLocalisedMetadata } from "@/components/utils";
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
const PDF_SECTION_ID = "pdfs";
const USAGE_SECTION_ID = "usage";
const RESOURCES_SECTION_ID = "resources";
const SUPPORT_SECTION_ID = "support";
const TRUST_SECTION_ID = "credibility";
const FAQ_SECTION_ID = "faq";

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
  pdfHeading: string;
  calendarCaption: string;
  properCaption: string;
  usageHeading: string;
  resourcesHeading: string;
  supportHeading: string;
  trustHeading: string;

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
    heroSubheading: "Complete resources for the Latin Mass",
    heroIntro:
      "A bilingual edition of the 1962 Roman Missal. Follow the liturgical year, study the daily propers, and keep trusted devotions close—wherever you pray.",
    primaryCtaLabel: "Learn more about Missale Meum",
    secondaryCtaLabel: "Browse the calendar",
    todayCtaLabel: "Open today's proper",
    internalNav: [
      { label: "Overview", targetId: ABOUT_SECTION_ID },
      { label: "Missal structure", targetId: STRUCTURE_SECTION_ID },
      { label: "Digital features", targetId: FEATURES_SECTION_ID },
      { label: "Printable PDFs", targetId: PDF_SECTION_ID },
      { label: "How the faithful use it", targetId: USAGE_SECTION_ID },
      { label: "Tools & resources", targetId: RESOURCES_SECTION_ID },
      { label: "How you can help", targetId: SUPPORT_SECTION_ID },
      { label: "About the author", targetId: TRUST_SECTION_ID },
      { label: "FAQ", targetId: FAQ_SECTION_ID },
    ],
    featuresHeading: "Everything you need for the Extraordinary Form",
    featuresIntro:
      "Missale Meum is more than a calendar — it is a tool for prayer, study, and preparation for the liturgy in the classical Roman Rite.",
    features: [
      {
        title: "Full propers in context",
        description:
          "Complete Mass propers with Latin and English side by side. Prayers, readings, antiphons, and rubrical notes are always in one place.",
      },
      {
        title: "Intelligent traditional calendar",
        description:
          "See the feast rank, vestment colour, and commemorations at a glance. Easily move between years and follow the structure of the temporale and sanctorale.",
      },
      {
        title: "Reference library",
        description:
          "Votives and Commons, seasonal chants, daily prayers — Missale Meum gathers the texts most often needed by families, choirs, and altar servers.",
      },
    ],
    pdfHeading: "Printable PDFs",
    calendarCaption: "Traditional liturgical calendar with feasts and commemorations.",
    properCaption: "Full daily propers in Latin and vernacular.",
    usageHeading: "How the faithful live with the missal",
    resourcesHeading: "Tools, feeds, and embeds",
    supportHeading: "How you can help",
    trustHeading: "About the author",
    faqHeading: "Frequently asked questions",
    faq: [
      {
        question: "Is Missale Meum free to use?",
        answer:
          "Yes. Missale Meum is a volunteer-maintained project and will always remain free for personal use, with no fees or ads. You can install it as a web app or use it from any modern browser without payment or registration. If you wish, optional donations help cover hosting and support Catholic education in Poland.",
      },
      {
        question: "Which edition of the Missal does it follow?",
        answer:
          "The texts follow the 1962 editio typica of the Roman Missal (Extraordinary Form).",
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
      { label: "Funkcje mszalika", targetId: FEATURES_SECTION_ID },
      { label: "Pliki PDF do druku", targetId: PDF_SECTION_ID },
      { label: "Jak korzystają wierni", targetId: USAGE_SECTION_ID },
      { label: "Suplement", targetId: RESOURCES_SECTION_ID },
      { label: "Wsparcie projektu", targetId: SUPPORT_SECTION_ID },
      { label: "O autorze", targetId: TRUST_SECTION_ID },
      { label: "FAQ", targetId: FAQ_SECTION_ID },
    ],
    featuresHeading: "Funkcje mszalika",
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
    pdfHeading: "Pliki PDF do druku",
    calendarCaption: "Tradycyjny kalendarz liturgiczny z obchodami i wspomnieniami.",
    properCaption: "Pełne proprium dnia w łacinie i przekładzie.",
    usageHeading: "Jak wierni korzystają z mszalika",
    resourcesHeading: "Narzędzia i materiały dodatkowe",
    supportHeading: "Wsparcie projektu",
    trustHeading: "O autorze",
    faqHeading: "Najczęstsze pytania",
    faq: [
      {
        question: "Czy Missale Meum jest płatne?",
        answer:
          "Nie. Missale Meum to projekt społeczny, bezpłatny do prywatnego użytku. Nie pobieramy opłat ani nie wyświetlamy reklam. Można z niego korzystać w przeglądarce lub dodać jako aplikację webową na telefonie. Dobrowolne darowizny pomagają pokryć koszty utrzymania i wspierają edukację katolicką w Polsce.",
      },
      {
        question: "Na jakim wydaniu mszału bazuje serwis?",
        answer:
          "Teksty pochodzą z wydania typicznego z 1962 r. (forma nadzwyczajna). Wielki Tydzień jest również dostępny w wersji pre-55.",
      },
      {
        question: "Skąd pochodzą teksty Missale Meum?",
        renderAnswer: renderProjectInfoSection,
        answer:
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
        <p>
          Nowością są <strong>starannie opracowane pliki PDF</strong> — solidnie złożone, czytelnie wystylizowane i dostępne w wielu formatach, w tym <strong>składanych zeszytowo (broszura)</strong>. To praktyczne uzupełnienie serwisu: można je wydrukować i <strong>korzystać podczas Mszy</strong> albo w domowej modlitwie.
        </p>
      </>
    );
  }

  return (
    <>
      <p>
        Missale Meum was created to give the faithful attached to the classical liturgy convenient access to the 1962 Roman Missal. Each proper has been faithfully transcribed,
        with the Latin texts set alongside their English translation so both versions can always be used in parallel.
      </p>
      <p>
        The site covers the entire liturgical year: from Advent through the last Sunday after Pentecost, including Ember Days, octaves, and vigils. Additional notes help 
        explain rubrics and liturgical seasons. The search function leads directly to specific feasts, while the <Link href="/en/calendar">calendar</Link> makes it easy to move between cycles without losing context.
      </p>
      <p>
        Missale Meum supports daily prayer. In one place you can open <Link href="/en/votive">votive Masses</Link>, <Link href="/en/oratio">daily prayers</Link>, <Link href="/en/canticum">seasonal chants</Link>, and a detailed <Link href="/en/supplement/index">supplement</Link> of rubrics and commentary.
        The faithful turn to Missale Meum as a simple and clear online missal, helpful for preparing for Mass, for personal prayer, and always at hand when a printed copy is out of reach.
      </p>
      <p>
        A recent addition is our <strong>well-crafted PDF collection</strong> — robustly typeset, cleanly styled, and available in multiple formats, including <strong>foldable booklet</strong> layouts. They are a practical complement to the site: print them and <strong>use them at Mass</strong> or for prayer at home.
      </p>
    </>
  );
};

const renderStructureSection = (lang: Locale) => {
  const tiles = [
    { href: `/${lang}/calendar`, label: MENUITEM_PROPER[lang], icon: "mdi:calendar-month" },
    { href: `/${lang}/ordo`, label: MENUITEM_ORDO[lang], icon: "mdi:text-box-outline" },
    { href: `/${lang}/votive`, label: MENUITEM_VOTIVE[lang], icon: "mdi:alpha-v-box-outline" },
    { href: `/${lang}/canticum`, label: MENUITEM_CANTICUM[lang], icon: "mdi:music-note-sixteenth" },
    { href: `/${lang}/oratio`, label: MENUITEM_ORATIO[lang], icon: "mdi:hands-pray" },
    { href: `/${lang}/supplement/info`, label: MENUITEM_INFO[lang], icon: "mdi:information-slab-box-outline" },
    { href: `/${lang}/supplement/index`, label: MENUITEM_SUPPLEMENT[lang], icon: "mdi:book-plus" },
  ];

  const tileGrid = (
    <div className={styles.structureTiles}>
      {tiles.map(({ href, label, icon }) => (
        <Link key={href} href={href} className={styles.structureTile}>
          <span className={styles.structureTileIcon}>
            <Icon icon={icon} width={22} height={22} />
          </span>
          <span className={styles.structureTileLabel}>{label}</span>
        </Link>
      ))}
    </div>
  );

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
        {tileGrid}
      </>
    );
  }

  return (
    <>
      <p>
        Missale Meum faithfully reflects the layout of the 1962 printed missal. The site includes both the fixed parts (Ordo Missae) and the proper of each day of the liturgical year—readings, prayers, and antiphons.
      </p>
      <p>
        The Latin text is presented alongside the English translation, which makes it easier to follow the liturgy, learn Latin, and prepare for catechesis or homilies. Additional information—such as feast rank, vestment colour, and saints’ commemorations—creates a coherent guide to the propers and the entire church year.
      </p>
      {tileGrid}
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

const renderPdfSection = (lang: Locale) => {
  if (lang === "pl") {
    return (
      <div className={styles.twoColumn}>
        <div className={styles.longForm}>
          <p>
            Oprócz widoków online udostępniamy <strong>wysokiej jakości pliki PDF</strong>, zaprojektowane do druku. Są <strong>solidnie złożone</strong>, <strong>estetycznie wystylizowane</strong> i łatwe w czytaniu.
          </p>
          <ul className={styles.articleList}>
            <li><strong>Wiele formatów:</strong> A4, A5 i inne.</li>
            <li><strong>Wersja składana (broszura):</strong> do druku dwustronnego i złożenia w zeszyt.</li>
            <li><strong>Spójna typografia:</strong> klasyczne kroje, wyraźna hierarchia nagłówków, właściwe łamanie łaciny i polskiego.</li>
            <li><strong>Praktyczne zastosowanie:</strong> idealne do <strong>użytku podczas Mszy</strong>, prób scholi lub modlitwy w domu.</li>
          </ul>
          <p>
            Te materiały są <strong>świetnym uzupełnieniem</strong> mszalika online — możesz je zabrać do kościoła, rozdać rodzinie lub wydrukować dla wspólnoty.
          </p>
          <p>
            Poniżej zobaczysz <strong>fotografię gotowego wydruku</strong> w formie broszury — to dokładnie ten efekt, który można osiągnąć dzięki naszym wariantom PDF.
          </p>
        </div>
        <div className={styles.twoColumnMedia}>
          <picture>
            <source srcSet="/images/printed-booklet.webp" type="image/jpeg" />
            <img
              src="/images/printed-booklet.webp"
              alt="Wydrukowana broszura Missale Meum przygotowana z wariantu PDF booklet"
              loading="lazy"
            />
          </picture>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.twoColumn}>
      <div className={styles.longForm}>
        <p>
          Beyond the online views, we provide <strong>high-quality printable PDFs</strong>. They are <strong>well crafted</strong>, <strong>nicely styled</strong>, and easy to read.
        </p>
        <ul className={styles.articleList}>
          <li><strong>Multiple formats:</strong> A4, Letter, and more.</li>
          <li><strong>Foldable booklet:</strong> designed for two-sided printing and simple saddle folding.</li>
          <li><strong>Consistent typography:</strong> classic faces, clear heading hierarchy, proper Latin/English line breaking.</li>
          <li><strong>Real-world use:</strong> perfect to <strong>use at Mass</strong>, choir practice, or family prayer at home.</li>
        </ul>
        <p>
          These PDFs are a <strong>great addition</strong> to the digital missal — print them for church, share with family, or prepare sets for your community.
        </p>
        <p>
          Below you can see a <strong>photo of a finished printed booklet</strong> — the result you can achieve with the booklet variant of our PDFs.
        </p>
      </div>
      <div className={styles.twoColumnMedia}>
        <picture>
          <source srcSet="/images/printed-booklet.webp" type="image/jpeg" />
          <img
            src="/images/printed-booklet.webp"
            alt="Printed Missale Meum booklet produced from the PDF download"
            loading="lazy"
          />
        </picture>
      </div>
    </div>
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
          Dla jednych staje się częścią <em>lectio divina</em> i modlitwy osobistej, dla innych najwygodniejszym sposobem, by sprawdzić jaki formularz 
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
        For some it becomes part of <em>lectio divina</em> and private prayer, for others the most convenient 
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
      </>
    );
  }

  return (
    <>
      <p>
        Latin texts largely come from the venerable <a href="https://www.divinumofficium.com/" target="_blank" rel="noopener noreferrer">Divinum Officium</a>, while parallel English passages draw on carefully reviewed translations of the same sources. Elements of the Ordo borrow from <a href="https://www.fisheaters.com/" target="_blank" rel="noopener noreferrer">Fish Eaters</a>.
      </p>
    </>
  );
}

const renderSupportSection = (lang: Locale) => {
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
            dobrowolna darowizna — Missale Meum jest i pozostanie bezpłatne. Nie pobieramy opłat ani nie wyświelamy reklam.
            Twoja darowizna w pierwszej kolejności pokrywa podstawowe koszty działania serwisu – domenę, serwer i usługi pomocnicze.
            Pozostałe środki kierujemy na wsparcie edukacji katolickiej w Polsce.
          </li>
        </ul>
        <DonationWidget lang={lang} className={styles.donateCta} />
      </>
    );
  }

  return (
    <>
      <p>
        Missale Meum will always remain free to use. We do not charge fees or display ads. If you would like to help sustain the project, you can:
      </p>
      <ul className={styles.articleList}>
        <li>remember Missale Meum in your prayers;</li>
        <li>send feedback and corrections—it helps us improve;</li>
        <li>share the project with friends, families, and parish groups;</li>
        <li>contribute missing texts or trusted commentaries;</li>
        <li>
          make a donation — Missale Meum remains free to use. Your donation is used first to cover the essential costs of running Missale Meum – the domain, server, and auxiliary services.
          Any remainder is directed to supporting Catholic education in Poland.
        </li>
      </ul>
      <DonationWidget lang={lang} className={styles.donateCta} />
    </>
  );
};

const renderResourcesSection = (lang: Locale) => {
  if (lang === "pl") {
    return (
      <>
        <p>
          <Link href="/pl/supplement/index?ref=/">Suplement</Link> Missale Meum zawiera rozbudowane opracowania okresów liturgicznych, sakramentów oraz materiały pomocnicze dla wiernych.
        </p>
        <ul className={styles.articleList}>
          <li><strong>Okresy liturgiczne</strong> – komentarze i przepisy: <Link href="/pl/supplement/1-wprowadzenie?ref=/">Wprowadzenie</Link>, <Link href="/pl/supplement/2-adwent?ref=/">Adwent</Link>, <Link href="/pl/supplement/3-boze-narodzenie?ref=/">Boże Narodzenie</Link>, <Link href="/pl/supplement/6-wielki-post?ref=/">Wielki Post</Link> i kolejne aż po okres po Zesłaniu Ducha Świętego.</li>
          <li><strong>Sakramenty</strong> – praktyczne przewodniki: <Link href="/pl/supplement/20-chrzest?ref=/">Chrzest</Link>, <Link href="/pl/supplement/21-pokuta?ref=/">Pokuta</Link>, <Link href="/pl/supplement/22-malzenstwo?ref=/">Małżeństwo</Link>.</li>
          <li><strong>Ebook</strong> – mszalik na czytniki: <a href="https://www.dropbox.com/s/88z242hgr0q6e2e/mszalik.epub?dl=0" target="_blank" rel="noopener noreferrer">pobierz epuba</a>.</li>
          <li><strong>Msza dla początkujących</strong> – przewodnik PDF: <a href="https://www.dropbox.com/s/a94bingl33xlirx/msza-dla-pocz%C4%85tkuj%C4%85cych.pdf?dl=0" target="_blank" rel="noopener noreferrer">msza-dla-początkujących.pdf</a>.</li>
        </ul>
        <p>Missale Meum oferuje praktyczne narzędzia, które wykraczają poza samą stronę internetową.</p>
        <ul className={styles.articleList}>
          <li><strong>Instalacja jako aplikacja <abbr title="Progressive Web App">PWA</abbr>:</strong> dodaj do ekranu głównego na Androidzie lub iPhonie, aby uzyskać wrażenie korzystania z prawdziwej aplikacji.</li>
          <li><strong>Kalendarz liturgiczny:</strong> zasubskrybuj przez iCalendar i używaj w Google Calendar, Outlooku itp.</li>
          <li><strong>Osadzany widget:</strong> umieść proprium Missale Meum na swojej stronie internetowej.</li>
        </ul>
      </>
    );
  }

  return (
    <>
      <p>Missale Meum provides practical tools that extend beyond the website itself.</p>
      <ul className={styles.articleList}>
        <li><strong>Install as a PWA:</strong> add to your Home Screen on Android or iPhone for a real app-like experience.</li>
        <li><strong>Liturgical calendar feeds:</strong> subscribe via iCalendar and use in Google Calendar, Outlook, etc.</li>
        <li><strong>Embeddable widget:</strong> place Missale Meum propers on your website.</li>
      </ul>
      <p>Browse the full supplement for chants, seasonal meditations, and more: <Link href="/en/supplement/index?ref=/">Supplement index</Link>.</p>
    </>
  );
};

const renderTrustSection = (lang: Locale) => {
  if (lang === "pl") {
    return (
      <>
        <p>
          Missale Meum zbudował i utrzymuje Marcin Molenda — mąż i ojciec, który z pasją łączy liturgię i technologię. Serwis działa w sieci od 2018 roku, a przez lata rozwinął się dzięki
          wiernym korzystającym z tradycyjnej liturgii w Polsce i na świecie.
        </p>
        <p>
          Marcin współpracuje z kapłanami celebrującymi Mszę trydencką i z redaktorami świeckimi. Każda aktualizacja jest publicznie dokumentowana, a
          zgłoszenia użytkowników trafiają do repozytorium <Link href="https://github.com/mmolenda/missalemeum">GitHub</Link>, gdzie przechodzą weryfikację przed publikacją.
          Dzięki przejrzystości źródeł i korekt Missale Meum pozostaje wiarygodnym narzędziem do modlitwy i studium.
        </p>
        <p>
          Zapraszam do kontaktu pod adresem <a href="mailto:marcin@missalemeum.com">marcin@missalemeum.com</a> lub do śledzenia aktualności na <a href="https://www.facebook.com/missalemeum" target="_blank" rel="noopener noreferrer">facebook.com/missalemeum</a>.
        </p>
      </>
    );
  }

  return (
      <>
        <p>
          Missale Meum was built and is maintained by Marcin Molenda — a husband and father who combines a passion for liturgy with technology. Online since 2018, the project has grown
          thanks to the faithful who use the traditional liturgy in Poland and around the world.
        </p>
        <p>
          Marcin collaborates with priests who celebrate the Traditional Latin Mass and with lay editors. Every update is documented publicly, and user contributions are submitted to the <Link href="https://github.com/mmolenda/missalemeum">GitHub</Link> repository,
          where they are reviewed before publication. Thanks to the transparency of its sources and corrections,
          Missale Meum remains a reliable tool for prayer and study.
        </p>
        <p>
          Feel free to reach out at <a href="mailto:marcin@missalemeum.com">marcin@missalemeum.com</a> or follow updates at <a href="https://www.facebook.com/missalemeum" target="_blank" rel="noopener noreferrer">facebook.com/missalemeum</a>.
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

        <section id={PDF_SECTION_ID} className={styles.section}>
          <h2 className={styles.sectionHeading}>{copy.pdfHeading}</h2>
          {renderPdfSection(lang)}
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
        <BackToTopButton />
      </div>

      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: structuredData }} />
    </>
  );
}
