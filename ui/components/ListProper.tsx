"use client"

import Link from "next/link";
import List from "@mui/material/List";
import {SidenavListItem} from "@/components/styledComponents/SidenavListItem";
import SidenavListItemText from "@/components/styledComponents/SidenavListItemText";
import React, {createRef, Dispatch, Fragment, RefObject, SetStateAction, useEffect, useState} from "react";
import {
  COMMEMORATION,
  IN,
  Locale,
  MUI_DATEPICKER_LOCALE_TEXT,
  RANK_NAMES,
  SEARCH_PLACEHOLDER,
  SEARCH_SUGGESTIONS_PROPER
} from "@/components/intl";
import moment from "moment";
import {
  Autocomplete,
  Box,
  ListItemButton,
  ListItemIcon,
  TextField,
  IconButton,
  AutocompleteRenderInputParams
} from "@mui/material";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import ListItemText from "@mui/material/ListItemText";
import EventIcon from '@mui/icons-material/Event';
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import CalendarMonthIcon from '@mui/icons-material/CalendarMonth';
import "react-datepicker/dist/react-datepicker.css";
import {LocalizationProvider, MobileDatePicker} from "@mui/x-date-pickers";
import {AdapterDayjs} from "@mui/x-date-pickers/AdapterDayjs";
import "dayjs/locale/pl";
import {useRouter} from "next/navigation";
import {ListItemType} from "@/components/types";
import {Dayjs} from "dayjs";

export default function ListProper({
                                     lang,
                                     year,
                                     items
                                   }: {
  lang: string
  year: number
  items: ListItemType[]
}) {
  const dateFormat = 'YYYY-MM-DD'
  const todayFmt = moment().format(dateFormat)
  const [itemsFiltered, setItemsFiltered] = useState(items)
  const [filterString, setFilterString] = useState("")
  const [selectedItem, setSelectedItem] = useState("")
  const router = useRouter()
  const listItemRefs: Record<string, RefObject<any>> = {}

  useEffect(() => {
    setSelectedItem(window.location.hash.substring(1) || todayFmt)
    let listItemRef = listItemRefs[selectedItem]
    if (listItemRef && listItemRef.current) {
      listItemRef.current.scrollIntoView({block: "center", behavior: "auto"})
    }
  })

  const filterItems = (filterString: string) => {
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

  interface ButtonFieldProps {
    setOpen?: Dispatch<SetStateAction<boolean>>;
  }

  function ButtonField({setOpen}: ButtonFieldProps) {
    return (
      <IconButton
        onClick={() => setOpen?.((prev) => !prev)}
      >
        <CalendarMonthIcon/>
      </IconButton>
    )
  }

  const MyDatePicker = () => {
    const [open, setOpen] = useState(false);
    const handleDateChange = (newValue: Dayjs | null) => {
      if (newValue) {
        router.push(`${lang}/${newValue.format(dateFormat)}`);
      }
    }
    return (
      <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale={lang}
                            localeText={MUI_DATEPICKER_LOCALE_TEXT[lang as Locale]}>
        <MobileDatePicker
          slots={{field: ButtonField}}
          slotProps={
            {field: {setOpen} as any}
          }
          open={open}
          onClose={() => setOpen(false)}
          onOpen={() => setOpen(true)}
          onChange={handleDateChange}

        />
      </LocalizationProvider>
    )
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
          options={SEARCH_SUGGESTIONS_PROPER[lang as Locale] || []}
          renderInput={(params: AutocompleteRenderInputParams): React.ReactNode => {
            return (<TextField
              {...params}
              label={`${SEARCH_PLACEHOLDER[lang as Locale]} ${IN[lang as Locale]} ${year}`}
            />)
          }}
        />
        <MyDatePicker/>
      </Box>
      <List>
        <PrevOrNextYearListItem lang={lang} year={year} isNext={false}/>
        {itemsFiltered.map((indexItem) => {
            let colorCode = indexItem.colors[0]
            let dateParsed = moment(indexItem.id, "YYYY-MM-DD")
            let isFirstDayOfMonth = dateParsed.date() === 1
            let isLastDayOfMonth = dateParsed.date() === dateParsed.daysInMonth()
            let isSunday = dateParsed.isoWeekday() === 7
            let myRef: RefObject<HTMLLIElement | null> = createRef<HTMLLIElement>()
            listItemRefs[indexItem.id] = myRef
            return <Fragment key={indexItem.id + "1"}>
              {/* Optional heading with the name of month and year */}
              <>{(isFirstDayOfMonth) &&
                <SidenavListItem key={dateParsed.format("MMYYYY")} sx={{borderLeft: 0, borderRight: 0}}>
                  <ListItemText
                    primary={dateParsed.format("MMMM YYYY")}
                    slotProps={{
                      primary: {
                        py: "1.5rem",
                        textTransform: "uppercase",
                        fontWeight: 600,
                        fontFamily: (theme) => theme.typography.fontFamily
                      }
                    }}
                  />
                </SidenavListItem>}</>

              {/* Regular calendar day */}
              <SidenavListItem
                ref={myRef}
                key={indexItem.id}
                disableGutters
                sx={{
                  boxShadow: (isLastDayOfMonth) ? 1 : 0,
                  borderTop: (isSunday) ? "2px solid" : "",
                  borderTopColor: (isSunday) ? "text.disabled" : "",
                  borderLeftWidth: "5px",
                  borderLeftStyle: "solid",
                  borderLeftColor: `vestment${colorCode}.main`
                }}>
                <ListItemButton
                  selected={indexItem.id == selectedItem}
                  component={Link}
                  href={`/${lang}/${indexItem.id}`}
                >
                  <>{indexItem.id === todayFmt &&
                    <ListItemIcon sx={{minWidth: "2.5rem", display: "flex", alignItems: "center"}}><EventIcon
                      sx={{color: "secondary.main"}}/></ListItemIcon>}</>
                  <SidenavListItemText
                    rank={indexItem.rank}
                    prim={indexItem.title}
                    sec={`${dateParsed.format("dd DD.MM")} / 
                  ${RANK_NAMES[lang as Locale][indexItem.rank]}
                  ${(indexItem.commemorations && indexItem.commemorations.length > 0) ? " / " + COMMEMORATION[lang as Locale] + " " + indexItem.commemorations.join(", ") : ""}`}
                  />
                </ListItemButton>
              </SidenavListItem>
            </Fragment>
          }
        )}
        <PrevOrNextYearListItem lang={lang} year={year} isNext={true}/>
      </List>
    </>
  )
}

function PrevOrNextYearListItem({lang, year, isNext}: { lang: string, year: number, isNext: boolean }) {
  const prevYear = year - 1
  const prevYearLastDay = prevYear + "-12-31"
  const nextYear = year + 1
  const nextYearFirstDay = nextYear + "-01-01"
  return (
    <SidenavListItem
      key={isNext ? nextYear : prevYear}
      disableGutters
    >
      <ListItemButton
        component={Link}
        href={`/${lang}/${isNext ? nextYearFirstDay : prevYearLastDay}`}
      >
        <>{!isNext ? <ListItemIcon><ArrowBackIcon sx={{color: "secondary.main"}}/></ListItemIcon> : null}</>
        <SidenavListItemText prim={(isNext ? nextYear : prevYear).toString()}/>
        <>{isNext && <ListItemIcon><ArrowForwardIcon sx={{color: "secondary.main"}}/></ListItemIcon>}</>
      </ListItemButton>
    </SidenavListItem>)
}
