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
import 'moment/locale/pl';
import PrintIcon from '@mui/icons-material/Print';
import ShareIcon from '@mui/icons-material/Share';
import {
  MENUITEM_SUPPLEMENT, MSG_ADDRESS_COPIED, COMMEMORATION
} from "./intl";
import SkeletonContent from "./SkeletonContent";
import Md from "./styledComponents/Md";
import MdPrintable from "./styledComponents/MdPrintable";
import MyLink from "./MyLink";
import ArticleTags from "./ArticleTags";
import {createRef, Fragment, useEffect, useRef, useState} from "react";


const xVernacular = 'x-vernacular'
const xLatin = 'x-latin'

export default function BilingualContent(props) {
  const [index, setIndex] = useState(0)

  useEffect(() => {
    let hashValue = window.location.hash.substring(1)
    setIndex(parseInt(hashValue) || 0)
  })

  return (
    <Article
      id={props.id}
      lang={props.lang}
      content={props.contents}
      index={index}
      setIndex={setIndex}
      singleColumnAsRubric={props.singleColumnAsRubric}
      backButton={props.backButton}
      markdownNewlines={props.markdownNewlines}
      widgetMode={props.widgetMode}
    />
  )
}

const Article = (props) => {
  const [bilingualLang, setBilingualLang] = useState(xVernacular)
  const [sharePopoverOpen, setSharePopoverOpen] = useState(false)
  let shareButtonRef = useRef()
  let content = props.content[props.index]
  let itemRefs = {}
  useEffect(() => {
    scrollToListItem(window.location.hash.substring(1))
  }, [])

  const scrollToListItem = (itemId) => {
    let itemRef = itemRefs[itemId]
    if (itemRef && itemRef.current) {
      itemRef.current.scrollIntoView({block: "center", behavior: "auto"})
    } else {
      window.scrollTo({ top: 0 });
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
      navigator.clipboard.writeText(url).then(function() {
      }, function(err) {
        alert(`Couldn't copy address: ${err}`);
      });
    }
  }

  const print = () => {
    let newWindow = window.open('','', "width=650, height=750");
    let newContent = (
      <html>
      <body style={{margin: "4%", minWidth: "300px"}}>
      <h1>{content.info.title}</h1>
      <ArticleTags info={content.info} lang={props.lang} showIcon={false} />
      {content.info.description && <MdPrintable text={content.info.description} markdownNewlines={props.markdownNewlines} />}
      {content.sections.map((section) => {
        return <div>
          {section.label && <h2>{section.label}</h2>}
          {section.body.map((paragraph) => {
            return (paragraph.length === 1) ?
              <div><div><MdPrintable text={paragraph[0]} markdownNewlines={props.markdownNewlines} /></div></div> :
              <div style={{display: "inline-grid", gridTemplateColumns: "50% 50%"}}><div style={{marginRight: "5%"}}><MdPrintable text={paragraph[0]} markdownNewlines={props.markdownNewlines} /></div><div><MdPrintable text={paragraph[1]} markdownNewlines={props.markdownNewlines} /></div></div>
          })}
        </div>
      })}
      <p><em>https://www.missalemeum.com</em></p>
      </body>
      </html>)
    newWindow.document.write(ReactDOMServer.renderToStaticMarkup(newContent));
    newWindow.document.close();
    newWindow.focus();
  }
  if (props.id === null) {
    return <SkeletonContent />
  } else {
    return (
      <>
        <Box sx={{
          position: "fixed",
          top: (theme) => theme.components.MuiAppBar.styleOverrides.root.height}}
        >
          {props.backButton}
        </Box>
        {!props.widgetMode && <Box sx={{display: "flex", justifyContent: "flex-end"}}>
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
              <Typography sx={{ p: 2 }}>{MSG_ADDRESS_COPIED[props.lang]}</Typography>
            </Popover>
          </IconButton>
          <IconButton onClick={() => print()}>
            <PrintIcon/>
          </IconButton>
        </Box>}
        <Box sx={{px: "0.75rem"}}>
          <>{props.content.length > 1 ?
            <Select
              value={props.index}
              defaultValue={props.index}
              onChange={(e) => {
                props.setIndex(e.target.value)
                window.location.hash = `#${e.target.value}`;
              }}
              sx={{
                fontSize: (theme) => theme.typography.h2.fontSize,
                fontWeight: (theme) => theme.typography.h2.fontWeight,
                color: (theme) => theme.typography.h2.color
              }}
            >
              {props.content.map((content, xindex) => {
                return <MenuItem key={xindex} value={xindex}>{content.info.title}</MenuItem>
              })}
            </Select> :
            <Typography variant="h2">
              {content.info.title}
            </Typography>
          }</>
          { content.info.commemorations && content.info.commemorations.length > 0 && <Typography variant="h3">{COMMEMORATION[props.lang]}{" "}{content.info.commemorations.join(", ")}</Typography> }
          <Box sx={{ padding: "0.5rem" }}>
            <ArticleTags info={content.info} lang={props.lang} showIcon />
          </Box>
          <>{content.info.description && <Typography component="div" variant="body1" align="justify" sx={{ padding: "0.5rem", hyphens: "auto" }}>
            <Md text={content.info.description} markdownNewlines={props.markdownNewlines} widgetMode={props.widgetMode} />
          </Typography>}</>
          {content.info.supplements && content.info.supplements.length > 0 &&
            <Typography variant="body1" align="justify" sx={{ padding: "0.5rem" }}>
              {`${MENUITEM_SUPPLEMENT[props.lang]}: `}
              {content.info.supplements.map((supplement, index) => {
                return (<Fragment key={index}>
                  <MyLink href={`${supplement.path}?ref=${props.id}`} text={supplement.label} widgetMode={props.widgetMode} />
                  {index + 1 < content.info.supplements.length && ", "}
                </Fragment>)
              })}
            </Typography>}

          <Box className="qpa" sx={{ display: "grid" }}>
          {content.sections.map((section, index) => {
            return <BilingualSection
              key={"section-" + index}
              key_={"section-" + index}
              titleVernacular={section.label}
              titleLatin={section.id}
              body={section.body}
              singleColumnAsRubric={props.singleColumnAsRubric}
              bilingualLang={bilingualLang}
              markdownNewlines={props.markdownNewlines}
              widgetMode={props.widgetMode}
              itemRefs={itemRefs}
            />
          })}
          </Box>
        </Box>
        {isBilingual() && <BilingualSelector lang={props.lang} bilingualLang={bilingualLang} setBilingualLang={(l) => setBilingualLang(l)}/>}
      </>
    )
  }
}

const BilingualSection = (props) => {
  let isSmallScreen = useMediaQuery((theme) => theme.breakpoints.down('sm'));
  const formatBody = () => {
    let paragraphs = [];
    for (let row of props.body) {
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

  const showHeading = (bilingualLang) => {
    if (isSmallScreen) {
      if (bilingualLang === xLatin && !props.titleLatin) {
        return false
      }
      if (bilingualLang === xVernacular && !props.titleLatin) {
        return true
      }
      if (bilingualLang !== props.bilingualLang) {
        return false;
      }
    }
    return true
  }

  let itemRef = createRef()
  let titleVernacularSlug = slugify(props.titleVernacular)
  if (titleVernacularSlug) {
    props.itemRefs[titleVernacularSlug] = itemRef
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
          {props.titleVernacular}
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
          {props.titleLatin}
        </Typography>
        <>{formatBody().map((paragraph, index) => (
          <BilingualSectionParagraph
            key={props.key_ + "-" + index}
            text={paragraph.text}
            singleColumn={paragraph.singleColumn}
            singleColumnAsRubric={props.singleColumnAsRubric}
            bilingualLang={props.bilingualLang}
            bilingualLangClass={paragraph.bilingualLangClass}
            markdownNewlines={props.markdownNewlines}
            widgetMode={props.widgetMode}
          />
        ))}</>
      </Box>
  )
}

const BilingualSectionParagraph = (props) => {
  let show = (!(useMediaQuery((theme) => theme.breakpoints.down('sm')) && props.bilingualLangClass !== props.bilingualLang) || props.singleColumn);
  return (
    <Typography
      component="div"
      variant="body1"
      className={props.bilingualLangClass}
      align="justify"
      sx={{
        display: (show) ? "block" : "none",
        gridColumn: (props.singleColumn) ? "1 / span 2" : "unset",
        color: (props.singleColumn && props.singleColumnAsRubric) ? "secondary.main" : "text.primary",
        padding: "0.5rem",
        hyphens: "auto"
      }}
    >
      <Md text={props.text} markdownNewlines={props.markdownNewlines} widgetMode={props.widgetMode} />
    </Typography>
  )
}

const BilingualSelector = (props) => {
  const handleChange = (event, newBilingualLang) => {
    if (newBilingualLang !== null) {
      props.setBilingualLang(newBilingualLang)
    }
  }
  return (
    <ToggleButtonGroup
      sx={{
        display: { xs: 'block', sm: 'none' },
        position: "fixed",
        right: "20px",
        bottom: "20px",
        opacity: 0.9,
        backgroundColor: "background.default"
      }}
      color="secondary"
      value={props.bilingualLang}
      exclusive
      onChange={handleChange}
    >
      <ToggleButton value={xVernacular}>{props.lang.toUpperCase()}</ToggleButton>
      <ToggleButton value={xLatin}>LAT</ToggleButton>
    </ToggleButtonGroup>
  )
}
