import React from 'react';
import ContainerWithSidenav from "./ContainerWithSidenav";

export default function Votive() {

  const getContentUrl = 'api/v5/proper'
  const getSidenavItemsUrl = 'api/v5/votive'
  const path = '/votive/'
  const init = ((id, internalLang, internalYear, sidenavItems, getSidenavItems, getContent, setSidenavHidden) => {
    setSidenavHidden(Boolean(id))
    if (sidenavItems === null) {
      getSidenavItems()
    }
    getContent(id)
  })

  return (
    <ContainerWithSidenav
      init={init}
      getContentUrl={getContentUrl}
      getSidenavItemsUrl={getSidenavItemsUrl}
      sidenavPath={path}
    />
  )
}

