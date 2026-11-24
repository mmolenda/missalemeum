"use client"

import Link from "next/link";
import List from "@mui/material/List";
import {CalendarSurface} from "@/components/calendarStyles";
import {ListControls, ListSearchPaper} from "@/components/listStyles";
import React, {
  createRef,
  Dispatch,
  RefObject,
  SetStateAction,
  useCallback,
  useEffect,
  useLayoutEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import {
  CALENDAR_BUTTON_TOOLTIP,
  COMMEMORATION,
  FIRST_FRIDAY,
  FIRST_SATURDAY,
  IN,
  Locale,
  MUI_DATEPICKER_LOCALE_TEXT,
  RANK_NAMES,
  SEARCH_PLACEHOLDER,
  SEARCH_SUGGESTIONS_PROPER,
  TODAY,
  TODAY_BUTTON_TOOLTIP,
} from "@/components/intl";
import moment, {Moment} from "moment";
import {
  Autocomplete,
  AutocompleteRenderInputParams,
  Box,
  IconButton,
  ListItemButton,
  PaletteColor,
  TextField,
  Tooltip,
  darken,
  lighten,
} from "@mui/material";
import ListItem from "@mui/material/ListItem";
import SearchIcon from "@mui/icons-material/Search";
import InputAdornment from "@mui/material/InputAdornment";
import EventIcon from "@mui/icons-material/Event";
import CalendarMonthIcon from "@mui/icons-material/CalendarMonth";
import "react-datepicker/dist/react-datepicker.css";
import {LocalizationProvider, MobileDatePicker, PickersDay} from "@mui/x-date-pickers";
import {AdapterMoment} from "@mui/x-date-pickers/AdapterMoment";
import "moment/locale/pl";
import {useRouter} from "next/navigation";
import {ListItemType} from "@/components/types";
import {callApi} from "@/components/utils";
import {useMeasuredHeight} from "@/components/useMeasuredHeight";
import { PdfDownloadMenu } from "@/components/pdfDownload";

const DATE_FORMAT = "YYYY-MM-DD";
const CHUNK_SIZE = 10;

const getObservanceTitle = (observance: string | { title?: string }) =>
  typeof observance === "string" ? observance : (observance.title ?? "");

type SearchOption =
  | { kind: "suggestion"; label: string }
  | { kind: "day"; item: ListItemType };

const sortItemsByDate = (list: ListItemType[]): ListItemType[] =>
  [...list].sort((a, b) => a.id.localeCompare(b.id));

const buildItemsMap = (list: ListItemType[]): Record<string, ListItemType> =>
  list.reduce((acc, item) => {
    acc[item.id] = item;
    return acc;
  }, {} as Record<string, ListItemType>);

export default function ListProper({
  lang,
  year,
  items,
  basePath,
}: {
  lang: string;
  year: number;
  items: ListItemType[];
  basePath?: string;
}) {
  const resolvedBasePath = basePath ?? `/${lang}/calendar`;
  const todayFmt = moment().format(DATE_FORMAT);
  const calendarTooltipLabel = CALENDAR_BUTTON_TOOLTIP[lang as Locale];
  const todayTooltipLabel = TODAY_BUTTON_TOOLTIP[lang as Locale];

  const sortedInitialItems = useMemo(() => sortItemsByDate(items), [items]);
  const initialItemsMap = useMemo(() => buildItemsMap(sortedInitialItems), [sortedInitialItems]);
  const initialIds = useMemo(() => sortedInitialItems.map((item) => item.id), [sortedInitialItems]);

  const [itemsById, setItemsById] = useState<Record<string, ListItemType>>(() => initialItemsMap);
  const [sortedIds, setSortedIds] = useState<string[]>(() => initialIds);
  const [visibleIds, setVisibleIds] = useState<string[]>(() => initialIds);
  const [yearStatus, setYearStatus] = useState<Record<number, "partial" | "full">>({ [year]: "partial" });
  const [searchInput, setSearchInput] = useState("");
  const [searchResults, setSearchResults] = useState<ListItemType[]>([]);
  const [selectedItem, setSelectedItem] = useState("");
  const [hasMounted, setHasMounted] = useState(false);
  const [currentYear, setCurrentYear] = useState(year);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [isDatePickerOpen, setIsDatePickerOpen] = useState(false);
  const pdfResourceId = useMemo(() => String(currentYear), [currentYear]);

  const router = useRouter();
  const controlsRef = useRef<HTMLDivElement>(null);
  useMeasuredHeight(controlsRef, "--list-controls-height");

  const listItemRefs = useRef<Record<string, RefObject<HTMLLIElement | null>>>({});
  const topSentinelRef = useRef<HTMLDivElement | null>(null);
  const bottomSentinelRef = useRef<HTMLDivElement | null>(null);
  const scrollFrameRef = useRef<number | null>(null);
  const shouldScrollToSelectedRef = useRef(false);
  const prependAnchorRef = useRef<{id: string; top: number} | null>(null);
  const pendingExtendRef = useRef<"forward" | "backward" | null>(null);
  const loadingDirectionRef = useRef<{ forward: boolean; backward: boolean }>({ forward: false, backward: false });
  const fetchingYearsRef = useRef(new Set<number>());

  const itemsByIdRef = useRef<Record<string, ListItemType>>(initialItemsMap);
  const sortedIdsRef = useRef<string[]>(initialIds);
  const visibleIdsRef = useRef<string[]>(initialIds);

  useEffect(() => {
    itemsByIdRef.current = itemsById;
  }, [itemsById]);

  useEffect(() => {
    sortedIdsRef.current = sortedIds;
  }, [sortedIds]);

  useEffect(() => {
    visibleIdsRef.current = visibleIds;
  }, [visibleIds]);

  const visibleItems = useMemo(
    () => visibleIds.map((id) => itemsById[id]).filter((item): item is ListItemType => Boolean(item)),
    [visibleIds, itemsById],
  );

  const yearItemsCache = useMemo(() => {
    const grouped: Record<number, ListItemType[]> = {};
    Object.values(itemsById).forEach((item) => {
      const itemYear = Number(item.id.slice(0, 4));
      if (Number.isNaN(itemYear)) {
        return;
      }
      if (!grouped[itemYear]) {
        grouped[itemYear] = [];
      }
      grouped[itemYear].push(item);
    });
    Object.keys(grouped).forEach((key) => {
      const numericYear = Number(key);
      grouped[numericYear] = grouped[numericYear].sort((a, b) => a.id.localeCompare(b.id));
    });
    return grouped;
  }, [itemsById]);

  const resetFromProps = useCallback(
    (nextItems: ListItemType[], nextYear: number) => {
      const sorted = sortItemsByDate(nextItems);
      const ids = sorted.map((item) => item.id);
      const currentIds = sortedIdsRef.current;
      const sameIds =
        currentIds.length === ids.length && currentIds.every((id, index) => id === ids[index]);
      if (sameIds) {
        setYearStatus((prev) => (prev[nextYear] ? prev : { ...prev, [nextYear]: prev[nextYear] ?? "partial" }));
        return;
      }
      const map = buildItemsMap(sorted);
      itemsByIdRef.current = map;
      sortedIdsRef.current = ids;
      visibleIdsRef.current = ids;
      fetchingYearsRef.current.clear();
      pendingExtendRef.current = null;
      prependAnchorRef.current = null;
      loadingDirectionRef.current = { forward: false, backward: false };
      setItemsById(map);
      setSortedIds(ids);
      setVisibleIds(ids);
      setYearStatus({ [nextYear]: "partial" });
      setCurrentYear(nextYear);
      setSearchInput("");
      setSearchResults([]);
    },
    [],
  );

  useEffect(() => {
    resetFromProps(items, year);
  }, [items, year, resetFromProps]);

  const updateItemsStore = useCallback((newItems: ListItemType[]) => {
    if (!newItems.length) {
      return;
    }
    const mergedMap = { ...itemsByIdRef.current };
    let changed = false;
    newItems.forEach((item) => {
      if (!mergedMap[item.id]) {
        mergedMap[item.id] = item;
        changed = true;
      }
    });
    if (!changed) {
      return;
    }
    const mergedSorted = new Set(sortedIdsRef.current);
    newItems.forEach((item) => mergedSorted.add(item.id));
    const nextSorted = Array.from(mergedSorted).sort();
    itemsByIdRef.current = mergedMap;
    sortedIdsRef.current = nextSorted;
    setItemsById(mergedMap);
    setSortedIds(nextSorted);
  }, []);

  const fetchYear = useCallback(
    async (targetYear: number) => {
      if (fetchingYearsRef.current.has(targetYear)) {
        return;
      }
      fetchingYearsRef.current.add(targetYear);
      setYearStatus((prev) => ({ ...prev, [targetYear]: prev[targetYear] ?? "partial" }));
      try {
        const response = await callApi(lang, "calendar", targetYear.toString());
        if (!response.ok) {
          throw new Error(`Failed to fetch calendar for year ${targetYear}`);
        }
        const data: ListItemType[] = await response.json();
        updateItemsStore(data);
        setYearStatus((prev) => ({ ...prev, [targetYear]: "full" }));
      } catch (error) {
        console.error(error);
      } finally {
        fetchingYearsRef.current.delete(targetYear);
      }
    },
    [lang, updateItemsStore],
  );

  const ensureDateAvailable = useCallback(
    async (targetDate: Moment) => {
      const id = targetDate.format(DATE_FORMAT);
      if (itemsByIdRef.current[id]) {
        return;
      }
      const targetYear = targetDate.year();
      await fetchYear(targetYear);
    },
    [fetchYear],
  );

  const extendVisible = useCallback((direction: "forward" | "backward") => {
    const sorted = sortedIdsRef.current;
    if (!sorted.length) {
      return false;
    }
    const currentVisible = visibleIdsRef.current;
    if (!currentVisible.length) {
      return false;
    }
    if (direction === "forward") {
      const lastId = currentVisible[currentVisible.length - 1];
      const lastIndex = sorted.indexOf(lastId);
      if (lastIndex === -1) {
        return false;
      }
      const nextIds = sorted.slice(lastIndex + 1, lastIndex + 1 + CHUNK_SIZE);
      if (!nextIds.length) {
        return false;
      }
      const updated = [...currentVisible, ...nextIds];
      visibleIdsRef.current = updated;
      setVisibleIds(updated);
      return true;
    }
    const firstId = currentVisible[0];
    const firstIndex = sorted.indexOf(firstId);
    if (firstIndex === -1) {
      return false;
    }
    const startIndex = Math.max(0, firstIndex - CHUNK_SIZE);
    const previousIds = sorted.slice(startIndex, firstIndex);
    if (!previousIds.length) {
      return false;
    }
    const anchor = listItemRefs.current[firstId]?.current;
    if (anchor) {
      prependAnchorRef.current = {id: firstId, top: anchor.getBoundingClientRect().top};
    }
    const updated = [...previousIds, ...currentVisible];
    visibleIdsRef.current = updated;
    setVisibleIds(updated);
    return true;
  }, []);

  const ensureItemVisible = useCallback((targetId: string) => {
    const sorted = sortedIdsRef.current;
    const index = sorted.indexOf(targetId);
    if (index === -1) {
      return false;
    }
    const halfWindow = Math.floor(CHUNK_SIZE / 2);
    const start = Math.max(0, index - halfWindow);
    const end = Math.min(sorted.length - 1, index + halfWindow);
    const nextIds = sorted.slice(start, end + 1);
    prependAnchorRef.current = null;
    visibleIdsRef.current = nextIds;
    setVisibleIds(nextIds);
    return true;
  }, []);

  const handleLoadMore = useCallback(
    async (direction: "forward" | "backward") => {
      if (!hasMounted) {
        return;
      }
      if (loadingDirectionRef.current[direction]) {
        return;
      }
      const currentVisible = visibleIdsRef.current;
      if (!currentVisible.length) {
        return;
      }
      loadingDirectionRef.current[direction] = true;
      try {
        const referenceId =
          direction === "forward" ? currentVisible[currentVisible.length - 1] : currentVisible[0];
        const referenceMoment = moment(referenceId, DATE_FORMAT);
        const targetMoment =
          direction === "forward"
            ? referenceMoment.clone().add(1, "day")
            : referenceMoment.clone().subtract(1, "day");
        await ensureDateAvailable(targetMoment);
        const extended = extendVisible(direction);
        if (!extended) {
          pendingExtendRef.current = direction;
        }
      } finally {
        loadingDirectionRef.current[direction] = false;
      }
    },
    [ensureDateAvailable, extendVisible, hasMounted],
  );

  useEffect(() => {
    const direction = pendingExtendRef.current;
    if (!direction) {
      return;
    }
    const extended = extendVisible(direction);
    if (extended) {
      pendingExtendRef.current = null;
    } else {
      pendingExtendRef.current = null;
    }
  }, [sortedIds, extendVisible]);

  // Re-observe after each batch: a short batch at a year boundary may leave
  // the sentinel inside rootMargin, without another intersection transition.
  useEffect(() => {
    if (!hasMounted) {
      return;
    }
    const options: IntersectionObserverInit = {
      root: null,
      rootMargin: "300px 0px",
      threshold: 0.01,
    };
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) {
          return;
        }
        if (entry.target === bottomSentinelRef.current) {
          void handleLoadMore("forward");
        } else if (entry.target === topSentinelRef.current) {
          void handleLoadMore("backward");
        }
      });
    }, options);

    const bottom = bottomSentinelRef.current;
    const top = topSentinelRef.current;

    if (bottom) {
      observer.observe(bottom);
    }
    if (top) {
      observer.observe(top);
    }

    return () => {
      if (bottom) {
        observer.unobserve(bottom);
      }
      if (top) {
        observer.unobserve(top);
      }
      observer.disconnect();
    };
  }, [handleLoadMore, hasMounted, visibleIds]);

  const updateCurrentYear = useCallback(() => {
    const middle = window.innerHeight / 2;
    let closestId: string | null = null;
    let closestDistance = Number.POSITIVE_INFINITY;

    Object.entries(listItemRefs.current).forEach(([id, ref]) => {
      const element = ref.current;
      if (!element) {
        return;
      }
      const rect = element.getBoundingClientRect();
      const elementMiddle = rect.top + rect.height / 2;
      const distance = Math.abs(elementMiddle - middle);
      if (distance < closestDistance) {
        closestDistance = distance;
        closestId = id;
      }
    });

    if (!closestId) {
      return;
    }
    const idForYear: string = closestId;
    const detectedYear = Number(idForYear.slice(0, 4));
    if (Number.isNaN(detectedYear)) {
      return;
    }
    setCurrentYear((prev) => (prev === detectedYear ? prev : detectedYear));
  }, []);

  useEffect(() => {
    const handleScroll = () => {
      if (scrollFrameRef.current !== null) {
        return;
      }
      scrollFrameRef.current = window.requestAnimationFrame(() => {
        scrollFrameRef.current = null;
        updateCurrentYear();
      });
    };
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => {
      window.removeEventListener("scroll", handleScroll);
      if (scrollFrameRef.current !== null) {
        window.cancelAnimationFrame(scrollFrameRef.current);
      }
    };
  }, [updateCurrentYear]);

  useEffect(() => {
    updateCurrentYear();
  }, [visibleItems, updateCurrentYear]);

  useEffect(() => {
    const hashValue = window.location.hash.substring(1);
    setSelectedItem(hashValue || todayFmt);
    shouldScrollToSelectedRef.current = true;
    setHasMounted(true);
  }, [todayFmt]);

  // Keep the same row at the same screen position when earlier dates are inserted.
  // Measuring the row (rather than scrollHeight) also handles month labels and wrapping.
  useLayoutEffect(() => {
    const anchor = prependAnchorRef.current;
    prependAnchorRef.current = null;
    if (!anchor || shouldScrollToSelectedRef.current) return;
    const element = listItemRefs.current[anchor.id]?.current;
    if (element) {
      window.scrollBy({top: element.getBoundingClientRect().top - anchor.top, behavior: "instant"});
    }
  }, [visibleItems]);

  useLayoutEffect(() => {
    if (!selectedItem) {
      return;
    }
    if (!shouldScrollToSelectedRef.current) {
      return;
    }
    const listItemRef = listItemRefs.current[selectedItem];
    if (listItemRef?.current) {
      const rect = listItemRef.current.getBoundingClientRect();
      const controlsBottom = controlsRef.current?.getBoundingClientRect().bottom ?? 0;
      const targetTop = controlsBottom + Math.max(16, (window.innerHeight - controlsBottom - rect.height) / 2);
      window.scrollBy({top: rect.top - targetTop, behavior: "instant"});
      shouldScrollToSelectedRef.current = false;
    }
  }, [visibleItems, selectedItem]);

  useEffect(() => {
    const trimmed = searchInput.trim();
    if (trimmed.length < 2) {
      setSearchResults([]);
      return;
    }
    const searchSpace = yearItemsCache[currentYear] ?? [];
    const query = trimmed.toLowerCase();
    const matches: ListItemType[] = [];
    for (const item of searchSpace) {
      const searchBody = JSON.stringify(item).toLowerCase();
      if (searchBody.includes(query)) {
        matches.push(item);
        if (matches.length >= 20) {
          break;
        }
      }
    }
    setSearchResults(matches);
  }, [searchInput, currentYear, yearItemsCache]);

  const handleSearchFocus = useCallback(() => {
    if (yearStatus[currentYear] !== "full") {
      void fetchYear(currentYear);
    }
    setIsSearchOpen(true);
  }, [currentYear, fetchYear, yearStatus]);

  const handleSearchSelection = useCallback(
    async (item: ListItemType) => {
      const targetMoment = moment(item.id, DATE_FORMAT);
      await ensureDateAvailable(targetMoment);
      ensureItemVisible(item.id);
      shouldScrollToSelectedRef.current = true;
      setSelectedItem(item.id);
      setSearchInput("");
      setSearchResults([]);
      setIsSearchOpen(false);
      router.push(`${resolvedBasePath}/${item.id}`);
    },
    [ensureDateAvailable, ensureItemVisible, resolvedBasePath, router],
  );

  const autocompleteSuggestions = useMemo<SearchOption[]>(() => {
    const suggestions = SEARCH_SUGGESTIONS_PROPER[lang as Locale] || [];
    return suggestions.map((label) => ({ kind: "suggestion", label }));
  }, [lang]);

  const autocompleteOptions: SearchOption[] =
    searchInput.trim().length >= 2
      ? searchResults.map((item) => ({ kind: "day", item }))
      : autocompleteSuggestions;

  interface ButtonFieldProps {
    setOpen?: Dispatch<SetStateAction<boolean>>;
  }

  function ButtonField({ setOpen }: ButtonFieldProps) {
    return (
      <Tooltip title={calendarTooltipLabel}>
        <IconButton
          aria-label={calendarTooltipLabel}
          onClick={() => {
            if (isDatePickerOpen) {
              setIsDatePickerOpen(false);
              setOpen?.(false);
              return;
            }
            handleDatePickerOpen();
            setOpen?.(true);
          }}
        >
          <CalendarMonthIcon/>
        </IconButton>
      </Tooltip>
    );
  }

  type DatesPropertiesFormat = Record<string, { color: string; rank: number }>;
  const datesProperties = useMemo<DatesPropertiesFormat>(() => {
    return Object.values(itemsById).reduce((acc, item) => {
      acc[item.id] = { color: item.colors[0], rank: item.rank };
      return acc;
    }, {} as DatesPropertiesFormat);
  }, [itemsById]);

  const ensureCurrentYearLoaded = useCallback(() => {
    if (yearStatus[currentYear] !== "full") {
      void fetchYear(currentYear);
    }
  }, [currentYear, fetchYear, yearStatus]);

  const handleDatePickerOpen = useCallback(() => {
    setIsDatePickerOpen(true);
    ensureCurrentYearLoaded();
  }, [ensureCurrentYearLoaded]);

  const handleDateChange = useCallback((newValue: Moment | null) => {
    if (newValue) {
      setIsDatePickerOpen(false);
      router.push(`${resolvedBasePath}/${newValue.format(DATE_FORMAT)}`);
    }
  }, [resolvedBasePath, router]);

  const handleTodayClick = useCallback(async () => {
    const todayMoment = moment(todayFmt, DATE_FORMAT);
    await ensureDateAvailable(todayMoment);
    ensureItemVisible(todayFmt);
    shouldScrollToSelectedRef.current = true;
    setSelectedItem(todayFmt);
    setIsDatePickerOpen(false);
    setIsSearchOpen(false);
  }, [ensureDateAvailable, ensureItemVisible, todayFmt]);

  type PickersDayAllProps = React.ComponentProps<typeof PickersDay>;
  type CustomDayProps = Omit<PickersDayAllProps, "day"> & { day: Moment };

  const CustomDay = ({ day, ...rest }: CustomDayProps) => {
    const dateProperties = datesProperties[day.format(DATE_FORMAT)];
    if (!dateProperties) {
      return <PickersDay {...rest} day={day}/>;
    }
    const color = `vestment${dateProperties.color}`;
    const rank = dateProperties.rank;

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

  return (
    <CalendarSurface>
      <ListControls ref={controlsRef} className="list-controls calendar-controls">
        <Autocomplete<SearchOption, false, false, true>
          slots={{paper: ListSearchPaper}}
          size="small"
          sx={{flex: 1, minWidth: 0, mr: {xs: 0.5, sm: "auto"}, maxWidth: {sm: 400}}}
          freeSolo
          value={null}
          options={autocompleteOptions}
          filterOptions={(optionList) => optionList}
          inputValue={searchInput}
          open={isSearchOpen}
          onOpen={() => setIsSearchOpen(true)}
          onClose={(_, reason) => {
            if (reason === "selectOption") {
              return;
            }
            setIsSearchOpen(false);
          }}
          onInputChange={(event, newInputValue, reason) => {
            if (reason === "reset") {
              return;
            }
            setSearchInput(newInputValue);
            if (reason === "input" || reason === "clear") {
              setIsSearchOpen(true);
            }
          }}
          onChange={(_event, newValue) => {
            if (!newValue) {
              return;
            }
            if (typeof newValue === "string") {
              const match = searchResults.find(
                (item) => item.title.toLowerCase() === newValue.toLowerCase(),
              );
              if (match) {
                void handleSearchSelection(match);
              }
              return;
            }
            if (newValue.kind === "suggestion") {
              setSearchInput(newValue.label);
              setIsSearchOpen(true);
              return;
            }
            void handleSearchSelection(newValue.item);
          }}
          getOptionLabel={(option) => {
            if (typeof option === "string") {
              return option;
            }
            if (option.kind === "suggestion") {
              return option.label;
            }
            const dateText = moment(option.item.id, DATE_FORMAT).format("DD MMM YYYY");
            return `${dateText} – ${option.item.title}`;
          }}
          renderOption={(props, option) => {
            const {key, ...optionProps} = props;
            if (option.kind === "day") {
              const dateText = moment(option.item.id, DATE_FORMAT).format("DD MMM YYYY");
              return (
                <li key={key} {...optionProps}>
                  <Box component="span" sx={{ fontWeight: 600, mr: 1 }}>{dateText}</Box>
                  {option.item.title}
                </li>
              );
            }
            return (
              <li key={key} {...optionProps}>{option.label}</li>
            );
          }}
          renderInput={(params: AutocompleteRenderInputParams) => (
            <TextField
              key={`search-input-${currentYear}`}
              {...params}
              onFocus={handleSearchFocus}
              placeholder={`${SEARCH_PLACEHOLDER[lang as Locale]} ${IN[lang as Locale]} ${currentYear}`}
              slotProps={{
                htmlInput: {...params.inputProps, "aria-label": `${SEARCH_PLACEHOLDER[lang as Locale]} ${IN[lang as Locale]} ${currentYear}`},
                input: {...params.InputProps, startAdornment: <InputAdornment position="start"><SearchIcon sx={{color: "var(--list-muted)"}} /></InputAdornment>},
              }}
            />
          )}
        />
        <LocalizationProvider
          dateAdapter={AdapterMoment}
          adapterLocale={lang}
          localeText={MUI_DATEPICKER_LOCALE_TEXT[lang as Locale]}
        >
          <MobileDatePicker
            value={moment(selectedItem || todayFmt, DATE_FORMAT)}
            open={isDatePickerOpen}
            onOpen={handleDatePickerOpen}
            onClose={() => setIsDatePickerOpen(false)}
            onChange={handleDateChange}
            slots={{
              field: ButtonField,
              day: CustomDay,
            }}
          />
        </LocalizationProvider>
        <Tooltip title={todayTooltipLabel}>
          <IconButton
            aria-label={todayTooltipLabel}
            onClick={() => {
              void handleTodayClick();
            }}
          >
            <EventIcon/>
          </IconButton>
        </Tooltip>
        <PdfDownloadMenu
          lang={lang}
          apiEndpoint="calendar"
          resourceId={pdfResourceId}
        />
      </ListControls>
      <List className="list-index calendar-list" aria-label={lang === "pl" ? "Kalendarz liturgiczny" : "Liturgical calendar"}>
        <Box component="li" ref={topSentinelRef} sx={{ listStyle: "none", height: "1px", p: 0, m: 0 }}/>
        {visibleItems.map((indexItem) => {
          const dateParsed = moment(indexItem.id, DATE_FORMAT).locale(lang);
          const isMonthStart = dateParsed.date() === 1;
          const weekday = dateParsed.isoWeekday();
          const isSunday = weekday === 7;
          const isFirstFriday = weekday === 5 && dateParsed.date() <= 7;
          const isFirstSaturday = weekday === 6 && dateParsed.date() <= 7;
          const isToday = indexItem.id === todayFmt;
          const myRef = listItemRefs.current[indexItem.id] ?? createRef<HTMLLIElement>();
          listItemRefs.current[indexItem.id] = myRef;
          return (
            <ListItem
              key={indexItem.id}
              ref={myRef}
              data-date={indexItem.id}
              disableGutters
              className={[
                "list-item calendar-day",
                isSunday || indexItem.rank === 1 ? "calendar-important" : "",
                !isSunday && indexItem.rank === 4 ? "calendar-feria" : "",
                isSunday ? "calendar-week-start" : "",
              ].filter(Boolean).join(" ")}
            >
              {isMonthStart && (
                <Box component="span" className="calendar-month">{dateParsed.format("MMMM YYYY")}</Box>
              )}
              <ListItemButton
                className="list-link calendar-day-link"
                selected={indexItem.id === selectedItem}
                component={Link}
                href={`${resolvedBasePath}/${indexItem.id}`}
                aria-current={isToday ? "date" : undefined}
                style={{"--day-color": `var(--vestment-${indexItem.colors[0]})`} as React.CSSProperties}
              >
                <Box component="h3" className="list-title calendar-title">{indexItem.title}</Box>
                <Box className="calendar-meta">
                  <Box component="time" dateTime={indexItem.id} className="calendar-date">
                    {dateParsed.format("dddd, D MMMM")}
                  </Box>
                  <Box component="span" className="calendar-rank">{RANK_NAMES[lang as Locale][indexItem.rank]}</Box>
                  {isToday && <Box component="span" className="calendar-today">{TODAY[lang as Locale]}</Box>}
                  {(isFirstFriday || isFirstSaturday) && (
                    <Box component="span" className="calendar-first-weekday">
                      {isFirstFriday ? FIRST_FRIDAY[lang as Locale] : FIRST_SATURDAY[lang as Locale]}
                    </Box>
                  )}
                </Box>
                {indexItem.commemorations?.length > 0 && (
                  <Box className="calendar-commemorations">
                    <Box component="span" className="calendar-commemoration-label">{COMMEMORATION[lang as Locale]}</Box>{" "}
                    {indexItem.commemorations.map(getObservanceTitle).join(", ")}
                  </Box>
                )}
              </ListItemButton>
            </ListItem>
          );
        })}
        <Box component="li" ref={bottomSentinelRef} sx={{ listStyle: "none", height: "1px", p: 0, m: 0 }}/>
      </List>
    </CalendarSurface>
  );
}
