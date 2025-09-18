import React from "react";
import ListProper from "@/components/ListProper";
import moment from "moment/moment";
import { notFound } from "next/navigation";
import BilingualContent from "@/components/BilingualContent";
import { callApi, generateLocalisedMetadata } from "@/components/utils";
import {
  CALENDAR_PAGE_DESCRIPTION,
  CALENDAR_PAGE_TITLE,
  Locale,
  RANK_NAMES,
  VESTMENTS_BLACK,
  VESTMENTS_GREEN,
  VESTMENTS_PINK,
  VESTMENTS_RED,
  VESTMENTS_VIOLET,
  VESTMENTS_WHITE,
} from "@/components/intl";
import { ColorCode, Content } from "@/components/types";

const COLOR_LABELS: Record<ColorCode, Record<Locale, string>> = {
  r: VESTMENTS_RED,
  g: VESTMENTS_GREEN,
  w: VESTMENTS_WHITE,
  v: VESTMENTS_VIOLET,
  b: VESTMENTS_BLACK,
  p: VESTMENTS_PINK,
};

const DAY_COPY: Record<Locale, {
  titleSuffix: (date: string) => string;
  lead: (title: string, date: string) => string;
  rankLabel: string;
  vestmentsLabel: string;
  commemorationsLabel: string;
}> = {
  en: {
    titleSuffix: (date) => `${date} Traditional Latin Mass propers`,
    lead: (title, date) => `Daily propers for ${title} (${date}) according to the 1962 Roman Missal.`,
    rankLabel: "Rank",
    vestmentsLabel: "Vestments",
    commemorationsLabel: "Commemorations",
  },
  pl: {
    titleSuffix: (date) => `${date} proprium Mszy trydenckiej`,
    lead: (title, date) => `Proprium Mszy świętej na ${title} (${date}) według Mszału Rzymskiego z 1962 r.`,
    rankLabel: "Klasa",
    vestmentsLabel: "Szaty",
    commemorationsLabel: "Wspomnienia",
  },
};

const toLocale = (value: string): Locale => (value === "pl" ? "pl" : "en");

const formatHumanDate = (isoDate: string, lang: Locale) => {
  const date = new Date(`${isoDate}T00:00:00Z`);
  return new Intl.DateTimeFormat(lang === "pl" ? "pl-PL" : "en-US", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
  }).format(date);
};

const cleanText = (value?: string) => value?.replace(/\s+/g, " ").trim() ?? "";

const buildDayDescription = (info: Content["info"], humanDate: string, lang: Locale) => {
  const copy = DAY_COPY[lang];
  const pieces: string[] = [copy.lead(info.title, humanDate)];

  const additional = cleanText(info.description);
  if (additional) {
    pieces.push(additional);
  }

  const rankName = RANK_NAMES[lang][info.rank] ?? "";
  if (rankName) {
    pieces.push(`${copy.rankLabel}: ${rankName}.`);
  }

  const colorLabels = (info.colors || [])
    .map((code) => COLOR_LABELS[code as ColorCode]?.[lang])
    .filter(Boolean);
  if (colorLabels.length) {
    pieces.push(`${copy.vestmentsLabel}: ${colorLabels.join(", ")}.`);
  }

  if (info.commemorations && info.commemorations.length > 0) {
    pieces.push(`${copy.commemorationsLabel}: ${info.commemorations.join(", ")}.`);
  }

  return pieces.join(" ");
};

const buildDayMetadata = (info: Content["info"], id: string, lang: Locale) => {
  const humanDate = formatHumanDate(id, lang);
  const suffix = DAY_COPY[lang].titleSuffix(humanDate);
  const titleFragment = `${info.title} - ${suffix}`;
  const description = buildDayDescription(info, humanDate, lang);
  const publishedIso = new Date(`${id}T00:00:00Z`).toISOString();

  return {
    titleFragment,
    description,
    pathSuffix: `/calendar/${id}`,
    openGraphType: "article" as const,
    publishedTime: publishedIso,
    modifiedTime: publishedIso,
  };
};

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string; id?: string }>;
}) {
  const { locale, id } = await params;
  const lang = toLocale(locale);

  if (id && /^\d{4}-\d{2}-\d{2}$/.test(id) && moment(id).isValid()) {
    try {
      const response = await callApi(locale, "proper", id);
      if (response.ok) {
        const contents: Content[] = await response.json();
        if (contents.length > 0) {
          return generateLocalisedMetadata(locale, buildDayMetadata(contents[0].info, id, lang));
        }
      }
    } catch {
      // Ignore metadata fetch errors and fall back to generic metadata.
    }

    return generateLocalisedMetadata(locale, {
      titleFragment: `${id} - ${DAY_COPY[lang].titleSuffix(formatHumanDate(id, lang))}`,
      description: CALENDAR_PAGE_DESCRIPTION[lang],
      pathSuffix: `/calendar/${id}`,
    });
  }

  if (id && /^\d{4}$/.test(id)) {
    const titleFragment = `${id} - ${CALENDAR_PAGE_TITLE[lang]}`;
    const description =
      lang === "pl"
        ? `${CALENDAR_PAGE_DESCRIPTION[lang]} Pełny kalendarz tradycyjny na ${id} r.`
        : `${CALENDAR_PAGE_DESCRIPTION[lang]} Explore the complete traditional calendar for ${id}.`;

    return generateLocalisedMetadata(locale, {
      titleFragment,
      description,
      pathSuffix: `/calendar/${id}`,
    });
  }

  return generateLocalisedMetadata(locale, {
    titleFragment: CALENDAR_PAGE_TITLE[lang],
    description: CALENDAR_PAGE_DESCRIPTION[lang],
    pathSuffix: "/calendar",
  });
}

export default async function Page({
  params,
}: {
  params: Promise<{ locale: string; id: string }>;
}) {
  const { id, locale } = await params;

  if (/^\d{4}$/.test(id)) {
    const response = await callApi(locale, "calendar", id);
    if (response.status !== 200) {
      notFound();
    }
    return (
      <ListProper
        lang={locale}
        year={parseInt(id, 10)}
        items={await response.json()}
        basePath={`/${locale}/calendar`}
      />
    );
  }

  const parsedDate = moment(id);
  if (!parsedDate.isValid()) {
    notFound();
  }
  const response = await callApi(locale, "proper", id);
  if (response.status !== 200) {
    notFound();
  }
  const providedYear = id.split("-")[0];
  const currentYear = moment().format("YYYY");
  const yearBit = providedYear !== currentYear ? `/${providedYear}` : "";
  return (
    <BilingualContent
      lang={locale}
      id={id}
      contents={await response.json()}
      backButtonRef={`/${locale}/calendar${yearBit}#${id}`}
    />
  );
}
