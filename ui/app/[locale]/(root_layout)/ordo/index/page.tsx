import React from "react";
import ListOrdo from "@/components/ListOrdo";
import {notFound} from "next/navigation";


export default async function Page({params}: { params: Promise<{locale: string, id: string}> }) {
  const { locale } = await params
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/${locale}/api/v5/ordo`, {mode: "cors"});
  response.status !== 200 && notFound()
  const items = await response.json();
  return <ListOrdo lang={locale} items={items[0]["sections"]}/>
}