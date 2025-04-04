import React from "react";
import ListProper from "@/components/ListProper";
import moment from "moment";
import {notFound} from "next/navigation";
import {callApi, generateLocalisedMetadata} from "@/components/utils";

export async function generateMetadata({ params }: { params: Promise<{ locale: string; id?: string }> }){
  const { locale } = await params
  return generateLocalisedMetadata(locale);
}

export default async function Page({params}: { params: Promise<{locale: string}> }) {
  const { locale } = await params
  const response = await callApi(locale, "calendar")
  if (response.status !== 200) {
    notFound();
  }
  const items = await response.json();
  return <ListProper lang={locale} year={parseInt(moment().format("YYYY"))} items={items}/>

}
