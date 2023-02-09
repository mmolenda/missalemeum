import React, {createRef, useEffect} from 'react';
import ContainerWithSidenav from "./ContainerWithSidenav";
import moment from "moment";
import {Link as RouterLink, useNavigate, useParams} from "react-router-dom";
import DatePicker, {registerLocale} from "react-datepicker";
import List from "@mui/material/List";
import {IconButton, ListItemButton, ListItemIcon} from "@mui/material";
import CalendarMonthIcon from '@mui/icons-material/CalendarMonth';
import {SidenavListItem} from "./styledComponents/SidenavListItem";
import pl from "date-fns/locale/pl";
import EventIcon from '@mui/icons-material/Event';
import SidenavListItemText from "./styledComponents/SidenavListItemText";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import ListItemText from "@mui/material/ListItemText";
import SkeletonSidenav from "./SkeletonSidenav";

registerLocale("pl", pl)
const dateFormat = 'YYYY-MM-DD'
const yearFormat = 'YYYY'

export default function Proper() {
  const {lang} = useParams()
  const getContentUrl = 'api/v5/proper'
  const getSidenavItemsUrl = 'api/v5/calendar'
  const path = '/'
  const init = ((id, internalLang, internalYear, sidenavItems, getSidenavItems, getContent, setSidenavHidden) => {
    setSidenavHidden(Boolean(id))
    let initialDate = moment(id)
    let initialYear = parseInt(initialDate.format(yearFormat))
    if (!sidenavItems || (Boolean(id) && initialYear !== internalYear) || lang !== internalLang) {
      getSidenavItems(initialYear)
    }
    getContent(id)
  })

  return (
    <ContainerWithSidenav
      init={init}
      getContentUrl={getContentUrl}
      getSidenavItemsUrl={getSidenavItemsUrl}
      sidenav={<Sidenav/>}
      extraTools={<MyDatePicker/>}
      sidenavPath={path}
      singleColumnAsRubric
    />
  )
}

const Sidenav = (props) => {
  let today = moment()
  let todayFmt = today.format(dateFormat)
  let listItemRefs = {}
  const scrollToListItem = (id) => {
    let key = id ? id : todayFmt
    let listItemRef = listItemRefs[key]
    if (listItemRefs) {
      for (let listItemRef of Object.values(listItemRefs)) {
        listItemRef.current.classList.remove("sidenavItemActive")
      }
    }
    if (listItemRef) {
      listItemRef.current.classList.add("sidenavItemActive")
      listItemRef.current.scrollIntoView({block: "center"})
    }
  }

  useEffect(() => {
    scrollToListItem(props.internalId)
  })

  const formatDateAndTempora = (dateParsed, tags) => {
    let bits = []
    if (props.lang === "pl") {
      if (tags.length > 0) {
        bits.push(dateParsed.format("DD MMMM,"))
        bits.push(tags[0][0].toLowerCase() + tags[0].substring(1))
      } else {
        bits.push(dateParsed.format("DD MMMM, dddd"))
      }
      return bits.join(" ")
    } else {
      bits = [dateParsed.format("dd, DD MMM"), ...tags]
      return bits.join(" / ")
    }
  }

  if (props.items === null) {
    return <SkeletonSidenav />
  } else {
    let selectedDay = props.internalId ? moment(props.internalId) : today
    let currentYear = parseInt(selectedDay.format(yearFormat))
    let prevYear = currentYear ? currentYear - 1 : null
    let prevYearLastDay = prevYear ? prevYear + "-12-31" : null
    let nextYear = currentYear ? currentYear + 1 : null
    let nextYearFirstDay = nextYear ? nextYear + "-01-01" : null
    moment.locale(props.lang)
    return (
      <List>
        {/* Link to previous year */}
        {prevYear &&
          <SidenavListItem
            key={prevYear}
            disableGutters
          >
            <ListItemButton
              component={RouterLink}
              to={{pathname: `/${props.lang}/${prevYearLastDay}`, hash: ""}}
            >
              <ListItemIcon sx={{minWidth: "2.5rem"}}><ArrowBackIcon sx={{color: "secondary.main"}}/></ListItemIcon>
              <SidenavListItemText primary={prevYear} />
            </ListItemButton>
          </SidenavListItem>
        }

        {/* Days in current year */}
        {props.items.map((indexItem) => {
          let listItemRef = createRef()
          let colorCode = indexItem.colors[0]
          let dateParsed = moment(indexItem.id, "YYYY-MM-DD")
          let isFirstDayOfMonth = dateParsed.date() === 1
          let isLastDayOfMonth = dateParsed.date() === dateParsed.daysInMonth()
          let isSunday = dateParsed.isoWeekday() === 7;
          listItemRefs[indexItem.id] = listItemRef
          return <React.Fragment key={indexItem.id + "1"}>
            {/* Optional heading with the name of month and year */}
            {(isFirstDayOfMonth) && <SidenavListItem key={dateParsed.format("MMYYYY")} sx={{borderLeft: 0, borderRight: 0}}>
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
              ref={listItemRef}
              disableGutters
              sx={{
                  boxShadow: (isLastDayOfMonth) ? 1 : 0,
                  borderTop: (isSunday) ? "2px solid" : "",
                  borderTopColor: (isSunday) ? "text.disabled": "",
                  borderLeftWidth: "5px",
                  borderLeftStyle: "solid",
                  borderLeftColor: `vestment${colorCode}.main`,
              }}>
              <ListItemButton
                component={RouterLink}
                to={{pathname: `/${props.lang}/${indexItem.id}`, hash: ""}}
                onClick={() => {props.setSidenavHidden(true)}}
              >
                { indexItem.id === todayFmt && <ListItemIcon sx={{minWidth: "2.5rem", display: "flex", alignItems: "center"}}><EventIcon sx={{color: "secondary.main"}}/></ListItemIcon> }
                <SidenavListItemText
                  primary={indexItem.title}
                  secondary={formatDateAndTempora(dateParsed, indexItem.tags)}
                />
              </ListItemButton>
            </SidenavListItem>
          </React.Fragment>
          }
        )}

        {/* Link to the next year */}
        {nextYear &&
          <SidenavListItem
            key={nextYear}
            disableGutters
          >
            <ListItemButton
              component={RouterLink}
              to={{pathname: `/${props.lang}/${nextYearFirstDay}`, hash: ""}}
            >
              <SidenavListItemText primary={nextYear} />
              <ListItemIcon><ArrowForwardIcon sx={{color: "secondary.main"}}/></ListItemIcon>
            </ListItemButton>
          </SidenavListItem>
        }
      </List>
    )
  }
}

const MyDatePicker = (props) => {
  const navigate = useNavigate()
  let locale = {"en": "", "pl": "pl"}[props.lang]
  return (
    <DatePicker
      dateFormat={"yyyy-MM-dd"}
      locale={locale}
      selected={new Date()}
      onChange={(date) => navigate(`/${props.lang}/${moment(date).format(dateFormat)}`)}
      customInput={
        <IconButton>
          <CalendarMonthIcon />
        </IconButton>
      }
    />
  )
}


