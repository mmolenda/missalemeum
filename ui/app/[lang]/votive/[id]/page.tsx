import {Box, ListItem, Typography} from "@mui/material";
import React from "react";
import List from "@mui/material/List";
import Link from "next/link";
import ContainerNext from "@/components/ContainerNext";


export default async function Page({params}) {
  const lang = (await params).lang
  const id = (await params).id

  const response = await fetch(`http://localhost:8000/${lang}/api/v5/proper/${id}`, {mode: "cors"});
  const proper = await response.json();
  return <ContainerNext lang={lang} content={proper}/>
}