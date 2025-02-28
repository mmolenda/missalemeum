import React from "react";
import WidgetPropers from "@/components/WidgetPropers";
import moment from "moment";

export default async function Page({params}: { params: Promise<{locale: string, id: string}> }) {
  const { id, locale } = await params
  const idOrToday = id ? id[0] : moment().format("YYYY-MM-DD")
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/${locale}/api/v5/proper/${idOrToday}`, {mode: "cors"});
  return (<WidgetPropers lang={locale} id={idOrToday} content={await response.json()} version={process.env.NEXT_PUBLIC_BUILD_VERSION} />)
}