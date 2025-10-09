import {Locale, META_DESCRIPTION} from "@/components/intl";

const trimTrailingSlash = (value: string) => value.endsWith("/") ? value.slice(0, -1) : value;

const resolveApiBase = (isServer: boolean) => {
  if (isServer) {
    return trimTrailingSlash(process.env.API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? "");
  }
  return trimTrailingSlash(process.env.NEXT_PUBLIC_API_URL ?? "");
};

const normaliseEndpoint = (endpoint: string) => endpoint.startsWith("/") ? endpoint.slice(1) : endpoint;

export const buildApiUrl = (locale: string, endpoint: string, id?: string) => {
  const isServer = typeof window === "undefined";
  const resolvedBase = resolveApiBase(isServer);
  const cleanEndpoint = normaliseEndpoint(endpoint);

  let url = resolvedBase
    ? `${resolvedBase}/${locale}/api/v5/${cleanEndpoint}`
    : `/${locale}/api/v5/${cleanEndpoint}`;

  if (id) {
    url += `/${id}`;
  }

  return url;
};

export async function callApi(locale: string, endpoint: string, id?: string) {
  const isServer = typeof window === "undefined";
  const url = buildApiUrl(locale, endpoint, id);

  const init: RequestInit = {
    mode: "cors",
    cache: isServer ? "force-cache" : "no-store",
  };

  if (isServer) {
    const headers: Record<string, string> = {};
    const buildVersion = process.env.NEXT_PUBLIC_BUILD_VERSION ?? "dev";
    headers["User-Agent"] = `MissaleMeumUI/${buildVersion}`;
    init.headers = headers;
  }

  return await fetch(url, init);
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

  const titleFragment = options.titleFragment;
  const title = titleFragment
    ? titleFragment.toLowerCase().includes("missale meum")
      ? titleFragment
      : `${titleFragment} | Missale Meum`
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
