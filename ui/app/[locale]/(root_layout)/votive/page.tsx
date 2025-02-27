import React from "react";
import ListCommon from "@/components/ListCommon";


export default async function Page({params}) {
  const locale = (await params).locale
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/${locale}/api/v5/votive`, {mode: "cors"});
  const items = await response.json();
  return <ListCommon lang={locale} sidenavPath="votive/" items={items}/>
}