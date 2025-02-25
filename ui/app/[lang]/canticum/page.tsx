import React from "react";
import ListCommon from "@/components/ListCommon";


export default async function Page({params}) {
  const lang = (await params).lang
    const response = await fetch(`${process.env.MISSALEMEUM_API_URL}/${lang}/api/v5/canticum`, {mode: "cors"});
    const items = await response.json();
    return <ListCommon lang={lang} sidenavPath="canticum/" items={items} />
}