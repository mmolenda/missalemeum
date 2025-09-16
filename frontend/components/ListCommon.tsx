"use client"

import Link from "next/link";
import List from "@mui/material/List";
import {SidenavListItem} from "@/components/styledComponents/SidenavListItem";
import {Autocomplete, AutocompleteRenderInputParams, Box, ListItemButton, TextField} from "@mui/material";
import SidenavListItemText from "@/components/styledComponents/SidenavListItemText";
import React, {createRef, RefObject, useEffect, useState} from "react";
import {Locale, SEARCH_PLACEHOLDER} from "@/components/intl";
import {ListItemType} from "@/components/types";

export default function ListCommon({
                                     lang,
                                     sidenavPath,
                                     items,
                                     searchSuggestions = []
                                   }:
                                     {
                                       lang: string,
                                       sidenavPath: string,
                                       items: ListItemType[],
                                       searchSuggestions?: string[]
                                     }) {
  const [selectedItem, setSelectedItem] = useState("")
  const listItemRefs: Record<string, RefObject<HTMLLIElement | null>> = {}
  const [itemsFiltered, setItemsFiltered] = useState(items)
  const [filterString, setFilterString] = useState("")

  useEffect(() => {
    setSelectedItem(window.location.hash.substring(1))
    scrollToListItem(selectedItem)
  })

  const scrollToListItem = (itemId: string) => {
    const listItemRef = listItemRefs[itemId]
    if (listItemRef && listItemRef.current) {
      listItemRef.current.scrollIntoView({block: "center", behavior: "auto"})
      listItemRef.current.classList.add("sidenavItemActive")
    }
  }

  const filterItems = (filterString: string) => {
    if (filterString.length === 0) {
      setItemsFiltered(items)
    } else if (filterString.length > 2) {
      filterString = filterString.toLowerCase()
      const collectedItems = []
      for (const item of items) {
        const searchBody = JSON.stringify(item).toLowerCase()
        if (searchBody.includes(filterString)) {
          collectedItems.push(item)
        }
      }
      setItemsFiltered(collectedItems)
    }
  }


  return (

    <>
      <Box sx={{
        position: "fixed",
        display: "flex",
        top: (theme) => {
            // we just need the value of theme.components?.MuiAppBar?.styleOverrides?.root.height
            // all the code below is to appease typescript linter
            const root = theme.components?.MuiAppBar?.styleOverrides?.root;
            const height = root && typeof root === 'object' && 'height' in root ? root.height : "0px";
            return height as string;
          },
        width: "875px",
        p: "0.75rem",
        boxShadow: 2,
        backgroundColor: "background.default",
        zIndex: 100
      }}>
        <Autocomplete
          size="small"
          sx={{width: "30%"}}
          freeSolo
          value={filterString}
          onInputChange={(event, newValue) => {
            setFilterString(newValue)
            filterItems(newValue)
          }}
          options={searchSuggestions || []}
          renderInput={(params: AutocompleteRenderInputParams): React.ReactNode => {
            return (<TextField
              {...params}
              label={SEARCH_PLACEHOLDER[lang as Locale]}
            />)
          }}
        />
      </Box>
      <List>
        {itemsFiltered.map((indexItem) => {
          const myRef: RefObject<HTMLLIElement | null> = createRef<HTMLLIElement | null>()
          listItemRefs[indexItem.id] = myRef
          return (
            <SidenavListItem
              key={indexItem.id}
              ref={myRef}
              disableGutters
            >
              <ListItemButton
                selected={indexItem.id == selectedItem}
                component={Link}
                href={sidenavPath + indexItem.id}
              >
                <SidenavListItemText
                  prim={indexItem.title}
                  sec={indexItem.tags.length > 0 ? indexItem.tags.join(", "): ""}
                />
              </ListItemButton>
            </SidenavListItem>)
        })}
      </List>
    </>
  )
}
