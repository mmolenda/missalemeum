import React from "react";
import ListCommon from "@/components/ListCommon";
import {notFound} from "next/navigation";


export default async function Page({params}) {
  const locale = (await params).locale
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/${locale}/api/v5/oratio`, {mode: "cors"});
    response.status !== 200 && notFound()
    const items = await response.json();
    return <ListCommon lang={locale} sidenavPath="oratio/" items={items} />
}