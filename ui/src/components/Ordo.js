import React, {createRef} from 'react';
import ContainerWithSidenav from "./ContainerWithSidenav";
import {Link as ScrollLink} from "react-scroll";
import List from "@mui/material/List";
import {SidenavListItem} from "./styledComponents/SidenavListItem";
import {grey} from "@mui/material/colors";
import SidenavListItemText from "./styledComponents/SidenavListItemText";

export default function Ordo() {

  const getContentUrl = 'api/v5/ordo'
  const getSidenavItemsUrl = null
  const path = null
  const init = ((id, internalLang, internalYear, sidenavItems, getSidenavItems, getContent, setSidenavHidden) => {
    setSidenavHidden(true)
    getContent(undefined, true)
  })

  return (
    <ContainerWithSidenav
      init={init}
      getContentUrl={getContentUrl}
      getSidenavItemsUrl={getSidenavItemsUrl}
      sidenav={<Sidenav/>}
      sidenavPath={path}
      singleColumnAsRubric={true}
      // We need container height fixed to 100vh in order to make react-scroll spy/hash/etc.
      // working in this setup. On the other hand height: 100% is preferable so the address bar
      // hides nicely on mobile. This workaround makes it looking 100% correct on mobile for all but Ordo,
      // where scroll works good at the cost of address bar not hiding on mobile. Refactor in further releases.
      fixedContainerHeight={true}
    />
  )
}

const Sidenav = (props) => {
  let listItemRefs = {}
  const scrollToListItem = (sidenavItemId) => {
    let listItemRef = listItemRefs[sidenavItemId]
    if (listItemRef && listItemRef.current) {
      listItemRef.current.scrollIntoView({block: "center", behavior: "auto"})
    }
  }
  if (props.items === null) {
    return (<List></List>)
  } else {
    return (
      <List>
        {props.items.map((indexItem) => {
          let myRef = createRef()
          listItemRefs[indexItem.id] = myRef
          return <SidenavListItem
            key={indexItem.id}
            ref={myRef}
            disableGutters={true}
          >
            <ScrollLink
              href="#"
              activeClass="sidenavItemActive"
              to={indexItem.id}
              containerId="content"
              spy={true}
              hashSpy={true}
              onSetActive={(sidenavItemId) => {
                props.setSidenavHidden(true)
                scrollToListItem(sidenavItemId)
              }}
              onClick={() => props.setSidenavHidden(true)}
              style={{
                display: "block",
                width: "100%",
                color: grey[800],
                paddingLeft: "1rem",
                paddingRight: "1rem",
                paddingTop: "0.5rem",
                paddingBottom: "0.5rem",
                textDecoration: "none"
              }}
            >
              <SidenavListItemText primary={indexItem.title} />
            </ScrollLink>
          </SidenavListItem>
        })}
      </List>
    )
  }
}


