import React from "react";
import ListCommon from "@/components/ListCommon";
import {notFound} from "next/navigation";
import {generateLocalisedMetadata} from "@/components/utils";
import {Locale, MENUITEM_VOTIVE} from "@/components/intl";

export async function generateMetadata({ params }: { params: Promise<{ locale: string; id?: string }> }){
  const { locale, id } = await params
  return generateLocalisedMetadata(locale, MENUITEM_VOTIVE[locale as Locale]);
}
export default async function Page({params}: { params: Promise<{locale: string, id: string}> }) {
  const { locale } = await params
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/${locale}/api/v5/votive`, {mode: "cors"});
  response.status !== 200 && notFound()
  const items = await response.json();
  return <ListCommon lang={locale} sidenavPath="votive/" items={items}/>
}