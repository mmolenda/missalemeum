"use client"

import Link from "next/link";
import List from "@mui/material/List";
import {SidenavListItem} from "@/components/styledComponents/SidenavListItem";
import {ListItemButton} from "@mui/material";
import SidenavListItemText from "@/components/styledComponents/SidenavListItemText";
import slugify from "slugify";
import {ListItemType} from "@/components/types";

export default function ListOrdo({
                                   lang,
                                   items
}: {
  lang: string
  items: ListItemType[]
}) {
  return (
    <List>
      <>{items.map((indexItem) => {
        return (
          <SidenavListItem
            key={indexItem.label}
            disableGutters
          >
            <ListItemButton
              component={Link}
              href={`/${lang}/ordo#${slugify(indexItem.label)}`}
            >
              <SidenavListItemText
                prim={indexItem.label}
              />
            </ListItemButton>
          </SidenavListItem>)
      })}</>
    </List>
  )
}