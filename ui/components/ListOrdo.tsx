"use client"

import Link from "next/link";
import List from "@mui/material/List";
import {SidenavListItem} from "@/components/styledComponents/SidenavListItem";
import {ListItemButton} from "@mui/material";
import SidenavListItemText from "@/components/styledComponents/SidenavListItemText";
import {ContainerMedium} from "@/components/styledComponents/ContainerMedium";

export default function ListOrdo({lang, items}) {
  return (
    <ContainerMedium disableGutters>
      <List>
        {items.map((indexItem) => {
          return (
            <SidenavListItem
              key={indexItem.label}
              disableGutters
            >
              <ListItemButton
                component={Link}
                to={{pathname: `/${lang}/ordo`, hash: indexItem.label}}
              >
                <SidenavListItemText
                  primary={indexItem.label}
                />
              </ListItemButton>
            </SidenavListItem>)
        })}
      </List>
    </ContainerMedium>

  )
}