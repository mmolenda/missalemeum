import React from "react";
import ContainerNext from "@/components/ContainerNext";


export default async function Page({params}) {
  const locale = (await params).locale
  const id = (await params).id
  const response = await fetch(`${process.env.MISSALEMEUM_API_URL}/${locale}/api/v5/canticum/${id}`, {mode: "cors"});
  const item = await response.json();
  return <ContainerNext lang={locale} id={id} content={item} backButtonRef={`/${locale}/canticum#${id}`} />
}