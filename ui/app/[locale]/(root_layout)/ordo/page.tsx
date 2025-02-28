import React from "react";
import {notFound} from "next/navigation";
import BilingualContent from "@/components/BilingualContent";


export default async function Page({params}) {
  const locale = (await params).locale
  const id = (await params).id
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/${locale}/api/v5/ordo`, {mode: "cors"});
  response.status !== 200 && notFound()
  const proper = await response.json();
  return <BilingualContent lang={locale} id={id} content={proper} backButtonRef={`/${locale}/ordo/index`} singleColumnAsRubric={true} />
}