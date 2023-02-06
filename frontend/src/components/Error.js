import React from 'react';
import {useParams} from "react-router-dom";
import ContainerSimple from "./ContainerSimple";
import {Alert} from "@mui/material";

export default function Info() {
  const {lang} = useParams()
  let content
  if (lang === 'pl') {
    content = 'Wystąpił błąd. Spróbuj ponownie później.'
  } else {
    content = 'An error occurred, please try again later'
  }
  let alert = <Alert severity="error">{content}</Alert>
  return (
    <ContainerSimple title="Błąd" content={alert} />
  )
}
