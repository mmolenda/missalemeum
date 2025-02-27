"use client"

import Link from "next/link";
import List from "@mui/material/List";
import {SidenavListItem} from "@/components/styledComponents/SidenavListItem";
import SidenavListItemText from "@/components/styledComponents/SidenavListItemText";
import React, {createRef, Fragment, useEffect, useState} from "react";
import {COMMEMORATION, IN, RANK_NAMES, SEARCH_PLACEHOLDER, SEARCH_SUGGESTIONS_PROPER} from "@/components/intl";
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

export default function ListProper({lang, year, items}) {
  const dateFormat = 'YYYY-MM-DD'
  const todayFmt = moment().format(dateFormat)
  const [itemsFiltered, setItemsFiltered] = useState(items)
  const [filterString, setFilterString] = useState("")
  const [selectedItem, setSelectedItem] = useState("")
  const router = useRouter()
  let listItemRefs = {}

  useEffect(() => {
    setSelectedItem(window.location.hash.substring(1) || todayFmt)
    let listItemRef = listItemRefs[selectedItem]
    if (listItemRef && listItemRef.current) {
      listItemRef.current.scrollIntoView({block: "center", behavior: "auto"})
    }
  })

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

  function ButtonField(props) {
    const {
      setOpen,
      label,
      id,
      disabled,
      InputProps: {ref} = {},
      inputProps: {'aria-label': ariaLabel} = {},
    } = props;

    return (
      <IconButton
        onClick={() => setOpen?.((prev) => !prev)}
      >
        <CalendarMonthIcon/>
      </IconButton>
    )
  }

  const MyDatePicker = (props) => {
    const [open, setOpen] = useState(false);
    let locale = {"en": "", "pl": "pl"}[props.lang]

    const handleDateChange = (newValue) => {
      if (newValue) {
        router.push(`${lang}/${newValue.format(dateFormat)}`);
      }
    };
    return (
      <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale="pl">
        <MobileDatePicker
          slots={{...props.slots, field: ButtonField}}
          slotProps={{...props.slotProps, field: {setOpen} as any}}
          {...props}
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
          options={SEARCH_SUGGESTIONS_PROPER[lang] || []}
          renderInput={(params: AutocompleteRenderInputParams): React.ReactNode => {
            return (<TextField
              {...params}
              label={`${SEARCH_PLACEHOLDER[lang]} ${IN[lang]} ${year}`}
            />)
          }}
        />
        <MyDatePicker lang={lang}/>
      </Box>
      <List>
        <PrevOrNextYearListItem lang={lang} year={year} isNext={false}/>
        {itemsFiltered.map((indexItem) => {
            let colorCode = indexItem.colors[0]
            let dateParsed = moment(indexItem.id, "YYYY-MM-DD")
            let isFirstDayOfMonth = dateParsed.date() === 1
            let isLastDayOfMonth = dateParsed.date() === dateParsed.daysInMonth()
            let isSunday = dateParsed.isoWeekday() === 7
            let myRef = createRef()
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
                  to={{pathname: `/${lang}/${indexItem.id}`, hash: ""}}
                >
                  <>{indexItem.id === todayFmt &&
                    <ListItemIcon sx={{minWidth: "2.5rem", display: "flex", alignItems: "center"}}><EventIcon
                      sx={{color: "secondary.main"}}/></ListItemIcon>}</>
                  <SidenavListItemText
                    rank={indexItem.rank}
                    primary={indexItem.title}
                    secondary={`${dateParsed.format("dd DD.MM")} / 
                  ${RANK_NAMES[lang][indexItem.rank]}
                  ${(indexItem.commemorations && indexItem.commemorations.length > 0) ? " / " + COMMEMORATION[lang] + " " + indexItem.commemorations.join(", ") : ""}`}
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

function PrevOrNextYearListItem({lang, year, isNext}) {
  const prevYear = parseInt(year) - 1
  const prevYearLastDay = prevYear + "-12-31"
  const nextYear = parseInt(year) + 1
  const nextYearFirstDay = nextYear + "-01-01"
  return (
    <SidenavListItem
      key={isNext ? nextYear : prevYear}
      disableGutters
    >
      <ListItemButton
        component={Link}
        to={{pathname: `/${lang}/${isNext ? nextYearFirstDay : prevYearLastDay}`, hash: ""}}
      >
        <>{!isNext ? <ListItemIcon><ArrowBackIcon sx={{color: "secondary.main"}}/></ListItemIcon> : null}</>
        <SidenavListItemText primary={isNext ? nextYear : prevYear}/>
        <>{isNext && <ListItemIcon><ArrowForwardIcon sx={{color: "secondary.main"}}/></ListItemIcon>}</>
      </ListItemButton>
    </SidenavListItem>)
}
