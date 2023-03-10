import React from 'react';
import ContainerWithSidenav from "./ContainerWithSidenav";
import {useParams} from "react-router-dom";

export default function Canticum() {
  const {lang} = useParams()
  const {id} = useParams()
  const getContentUrl = 'api/v5/canticum'
  const getSidenavItemsUrl = 'api/v5/canticum'
  const path = '/canticum/'
  const init = ((id, internalLang, internalYear, sidenavItems, getSidenavItems, getContent, setSidenavHidden) => {
    setSidenavHidden(Boolean(id))
    if (sidenavItems === null) {
      getSidenavItems()
    }
    getContent(id)
  })

  return (
    <ContainerWithSidenav
      lang={lang}
      id={id}
      init={init}
      getContentUrl={getContentUrl}
      getSidenavItemsUrl={getSidenavItemsUrl}
      sidenavPath={path}
      markdownNewlines
    />
  )
}

