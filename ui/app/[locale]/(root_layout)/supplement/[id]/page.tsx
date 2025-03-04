import React from "react";
import {notFound} from "next/navigation";
import BilingualContent from "@/components/BilingualContent";
import {Content} from "@/components/types";
import {generateLocalisedMetadata} from "@/components/utils";

export async function generateMetadata({ params }: { params: Promise<{ locale: string; id?: string }> }) {
  const { locale, id } = await params
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/${locale}/api/v5/supplement/${id}`, {mode: "cors", cache: "force-cache"});
  if (response.status == 200) {
    const contents: Content[] = await response.json()
    const titleFragment = `${contents[0].info.title}`
    return generateLocalisedMetadata(locale, titleFragment)
  }
  return generateLocalisedMetadata(locale)
}

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