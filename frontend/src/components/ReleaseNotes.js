import * as React from 'react';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import {IconButton} from "@mui/material";
import CloseIcon from '@mui/icons-material/Close';
import {myLocalStorage} from "../myLocalStorage";
import MyLink from "./MyLink";
import moment from "moment";
import {useEffect} from "react";

export default function ReleaseNotes(props) {
  const storageKey = `releaseDialogSeen-${props.lang}`
  const expirationDate = "2023-08-11 12:00:00"
  useEffect(() => {
    // must be before the date AND storage says its not seen  OR
    // debug always opens
    let isNotSeen= myLocalStorage.getItem(storageKey) !== props.version
    let isNotExpired = moment(expirationDate) > moment()
    // if open state is provided from the outside - open; otherwise evaluate if it should be opened
    props.open || props.setOpen((isNotSeen && isNotExpired) || props.debug === true)
  }, [])

  const handleClose = () => {
    myLocalStorage.setItem(storageKey, props.version)
    props.setOpen(false);
  };

  return (
      <Dialog
        open={props.open}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <IconButton
          aria-label="close"
          onClick={handleClose}
          sx={{
            position: 'absolute',
            right: 8,
            top: 8,
            color: (theme) => theme.palette.grey[500],
          }}
        >
          <CloseIcon />
        </IconButton>
        <DialogTitle id="alert-dialog-title">{(props.lang === "pl") ? "Missale Meum 5.4.0" : "Missale Meum 5.4.0"}</DialogTitle>
        <DialogContent>
          {(props.lang === "en")
            ? <DialogContentText id="alert-dialog-description">
            Laudetur Iesus Christus!<br/>
            We are happy to announce the next release of the online missal.<br/><br />

            <strong>What's new</strong><br />
            - You can now adjust the font size in the application! Take a look at the bottom of the main menu.<br/>
            - Missale Meum widget with daily propers that can be embedded on your website as an iframe. More details on <MyLink href="/en/supplement/index" text="Supplement" /> page.<br/>
            - We have fixed several errors and typos reported by the users.<br/><br/>

            More details can be found on the project's <MyLink href="https://github.com/mmolenda/missalemeum/releases" text="GitHub page" />.<br />
            Any comments on the operation of the website, suggestions, etc. are welcome at marcin@missalemeum.com.
          </DialogContentText>
          : <DialogContentText id="alert-dialog-description">
            Laudetur Iesus Christus!<br/>
            Prezentujemy Państwu kolejne wydanie mszalika online.<br/><br />

            <strong>Co nowego</strong><br />
            - Rozmiar tekstu w aplikacji można dostosować za pomocą przełącznika w głównym menu.<br/>
            - Widget Missale Meum z tekstami na dziś, który można umieścić na własnej stronie internetowej jako iframe. Więcej szczegółów w zakładce <MyLink href="/pl/supplement/index" text="Suplement" />.<br/>
            - Poprawiliśmy kilka błędów i literówek zgłoszonych przez użytkowników.<br/><br/>

            Po więcej szczegółów odsyłamy do <MyLink href="https://github.com/mmolenda/missalemeum/releases" text="strony projektu na GitHubie" />.<br />
            Wszelkie uwagi na temat działania serwisu, sugestie, etc. są mile widziane pod adresem marcin@missalemeum.com.
          </DialogContentText>}
        </DialogContent>
      </Dialog>
  );
}