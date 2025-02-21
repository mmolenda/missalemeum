import React from "react";
import ContainerNext from "@/components/ContainerNext";


export default async function Index({params}) {
  const lang = (await params).lang
  const response = await fetch(`${process.env.MISSALEMEUM_API_URL}/${lang}/api/v5/supplement/index`, {mode: "cors"});
  const proper = await response.json();
  return <ContainerNext lang={lang} content={proper} />
}