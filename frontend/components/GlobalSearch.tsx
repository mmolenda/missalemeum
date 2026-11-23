"use client";

import React, {useEffect, useId, useMemo, useRef, useState} from "react";
import {Button, CircularProgress, Dialog, DialogContent, DialogTitle, IconButton, InputAdornment, List, ListItemButton, ListItemIcon, ListItemText, TextField, Tooltip, Typography} from "@mui/material";
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
  shortcut: string; title: string; close: string; loading: string; error: string; retry: string;
  resultCount: (count: number) => string;
  types: Record<SearchType, string>; statuses: Record<NonNullable<SearchResult["status"]>, string>;
}> = {
  pl: {
    open: "Otwórz wyszukiwarkę",
    clear: "Wyczyść wyszukiwanie",
    placeholder: "Szukaj mszy, pieśni, modlitw…", empty: "Zacznij pisać, aby wyszukać treści.", noResults: "Brak pasujących wyników.",
    shortcut: "Szukaj (⌘K / Ctrl+K)",
    title: "Szukaj", close: "Zamknij wyszukiwarkę", loading: "Wczytywanie wyszukiwarki…",
    error: "Nie udało się wczytać wyszukiwarki. Sprawdź połączenie i spróbuj ponownie.", retry: "Spróbuj ponownie",
    resultCount: (count) => `Liczba wyników: ${count}`,
    types: {mass: "Msza", prayer: "Modlitwa", chant: "Pieśń", supplement: "Suplement", ordinary: "Ordo"},
    statuses: {commemoration: "Wspomnienie", displaced: "Obchód pominięty"},
  },
  en: {
    open: "Open search",
    clear: "Clear search",
    placeholder: "Search masses, chants, prayers…", empty: "Start typing to search.", noResults: "No matching results.",
    shortcut: "Search (⌘K / Ctrl+K)",
    title: "Search", close: "Close search", loading: "Loading search…",
    error: "Could not load search. Check your connection and try again.", retry: "Try again",
    resultCount: (count) => `Results: ${count}`,
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

export default function GlobalSearch({lang}: {lang: Locale}) {
  const copy = COPY[lang];
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [index, setIndex] = useState<SearchResult[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [loadFailed, setLoadFailed] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const titleId = useId();
  const dateFormatter = useMemo(() => new Intl.DateTimeFormat(lang, {
    day: "numeric", month: "long", year: "numeric",
  }), [lang]);

  useEffect(() => { setIndex(null); setLoadFailed(false); }, [lang]);
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
    if (!open || index || loadFailed) return;
    const controller = new AbortController();
    setLoading(true);
    const load = async () => {
      try {
        const [content, calendar] = await Promise.all([
          fetch(buildApiUrl(lang, "search/index"), {signal: controller.signal}),
          fetch(`${buildApiUrl(lang, `search/calendar-index/${currentWeekStart()}`)}?schema=${CALENDAR_INDEX_SCHEMA_VERSION}`, {signal: controller.signal}),
        ]);
        if (!content.ok || !calendar.ok) throw new Error("Search index request failed");
        const entries = [...(await content.json()), ...(await calendar.json())];
        if (!controller.signal.aborted) setIndex(entries);
      } catch (error) {
        if (!controller.signal.aborted && (error as Error).name !== "AbortError") setLoadFailed(true);
      } finally {
        if (!controller.signal.aborted) setLoading(false);
      }
    };
    void load();
    return () => controller.abort();
  }, [index, lang, loadFailed, open]);

  const searchIndex = useMemo(() => (index ?? []).map(result => {
    const date = result.date ? new Date(`${result.date}T12:00:00`) : null;
    const formattedDate = date ? dateFormatter.format(date) : "";
    return {result, date, formattedDate, title: normalise(result.title),
      tags: normalise((result.tags ?? []).join(" ")),
      dateText: normalise(`${formattedDate} ${result.date ?? ""}`)};
  }), [dateFormatter, index]);

  const results = useMemo(() => {
    const normalizedQuery = normalise(query.trim());
    if (!normalizedQuery || !index) return [];
    const today = new Date();
    const windowStart = shiftMonths(today, -1);
    const windowEnd = shiftMonths(today, 12);
    return searchIndex.map(({result, date: resultDate, title, tags, dateText}) => {
      const score = title.startsWith(normalizedQuery) ? 0 : title.includes(normalizedQuery) ? 1 : tags.includes(normalizedQuery) ? 2 : dateText.includes(normalizedQuery) ? 3 : 4;
      const dateDistance = resultDate ? Math.abs(resultDate.getTime() - today.getTime()) : Number.MAX_SAFE_INTEGER;
      return {result, score, dateDistance, inDateWindow: !resultDate || (resultDate >= windowStart && resultDate <= windowEnd)};
    }).filter(({score, inDateWindow}) => score < 4 && inDateWindow).sort((a, b) => a.score - b.score || a.dateDistance - b.dateDistance || a.result.title.localeCompare(b.result.title, lang)).slice(0, 30).map(({result}) => result);
  }, [index, lang, query, searchIndex]);

  const close = () => { setOpen(false); setQuery(""); };
  return <>
    <Tooltip title={copy.shortcut}>
      <IconButton aria-label={copy.open} color="inherit" onClick={() => setOpen(true)} sx={{ml: "auto", color: "yellowish.main"}}><SearchIcon /></IconButton>
    </Tooltip>
    <Dialog open={open} onClose={close} aria-labelledby={titleId} fullWidth maxWidth="sm" slotProps={{
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
      <DialogTitle id={titleId} sx={{display: "flex", alignItems: "center", justifyContent: "space-between"}}>
        {copy.title}
        <IconButton aria-label={copy.close} onClick={close}><ClearIcon /></IconButton>
      </DialogTitle>
      <DialogContent sx={{p: {xs: 2.5, sm: 3}}}>
        <TextField autoFocus fullWidth inputRef={inputRef} value={query} onChange={(event) => setQuery(event.target.value)} placeholder={copy.placeholder} sx={{
          "& .MuiOutlinedInput-root": {
            borderRadius: 1.5,
            "& fieldset": {borderColor: "divider"},
            "&:hover fieldset": {borderColor: "text.secondary"},
            "&.Mui-focused fieldset": {borderColor: "primary.main", borderWidth: 2},
          },
          "& .MuiInputBase-input::placeholder": {color: "text.secondary", opacity: 0.72},
        }} slotProps={{htmlInput: {"aria-label": copy.placeholder}, input: {
          startAdornment: <InputAdornment position="start" sx={{color: "text.secondary"}}><SearchIcon /></InputAdornment>,
          endAdornment: query ? <InputAdornment position="end"><IconButton aria-label={copy.clear} edge="end" onClick={() => setQuery("")}><ClearIcon /></IconButton></InputAdornment> : null,
        }}} />
        {loading ? <CircularProgress aria-label={copy.loading} size={24} sx={{display: "block", mx: "auto", my: 3}} /> : null}
        {loadFailed && <>
          <Typography role="alert" color="error" sx={{pt: 2}}>{copy.error}</Typography>
          <Button onClick={() => setLoadFailed(false)}>{copy.retry}</Button>
        </>}
        <Typography role="status" aria-live="polite" aria-atomic="true" color="text.secondary" sx={{pt: 2, pb: 0.25}}>
          {loading ? copy.loading : loadFailed ? "" : !query.trim() ? copy.empty : results.length ? copy.resultCount(results.length) : copy.noResults}
        </Typography>
        <List disablePadding sx={{pt: results.length ? 1.25 : 0}}>{results.map((result) => {
          const details: string[] = [copy.types[result.type]];
          if (result.status) details.push(copy.statuses[result.status]);
          if (result.date) details.push(dateFormatter.format(new Date(`${result.date}T12:00:00`)));
          return <ListItemButton component={Link} href={`/${lang}/${result.path}`} prefetch={false} key={`${result.source}-${result.id}`} onClick={close} sx={{px: 1.25, py: 1.1, borderRadius: 1}}>
            <ListItemIcon sx={{color: "text.secondary", minWidth: 44}}><Icon icon={iconFor(result)} width={20} height={20} /></ListItemIcon>
            <ListItemText primary={result.title} secondary={details.join(" · ")} slotProps={{secondary: {sx: {color: "text.secondary", opacity: 0.82}}}} />
          </ListItemButton>;
        })}</List>
      </DialogContent>
    </Dialog>
  </>;
}
