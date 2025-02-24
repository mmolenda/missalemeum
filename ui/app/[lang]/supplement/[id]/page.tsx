import React from "react";
import ContainerNext from "@/components/ContainerNext";


export default async function Page({params, searchParams}) {
  const lang = (await params).lang
  const id = (await params).id
  const ref = (await searchParams).ref
  let backButtonRef = `/${lang}/${ref}`
    //id != "index" ? "index" : null
  const response = await fetch(`${process.env.MISSALEMEUM_API_URL}/${lang}/api/v5/supplement/${id}`, {mode: "cors"});
  const proper = await response.json();
  return <ContainerNext lang={lang} id={id} content={proper} backButtonRef={backButtonRef} />
}