import React from "react";
import ListCommon from "@/components/ListCommon";
import {notFound} from "next/navigation";
import {SEARCH_SUGGESTIONS_CANTICUM} from "@/components/intl";


export default async function Page({params}) {
  const locale = (await params).locale
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/${locale}/api/v5/canticum`, {mode: "cors"});
    response.status !== 200 && notFound()
    const items = await response.json();
    return <ListCommon lang={locale} sidenavPath="canticum/" items={items}
                       searchSuggestions={SEARCH_SUGGESTIONS_CANTICUM[locale]}/>
}