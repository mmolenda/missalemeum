"use client"

import "react-datepicker/dist/react-datepicker.css";
import slugify from "slugify";
import {
  Box,
  Typography,
  ToggleButtonGroup,
  ToggleButton,
  useMediaQuery,
  IconButton,
  Select,
  MenuItem,
  Popover,
  Menu
} from "@mui/material";
import PrintIcon from '@mui/icons-material/Print';
import ShareIcon from '@mui/icons-material/Share';
import {
  MENUITEM_SUPPLEMENT,
  MSG_ADDRESS_COPIED,
  COMMEMORATION,
  Locale,
  PDF_VARIANTS
} from "./intl";
import Md from "./styledComponents/Md";
import MyLink from "./MyLink";
import ArticleTags from "./ArticleTags";
import { buildApiUrl } from "./utils";
import React, {
  Dispatch,
  Fragment,
  SetStateAction,
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState
} from "react";
import Link from "next/link";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import {Body, Content} from "@/components/types";


const xVernacular = 'x-vernacular'
const xLatin = 'x-latin'

export type BilingualContentProps = {
  lang: string
  id: string
  contents: Content[]
  backButtonRef?: string
  singleColumnAsRubric?: boolean
  markdownNewlines?: boolean
  widgetMode?: boolean
  apiEndpoint?: string
}

export default function BilingualContent({
                                           lang,
                                           id,
                                           contents,
                                           backButtonRef = "",
                                           singleColumnAsRubric = false,
                                           markdownNewlines = false,
                                           widgetMode = false,
                                           apiEndpoint
                                         }: BilingualContentProps) {
  const [index, setIndex] = useState(0)
  const [hashIndex, setHashIndex] = useState<number | null>(null)

  useEffect(() => {
    if (typeof window === "undefined") {
      return
    }

    const updateFromHash = () => {
      const hashValue = window.location.hash.substring(1)
      const parsed = Number.parseInt(hashValue, 10)
      const hasValidIndex = !Number.isNaN(parsed) && parsed >= 0 && parsed < contents.length

      if (hasValidIndex) {
        setIndex(parsed)
        if (parsed <= 2) {
          setHashIndex(parsed)
        } else {
          setHashIndex(null)
        }
      } else {
        setIndex(0)
        setHashIndex(null)
      }
    }

    updateFromHash()
    window.addEventListener("hashchange", updateFromHash)

    return () => {
      window.removeEventListener("hashchange", updateFromHash)
    }
  }, [contents.length])

  const backButton = (backButtonRef && <IconButton
    aria-label="back"
    component={Link}
    href={backButtonRef}
    sx={{backgroundColor: "background.default", opacity: 0.9}}
  >
    <ArrowBackIcon/>
  </IconButton>)

  return (
    <Article
      id={id}
      lang={lang}
      contents={contents}
      index={index}
      setIndex={setIndex}
      singleColumnAsRubric={singleColumnAsRubric}
      backButton={backButton}
      markdownNewlines={markdownNewlines}
      widgetMode={widgetMode}
      hashIndex={hashIndex}
      setHashIndex={setHashIndex}
      apiEndpoint={apiEndpoint}
    />
  )
}

const Article = ({
                   lang,
                   id,
                   contents,
                   index,
                   setIndex,
                   markdownNewlines,
                   backButton,
                   widgetMode,
                   singleColumnAsRubric,
                   hashIndex,
                   setHashIndex,
                   apiEndpoint
                 }: {
  lang: string
  id: string
  contents: Content[]
  index: number
  setIndex: Dispatch<SetStateAction<number>>
  setHashIndex: Dispatch<SetStateAction<number | null>>
  backButton: React.ReactNode
  markdownNewlines: boolean
  widgetMode: boolean
  singleColumnAsRubric: boolean
  hashIndex: number | null
  apiEndpoint?: string
}) => {
  const [bilingualLang, setBilingualLang] = useState(xVernacular)
  const sharePopoverOpen = false
  const shareButtonRef = useRef(null)
  const [pdfMenuAnchor, setPdfMenuAnchor] = useState<null | HTMLElement>(null)
  const pdfMenuOpen = Boolean(pdfMenuAnchor)
  const content: Content = contents[index]
  const itemRefs = useRef<Record<string, HTMLElement | null>>({})
  const pdfVariantOptions = useMemo(() => {
    const options = PDF_VARIANTS[lang as Locale] ?? PDF_VARIANTS.en
    if (lang === "en") {
      return options
    }
    return options.filter((option) => !option.variant.startsWith("letter"))
  }, [lang])
  const hasPdfDownload = Boolean(apiEndpoint)

  const buildPdfUrl = useCallback((variant: string) => {
    if (!apiEndpoint) {
      return null
    }
    const apiUrl = buildApiUrl(lang, apiEndpoint, id)
    const questionMarkIndex = apiUrl.indexOf("?")
    const path = questionMarkIndex === -1 ? apiUrl : apiUrl.slice(0, questionMarkIndex)
    const existingQuery = questionMarkIndex === -1 ? "" : apiUrl.slice(questionMarkIndex + 1)

    const cleanedVariant = variant.startsWith("?") ? variant.slice(1) : variant
    const params = new URLSearchParams(existingQuery)
    params.set("format", "pdf")
    params.set("variant", cleanedVariant)
    if (hashIndex !== null) {
      params.set("index", String(hashIndex))
    } else {
      params.delete("index")
    }

    const query = params.toString()
    return query ? `${path}?${query}` : path
  }, [apiEndpoint, hashIndex, lang, id])

  const handlePdfMenuOpen = useCallback((event: React.MouseEvent<HTMLElement>) => {
    setPdfMenuAnchor(event.currentTarget)
  }, [])

  const handlePdfMenuClose = useCallback(() => {
    setPdfMenuAnchor(null)
  }, [])

  const registerItemRef = useCallback((slug: string | null) => (element: HTMLElement | null) => {
    if (!slug) {
      return
    }

    if (element) {
      itemRefs.current[slug] = element
    } else {
      delete itemRefs.current[slug]
    }
  }, [])

  const scrollToListItem = useCallback((itemId: string) => {
    if (!itemId) {
      window.scrollTo({top: 0})
      return
    }

    const itemElement = itemRefs.current[itemId]
    if (itemElement) {
      itemElement.scrollIntoView({block: "center", behavior: "auto"})
    } else {
      window.scrollTo({top: 0})
    }
  }, [])

  useEffect(() => {
    scrollToListItem(window.location.hash.substring(1))
  }, [scrollToListItem])

  const isBilingual = () => {
    for (const section of content.sections) {
      for (const bodyItem of section.body) {
        if (bodyItem.length > 1) {
          return true
        }
      }
    }
    return false
  }

  const share = () => {
    const title = document.title
    const url = document.location.href
    try {
      navigator.share({
        title,
        url
      })
    } catch {
      navigator.clipboard.writeText(url).then(function () {
      }, function (err) {
        alert(`Couldn't copy address: ${err}`);
      });
    }
  }
  return (
    <>
      <Box sx={{
        position: "fixed",
        top: (theme) => {
          // we just need the value of theme.components?.MuiAppBar?.styleOverrides?.root.height
          // all the code below is to appease typescript linter
          const root = theme.components?.MuiAppBar?.styleOverrides?.root;
          const height = root && typeof root === 'object' && 'height' in root ? root.height : "0px";
          return height as string;
        }
      }}
      >
        {backButton}
      </Box>
      {!widgetMode && <Box sx={{display: "flex", justifyContent: "flex-end"}}>
        <IconButton aria-label="share" ref={shareButtonRef} onClick={() => share()}>
          <ShareIcon/>
          <Popover
            open={sharePopoverOpen}
            anchorEl={shareButtonRef.current}
            anchorOrigin={{
              vertical: 'bottom',
              horizontal: 'left',
            }}
          >
            <Typography sx={{p: 2}}>{MSG_ADDRESS_COPIED[lang as Locale]}</Typography>
          </Popover>
        </IconButton>
        {hasPdfDownload && (
          <>
            <IconButton
              aria-label="download pdf"
              aria-controls={pdfMenuOpen ? "pdf-variant-menu" : undefined}
              aria-haspopup="true"
              aria-expanded={pdfMenuOpen ? "true" : undefined}
              onClick={handlePdfMenuOpen}
            >
              <PrintIcon/>
            </IconButton>
            <Menu
              id="pdf-variant-menu"
              anchorEl={pdfMenuAnchor}
              open={pdfMenuOpen}
              onClose={handlePdfMenuClose}
              anchorOrigin={{
                vertical: "bottom",
                horizontal: "right",
              }}
              transformOrigin={{
                vertical: "top",
                horizontal: "right",
              }}
            >
              {pdfVariantOptions.map(({label, variant}) => {
                const downloadHref = buildPdfUrl(variant)
                return (
                  <MenuItem
                    key={variant}
                    component="a"
                    href={downloadHref ?? "#"}
                    onClick={handlePdfMenuClose}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {label}
                  </MenuItem>
                )
              })}
            </Menu>
          </>
        )}
      </Box>}
      <Box sx={{px: "0.75rem"}}>
        <>{contents.length > 1 ?
          <Select
            value={index}
            defaultValue={index}
            onChange={(e) => {
              const nextIndex = Number(e.target.value)
              setIndex(nextIndex)
              if (nextIndex >= 0 && nextIndex <= 2) {
                setHashIndex(nextIndex)
              } else {
                setHashIndex(null)
              }
              window.location.hash = `#${nextIndex}`;
            }}
            sx={{
              fontSize: (theme) => theme.typography.h2.fontSize,
              fontWeight: (theme) => theme.typography.h2.fontWeight,
              color: (theme) => theme.typography.h2.color
            }}
          >
            {contents.map((content, xindex) => {
              return <MenuItem key={xindex} value={xindex}>{content.info.title}</MenuItem>
            })}
          </Select> :
          <Typography variant="h2">
            {content.info.title}
          </Typography>
        }</>
        {content.info.commemorations && content.info.commemorations.length > 0 && <Typography
          variant="h3">{COMMEMORATION[lang as Locale]}{" "}{content.info.commemorations.join(", ")}</Typography>}
        <Box sx={{padding: "0.5rem"}}>
          <ArticleTags info={content.info} lang={lang} showIcon/>
        </Box>
        <>{content.info.description &&
          <Typography component="div" variant="body1" align="justify" sx={{padding: "0.5rem", hyphens: "auto"}}>
            <Md text={content.info.description} markdownNewlines={markdownNewlines}
                widgetMode={widgetMode}/>
          </Typography>}</>
        {content.info.supplements && content.info.supplements.length > 0 &&
          <Typography variant="body1" align="justify" sx={{padding: "0.5rem"}}>
            {`${MENUITEM_SUPPLEMENT[lang as Locale]}: `}
            {content.info.supplements.map((supplement, index) => {
              return (<Fragment key={index}>
                <MyLink href={`${supplement.path}?ref=${id}`} text={supplement.label}
                        widgetMode={widgetMode}/>
                {index + 1 < content.info.supplements.length && ", "}
              </Fragment>)
            })}
          </Typography>}

        <Box sx={{display: "grid"}}>
          {content.sections.map((section, index) => {
            return <BilingualSection
              key={"section-" + index}
              titleVernacular={section.label}
              titleLatin={section.id}
              body={section.body}
              singleColumnAsRubric={singleColumnAsRubric}
              bilingualLang={bilingualLang}
              markdownNewlines={markdownNewlines}
              widgetMode={widgetMode}
              registerItemRef={registerItemRef}
            />
          })}
        </Box>
      </Box>
      {isBilingual() && <BilingualSelector lang={lang} bilingualLang={bilingualLang}
                                           setBilingualLang={setBilingualLang}/>}
    </>
  )
}


const BilingualSection = ({
                            titleVernacular,
                            titleLatin,
                            body,
                            singleColumnAsRubric,
                            bilingualLang,
                            markdownNewlines,
                            widgetMode,
                            registerItemRef
                          }: {
  titleVernacular: string
  titleLatin: string
  body: Body
  singleColumnAsRubric: boolean
  bilingualLang: string
  markdownNewlines: boolean
  widgetMode: boolean
  registerItemRef: (slug: string | null) => (element: HTMLElement | null) => void
}) => {
  const isSmallScreen = useMediaQuery((theme) => theme.breakpoints.down('sm'));
  const formatBody = () => {
    const paragraphs = [];
    for (const row of body) {
      const singleColumn = row.length === 1
      for (const [index, col] of row.entries()) {
        let bilingualLangClass = ""
        if (!singleColumn) {
          bilingualLangClass = (index === 0) ? xVernacular : xLatin
        }
        paragraphs.push({text: col, singleColumn: singleColumn, bilingualLangClass: bilingualLangClass})
      }
    }
    return paragraphs;
  }

  const showHeading = (headingLang: string) => {
    if (isSmallScreen) {
      if (headingLang === xLatin && !titleLatin) {
        return false
      }
      if (headingLang === xVernacular && !titleLatin) {
        return true
      }
      if (headingLang !== bilingualLang) {
        return false;
      }
    }
    return true
  }

  const titleVernacularSlug = slugify(titleVernacular) || null
  const itemRef = useMemo(() => registerItemRef(titleVernacularSlug), [registerItemRef, titleVernacularSlug])

  return (
    <Box ref={itemRef} sx={{
      display: isSmallScreen ? "block" : "inline-grid",
      gridTemplateColumns: isSmallScreen ? "unset" : "repeat(2, 1fr)"
    }}>
      <Typography
        variant="h4"
        className={xVernacular}
        sx={{
          display: (showHeading(xVernacular)) ? "block" : "none",
          px: "0.5rem",
          pt: "1rem"
        }}
      >
        {titleVernacular}
      </Typography>
      <Typography
        variant="h4"
        className={xLatin}
        sx={{
          display: (showHeading(xLatin)) ? "block" : "none",
          px: "0.5rem",
          pt: "1rem"
        }}
      >
        {titleLatin}
      </Typography>
      <>{formatBody().map((paragraph, index) => (
        <BilingualSectionParagraph
          key={index}
          text={paragraph.text}
          singleColumn={paragraph.singleColumn}
          singleColumnAsRubric={singleColumnAsRubric}
          bilingualLang={bilingualLang}
          bilingualLangClass={paragraph.bilingualLangClass}
          markdownNewlines={markdownNewlines}
          widgetMode={widgetMode}
        />
      ))}</>
    </Box>
  )
}

const BilingualSectionParagraph = ({
                                     text,
                                     singleColumn,
                                     singleColumnAsRubric,
                                     bilingualLang,
                                     bilingualLangClass,
                                     markdownNewlines,
                                     widgetMode
                                   }: {
  text: string
  singleColumn: boolean
  singleColumnAsRubric: boolean
  bilingualLang: string
  bilingualLangClass: string
  markdownNewlines: boolean
  widgetMode: boolean
}) => {
  const show = (!(useMediaQuery((theme) => theme.breakpoints.down('sm')) && bilingualLangClass !== bilingualLang) || singleColumn);
  return (
    <Typography
      component="div"
      variant="body1"
      className={bilingualLangClass}
      align="justify"
      sx={{
        display: (show) ? "block" : "none",
        gridColumn: (singleColumn) ? "1 / span 2" : "unset",
        color: (singleColumn && singleColumnAsRubric) ? "secondary.main" : "text.primary",
        padding: "0.5rem",
        hyphens: "auto"
      }}
    >
      <Md text={text} markdownNewlines={markdownNewlines} widgetMode={widgetMode}/>
    </Typography>
  )
}

const BilingualSelector = ({lang, bilingualLang, setBilingualLang}: {
  lang: string
  bilingualLang: string,
  setBilingualLang: Dispatch<SetStateAction<string>>
}) => {
  const handleChange = (
    event: React.MouseEvent<HTMLElement>,
    newBilingualLang: string | null
  ) => {
    if (newBilingualLang !== null) {
      setBilingualLang(newBilingualLang);
    }
  }
  return (
    <ToggleButtonGroup
      sx={{
        display: {xs: 'block', sm: 'none'},
        position: "fixed",
        right: "20px",
        bottom: "20px",
        opacity: 0.9,
        backgroundColor: "background.default"
      }}
      color="secondary"
      value={bilingualLang}
      exclusive
      onChange={handleChange}
    >
      <ToggleButton value={xVernacular}>{lang.toUpperCase()}</ToggleButton>
      <ToggleButton value={xLatin}>LAT</ToggleButton>
    </ToggleButtonGroup>
  )
}
