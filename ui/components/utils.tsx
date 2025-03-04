import {Locale, META_DESCRIPTION} from "@/components/intl";

export function generateLocalisedMetadata(
  locale: string,
  titleFragment?: string
) {
  return {
    title: titleFragment ? `${titleFragment} | Missale Meum` : "Missale Meum",
    description: META_DESCRIPTION[locale as Locale],
  };
}
