"use client"

import Link from "next/link";
import List from "@mui/material/List";
import {SidenavListItem} from "@/components/styledComponents/SidenavListItem";
import {ListItemButton} from "@mui/material";
import SidenavListItemText from "@/components/styledComponents/SidenavListItemText";
import {ContainerMedium} from "@/components/styledComponents/ContainerMedium";
import {createRef, useEffect, useState} from "react";

export default function ListCommon({sidenavPath, items}) {
  let [selectedItem, setSelectedItem] = useState(null)
  let listItemRefs = {}

  useEffect(() => {
    setSelectedItem(window.location.hash.substring(1))
    scrollToListItem(selectedItem)
  })

  const scrollToListItem = (itemId) => {
    let listItemRef = listItemRefs[itemId]
    if (listItemRef && listItemRef.current) {
      listItemRef.current.scrollIntoView({block: "center", behavior: "auto"})
      listItemRef.current.classList.add("sidenavItemActive")
    }
  }

  return (
    <ContainerMedium disableGutters>
      <List>
        {items.map((indexItem) => {
          let myRef = createRef()
          listItemRefs[indexItem.id] = myRef
          return (
            <SidenavListItem
              key={indexItem.id}
              ref={myRef}
              disableGutters
            >
              <ListItemButton
                selected={ indexItem.id == selectedItem }
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

  )
}