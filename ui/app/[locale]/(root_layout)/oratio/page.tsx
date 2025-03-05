import React from "react";
import ListCommon from "@/components/ListCommon";
import {notFound} from "next/navigation";
import {Locale, MENUITEM_ORATIO, SEARCH_SUGGESTIONS_ORATIO} from "@/components/intl";
import {callApi, generateLocalisedMetadata, userAgentString} from "@/components/utils";

export async function generateMetadata({ params }: { params: Promise<{ locale: string; id?: string }> }){
  const { locale, id } = await params
  return generateLocalisedMetadata(locale, MENUITEM_ORATIO[locale as Locale]);
}

export default async function Page({params}: { params: Promise<{locale: string, id: string}> }) {
  const { locale } = await params
  const response = await callApi(locale, "oratio")
  response.status !== 200 && notFound()
  const items = await response.json();
  return <ListCommon lang={locale} sidenavPath="oratio/" items={items}
                     searchSuggestions={SEARCH_SUGGESTIONS_ORATIO[locale as Locale]}/>
}