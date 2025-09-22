import React from "react";
import ListProper from "@/components/ListProper";
import moment from "moment";
import { notFound } from "next/navigation";
import { callApi, generateLocalisedMetadata } from "@/components/utils";
import { CALENDAR_PAGE_DESCRIPTION, CALENDAR_PAGE_TITLE, Locale } from "@/components/intl";

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  const lang = (locale === "pl" ? "pl" : "en") as Locale;
  return generateLocalisedMetadata(locale, {
    titleFragment: CALENDAR_PAGE_TITLE[lang],
    description: CALENDAR_PAGE_DESCRIPTION[lang],
    pathSuffix: "/calendar",
  });
}

export default async function Page({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  const response = await callApi(locale, "calendar");
  if (response.status !== 200) {
    notFound();
  }
  const items = await response.json();
  return (
    <ListProper
      lang={locale}
      year={parseInt(moment().format("YYYY"))}
      items={items}
    />
  );
}
