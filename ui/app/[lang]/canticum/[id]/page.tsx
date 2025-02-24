import React from "react";
import ContainerNext from "@/components/ContainerNext";


export default async function Page({params}) {
  const lang = (await params).lang
  const id = (await params).id
  const response = await fetch(`${process.env.MISSALEMEUM_API_URL}/${lang}/api/v5/canticum/${id}`, {mode: "cors"});
  const item = await response.json();
  return <ContainerNext lang={lang} content={item} backButtonRef={`/${lang}/canticum#${id}`} />
}