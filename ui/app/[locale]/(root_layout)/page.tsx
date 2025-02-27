import React from "react";
import ListProper from "@/components/ListProper";
import moment from "moment";

export default async function Page({params}) {
  const locale = (await params).locale
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/${locale}/api/v5/calendar`, {mode: "cors"});
  const items = await response.json();
  return <ListProper lang={locale} year={moment().format("YYYY")} items={items}/>

}
