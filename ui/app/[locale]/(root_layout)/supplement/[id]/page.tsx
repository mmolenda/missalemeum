import React from "react";
import {notFound} from "next/navigation";
import BilingualContent from "@/components/BilingualContent";



export default async function Page({
  params,
  searchParams
}: {
  params: Promise<{locale: string, id: string}>
  searchParams: Promise<{ref: string}>
}) {
  const { locale, id } = await params
  const { ref } = await searchParams
  let backButtonRef = ref && `/${locale}/${ref}`
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/${locale}/api/v5/supplement/${id}`, {mode: "cors"});
  response.status !== 200 && notFound()
  const proper = await response.json();
  return <BilingualContent lang={locale} id={id} contents={proper} backButtonRef={backButtonRef} markdownNewlines={true} />
}