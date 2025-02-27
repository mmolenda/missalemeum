import React from "react";
import WidgetPropers from "@/components/WidgetPropers";
import moment from "moment";

export default async function Page({params}) {
  const locale = (await params).locale
  const idCatchAll = (await params).id
  const id = idCatchAll ? idCatchAll[0] : moment().format("YYYY-MM-DD")
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/${locale}/api/v5/proper/${id}`, {mode: "cors"});
  return (<WidgetPropers lang={locale} id={id} content={await response.json()} version={process.env.NEXT_PUBLIC_BUILD_VERSION} />)
}