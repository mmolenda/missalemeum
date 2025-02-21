"use client"

import Link from "next/link";
import List from "@mui/material/List";
import {SidenavListItem} from "@/components/styledComponents/SidenavListItem";
import {ListItemButton} from "@mui/material";
import SidenavListItemText from "@/components/styledComponents/SidenavListItemText";
import {ContainerMedium} from "@/components/styledComponents/ContainerMedium";

export default function ListCommon({sidenavPath, items}) {
      return (
        <ContainerMedium disableGutters>
        <List>
        {items.map((indexItem) => {
          // let listItemRef = createRef()
          // listItemRefs[indexItem.id] = listItemRef
          return (
            <SidenavListItem
              key={indexItem.id}
              disableGutters
            >
              <ListItemButton
                component={Link}
                to={{pathname: sidenavPath + indexItem.id, hash: ""}}
              >
                <SidenavListItemText
                  primary={indexItem.title}
                  secondary={indexItem.tags.length > 0 && indexItem.tags.join(", ")}
                />
              </ListItemButton>
            </SidenavListItem>)
        })}
      </List>
        </ContainerMedium>

              ) }