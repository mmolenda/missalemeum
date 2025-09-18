import Link from "next/link";
import { callApi, generateLocalisedMetadata } from "@/components/utils";
import { Locale, MENUITEM_ORATIO, MENUITEM_VOTIVE, RANK_NAMES } from "@/components/intl";
import styles from "@/app/landing.module.css";
import type { Content } from "@/components/types";

const SITE_BASE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? "https://www.missalemeum.com";

const formatDisplayDate = (isoDate: string, lang: Locale) => {
  const date = new Date(`${isoDate}T00:00:00Z`);
  const formatted = new Intl.DateTimeFormat(lang === "pl" ? "pl-PL" : "en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
  }).format(date);

  if (lang === "pl" && formatted.length > 0) {
    return formatted[0].toUpperCase() + formatted.slice(1);
  }

  return formatted;
};

const toLocale = (value: string): Locale => (value === "pl" ? "pl" : "en");

type LandingCopy = {
  metaTitle: string;
  metaDescription: string;
  heroTag: string;
  heroHeading: string;
  heroIntro: string;
  todayIntro: (params: { date: string; title?: string; rank?: string }) => string;
  primaryCta: string;
  secondaryCta: string;
  featureHeading: string;
  features: Array<{ title: string; description: string }>;
  practicesHeading: string;
  practicesIntro: string;
  practices: string[];
  faqHeading: string;
  faq: Array<{ question: string; answer: string }>;
  metaNote: string;
};

const LANDING_COPY: Record<Locale, LandingCopy> = {
  en: {
    metaTitle: "Traditional Latin Mass Missal online",
    metaDescription:
      "Missale Meum brings together the complete 1962 Roman Missal: propers, readings, chants, prayers, and votive Masses for every day of the traditional liturgical year.",
    heroTag: "1962 Roman Missal",
    heroHeading: "Pray the Traditional Latin Mass with confidence",
    heroIntro:
      "Missale Meum is a carefully researched, bilingual edition of the 1962 Roman Missal. Explore the liturgical calendar, read the daily propers in Latin and vernacular, and discover votive Masses alongside a traditional prayer book in one place.",
    todayIntro: ({ date, title, rank }) =>
      title
        ? `Today is ${date}, ${title}${rank ? `, ${rank}` : ""}`
        : `Today is ${date}. Explore the day's propers below.`,
    primaryCta: "Read the full proper",
    secondaryCta: "Open the liturgical calendar",
    featureHeading: "Everything you need for the Extraordinary Form",
    features: [
      {
        title: "Daily propers in two languages",
        description:
          "View the full text of the Mass of the day in Latin with a parallel vernacular translation. Rubrics, commemorations, and notes follow the 1962 editio typica.",
      },
      {
        title: "Smart traditional calendar",
        description:
          "See rank, liturgical color, commemorations, and sanctoral or temporal cycles at a glance. Quickly jump to any date or liturgical year back to 1960.",
      },
      {
        title: "Installable and focused",
        description:
          "Use Missale Meum as a progressive web app on iOS, Android, or desktop. Add it to your home screen for quick access to the current day's Mass texts.",
      },
    ],
    practicesHeading: "Built for the way traditional Catholics pray",
    practicesIntro:
      "Missale Meum keeps frequently used devotions close at hand so you never have to juggle multiple books or PDFs.",
    practices: [
      "Seasonal chants and hymns from the proprium and supplement",
      `Common prayers and devotions in the ${MENUITEM_ORATIO.en.toLowerCase()} section`,
      `Votive Mass formularies for saints, mysteries, and needs (${MENUITEM_VOTIVE.en})`,
      "Rubrical announcements, surveys, and community updates",
    ],
    faqHeading: "Frequently asked questions",
    faq: [
      {
        question: "Is Missale Meum free to use?",
        answer:
          "Yes. Missale Meum is a volunteer-maintained project and is free for personal use. You can install it as an app or use it from any modern browser without payment or registration.",
      },
      {
        question: "Which edition of the Missal does it follow?",
        answer:
          "The texts follow the 1962 editio typica of the Roman Missal (Extraordinary Form). Propers, commemorations, and rubrics reflect the traditional calendar in force after the 1960 code of rubrics.",
      },
      {
        question: "Does it work on phones and tablets?",
        answer:
          "Yes. The interface is optimised for mobile use and supports installation as a progressive web app. Add it to your home screen for fast access to the current day's calendar entry.",
      },
    ],
    metaNote: "Content sourced from the 1962 Roman Missal and related traditional Catholic liturgical books.",
  },
  pl: {
    metaTitle: "Mszał Rzymski 1962 online",
    metaDescription:
      "Missale Meum udostępnia kompletny Mszał Rzymski z 1962 r.: proprium, czytania, pieśni, modlitwy oraz msze wotywne na każdy dzień tradycyjnego kalendarza.",
    heroTag: "Msza Trydencka",
    heroHeading: "Z Missale Meum modlisz się według klasycznego Mszału",
    heroIntro:
      "Missale Meum to starannie opracowana, dwujęzyczna wersja Mszału Rzymskiego z 1962 r. Przeglądaj kalendarz liturgiczny, czytaj proprium dnia po łacinie i po polsku oraz sięgaj po msze wotywne i tradycyjne modlitwy w jednym miejscu.",
    todayIntro: ({ date, title, rank }) =>
      title
        ? `Dziś jest ${date}, ${title}${rank ? `, ${rank}` : ""}`
        : `Dziś jest ${date}. Zobacz formularz dnia poniżej.`,
    primaryCta: "Przeczytaj całe proprium",
    secondaryCta: "Otwórz kalendarz liturgiczny",
    featureHeading: "Wszystko dla Mszy w nadzwyczajnej formie",
    features: [
      {
        title: "Proprium dnia w dwóch językach",
        description:
          "Pełne teksty Mszy św. danego dnia w łacinie z równoległym tłumaczeniem. Rubryki, wspomnienia i komentarze zgodne z wydaniem z 1962 r.",
      },
      {
        title: "Tradycyjny kalendarz z rubrykami",
        description:
          "Na pierwszy rzut oka zobaczysz klasę obchodu, kolor szat, wspomnienia oraz cykle roku liturgicznego. Szybko przejdziesz do dowolnej daty lub roku.",
      },
      {
        title: "Aplikacja PWA – zawsze pod ręką",
        description:
          "Missale Meum możesz dodać do ekranu telefonu, tabletu lub komputera. Po uruchomieniu od razu otwiera kalendarz i dzisiejszy formularz.",
      },
    ],
    practicesHeading: "Dla tych, którzy żyją tradycją Kościoła",
    practicesIntro:
      "Najczęściej używane modlitwy i treści znajdziesz pod ręką – bez wertowania kilku książek i plików PDF.",
    practices: [
      "Pieśni i śpiewy okresowe oraz dodatki do proprium",
      `Modlitwy codzienne i nabożeństwa w sekcji ${MENUITEM_ORATIO.pl.toLowerCase()}`,
      `Formularze mszy wotywnych na różne intencje (${MENUITEM_VOTIVE.pl})`,
      "Ogłoszenia, ankiety i informacje o projekcie",
    ],
    faqHeading: "Najczęstsze pytania",
    faq: [
      {
        question: "Czy korzystanie z Missale Meum jest płatne?",
        answer:
          "Nie. Missale Meum to projekt tworzony społecznie i całkowicie darmowy do prywatnego użytku. Możesz dodać serwis do ekranu głównego lub korzystać z przeglądarki bez żadnej rejestracji.",
      },
      {
        question: "Na jakim wydaniu Mszału opiera się serwis?",
        answer:
          "Teksty pochodzą z typicznego wydania Mszału Rzymskiego z 1962 r. (forma nadzwyczajna). Proprium, wspomnienia i rubryki odpowiadają kalendarzowi wprowadzonemu reformą z 1960 r.",
      },
      {
        question: "Czy działa na telefonach i tabletach?",
        answer:
          "Tak. Interfejs jest zoptymalizowany pod urządzenia mobilne oraz instalację jako progresywna aplikacja webowa. Po dodaniu do ekranu głównego kalendarz otwiera się od razu na dzisiejszym formularzu.",
      },
    ],
    metaNote: "Treści zaczerpnięte z Mszału Rzymskiego z 1962 r. i tradycyjnych ksiąg liturgicznych.",
  },
};

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const lang = toLocale(locale);
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
  const lang = toLocale(locale);
  const copy = LANDING_COPY[lang];

  const today = new Date();
  const isoToday = today.toISOString().slice(0, 10);
  const currentYear = String(today.getFullYear());

  const calendarUrl = `/${lang}/calendar`;
  const todayUrl = `${calendarUrl}/${isoToday}`;
  const yearUrl = `${calendarUrl}/${currentYear}`;

  const formattedDate = formatDisplayDate(isoToday, lang);
  let todaySentence = copy.todayIntro({ date: formattedDate });

  try {
    const response = await callApi(locale, "proper", isoToday);
    if (response.ok) {
      const contents: Content[] = await response.json();
      const info = contents[0]?.info;

      if (info) {
        const rankValue = info.rank != null ? RANK_NAMES[lang][info.rank] : undefined;
        const rankLabel = typeof rankValue === 'string' && rankValue.length > 0 ? rankValue : undefined;

        todaySentence = copy.todayIntro({
          date: formattedDate,
          title: info.title,
          rank: rankLabel,
        });
      }
    }
  } catch {
    // Ignore errors and keep the fallback sentence.
  }

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
    mainEntity: copy.faq.map(({ question, answer }) => ({
      "@type": "Question",
      name: question,
      acceptedAnswer: {
        "@type": "Answer",
        text: answer,
      },
    })),
  };

  const structuredData = JSON.stringify([websiteSchema, faqSchema]);

  return (
    <main className={styles.page}>
      <section className={styles.hero}>
        <span className={styles.heroTag}>{copy.heroTag}</span>
        <h1 className={styles.heroHeading}>{copy.heroHeading}</h1>
        <p className={styles.heroIntro}>{copy.heroIntro}</p>
        <p className={styles.todayBlurb}>{todaySentence}</p>
        <div className={styles.ctaGroup}>
          <Link href={todayUrl} className={`${styles.ctaButton} ${styles.primaryCta}`}>
            {copy.primaryCta}
          </Link>
          <Link href={calendarUrl} className={`${styles.ctaButton} ${styles.secondaryCta}`}>
            {copy.secondaryCta}
          </Link>
        </div>
      </section>

      <section className={styles.section}>
        <h2 className={styles.sectionHeading}>{copy.featureHeading}</h2>
        <div className={styles.featureGrid}>
          {copy.features.map((item) => (
            <article key={item.title} className={styles.card}>
              <h3 className={styles.cardTitle}>{item.title}</h3>
              <p className={styles.cardText}>{item.description}</p>
            </article>
          ))}
        </div>
      </section>

      <section className={styles.section}>
        <h2 className={styles.sectionHeading}>{copy.practicesHeading}</h2>
        <p className={styles.textBlock}>{copy.practicesIntro}</p>
        <ul className={styles.articleList}>
          {copy.practices.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
        <p className={styles.textBlock}>
          <Link href={yearUrl} className={styles.inlineLink}>
            {lang === "pl" ? "Kalendarz na cały rok" : "Browse the full year"}
          </Link>{" "}
          ·
          {" "}
          <Link href={`/${lang}/votive`} className={styles.inlineLink}>
            {MENUITEM_VOTIVE[lang]}
          </Link>
          {" "}
          ·
          {" "}
          <Link href={`/${lang}/oratio`} className={styles.inlineLink}>
            {MENUITEM_ORATIO[lang]}
          </Link>
        </p>
      </section>

      <section className={styles.section}>
        <h2 className={styles.sectionHeading}>{copy.faqHeading}</h2>
        <div className={styles.faqList}>
          {copy.faq.map((item) => (
            <details key={item.question}>
              <summary>
                <span>{item.question}</span>
              </summary>
              <p className={styles.cardText}>{item.answer}</p>
            </details>
          ))}
        </div>
      </section>

      <p className={styles.meta}>{copy.metaNote}</p>

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: structuredData }}
      />
    </main>
  );
}
