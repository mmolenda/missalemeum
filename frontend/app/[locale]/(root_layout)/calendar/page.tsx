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


export default async function Page({
  params,
  searchParams,
}: {
  params: Promise<{ locale: string }>;
  searchParams?: Promise<{ fromDate?: string }>;
}) {
  const RANGE_RADIUS_DAYS = 10;
  const { locale } = await params;
  const { fromDate } = (await searchParams) ?? {};
  const anchorDate = moment(fromDate, "YYYY-MM-DD", true).isValid()
    ? fromDate!
    : moment().format("YYYY-MM-DD");
  const anchorMoment = moment(anchorDate, "YYYY-MM-DD");
  const rangeStart = anchorMoment.clone().subtract(RANGE_RADIUS_DAYS, "days").format("YYYY-MM-DD");
  const rangeEnd = anchorMoment.clone().add(RANGE_RADIUS_DAYS, "days").format("YYYY-MM-DD");
  const query = new URLSearchParams({ from: rangeStart, until: rangeEnd }).toString();
  const response = await callApi(locale, `calendar/range?${query}`);
  if (response.status !== 200) {
    notFound();
  }
  const items = await response.json();
  return (
    <ListProper
      lang={locale}
      year={parseInt(anchorDate.slice(0, 4))}
      items={items}
    />
  );
}
