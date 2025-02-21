import React from "react";
import ListOrdo from "@/components/ListOrdo";


export default async function Page({params}) {
  const lang = (await params).lang
  const response = await fetch(`${process.env.MISSALEMEUM_API_URL}/${lang}/api/v5/ordo`, {mode: "cors"});
  const items = await response.json();
  return <ListOrdo lang={lang} items={items[0]["sections"]}/>
}