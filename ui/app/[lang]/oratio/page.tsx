import {Box, ListItem, Typography} from "@mui/material";
import React from "react";
import List from "@mui/material/List";
import Link from "next/link";
import ListCommon from "@/components/ListCommon";


export default async function Page({params}) {
  const lang = (await params).lang
    const id = (await params).id
    const response = await fetch(`http://localhost:8000/${lang}/api/v5/oratio`, {mode: "cors"});
    const items = await response.json();
    return <ListCommon sidenavPath="oratio/" items={items} />
}