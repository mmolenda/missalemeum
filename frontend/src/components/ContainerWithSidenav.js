import React, {cloneElement, createRef, useEffect, useState} from 'react';
import {useParams, Link as RouterLink, useNavigate} from "react-router-dom";
import "react-datepicker/dist/react-datepicker.css";
import BilingualContent from "./BilingualContent";
import slugify from "slugify";
import {Box, Container, IconButton, InputAdornment, ListItemButton, OutlinedInput, Slide} from "@mui/material";
import List from "@mui/material/List";
import CancelIcon from '@mui/icons-material/Cancel';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import {SidenavListItem} from "./styledComponents/SidenavListItem";
import {SEARCH_PLACEHOLDER} from "../intl";
import SidenavListItemText from "./styledComponents/SidenavListItemText";
import SkeletonSidenav from "./SkeletonSidenav";

export default function ContainerWithSidenav(props) {
  const navigate = useNavigate()
  const apiUrlBase = process.env.REACT_APP_API_URL || ""
  const {lang} = useParams()
  const {id} = useParams()
  const queryParameters = new URLSearchParams(window.location.search)
  const backButtonRef = queryParameters.get("ref")
  const apiContentUrl = `${apiUrlBase}/${lang}/${props.getContentUrl}`
  const apiSidenavItemsUrl = `${apiUrlBase}/${lang}/${props.getSidenavItemsUrl}`
  const [internalId, setInternalId] = useState(null)
  const [internalYear, setInternalYear] = useState(null)
  const [internalLang, setInternalLang] = useState(null)
  const [content, setContent] = useState([])
  const [sidenavItems, setSidenavItems] = useState(null)
  const [sidenavItemsFiltered, setSidenavItemsFiltered] = useState(null)
  // does is have sidenav at all
  const sidenavDisabled = Boolean(props.sidenavDisabled)
  // if it has sidenav, controls if it is shown or hidden at the moment
  const [sidenavHidden, setSidenavHidden] = useState(false)
  const contentComponentRef = createRef()

  useEffect(() => {
    props.init(id, internalLang, internalYear, sidenavItems, getSidenavItems, getContent, setSidenavHidden)
    if (contentComponentRef.current) {
      contentComponentRef.current.scrollTo(0, 0)
    }
  }, [id, lang])


  const getContent = (id, sidenavItemsFromContent = false) => {
    setInternalId(null)
    if (id || sidenavItemsFromContent) {
      let url = id ? `${apiContentUrl}/${id}` : apiContentUrl
      fetch(url, {mode: "cors"})
        .then(response => {
          if (response.status === 404) {
            navigate(`/${lang}/404`)
          } else if (response.status !== 200) {
            navigate(`/${lang}/error`)
          } else {
            return response.json()
          }
        })
        .then(json => {
          setInternalId(id)
          setContent(json)
          if (sidenavItemsFromContent) {
            let sidenavItems = json[0].sections.map((item) => {
              return {id: slugify(item.label), title: item.label, tags: []}
            })
            setSidenavItems(sidenavItems)
            setSidenavItemsFiltered(sidenavItems)
          }
        })
        .catch(error => navigate(`/${lang}/404`))
    }
  }

  const getSidenavItems = (year) => {
    let url = year ? `${apiSidenavItemsUrl}/${year}` : apiSidenavItemsUrl
    fetch(url, {mode: "cors"})
      .then(response => {
          if (response.status === 404) {
            navigate(`/${lang}/404`)
          } else if (response.status !== 200) {
            navigate(`/${lang}/error`)
          } else {
            return response.json()
          }
      })
      .then(json => {
        setSidenavItems(json)
        setInternalYear(year)
        setInternalLang(lang)
        setSidenavItemsFiltered(json)
      })
      .catch(error => console.log(error))
  }

  const filterSidenavItems = (filter) => {
    if (filter.length === 0) {
      setSidenavItemsFiltered(sidenavItems)
    } else if (filter.length > 2) {
      filter = filter.toLowerCase()
      let collectedSidenavItems = []
      for (let sidenavItem of sidenavItems) {
        let searchBody = JSON.stringify(sidenavItem).toLowerCase()
        if (searchBody.includes(filter)) {
          collectedSidenavItems.push(sidenavItem)
        }
      }
      setSidenavItemsFiltered(collectedSidenavItems)
    }
  }

  let backButton = ((Boolean(backButtonRef) || !sidenavDisabled) && <IconButton
    component={RouterLink}
    to={{pathname: backButtonRef ? `/${lang}/${backButtonRef}` : ""}}
    onClick={() => {setSidenavHidden(false)}}
    sx={{backgroundColor: "background.default", opacity: 0.9}}
  >
    <ArrowBackIcon/>
  </IconButton>)

  let contentBox = <Box
    id="content"
    ref={contentComponentRef}
    sx={{
      overflowY: 'scroll',
      width: '100%',
      ml: (sidenavDisabled) ? 0 : '-100%',
      pt: (theme) => theme.components.MuiAppBar.styleOverrides.root.height,
      height: (sidenavHidden || sidenavDisabled) ? "100%" : "80vh"}}
    >
      <BilingualContent id={internalId} lang={lang} contents={content}
                        singleColumnAsRubric={props.singleColumnAsRubric} backButton={backButton}
                        markdownNewlines={props.markdownNewlines}/>
  </Box>

  return (
    <Container disableGutters sx={{width: {"md": "900px"}, display: 'flex', overflow: 'hidden', height: (props.fixedContainerHeight) ? "100vh" : "100%"}}>
      {!sidenavDisabled ? <><Slide in={!sidenavHidden} direction="right" appear={false}>
        <Box sx={{overflowY: 'scroll', width: '100%', pt: (theme) => `${parseInt(theme.components.MuiAppBar.styleOverrides.root.height) * 2}px`, height: (!sidenavHidden) ? "100%" : "80vh"}}>
          <SidenavToolbox
            internalId={internalId}
            lang={lang}
            filterSidenavItems={(d) => {
              filterSidenavItems(d)
            }}
            extraTools={props.extraTools}
          />
          <Box>
            {props.sidenav ?
              cloneElement(props.sidenav, {
                internalId: internalId,
                lang: lang,
                items: sidenavItemsFiltered,
                setSidenavHidden: setSidenavHidden
            }) :
              <Sidenav
                internalId={internalId}
                lang={lang}
                items={sidenavItemsFiltered}
                sidenavPath={`/${lang}${props.sidenavPath}`}
                setSidenavHidden={setSidenavHidden}
              />
            }
          </Box>
        </Box>
      </Slide>
      <Slide in={sidenavHidden} direction="left" appear={false}>
        {contentBox}
      </Slide></> : <>{contentBox}</>}
    </Container>
  )
}

const Sidenav = (props) => {
  let listItemRefs = {}

  useEffect(() => {
    if (listItemRefs) {
      for (let listItemRef of Object.values(listItemRefs)) {
        listItemRef.current.classList.remove("sidenavItemActive")
      }
    }
    if (props.internalId) {
      listItemRefs[props.internalId].current.scrollIntoView({block: "center"})
      listItemRefs[props.internalId].current.classList.add("sidenavItemActive")
    }
  })

  if (props.items === null) {
    return <SkeletonSidenav />
  } else {
    return (
      <List>
        {props.items.map((indexItem) => {
          let listItemRef = createRef()
          listItemRefs[indexItem.id] = listItemRef
          return (
            <SidenavListItem
              key={indexItem.id}
              ref={listItemRef}
              disableGutters
            >
              <ListItemButton
                component={RouterLink}
                to={{pathname: props.sidenavPath + indexItem.id, hash: ""}}
                onClick={() => {props.setSidenavHidden(true)}}
              >
                <SidenavListItemText
                  primary={indexItem.title}
                  secondary={indexItem.tags.length > 0 && indexItem.tags.join(", ")}
                />
              </ListItemButton>
            </SidenavListItem>)
        })}
      </List>
    )
  }
}

const SidenavToolbox = (props) => {
  const [filter, setFilter] = useState("")
  return (
    <Box sx={{
      position: "fixed",
      display: "flex",
      top: (theme) => theme.components.MuiAppBar.styleOverrides.root.height,
      width: "875px",
      p: "0.75rem",
      boxShadow: 2,
      backgroundColor: "background.default",
      zIndex: 100}}>
      <OutlinedInput
        size="small"
        type="text"
        placeholder={SEARCH_PLACEHOLDER[props.lang]}
        value={filter}
        onChange={e => {
          setFilter(e.target.value)
          props.filterSidenavItems(e.target.value)
        }}
        endAdornment={
          <InputAdornment position="end">
            <IconButton onClick={e => {
              e.preventDefault()
              setFilter("")
              props.filterSidenavItems("")
            }}>
              <CancelIcon />
            </IconButton>
          </InputAdornment>}
      />
      {props.extraTools && cloneElement(props.extraTools, {internalId: props.internalId, lang: props.lang})}
    </Box>
  )
}
