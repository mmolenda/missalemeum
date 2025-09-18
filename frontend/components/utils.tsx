import {Locale, META_DESCRIPTION} from "@/components/intl";

export async function callApi(locale: string, endpoint: string, id?: string) {
  let url = `${process.env.API_URL}/${locale}/api/v5/${endpoint}`
  if (id) {
    url += `/${id}`
  }
  return await fetch(url, {
    mode: "cors",
    cache: "force-cache",
    headers: {
      "User-Agent": `MissaleMeumUI/${process.env.NEXT_PUBLIC_BUILD_VERSION}`
    }
  });
}

export type MetadataOptions = {
  titleFragment?: string;
  description?: string;
  pathSuffix?: string;
  openGraphType?: "website" | "article";
  publishedTime?: string;
  modifiedTime?: string;
  noIndex?: boolean;
};

const SITE_BASE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? "https://www.missalemeum.com";
const FALLBACK_LOCALE: Locale = "en";
const SUPPORTED_LOCALES: Locale[] = ["pl", "en"];

const toSupportedLocale = (input: string): Locale => {
  return (SUPPORTED_LOCALES as readonly string[]).includes(input) ? (input as Locale) : FALLBACK_LOCALE;
};

const normalisePath = (pathSuffix?: string) => {
  if (!pathSuffix) {
    return "";
  }
  return pathSuffix.startsWith('/') ? pathSuffix : `/${pathSuffix}`;
};

export function generateLocalisedMetadata(
  locale: string,
  titleOrOptions?: string | MetadataOptions
) {
  const options: MetadataOptions = typeof titleOrOptions === "string"
    ? { titleFragment: titleOrOptions }
    : (titleOrOptions ?? {});

  const resolvedLocale = toSupportedLocale(locale);
  const pathSuffix = normalisePath(options.pathSuffix);
  const canonicalPath = `/${resolvedLocale}${pathSuffix}`;
  const canonicalUrl = new URL(canonicalPath || '/', SITE_BASE_URL).toString();
  const alternateEn = new URL(`/en${pathSuffix}`, SITE_BASE_URL).toString();
  const alternatePl = new URL(`/pl${pathSuffix}`, SITE_BASE_URL).toString();

  const title = options.titleFragment
    ? `${options.titleFragment} | Missale Meum`
    : resolvedLocale === 'pl'
      ? 'Missale Meum – Mszał Rzymski online'
      : 'Missale Meum – 1962 Roman Missal online';

  const description = options.description ?? META_DESCRIPTION[resolvedLocale];
  const openGraphBase: Record<string, unknown> = {
    type: options.openGraphType ?? 'website',
    locale: resolvedLocale === 'pl' ? 'pl_PL' : 'en_US',
    url: canonicalUrl,
    siteName: 'Missale Meum',
    title,
    description,
  };

  if (options.openGraphType === 'article') {
    if (options.publishedTime) {
      openGraphBase['publishedTime'] = options.publishedTime;
    }
    if (options.modifiedTime) {
      openGraphBase['modifiedTime'] = options.modifiedTime;
    }
  }

  const metadata: Record<string, unknown> = {
    title,
    description,
    alternates: {
      canonical: canonicalUrl,
      languages: {
        en: alternateEn,
        pl: alternatePl,
      },
    },
    openGraph: openGraphBase,
    twitter: {
      card: 'summary_large_image',
      title,
      description,
    },
  };

  if (options.noIndex) {
    metadata['robots'] = { index: false, follow: false };
  }

  return metadata;
}
