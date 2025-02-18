import React from 'react';
import ContainerWithSidenav from "@/components/ContainerWithSidenav";
import {SEARCH_SUGGESTIONS_ORATIO} from "@/components/intl";


import Logo from "@/components/Logo";
export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const id = (await params).id
  const lang = (await params).lang
  const getContentUrl = 'api/v5/oratio'
  const getSidenavItemsUrl = 'api/v5/oratio'
  const path = '/oratio/'
  const init = ((id, internalLang, internalYear, sidenavItems, getSidenavItems, getContent, setSidenavHidden) => {
    setSidenavHidden(Boolean(id))
    if (sidenavItems === null) {
      getSidenavItems()
    }
    getContent(id)
  })
  // return <div><h1>Oratio</h1><Logo width={10} height={10} /><p>Oratio: { lang }/{ id }</p></div>
  return (
    <ContainerWithSidenav
      lang={lang}
      id={id}
      init={init}
      getContentUrl={getContentUrl}
      getSidenavItemsUrl={getSidenavItemsUrl}
      sidenavPath={path}
      markdownNewlines
      searchSuggestions={ {} }
    />
  )
}
