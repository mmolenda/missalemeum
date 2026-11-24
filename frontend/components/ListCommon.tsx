"use client"

import List from "@mui/material/List";
import IndexListItem from "@/components/IndexListItem";
import SearchIcon from "@mui/icons-material/Search";
import InputAdornment from "@mui/material/InputAdornment";
import {ListControls, ListSearchPaper, ListSurface} from "@/components/listStyles";
import {Autocomplete, AutocompleteRenderInputParams, TextField} from "@mui/material";
import React, {createRef, RefObject, useCallback, useEffect, useMemo, useRef, useState} from "react";
import {Locale, SEARCH_PLACEHOLDER} from "@/components/intl";
import {ListItemType} from "@/components/types";
import {useMeasuredHeight} from "@/components/useMeasuredHeight";
import {isPageReference} from "@/components/pageSearch";

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

    <ListSurface>
      <ListControls ref={controlsRef} className="list-controls">
        <Autocomplete
          slots={{paper: ListSearchPaper}}
          size="small"
          sx={{flex: 1, minWidth: 0, maxWidth: {sm: 400}}}
          freeSolo
          value={filterString}
          onInputChange={(event, newValue) => {
            setFilterString(newValue)
          }}
          options={searchSuggestions || []}
          renderInput={(params: AutocompleteRenderInputParams): React.ReactNode => {
            return (<TextField
              {...params}
              placeholder={SEARCH_PLACEHOLDER[lang as Locale]}
              slotProps={{
                htmlInput: {...params.inputProps, "aria-label": SEARCH_PLACEHOLDER[lang as Locale]},
                input: {...params.InputProps, startAdornment: <InputAdornment position="start"><SearchIcon sx={{color: "var(--list-muted)"}} /></InputAdornment>},
              }}
            />)
          }}
        />
      </ListControls>
      <List className="list-index">
        {itemsFiltered.map((indexItem) => {
          const myRef: RefObject<HTMLLIElement | null> = listItemRefs.current[indexItem.id] ?? createRef<HTMLLIElement | null>()
          listItemRefs.current[indexItem.id] = myRef
          return (
            <IndexListItem
              key={indexItem.id}
              ref={myRef}
              selected={indexItem.id == selectedItem}
              href={sidenavPath + indexItem.id}
              title={indexItem.title}
              details={indexItem.tags.filter(tag => tag.trim() && !isPageReference(tag))}
            />)
        })}
      </List>
    </ListSurface>
  )
}
