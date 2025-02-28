"use client"

import Link from "next/link";
import List from "@mui/material/List";
import {SidenavListItem} from "@/components/styledComponents/SidenavListItem";
import {Autocomplete, AutocompleteRenderInputParams, Box, ListItemButton, TextField} from "@mui/material";
import SidenavListItemText from "@/components/styledComponents/SidenavListItemText";
import React, {createRef, useEffect, useState} from "react";
import {Locale, SEARCH_PLACEHOLDER} from "@/components/intl";

export default function ListCommon({
                                     lang,
                                     sidenavPath,
                                     items,
                                     searchSuggestions = []
                                   }:
                                     {
                                       lang: string,
                                       sidenavPath: string,
                                       items: object[],
                                       searchSuggestions?: string[]
                                     }) {
  let [selectedItem, setSelectedItem] = useState("")
  let listItemRefs = {}
  const [itemsFiltered, setItemsFiltered] = useState(items)
  const [filterString, setFilterString] = useState("")

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

  const filterItems = (filterString) => {
    if (filterString.length === 0) {
      setItemsFiltered(items)
    } else if (filterString.length > 2) {
      filterString = filterString.toLowerCase()
      let collectedItems = []
      for (let item of items) {
        let searchBody = JSON.stringify(item).toLowerCase()
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
        top: (theme) => theme.components.MuiAppBar.styleOverrides.root.height,
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
          let myRef = createRef()
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
    </>
  )
}