import {MenuItem, Select, useTheme} from "@mui/material";
import React, {useState} from "react";
import {
	RANK_NAMES, VESTMENTS_BLACK,
	VESTMENTS_GREEN, VESTMENTS_PINK,
	VESTMENTS_RED,
	VESTMENTS_VIOLET,
	VESTMENTS_WHITE
} from "../intl";
import moment from "moment/moment";
import Tag from "./styledComponents/Tag";
import EventIcon from "@mui/icons-material/Event";
import TimelapseIcon from "@mui/icons-material/Timelapse";
import ShieldOutlinedIcon from "@mui/icons-material/ShieldOutlined";
import ShieldIcon from "@mui/icons-material/Shield";

export default function ArticleTags(props) {
  const theme = useTheme()
  const [paperPage, setPaperPage] = useState(0)

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
      label = RANK_NAMES[props.lang][props.info.rank]
      tags.push(<Tag key={label} label={label} />);
  }
  if (props.info.colors) {
    for (let colorCode of props.info.colors) {
      let tag
      label = colorNames[colorCode]
      if (
        (colorCode === "w" && theme.palette.mode === "light")
        || (colorCode === "b" && theme.palette.mode === "dark")
        || !props.showIcon) {
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
        : paperPages.map((content) => <Tag key={content} label={content} />)
      }
    </>
  )
}