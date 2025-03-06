import React from "react";
import ListCommon from "@/components/ListCommon";
import {notFound} from "next/navigation";
import {Locale, MENUITEM_CANTICUM, SEARCH_SUGGESTIONS_CANTICUM} from "@/components/intl";
import {callApi, generateLocalisedMetadata} from "@/components/utils";

export async function generateMetadata({ params }: { params: Promise<{ locale: string; id?: string }> }){
  const { locale, id } = await params
  return generateLocalisedMetadata(locale, MENUITEM_CANTICUM[locale as Locale]);
}

export default async function Page({params}: { params: Promise<{locale: string}> }) {
  const { locale } = await params
  const response = await callApi(locale, "canticum")
  response.status !== 200 && notFound()
  const items = await response.json();
  return <ListCommon lang={locale} sidenavPath="canticum/" items={items}
                     searchSuggestions={SEARCH_SUGGESTIONS_CANTICUM[locale as Locale]}/>
}