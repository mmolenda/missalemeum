import React from "react";
import {notFound} from "next/navigation";
import BilingualContent from "@/components/BilingualContent";
import {generateLocalisedMetadata} from "@/components/utils";
import {Locale, MENUITEM_ORDO} from "@/components/intl";

export async function generateMetadata({ params }: { params: Promise<{ locale: string; id?: string }> }){
  const { locale, id } = await params
  return generateLocalisedMetadata(locale, MENUITEM_ORDO[locale as Locale]);
}

export default async function Page({params}: { params: Promise<{locale: string, id: string}> }) {
  const { id, locale } = await params
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/${locale}/api/v5/ordo`, {mode: "cors"});
  response.status !== 200 && notFound()
  const proper = await response.json();
  return <BilingualContent lang={locale} id={id} contents={proper} backButtonRef={`/${locale}/ordo/index`} singleColumnAsRubric={true} />
}