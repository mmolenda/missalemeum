import React from 'react';
import ContainerWithSidenav from "./ContainerWithSidenav";
import {useParams} from "react-router-dom";

export default function Supplement() {
  const {lang} = useParams()
  const {id} = useParams()
  const getContentUrl = 'api/v5/supplement'
  const init = ((id, internalLang, internalYear, sidenavItems, getSidenavItems, getContent, setSidenavHidden) => {
    getContent(id)
  })

  return (
    <ContainerWithSidenav
      lang={lang}
      id={id}
      init={init}
      getContentUrl={getContentUrl}
      sidenavDisabled
      markdownNewlines
    />
  )
}

