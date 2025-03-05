import {Locale, META_DESCRIPTION} from "@/components/intl";

export const userAgentString = `MissaleMeumUI ${process.env.NEXT_PUBLIC_BUILD_VERSION}`

export async function callApi(locale: string, endpoint: string, id?: string) {
  let url = `${process.env.NEXT_PUBLIC_API_URL}/${locale}/api/v5/${endpoint}`
  if (id) {
    url += `/${id}`
  }
  return await fetch(url, {
    mode: "cors",
    cache: "force-cache",
    headers: {
      "User-Agent": userAgentString
    }
  });
}

export function generateLocalisedMetadata(
  locale: string,
  titleFragment?: string
) {
  return {
    title: titleFragment ? `${titleFragment} | Missale Meum` : "Missale Meum",
    description: META_DESCRIPTION[locale as Locale],
  };
}
