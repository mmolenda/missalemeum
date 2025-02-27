"use client"

import Link from "next/link";
import List from "@mui/material/List";
import {SidenavListItem} from "@/components/styledComponents/SidenavListItem";
import {ListItemButton} from "@mui/material";
import SidenavListItemText from "@/components/styledComponents/SidenavListItemText";
import slugify from "slugify";

export default function ListOrdo({lang, items}) {
  return (
    <List>
      {items.map((indexItem) => {
        return (
          <SidenavListItem
            key={indexItem.label}
            disableGutters
          >
            <ListItemButton
              component={Link}
              to={{pathname: `/${lang}/ordo`, hash: slugify(indexItem.label)}}
            >
              <SidenavListItemText
                primary={indexItem.label}
              />
            </ListItemButton>
          </SidenavListItem>)
      })}
    </List>
  )
}