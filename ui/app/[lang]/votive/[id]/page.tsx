import React from "react";
import ContainerNext from "@/components/ContainerNext";


export default async function Page({params}) {
  const lang = (await params).lang
  const id = (await params).id
  const response = await fetch(`${process.env.MISSALEMEUM_API_URL}/${lang}/api/v5/proper/${id}`, {mode: "cors"});
  const proper = await response.json();
  return <ContainerNext lang={lang} content={proper} backButtonRef={`/${lang}/votive#${id}`}/>
}