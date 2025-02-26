import React from "react";
import ListCommon from "@/components/ListCommon";


export default async function Page({params}) {
  const locale = (await params).locale
    const response = await fetch(`${process.env.MISSALEMEUM_API_URL}/${locale}/api/v5/oratio`, {mode: "cors"});
    const items = await response.json();
    return <ListCommon lang={locale} sidenavPath="oratio/" items={items} />
}