import React, {useEffect, useRef, useState} from 'react';
import ReactDOMServer from 'react-dom/server';
import {useLocation, useNavigate} from "react-router-dom";
import "react-datepicker/dist/react-datepicker.css";
import slugify from "slugify";
import {Element} from 'react-scroll'
import {
  Box,
  Typography,
  ToggleButtonGroup,
  ToggleButton,
  useMediaQuery,
  IconButton,
  Select,
  MenuItem, Popover, useTheme
} from "@mui/material";
import moment from "moment";
import 'moment/locale/pl';
import PrintIcon from '@mui/icons-material/Print';
import ShareIcon from '@mui/icons-material/Share';
import ShieldIcon from '@mui/icons-material/Shield';
import ShieldOutlinedIcon from '@mui/icons-material/ShieldOutlined';
import EventIcon from '@mui/icons-material/Event';
import TimelapseIcon from '@mui/icons-material/Timelapse';
import {
  CLASS_1,
  CLASS_2,
  CLASS_3,
  CLASS_4, MENUITEM_SUPPLEMENT, MSG_ADDRESS_COPIED, VESTMENTS_BLACK,
  VESTMENTS_GREEN, VESTMENTS_PINK,
  VESTMENTS_RED,
  VESTMENTS_VIOLET,
  VESTMENTS_WHITE
} from "../intl";
import Tag from "./styledComponents/Tag";
import SkeletonContent from "./SkeletonContent";
import Md from "./styledComponents/Md";
import MdPrintable from "./styledComponents/MdPrintable";
import MyLink from "./MyLink";


const xVernacular = 'x-vernacular'
const xLatin = 'x-latin'

export default function BilingualContent(props) {
  const location = useLocation();
  const [index, setIndex] = useState(0)

  useEffect(() => {
    // TODO: regex to check if the index contains number only
    let hashValue = location.hash.replace("#", "")
    let indexValue = parseInt(hashValue) || 0
    setIndex(indexValue)
  }, [location.hash])

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
      contentToolbarDisabled={props.contentToolbarDisabled}
    />
  )
}

const ArticleTags = (props) => {
  const theme = useTheme()
  const [paperPage, setPaperPage] = useState(0)

  let rankNames = {
    1: CLASS_1[props.lang],
    2: CLASS_2[props.lang],
    3: CLASS_3[props.lang],
    4: CLASS_4[props.lang]}

  let colorNames = {
    r: VESTMENTS_RED[props.lang],
    g: VESTMENTS_GREEN[props.lang],
    w: VESTMENTS_WHITE[props.lang],
    v: VESTMENTS_VIOLET[props.lang],
    b: VESTMENTS_BLACK[props.lang],
    p: VESTMENTS_PINK[props.lang]}

  let tags = [];
  let date = props.info.date;
  let label
  if (date) {
      moment.locale(props.lang)
      let parsedDate = moment(date, "YYYY-MM-DD");
      label = parsedDate.format("DD MMMM YY, dddd")
      tags.push(<Tag key={label} icon={props.showIcon &&<EventIcon />} label={label} />);
  }
  if (props.info.tempora != null) {
      label = props.info.tempora
      tags.push(<Tag key={label} icon={props.showIcon &&<TimelapseIcon />} label={label} />);
  }
  if (props.info.rank) {
      label = rankNames[props.info.rank]
      tags.push(<Tag key={label} label={label} />);
  }
  if (props.info.colors) {
    for (let colorCode of props.info.colors) {
      let tag
      label = colorNames[colorCode]
      if ((colorCode === "w" && theme.palette.mode === "light") || (colorCode === "b" && theme.palette.mode === "dark")) {
        tag = <Tag key={label} icon={props.showIcon && <ShieldOutlinedIcon/>} label={label}/>
      } else {
        tag = <Tag key={label} color={`vestment${colorCode}`} icon={props.showIcon &&<ShieldIcon />} label={label} />
      }
      tags.push(tag);
    }
  }
  let paperPages = []
  if (props.info.tags != null) {
    for (let infoItem of props.info.tags.filter((i) => ! i.includes("Szaty"))) {
      if (infoItem.match(/ \w\. \d+/)) {
        // Paper pages references such as "Pallotinum s. 207" or "Angelus Press p. 359" are handled separately
        paperPages.push(infoItem)
      } else {
        tags.push(<Tag key={infoItem} label={infoItem} />)
      }
    }
  }
  return (
    <>
      {tags}
      {props.showIcon && paperPages.length > 1
        ? <Select
            value={paperPage}
            defaultValue={paperPage}
            variant="outlined"
            onChange={(e) => {
              setPaperPage(e.target.value)
            }}
            sx={{
              borderRadius: 10,
              fontFamily: "Arial",
              fontSize: "0.85rem",
              color: (theme) => theme.palette.secondary.main,
              "& .MuiSvgIcon-root": {
                  color: (theme) => theme.palette.secondary.main,
              },
              "& .MuiOutlinedInput-input": {
                  padding: "0.4rem 1rem",
              },
              "& .MuiOutlinedInput-notchedOutline": {
                borderColor: (theme) => theme.palette.secondary.main,
              }
            }}
          >
            {paperPages.map((content, xindex) => <MenuItem key={xindex} value={xindex}>{content}</MenuItem>)}
          </Select>
        : paperPages.map((content) => <Tag key={content} label={content} />)
      }
    </>
  )
}

const Article = (props) => {
  const [bilingualLang, setBilingualLang] = useState(xVernacular)
  const [sharePopoverOpen, setSharePopoverOpen] = useState(false)
  const navigate = useNavigate()
  let content = props.content[props.index]
  let shareButtonRef = useRef()

  useEffect(() => {
    content && (document.title = [content.info.title, content.info.date, "Missale Meum"].filter((i) => Boolean(i)).join(" | "))
  })

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
        setSharePopoverOpen(true)
        setInterval(() => {
           setSharePopoverOpen(false)
        }, 1000)
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
        {!props.contentToolbarDisabled && <Box sx={{display: "flex", justifyContent: "flex-end"}}>
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
          {props.content.length > 1 ?
            <Select
              value={props.index}
              defaultValue={props.index}
              onChange={(e) => {
                props.setIndex(e.target.value)
                navigate(`#${e.target.value}`)
              }}
              sx={{
                fontSize: (theme) => theme.typography.h2.fontSize,
                fontWeight: (theme) => theme.typography.h2.fontWeight,
                color: (theme) => theme.typography.h2.color
              }}
            >
              {props.content.map((content, xindex) => {
                return <MenuItem value={xindex}>{content.info.title}</MenuItem>
              })}
            </Select> :
            <Typography variant="h2">
              {content.info.title}
            </Typography>
          }
          <Box sx={{ padding: "0.5rem" }}>
            <ArticleTags info={content.info} lang={props.lang} showIcon />
          </Box>
          {content.info.description && <Typography component="div" variant="body1" align="justify" sx={{ padding: "0.5rem", hyphens: "auto" }}>
            <Md text={content.info.description} markdownNewlines={props.markdownNewlines} />
          </Typography>}
          {content.info.supplements && content.info.supplements.length > 0 &&
            <Typography variant="body1" align="justify" sx={{ padding: "0.5rem" }}>
              {`${MENUITEM_SUPPLEMENT[props.lang]}: `}
              {content.info.supplements.map((supplement, index) => {
                return (<React.Fragment key={index}>
                  <MyLink href={`${supplement.path}?ref=${props.id}`} text={supplement.label} />
                  {index + 1 < content.info.supplements.length && ", "}
                </React.Fragment>)
              })}
            </Typography>}

          <Box sx={{ display: "grid" }}>
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

  return (
    <Element name={slugify(props.titleVernacular)}>
      <Box sx={{
        display: isSmallScreen ? "block" : "inline-grid",
        gridTemplateColumns: isSmallScreen ? "unset" : "repeat(2, 1fr)"
      }}>
        <Typography
          variant="h3"
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
          variant="h3"
          className={xLatin}
          sx={{
            display: (showHeading(xLatin)) ? "block" : "none",
            px: "0.5rem",
            pt: "1rem"
          }}
        >
          {props.titleLatin}
        </Typography>
        {formatBody().map((paragraph, index) => (
          <BilingualSectionParagraph
            key={props.key_ + "-" + index}
            text={paragraph.text}
            singleColumn={paragraph.singleColumn}
            singleColumnAsRubric={props.singleColumnAsRubric}
            bilingualLang={props.bilingualLang}
            bilingualLangClass={paragraph.bilingualLangClass}
            markdownNewlines={props.markdownNewlines}
          />
        ))}
      </Box>
    </Element>
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
      <Md text={props.text} markdownNewlines={props.markdownNewlines} />
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
