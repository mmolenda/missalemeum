"use client"

import Link from "next/link";
import List from "@mui/material/List";
import {SidenavListItem} from "@/components/styledComponents/SidenavListItem";
import SidenavListItemText from "@/components/styledComponents/SidenavListItemText";
import {ContainerMedium} from "@/components/styledComponents/ContainerMedium";
import {Fragment, useEffect, useRef, useState} from "react";
import {COMMEMORATION, RANK_NAMES, SEARCH_PLACEHOLDER, SEARCH_SUGGESTIONS_PROPER} from "@/components/intl";
import moment from "moment";
import {Autocomplete, Box, ListItemButton, ListItemIcon, TextField, IconButton, Button} from "@mui/material";
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

export default function ListProper({lang, items}) {
  const dateFormat = 'YYYY-MM-DD'
  const yearFormat = 'YYYY'
  let today = moment()
  let todayFmt = today.format(dateFormat)
  let selectedDay = today
  let currentYear = parseInt(selectedDay.format(yearFormat))
  let prevYear = currentYear ? currentYear - 1 : null
  let prevYearLastDay = prevYear ? prevYear + "-12-31" : null
  let nextYear = currentYear ? currentYear + 1 : null
  let nextYearFirstDay = nextYear ? nextYear + "-01-01" : null
  const [itemsFiltered, setItemsFiltered] = useState(items)
  const [filterString, setFilterString] = useState("")
  const router = useRouter()

  const formatDate = (dateParsed) => {
    if (lang === "pl") {
      return dateParsed.format("dd DD.MM")
    }
    return dateParsed.format("dd DD.MM")
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
    const handleDateChange = (newValue) => {
      if (newValue) {
        const formattedDate = newValue.format("YYYY-MM-DD");
        router.push(`${lang}/${formattedDate}`);
      }
    };

    const [open, setOpen] = useState(false);
    let locale = {"en": "", "pl": "pl"}[props.lang]
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
    <ContainerMedium disableGutters sx={{display: 'flex', overflow: 'hidden', height: "100%"}}>
      <Box

        id="content"
        sx={{
          overflowY: 'scroll',
          width: '100%',
          ml: 0,
          pt: (theme) => `${parseInt(theme.components.MuiAppBar.styleOverrides.root.height) * 2}px`,
          height: "100%"
        }}>


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
            renderInput={(params) => (
              <TextField
                {...params}
                label={SEARCH_PLACEHOLDER[lang]}
              />
            )}
          />
          <MyDatePicker lang={lang}/>
        </Box>
        <Box

        >

          <List>
            {/* Link to previous year */}
            {prevYear &&
              <SidenavListItem
                key={prevYear}
                disableGutters
              >
                <ListItemButton
                  component={Link}
                  to={{pathname: `/${lang}/${prevYearLastDay}`, hash: ""}}
                >
                  <ListItemIcon sx={{minWidth: "2.5rem"}}><ArrowBackIcon sx={{color: "secondary.main"}}/></ListItemIcon>
                  <SidenavListItemText primary={prevYear}/>
                </ListItemButton>
              </SidenavListItem>
            }

            {/* Days in current year */}
            {itemsFiltered.map((indexItem) => {
                let colorCode = indexItem.colors[0]
                let dateParsed = moment(indexItem.id, "YYYY-MM-DD")
                let isFirstDayOfMonth = dateParsed.date() === 1
                let isLastDayOfMonth = dateParsed.date() === dateParsed.daysInMonth()
                let isSunday = dateParsed.isoWeekday() === 7;
                return <Fragment key={indexItem.id + "1"}>
                  {/* Optional heading with the name of month and year */}
                  {(isFirstDayOfMonth) &&
                    <SidenavListItem key={dateParsed.format("MMYYYY")} sx={{borderLeft: 0, borderRight: 0}}>
                      <ListItemText
                        primary={dateParsed.format("MMMM YYYY")}
                        primaryTypographyProps={{
                          py: "1.5rem",
                          textTransform: "uppercase",
                          fontWeight: 600,
                          fontFamily: (theme) => theme.typography.fontFamily
                        }}
                      />
                    </SidenavListItem>}

                  {/* Regular calendar day */}
                  <SidenavListItem
                    key={indexItem.id}
                    disableGutters
                    sx={{
                      boxShadow: (isLastDayOfMonth) ? 1 : 0,
                      borderTop: (isSunday) ? "2px solid" : "",
                      borderTopColor: (isSunday) ? "text.disabled" : "",
                      borderLeftWidth: "5px",
                      borderLeftStyle: "solid",
                      borderLeftColor: `vestment${colorCode}.main`,
                    }}>
                    <ListItemButton
                      component={Link}
                      to={{pathname: `/${lang}/${indexItem.id}`, hash: ""}}
                    >
                      {indexItem.id === todayFmt &&
                        <ListItemIcon sx={{minWidth: "2.5rem", display: "flex", alignItems: "center"}}><EventIcon
                          sx={{color: "secondary.main"}}/></ListItemIcon>}
                      <SidenavListItemText
                        rank={indexItem.rank}
                        primary={indexItem.title}
                        secondary={`${formatDate(dateParsed)} / 
                  ${RANK_NAMES[lang][indexItem.rank]}
                  ${(indexItem.commemorations && indexItem.commemorations.length > 0) ? " / " + COMMEMORATION[lang] + " " + indexItem.commemorations.join(", ") : ""}`}
                      />
                    </ListItemButton>
                  </SidenavListItem>
                </Fragment>
              }
            )}

            {/* Link to the next year */}
            {nextYear &&
              <SidenavListItem
                key={nextYear}
                disableGutters
              >
                <ListItemButton
                  component={Link}
                  to={{pathname: `/${lang}/${nextYearFirstDay}`, hash: ""}}
                >
                  <SidenavListItemText primary={nextYear}/>
                  <ListItemIcon><ArrowForwardIcon sx={{color: "secondary.main"}}/></ListItemIcon>
                </ListItemButton>
              </SidenavListItem>
            }
          </List>
        </Box>
      </Box>
    </ContainerMedium>

  )
}