import React from 'react';
import ContainerWithSidenav from "./ContainerWithSidenav";

export default function Supplement() {

  const getContentUrl = 'api/v5/supplement'
  const init = ((id, internalLang, internalYear, sidenavItems, getSidenavItems, getContent, setSidenavHidden) => {
    getContent(id)
  })

  return (
    <ContainerWithSidenav
      init={init}
      getContentUrl={getContentUrl}
      sidenavDisabled
      markdownNewlines
    />
  )
}

