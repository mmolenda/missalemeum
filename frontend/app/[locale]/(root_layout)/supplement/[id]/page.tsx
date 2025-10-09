import React from "react";
import { notFound } from "next/navigation";
import Script from "next/script";
import BilingualContent from "@/components/BilingualContent";
import { Content } from "@/components/types";
import { callApi, generateLocalisedMetadata } from "@/components/utils";
import { DonationWidget } from "@/components/donations";
import { Locale } from "@/components/intl";

export async function generateMetadata({ params }: { params: Promise<{ locale: string; id?: string }> }) {
  const { locale, id } = await params
  const response = await callApi(locale, "supplement", id)
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
  const backButtonRef = ref && `/${locale}/${ref}`
  const response = await callApi(locale, "supplement", id)
  if (response.status !== 200) {
    notFound();
  }
  const proper = await response.json();
  const showDonation = id === "info";
  const lang = (locale === "pl" ? "pl" : "en") as Locale;

  return (
    <>
      {showDonation ? <Script strategy="afterInteractive" src="https://js.stripe.com/v3/buy-button.js" /> : null}
      <BilingualContent lang={locale} id={id} contents={proper} backButtonRef={backButtonRef} markdownNewlines={true} apiEndpoint="supplement"/>
      {showDonation ? (
        <div
          style={{
            marginTop: "1.5rem",
            display: "flex",
            justifyContent: "center",
          }}
        >
          <DonationWidget lang={lang} />
        </div>
      ) : null}
    </>
  )
}
