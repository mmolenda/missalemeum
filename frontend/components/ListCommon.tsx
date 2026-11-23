"use client"

import Link from "next/link";
import List from "@mui/material/List";
import {SidenavListItem} from "@/components/styledComponents/SidenavListItem";
import {Autocomplete, AutocompleteRenderInputParams, Box, ListItemButton, TextField} from "@mui/material";
import SidenavListItemText from "@/components/styledComponents/SidenavListItemText";
import React, {createRef, RefObject, useCallback, useEffect, useMemo, useRef, useState} from "react";
import {Locale, SEARCH_PLACEHOLDER} from "@/components/intl";
import {ListItemType} from "@/components/types";
import {getAppBarHeightFromTheme} from "@/components/layoutMetrics";
import {useMeasuredHeight} from "@/components/useMeasuredHeight";

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
  const [filterString, setFilterString] = useState("")
  const controlsRef = useRef<HTMLDivElement>(null);
  useMeasuredHeight(controlsRef, "--list-controls-height");
  const searchIndex = useMemo(() => items.map(item => ({
    item, text: JSON.stringify(item).toLocaleLowerCase(lang),
  })), [items, lang]);
  const query = filterString.trim().toLocaleLowerCase(lang);
  const itemsFiltered = useMemo(() => query.length < 3 ? items : searchIndex
    .filter(({text}) => text.includes(query)).map(({item}) => item), [items, query, searchIndex]);

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


  return (

    <>
      <Box ref={controlsRef} sx={{
        position: "fixed",
        display: "flex",
        top: (theme) => {
          const appBarHeight = getAppBarHeightFromTheme(theme);
          return `calc(${appBarHeight}px + var(--announcement-banner-height, 0px))`;
        },
        width: "100%",
        maxWidth: "900px",
        left: "50%",
        transform: "translateX(-50%)",
        p: "0.75rem",
        boxShadow: 2,
        backgroundColor: "background.default",
        zIndex: 100
      }}>
        <Autocomplete
          size="small"
          sx={{width: {xs: "100%", sm: "30%"}, minWidth: 0}}
          freeSolo
          value={filterString}
          onInputChange={(event, newValue) => {
            setFilterString(newValue)
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
