import { headers, cookies } from "next/headers";
import { redirect } from "next/navigation";
import { resolveAcceptLanguage } from "resolve-accept-language";

const DEFAULT_LOCALE = "en-US";
const SUPPORTED = ["en-US", "pl-PL"] as const;
const FALLBACK = "en" as const;
const KNOWN_LOCALES = new Set(["en", "pl"]);

const toLocale = (value?: string): "en" | "pl" => {
  if (value && KNOWN_LOCALES.has(value)) {
    return value as "en" | "pl";
  }
  return FALLBACK;
};

const resolveLocale = async () => {
  const cookieStore = await cookies();
  const preferredFromCookie = cookieStore.get("mm-last-locale")?.value;
  if (preferredFromCookie) {
    return toLocale(preferredFromCookie);
  }

  const headerStore = await headers();
  const accept = headerStore.get("accept-language") ?? DEFAULT_LOCALE;
  const resolved = resolveAcceptLanguage(accept, SUPPORTED, DEFAULT_LOCALE);
  return toLocale(resolved.split("-")[0]);
};

export const dynamic = "force-dynamic";

export default async function CalendarLaunchPage() {
  const targetLocale = await resolveLocale();
  redirect(`/${targetLocale}/calendar`);
}
