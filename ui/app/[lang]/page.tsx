import Link from 'next/link'
import {Box, ListItem, Typography} from "@mui/material";
import React from "react";
import List from "@mui/material/List";
import ListCommon from "@/components/ListCommon";
import ListProper from "@/components/ListProper";

export default async function Page({params}) {
  const lang = (await params).lang

    const response = await fetch(`http://localhost:8000/${lang}/api/v5/calendar`, {mode: "cors"});
    const calendarItems = await response.json();

    return <ListProper sidenavPath="votive/" lang={lang} items={calendarItems} />
  // return (
  //   <Box>
  //        <Typography variant="h2">Main Calendar for {lang}</Typography>
  //     <List>
  //       {calendarItems.map((calendarItem) => (
  //         <ListItem key={calendarItem.id}>
  //             <Link href={`/${lang}/${calendarItem.id}`}>{calendarItem.id} {calendarItem.title}</Link>
  //         </ListItem>
  //       ))}
  //     </List>
  //   </Box>
  // );
}