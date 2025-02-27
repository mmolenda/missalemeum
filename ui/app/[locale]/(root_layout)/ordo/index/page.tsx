import React from "react";
import ListOrdo from "@/components/ListOrdo";


export default async function Page({params}) {
  const locale = (await params).locale
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/${locale}/api/v5/ordo`, {mode: "cors"});
  const items = await response.json();
  return <ListOrdo lang={locale} items={items[0]["sections"]}/>
}