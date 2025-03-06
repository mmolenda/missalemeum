import React from "react";
import ListOrdo from "@/components/ListOrdo";
import {notFound} from "next/navigation";
import {callApi, generateLocalisedMetadata} from "@/components/utils";
import {Locale, MENUITEM_ORDO} from "@/components/intl";

export async function generateMetadata({ params }: { params: Promise<{ locale: string; id?: string }> }){
  const { locale, id } = await params
  return generateLocalisedMetadata(locale, MENUITEM_ORDO[locale as Locale]);
}

export default async function Page({params}: { params: Promise<{locale: string, id: string}> }) {
  const { locale } = await params
  const response = await callApi(locale, "ordo")
  response.status !== 200 && notFound()
  const items = await response.json();
  return <ListOrdo lang={locale} items={items[0]["sections"]}/>
}