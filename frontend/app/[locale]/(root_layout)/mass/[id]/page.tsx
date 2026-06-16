import React from "react";
import { notFound } from "next/navigation";
import BilingualContent from "@/components/BilingualContent";
import { Content } from "@/components/types";
import { callApi, generateLocalisedMetadata } from "@/components/utils";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string; id?: string }>;
}) {
  const { locale, id } = await params;
  const response = await callApi(locale, "proper", id);
  if (response.status === 200) {
    const contents: Content[] = await response.json();
    return generateLocalisedMetadata(locale, {
      titleFragment: contents[0].info.title,
      pathSuffix: `/mass/${id}`,
    });
  }
  return generateLocalisedMetadata(locale, { pathSuffix: `/mass/${id}` });
}

export default async function Page({
  params,
  searchParams,
}: {
  params: Promise<{ locale: string; id: string }>;
  searchParams: Promise<{ ref?: string }>;
}) {
  const { id, locale } = await params;
  const { ref } = await searchParams;
  const backButtonRef = ref ? `/${locale}/${ref}` : undefined;
  const response = await callApi(locale, "proper", id);
  if (response.status !== 200) {
    notFound();
  }
  const proper = await response.json();
  return <BilingualContent lang={locale} id={id} contents={proper} backButtonRef={backButtonRef} apiEndpoint="proper"/>;
}
