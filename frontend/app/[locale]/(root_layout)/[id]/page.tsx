import React from "react";
import ListProper from "@/components/ListProper";
import moment from "moment/moment";
import { notFound } from "next/navigation";
import BilingualContent from "@/components/BilingualContent";
import {callApi, generateLocalisedMetadata} from "@/components/utils";
import {Content} from "@/components/types";

export async function generateMetadata({ params }: { params: Promise<{ locale: string; id?: string }> }) {
  const { locale, id } = await params
  if (id && /^\d{4}-\d{2}-\d{2}$/.test(id) && moment(id).isValid()) {
    const response = await callApi(locale, "proper", id)
    const contents: Content[] = await response.json()
    const titleFragment = `${contents[0].info.title} | ${id}`
    return generateLocalisedMetadata(locale, titleFragment);
  }
  return generateLocalisedMetadata(locale);
}

export default async function Page({params}: { params: Promise<{locale: string, id: string}> }) {
  const { id, locale } = await params

  if (/^\d{4}$/.test(id)) {
    // we will render either Proper's content or calendar for given year here
    // depending on passed ID. This is a subject to change when new URL layout
    // is done.
    const response = await callApi(locale, "calendar", id)
    if (response.status !== 200) {
      notFound();
    }
    return <ListProper lang={locale} year={parseInt(id)} items={await response.json()}/>
  } else {
    const parsedDate = moment(id)
    if (!parsedDate.isValid()) {
      notFound();
    }
    const response = await callApi(locale, "proper", id)
    if (response.status !== 200) {
      notFound();
    }
    const providedYear = id.split("-")[0]
    const currentYear = moment().format("YYYY")
    const yearBit = providedYear != currentYear ? `/${providedYear}` : ""
    return <BilingualContent lang={locale} id={id} contents={await response.json()} backButtonRef={`/${locale}${yearBit}#${id}`}/>
  }
}