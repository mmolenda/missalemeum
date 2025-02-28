import {MenuItem, Select, useTheme} from "@mui/material";
import React, {useState} from "react";
import {
  RANK_NAMES, VESTMENTS_BLACK,
  VESTMENTS_GREEN, VESTMENTS_PINK,
  VESTMENTS_RED,
  VESTMENTS_VIOLET,
  VESTMENTS_WHITE, Locale
} from "./intl";
import moment from "moment/moment";
import Tag from "./styledComponents/Tag";
import EventIcon from "@mui/icons-material/Event";
import TimelapseIcon from "@mui/icons-material/Timelapse";
import ShieldOutlinedIcon from "@mui/icons-material/ShieldOutlined";
import ShieldIcon from "@mui/icons-material/Shield";
import {ColorCode, Info} from "@/components/types";


export default function ArticleTags({lang, info, showIcon}: { lang: string, info: Info, showIcon: boolean }) {
  const theme = useTheme()
  const [paperPage, setPaperPage] = useState(0)

  let colorNames: {[key in ColorCode]: string} = {
    r: VESTMENTS_RED[lang as Locale],
    g: VESTMENTS_GREEN[lang as Locale],
    w: VESTMENTS_WHITE[lang as Locale],
    v: VESTMENTS_VIOLET[lang as Locale],
    b: VESTMENTS_BLACK[lang as Locale],
    p: VESTMENTS_PINK[lang as Locale]
  }

  let tags = [];
  let date = info.date;
  let label
  if (date) {
    moment.locale(lang)
    let parsedDate = moment(date, "YYYY-MM-DD");
    label = parsedDate.format("DD MMMM YY, dddd")
    tags.push(<Tag key={label} icon={showIcon && <EventIcon/>} label={label}/>);
  }
  if (info["tempora"] != null) {
    label = info["tempora"]
    tags.push(<Tag key={label} icon={showIcon && <TimelapseIcon/>} label={label}/>);
  }
  if (info.rank) {
    label = RANK_NAMES[lang as Locale][info.rank]
    tags.push(<Tag key={label} label={label}/>);
  }
  if (info.colors) {
    for (let colorCode of info.colors) {
      let tag
      label = colorNames[colorCode as ColorCode]
      if (
        (colorCode === "w" && theme.palette.mode === "light")
        || (colorCode === "b" && theme.palette.mode === "dark")
        || !showIcon) {
        tag = <Tag key={label} icon={showIcon && <ShieldOutlinedIcon/>} label={label}/>
      } else {
        tag = <Tag key={label} color={`vestment${colorCode}`} icon={showIcon && <ShieldIcon/>} label={label}/>
      }
      tags.push(tag);
    }
  }
  let paperPages = []
  if (info.tags) {
    for (let infoItem of info.tags.filter((i) => !i.includes("Szaty"))) {
      if (infoItem.match(/ \w\. \d+/)) {
        // Paper pages references such as "Pallotinum s. 207" or "Angelus Press p. 359" are handled separately
        paperPages.push(infoItem)
      } else {
        tags.push(<Tag key={infoItem} label={infoItem}/>)
      }
    }
  }
  return (
    <>
      {tags}
      {showIcon && paperPages.length > 1
        ? <Select
          value={paperPage}
          defaultValue={paperPage}
          variant="outlined"
          onChange={(e) => {
            setPaperPage(Number(e.target.value))
          }}
          sx={{
            borderRadius: 10,
            fontFamily: "Arial",
            fontSize: theme.typography.fontSize / 18 + "rem",
            height: (theme) => theme.typography.fontSize / 7 + "rem",
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
        : paperPages.map((content) => <Tag key={content} label={content}/>)
      }
    </>
  )
}