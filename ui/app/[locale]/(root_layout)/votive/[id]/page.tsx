import React from "react";
import ContainerNext from "@/components/ContainerNext";


export default async function Page({params}) {
  const locale = (await params).locale
  const id = (await params).id
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/${locale}/api/v5/proper/${id}`, {mode: "cors"});
  const proper = await response.json();
  return <ContainerNext lang={locale} id={id} content={proper} backButtonRef={`/${locale}/votive#${id}`}/>
}