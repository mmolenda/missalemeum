import React from "react";
import ListProper from "@/components/ListProper";
import moment from "moment";
import {notFound} from "next/navigation";

export default async function Page({params}: { params: Promise<{locale: string}> }) {
  const { locale } = await params
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/${locale}/api/v5/calendar`, {mode: "cors"});
  response.status !== 200 && notFound()
  const items = await response.json();
  return <ListProper lang={locale} year={parseInt(moment().format("YYYY"))} items={items}/>

}
