"use client";

import React, {useEffect, useMemo, useRef, useState} from "react";
import {CircularProgress, Dialog, DialogContent, IconButton, InputAdornment, List, ListItemButton, ListItemIcon, ListItemText, TextField, Tooltip, Typography} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import ClearIcon from "@mui/icons-material/Clear";
import {Icon} from "@iconify/react";
import Link from "next/link";
import {buildApiUrl} from "@/components/utils";
import {Locale} from "@/components/intl";

type SearchType = "mass" | "prayer" | "chant" | "supplement" | "ordinary";
type SearchResult = {
  id: string; title: string; tags?: string[]; type: SearchType;
  source: "calendar" | "proper" | "prayer" | "chant" | "supplement" | "ordinary";
  path: string; date?: string; status?: "commemoration" | "displaced";
};

const COPY: Record<Locale, {
  open: string; clear: string; placeholder: string; empty: string; noResults: string;
  shortcut: string;
  types: Record<SearchType, string>; statuses: Record<NonNullable<SearchResult["status"]>, string>;
}> = {
  pl: {
    open: "Otwórz wyszukiwarkę",
    clear: "Wyczyść wyszukiwanie",
    placeholder: "Szukaj mszy, pieśni, modlitw…", empty: "Zacznij pisać, aby wyszukać treści.", noResults: "Brak pasujących wyników.",
    shortcut: "Szukaj (⌘K / Ctrl+K)",
    types: {mass: "Msza", prayer: "Modlitwa", chant: "Pieśń", supplement: "Suplement", ordinary: "Ordo"},
    statuses: {commemoration: "Wspomnienie", displaced: "Obchód pominięty"},
  },
  en: {
    open: "Open search",
    clear: "Clear search",
    placeholder: "Search masses, chants, prayers…", empty: "Start typing to search.", noResults: "No matching results.",
    shortcut: "Search (⌘K / Ctrl+K)",
    types: {mass: "Mass", prayer: "Prayer", chant: "Chant", supplement: "Supplement", ordinary: "Ordinary"},
    statuses: {commemoration: "Commemoration", displaced: "Displaced observance"},
  },
};

const normalise = (value: string) => value.toLocaleLowerCase().replace(/ł/g, "l").normalize("NFD").replace(/[\u0300-\u036f]/g, "");

const currentWeekStart = () => {
  const date = new Date();
  date.setDate(date.getDate() - ((date.getDay() + 6) % 7));
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;
};

const CALENDAR_INDEX_SCHEMA_VERSION = "2";

const shiftMonths = (date: Date, months: number) => {
  const shifted = new Date(date);
  const day = shifted.getDate();
  shifted.setDate(1);
  shifted.setMonth(shifted.getMonth() + months);
  shifted.setDate(Math.min(day, new Date(shifted.getFullYear(), shifted.getMonth() + 1, 0).getDate()));
  return shifted;
};

const iconFor = (result: SearchResult) => {
  if (result.source === "calendar") return "mdi:calendar-month";
  return {proper: "mdi:text-box-outline", prayer: "mdi:hands-pray", chant: "mdi:music-note-sixteenth", supplement: "mdi:book-plus", ordinary: "mdi:text-box-outline"}[result.source];
};

const formatCalendarDate = (date: string, lang: Locale) => new Intl.DateTimeFormat(
  lang, {day: "numeric", month: "long", year: "numeric"},
).format(new Date(`${date}T12:00:00`));

export default function GlobalSearch({lang}: {lang: Locale}) {
  const copy = COPY[lang];
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [index, setIndex] = useState<SearchResult[] | null>(null);
  const [loading, setLoading] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => setIndex(null), [lang]);
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        setOpen(true);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);
  useEffect(() => {
    if (!open || index) return;
    const controller = new AbortController();
    setLoading(true);
    const load = async () => {
      try {
        const [content, calendar] = await Promise.all([
          fetch(buildApiUrl(lang, "search/index"), {signal: controller.signal}),
          fetch(`${buildApiUrl(lang, `search/calendar-index/${currentWeekStart()}`)}?schema=${CALENDAR_INDEX_SCHEMA_VERSION}`, {signal: controller.signal}),
        ]);
        setIndex(content.ok && calendar.ok ? [...(await content.json()), ...(await calendar.json())] : []);
      } catch (error) {
        if ((error as Error).name !== "AbortError") setIndex([]);
      } finally {
        if (!controller.signal.aborted) setLoading(false);
      }
    };
    void load();
    return () => controller.abort();
  }, [index, lang, open]);

  const results = useMemo(() => {
    const normalizedQuery = normalise(query.trim());
    if (!normalizedQuery || !index) return [];
    const today = new Date();
    const windowStart = shiftMonths(today, -1);
    const windowEnd = shiftMonths(today, 12);
    return index.map((result) => {
      const resultDate = result.date ? new Date(`${result.date}T12:00:00`) : null;
      const title = normalise(result.title);
      const tags = normalise((result.tags ?? []).join(" "));
      const dateText = result.date ? normalise(`${formatCalendarDate(result.date, lang)} ${result.date}`) : "";
      const score = title.startsWith(normalizedQuery) ? 0 : title.includes(normalizedQuery) ? 1 : tags.includes(normalizedQuery) ? 2 : dateText.includes(normalizedQuery) ? 3 : 4;
      const dateDistance = resultDate ? Math.abs(resultDate.getTime() - today.getTime()) : Number.MAX_SAFE_INTEGER;
      return {result, score, dateDistance, inDateWindow: !resultDate || (resultDate >= windowStart && resultDate <= windowEnd)};
    }).filter(({score, inDateWindow}) => score < 4 && inDateWindow).sort((a, b) => a.score - b.score || a.dateDistance - b.dateDistance || a.result.title.localeCompare(b.result.title, lang)).slice(0, 30).map(({result}) => result);
  }, [index, lang, query]);

  const close = () => { setOpen(false); setQuery(""); };
  return <>
    <Tooltip title={copy.shortcut}>
      <IconButton aria-label={copy.open} color="inherit" onClick={() => setOpen(true)} sx={{ml: "auto", color: "yellowish.main"}}><SearchIcon /></IconButton>
    </Tooltip>
    <Dialog open={open} onClose={close} fullWidth maxWidth="sm" slotProps={{
      transition: {onEntered: () => inputRef.current?.focus()},
      backdrop: {sx: {backgroundColor: "rgba(0, 0, 0, 0.46)"}},
      paper: {
        sx: {
          border: "1px solid", borderColor: "divider", borderRadius: 2,
          boxShadow: (theme) => theme.palette.mode === "dark"
            ? "0 18px 48px rgba(0, 0, 0, 0.48)"
            : "0 18px 48px rgba(0, 0, 0, 0.22)",
        },
      },
    }}>
      <DialogContent sx={{p: {xs: 2.5, sm: 3}}}>
        <TextField autoFocus fullWidth inputRef={inputRef} value={query} onChange={(event) => setQuery(event.target.value)} placeholder={copy.placeholder} sx={{
          "& .MuiOutlinedInput-root": {
            borderRadius: 1.5,
            "& fieldset": {borderColor: "divider"},
            "&:hover fieldset": {borderColor: "text.secondary"},
            "&.Mui-focused fieldset": {borderColor: "primary.main", borderWidth: 2},
          },
          "& .MuiInputBase-input::placeholder": {color: "text.secondary", opacity: 0.72},
        }} slotProps={{input: {
          startAdornment: <InputAdornment position="start" sx={{color: "text.secondary"}}><SearchIcon /></InputAdornment>,
          endAdornment: query ? <InputAdornment position="end"><IconButton aria-label={copy.clear} edge="end" onClick={() => setQuery("")}><ClearIcon /></IconButton></InputAdornment> : null,
        }}} />
        {loading ? <CircularProgress size={24} sx={{display: "block", mx: "auto", my: 3}} /> : null}
        {!loading && !query.trim() ? <Typography color="text.secondary" sx={{pt: 2, pb: 0.25}}>{copy.empty}</Typography> : null}
        {!loading && query.trim() && !results.length ? <Typography color="text.secondary" sx={{pt: 2, pb: 0.25}}>{copy.noResults}</Typography> : null}
        <List disablePadding sx={{pt: results.length ? 1.25 : 0}}>{results.map((result) => {
          const details: string[] = [copy.types[result.type]];
          if (result.status) details.push(copy.statuses[result.status]);
          if (result.date) details.push(formatCalendarDate(result.date, lang));
          return <ListItemButton component={Link} href={`/${lang}/${result.path}`} prefetch={false} key={`${result.source}-${result.id}`} onClick={close} sx={{px: 1.25, py: 1.1, borderRadius: 1}}>
            <ListItemIcon sx={{color: "text.secondary", minWidth: 44}}><Icon icon={iconFor(result)} width={20} height={20} /></ListItemIcon>
            <ListItemText primary={result.title} secondary={details.join(" · ")} slotProps={{secondary: {sx: {color: "text.secondary", opacity: 0.82}}}} />
          </ListItemButton>;
        })}</List>
      </DialogContent>
    </Dialog>
  </>;
}
