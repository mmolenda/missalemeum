import React from "react";
import ListCommon from "@/components/ListCommon";
import {notFound} from "next/navigation";
import {SEARCH_SUGGESTIONS_ORATIO} from "@/components/intl";


export default async function Page({params}: { params: Promise<{locale: string, id: string}> }) {
  const { locale } = await params
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/${locale}/api/v5/oratio`, {mode: "cors"});
  response.status !== 200 && notFound()
  const items = await response.json();
  return <ListCommon lang={locale} sidenavPath="oratio/" items={items}
                     searchSuggestions={SEARCH_SUGGESTIONS_ORATIO[locale]}/>
}