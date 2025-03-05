import React from "react";
import WidgetPropers from "@/components/WidgetPropers";
import moment from "moment";
import {callApi, generateLocalisedMetadata} from "@/components/utils";

export async function generateMetadata({ params }: { params: Promise<{ locale: string; id?: string }> }){
  const { locale, id } = await params
  return generateLocalisedMetadata(locale);
}

export default async function Page({params}: { params: Promise<{locale: string, id: string}> }) {
  const { id, locale } = await params
  const idOrToday = id ? id[0] : moment().format("YYYY-MM-DD")
  const response = await callApi(locale, "proper", idOrToday)
  return (<WidgetPropers lang={locale} id={idOrToday} contents={await response.json()} version={process.env.NEXT_PUBLIC_BUILD_VERSION} />)
}