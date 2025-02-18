import React from 'react';
import {useParams} from "react-router-dom";
import ContainerSimple from "./ContainerSimple";
import {Alert} from "@mui/material";

export default function Info() {
  const {lang} = useParams()
  let content
  if (lang === 'pl') {
    content = 'Strona nie została odnaleziona'
  } else {
    content = 'Page not found'
  }
  let alert = <Alert severity="warning">{content}</Alert>
  return (
    <ContainerSimple title="404" content={alert} />
  )
}