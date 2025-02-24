import React from "react";
import ListProper from "@/components/ListProper";
import moment from "moment";

export default async function Page({params}) {
  const lang = (await params).lang
  const response = await fetch(`${process.env.MISSALEMEUM_API_URL}/${lang}/api/v5/calendar`, {mode: "cors"});
  const items = await response.json();
  return <ListProper lang={lang} year={moment().format("YYYY")} items={items}/>

}
