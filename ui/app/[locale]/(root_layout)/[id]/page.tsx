import React from "react";
import ListProper from "@/components/ListProper";
import moment from "moment/moment";
import { notFound } from "next/navigation";
import BilingualContent from "@/components/BilingualContent";


export default async function Page({params}) {
  const locale = (await params).locale
  const id = (await params).id

  if (/^\d{4}$/.test(id)) {
    // we will render either Proper's content or calendar for given year here
    // depending on passed ID. This is a subject to change when new URL layout
    // is done.
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/${locale}/api/v5/calendar/${id}`, {mode: "cors"});
    return <ListProper lang={locale} year={id} items={await response.json()}/>
  } else {
    let parsedDate = moment(id)
    !parsedDate.isValid() && notFound()
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/${locale}/api/v5/proper/${id}`, {mode: "cors"});
    response.status !== 200 && notFound()
    const providedYear = id.split("-")[0]
    let currentYear = moment().format("YYYY")
    let yearBit = providedYear != currentYear ? `/${providedYear}` : ""
    return <BilingualContent lang={locale} id={id} content={await response.json()} backButtonRef={`/${locale}${yearBit}#${id}`}/>
  }
}