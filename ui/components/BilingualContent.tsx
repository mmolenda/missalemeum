"use client"

import ReactDOMServer from 'react-dom/server';
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
  MenuItem, Popover
} from "@mui/material";
import PrintIcon from '@mui/icons-material/Print';
import ShareIcon from '@mui/icons-material/Share';
import {
  MENUITEM_SUPPLEMENT, MSG_ADDRESS_COPIED, COMMEMORATION, Locale
} from "./intl";
import SkeletonContent from "./SkeletonContent";
import Md from "./styledComponents/Md";
import MdPrintable from "./styledComponents/MdPrintable";
import MyLink from "./MyLink";
import ArticleTags from "./ArticleTags";
import React, {createRef, Dispatch, Fragment, SetStateAction, useEffect, useRef, useState} from "react";
import Link from "next/link";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import {Body, Content} from "@/components/types";


const xVernacular = 'x-vernacular'
const xLatin = 'x-latin'

export default function BilingualContent({
                                           lang,
                                           id,
                                           contents,
                                           backButtonRef = "",
                                           singleColumnAsRubric = false,
                                           markdownNewlines = false,
                                           widgetMode = false
                                         }:
                                           {
                                             lang: string,
                                             id: string,
                                             contents: Content[],
                                             backButtonRef?: string,
                                             singleColumnAsRubric?: boolean,
                                             markdownNewlines?: boolean,
                                             widgetMode?: boolean
                                           }) {
  const [index, setIndex] = useState(0)

  useEffect(() => {
    let hashValue = window.location.hash.substring(1)
    setIndex(parseInt(hashValue) || 0)
  })

  let backButton = (backButtonRef && <IconButton
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
                   singleColumnAsRubric
                 }: {
  lang: string
  id: string
  contents: Content[]
  index: number
  setIndex: Dispatch<SetStateAction<number>>
  backButton: React.ReactNode
  markdownNewlines: boolean
  widgetMode: boolean
  singleColumnAsRubric: boolean
}) => {
  const [bilingualLang, setBilingualLang] = useState(xVernacular)
  const [sharePopoverOpen, setSharePopoverOpen] = useState(false)
  let shareButtonRef = useRef(null)
  let content: Content = contents[index]
  const itemRefs: Record<string, React.RefObject<HTMLElement>> = {};
  useEffect(() => {
    scrollToListItem(window.location.hash.substring(1))
  }, [])

  const scrollToListItem = (itemId: string) => {
    let itemRef = itemRefs[itemId]
    if (itemRef && itemRef.current) {
      itemRef.current.scrollIntoView({block: "center", behavior: "auto"})
    } else {
      window.scrollTo({top: 0});
    }
  }

  const isBilingual = () => {
    for (let section of content.sections) {
      for (let bodyItem of section.body) {
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
    } catch (err) {
      navigator.clipboard.writeText(url).then(function () {
      }, function (err) {
        alert(`Couldn't copy address: ${err}`);
      });
    }
  }

  const print = () => {
    let newWindow = window.open('', '', "width=650, height=750");
    let newContent = (
      <html>
      <body style={{margin: "4%", minWidth: "300px"}}>
      <h1>{content.info.title}</h1>
      <ArticleTags info={content.info} lang={lang} showIcon={false}/>
      {content.info.description &&
        <MdPrintable text={content.info.description} markdownNewlines={markdownNewlines}/>}
      {content.sections.map((section) => {
        return <div>
          {section.label && <h2>{section.label}</h2>}
          {section.body.map((paragraph) => {
            return (paragraph.length === 1) ?
              <div>
                <div><MdPrintable text={paragraph[0]} markdownNewlines={markdownNewlines}/></div>
              </div> :
              <div style={{display: "inline-grid", gridTemplateColumns: "50% 50%"}}>
                <div style={{marginRight: "5%"}}><MdPrintable text={paragraph[0]}
                                                              markdownNewlines={markdownNewlines}/></div>
                <div><MdPrintable text={paragraph[1]} markdownNewlines={markdownNewlines}/></div>
              </div>
          })}
        </div>
      })}
      <p><em>https://www.missalemeum.com</em></p>
      </body>
      </html>)
    newWindow && newWindow.document.write(ReactDOMServer.renderToStaticMarkup(newContent));
    newWindow && newWindow.document.close();
    newWindow && newWindow.focus();
  }
  if (id === null) {
    return <SkeletonContent/>
  } else {
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
          <IconButton ref={shareButtonRef} onClick={() => share()}>
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
          <IconButton onClick={() => print()}>
            <PrintIcon/>
          </IconButton>
        </Box>}
        <Box sx={{px: "0.75rem"}}>
          <>{contents.length > 1 ?
            <Select
              value={index}
              defaultValue={index}
              onChange={(e) => {
                setIndex(Number(e.target.value))
                window.location.hash = `#${e.target.value}`;
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
                key_={"section-" + index}
                titleVernacular={section.label}
                titleLatin={section.id}
                body={section.body}
                singleColumnAsRubric={singleColumnAsRubric}
                bilingualLang={bilingualLang}
                markdownNewlines={markdownNewlines}
                widgetMode={widgetMode}
                itemRefs={itemRefs}
              />
            })}
          </Box>
        </Box>
        {isBilingual() && <BilingualSelector lang={lang} bilingualLang={bilingualLang}
                                             setBilingualLang={setBilingualLang}/>}
      </>
    )
  }
}


const BilingualSection = ({
                            key_,
                            titleVernacular,
                            titleLatin,
                            body,
                            singleColumnAsRubric,
                            bilingualLang,
                            markdownNewlines,
                            widgetMode,
                            itemRefs
                          }: {
  key_: string
  titleVernacular: string
  titleLatin: string
  body: Body
  singleColumnAsRubric: boolean
  bilingualLang: string
  markdownNewlines: boolean
  widgetMode: boolean
  itemRefs: any
}) => {
  let isSmallScreen = useMediaQuery((theme) => theme.breakpoints.down('sm'));
  const formatBody = () => {
    let paragraphs = [];
    for (let row of body) {
      let singleColumn = row.length === 1
      for (let [index, col] of row.entries()) {
        let bilingualLangClass = ""
        if (!singleColumn) {
          bilingualLangClass = (index === 0) ? xVernacular : xLatin
        }
        paragraphs.push({text: col, singleColumn: singleColumn, bilingualLangClass: bilingualLangClass})
      }
    }
    return paragraphs;
  }

  const showHeading = (headingLang) => {
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

  let itemRef = createRef()
  let titleVernacularSlug = slugify(titleVernacular)
  if (titleVernacularSlug) {
    itemRefs[titleVernacularSlug] = itemRef
  }

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
          key={key_ + "-" + index}
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
  let show = (!(useMediaQuery((theme) => theme.breakpoints.down('sm')) && bilingualLangClass !== bilingualLang) || singleColumn);
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
