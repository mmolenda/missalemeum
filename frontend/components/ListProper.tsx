"use client"

import Link from "next/link";
import List from "@mui/material/List";
import {SidenavListItem} from "@/components/styledComponents/SidenavListItem";
import SidenavListItemText from "@/components/styledComponents/SidenavListItemText";
import React, {createRef, Dispatch, Fragment, RefObject, SetStateAction, useEffect, useRef, useState} from "react";
import {
  COMMEMORATION,
  IN,
  Locale,
  MUI_DATEPICKER_LOCALE_TEXT,
  RANK_NAMES,
  SEARCH_PLACEHOLDER,
  SEARCH_SUGGESTIONS_PROPER
} from "@/components/intl";
import moment, {Moment} from "moment";
import {
  Autocomplete,
  Box,
  ListItemButton,
  ListItemIcon,
  TextField,
  IconButton,
  AutocompleteRenderInputParams, lighten, darken, PaletteColor
} from "@mui/material";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import ListItemText from "@mui/material/ListItemText";
import EventIcon from '@mui/icons-material/Event';
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import CalendarMonthIcon from '@mui/icons-material/CalendarMonth';
import "react-datepicker/dist/react-datepicker.css";
import {LocalizationProvider, MobileDatePicker, PickersDay} from "@mui/x-date-pickers";
import {AdapterMoment} from "@mui/x-date-pickers/AdapterMoment";
import "moment/locale/pl";
import {useRouter} from "next/navigation";
import {ListItemType} from "@/components/types";
import {myLocalStorage} from "@/components/myLocalStorage";
import {
  BANNER_HEIGHT,
  BANNER_STORAGE_KEY,
  getAppBarHeightFromTheme,
  isBannerExpired
} from "@/components/layoutMetrics";

export default function ListProper({
                                     lang,
                                     year,
                                     items,
                                     basePath,
                                   }: {
  lang: string
  year: number
  items: ListItemType[]
  basePath?: string
}) {
  const resolvedBasePath = basePath ?? `/${lang}/calendar`;
  const dateFormat = 'YYYY-MM-DD'
  const todayFmt = moment().format(dateFormat)
  const [itemsFiltered, setItemsFiltered] = useState(items)
  const [filterString, setFilterString] = useState("")
  const [selectedItem, setSelectedItem] = useState("")
  const [hasMounted, setHasMounted] = useState(false)
  const router = useRouter()
  const listItemRefs = useRef<Record<string, RefObject<HTMLLIElement | null>>>({})

  useEffect(() => {
    const hashValue = window.location.hash.substring(1)
    setSelectedItem(hashValue || todayFmt)
    setHasMounted(true)
  }, [todayFmt])

  useEffect(() => {
    const listItemRef = listItemRefs.current[selectedItem]
    if (listItemRef && listItemRef.current) {
      listItemRef.current.scrollIntoView({block: "center", behavior: "auto"})
    }
  }, [itemsFiltered, listItemRefs, selectedItem])

  listItemRefs.current = {}

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

  interface ButtonFieldProps {
    setOpen?: Dispatch<SetStateAction<boolean>>;
  }

  function ButtonField({setOpen}: ButtonFieldProps) {
    return (
      <IconButton
        aria-label="calendar"
        onClick={() => setOpen?.((prev) => !prev)}
      >
        <CalendarMonthIcon/>
      </IconButton>
    )
  }

  const MyDatePicker = () => {
    const [open, setOpen] = useState(false);
    type DatesPropertiesFormat = Record<string, { color: string; rank: number }>;
    const datesProperties: DatesPropertiesFormat = items.reduce((acc, item) => {
      acc[item.id] = {color: item.colors[0], rank: item.rank};
      return acc;
    }, {} as DatesPropertiesFormat);

    const handleDateChange = (newValue: Moment | null) => {
      if (newValue) {
        router.push(`${resolvedBasePath}/${newValue.format(dateFormat)}`);
      }
    }

    // Grab the real prop type from the component…
    type PickersDayAllProps = React.ComponentProps<typeof PickersDay>;

    // …then override `day` to be a Moment instance (adapter must match this)
    type CustomDayProps = Omit<PickersDayAllProps, "day"> & { day: Moment };

    const CustomDay = ({ day, ...rest }: CustomDayProps) => {
      const dateProperties = datesProperties[day.format(dateFormat)];
      const color = dateProperties ? `vestment${dateProperties.color}` : "vestmentw";
      const rank = dateProperties ? dateProperties.rank : 4;

      return (
        <PickersDay
          {...rest}
          day={day}
          sx={{
            fontWeight: rank < 2 ? 800 : 400,
            backgroundColor: (theme) => {
              const paletteColor =
                theme.palette[color as keyof typeof theme.palette] as PaletteColor;
              return theme.palette.mode === "light"
                ? lighten(paletteColor.main, 0.5)
                : darken(paletteColor.main, 0.65);
            },
          }}
        />
      );
    };
    
    type MDPProps = React.ComponentProps<typeof MobileDatePicker>;
    type FieldSlotProps = NonNullable<MDPProps["slotProps"]> extends { field?: infer F } ? F : never;

    return (
      <LocalizationProvider dateAdapter={AdapterMoment} adapterLocale={lang}
                            localeText={MUI_DATEPICKER_LOCALE_TEXT[lang as Locale]}>
        <MobileDatePicker
          value={moment(selectedItem || todayFmt, dateFormat)}
          slots={{
            field: ButtonField,
            day: CustomDay
          }}
          slotProps={
            {field: (({ setOpen } as ButtonFieldProps) as unknown as FieldSlotProps)}
          }
          open={open}
          onClose={() => setOpen(false)}
          onOpen={() => setOpen(true)}
          onChange={handleDateChange}
        />
      </LocalizationProvider>
    )
  }

  const bannerDismissed = hasMounted && myLocalStorage.getItem(BANNER_STORAGE_KEY) === "true";
  const bannerExpired = isBannerExpired();

  return (
    <>
      <Box sx={{
        position: "fixed",
        display: "flex",
        top: (theme) => {
          const appBarHeight = getAppBarHeightFromTheme(theme);
          const offset = (bannerDismissed || bannerExpired) ? 0 : BANNER_HEIGHT;
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
        <PrevOrNextYearListItem basePath={resolvedBasePath} year={year} isNext={false}/>
        {itemsFiltered.map((indexItem) => {
            const colorCode = indexItem.colors[0]
            const dateParsed = moment(indexItem.id, "YYYY-MM-DD")
            const isFirstDayOfMonth = dateParsed.date() === 1
            const isLastDayOfMonth = dateParsed.date() === dateParsed.daysInMonth()
            const isSunday = dateParsed.isoWeekday() === 7
            const myRef: RefObject<HTMLLIElement | null> = createRef<HTMLLIElement>()
            listItemRefs.current[indexItem.id] = myRef
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
                  href={`${resolvedBasePath}/${indexItem.id}`}
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
        <PrevOrNextYearListItem basePath={resolvedBasePath} year={year} isNext={true}/>
      </List>
    </>
  )
}

function PrevOrNextYearListItem({basePath, year, isNext}: { basePath: string, year: number, isNext: boolean }) {
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
        href={`${basePath}/${isNext ? nextYearFirstDay : prevYearLastDay}`}
      >
        <>{!isNext ? <ListItemIcon><ArrowBackIcon sx={{color: "secondary.main"}}/></ListItemIcon> : null}</>
        <SidenavListItemText prim={(isNext ? nextYear : prevYear).toString()}/>
        <>{isNext && <ListItemIcon><ArrowForwardIcon sx={{color: "secondary.main"}}/></ListItemIcon>}</>
      </ListItemButton>
    </SidenavListItem>)
}
