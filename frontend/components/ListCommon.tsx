"use client"

import Link from "next/link";
import List from "@mui/material/List";
import {SidenavListItem} from "@/components/styledComponents/SidenavListItem";
import {Autocomplete, AutocompleteRenderInputParams, Box, ListItemButton, TextField} from "@mui/material";
import SidenavListItemText from "@/components/styledComponents/SidenavListItemText";
import React, {createRef, RefObject, useCallback, useEffect, useRef, useState} from "react";
import {Locale, SEARCH_PLACEHOLDER} from "@/components/intl";
import {ListItemType} from "@/components/types";
import {myLocalStorage} from "@/components/myLocalStorage";
import {
  BANNER_ENABLED,
  BANNER_HEIGHT,
  BANNER_STORAGE_KEY,
  getAppBarHeightFromTheme,
} from "@/components/layoutMetrics";

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
  const listItemRefs = useRef<Record<string, RefObject<HTMLLIElement | null>>>({})
  const [itemsFiltered, setItemsFiltered] = useState(items)
  const [filterString, setFilterString] = useState("")

  const scrollToListItem = useCallback((itemId: string) => {
    const listItemRef = listItemRefs.current[itemId]
    if (listItemRef && listItemRef.current) {
      listItemRef.current.scrollIntoView({block: "center", behavior: "auto"})
      listItemRef.current.classList.add("sidenavItemActive")
    }
  }, [listItemRefs])

  useEffect(() => {
    const hash = window.location.hash.substring(1)
    if (hash) {
      setSelectedItem(hash)
    }
  }, [])

  useEffect(() => {
    if (selectedItem) {
      scrollToListItem(selectedItem)
    }
  }, [scrollToListItem, selectedItem])

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
          const appBarHeight = getAppBarHeightFromTheme(theme);
          const bannerDismissed = myLocalStorage.getItem(BANNER_STORAGE_KEY) === "true";
          const offset = BANNER_ENABLED && !bannerDismissed ? BANNER_HEIGHT : 0;
          return `${appBarHeight + offset}px`;
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
          const myRef: RefObject<HTMLLIElement | null> = listItemRefs.current[indexItem.id] ?? createRef<HTMLLIElement | null>()
          listItemRefs.current[indexItem.id] = myRef
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
