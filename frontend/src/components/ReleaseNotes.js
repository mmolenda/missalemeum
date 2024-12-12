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
  const expirationDate = "2023-07-29 00:00:00"
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
        <DialogTitle id="alert-dialog-title">{(props.lang === "pl") ? "Missale Meum 5.10 (grudzień 2024)" : "Missale Meum 5.10 (December 2024)"}</DialogTitle>
        <DialogContent>
          {(props.lang === "en")
            ? <DialogContentText id="alert-dialog-description">
            Laudetur Iesus Christus!<br/>
            We are happy to announce the next release of the online missal.<br/><br />

            <strong>What's new</strong><br />
            - Commemorations are now displayed in the calendar.<br/><br/>

            More details can be found on the project's <MyLink href="https://github.com/mmolenda/missalemeum/releases" text="GitHub page" />.<br />
            Any comments on the operation of the website, suggestions, etc. are welcome at marcin@missalemeum.com.
          </DialogContentText>
          : <DialogContentText id="alert-dialog-description">
            Laudetur Iesus Christus!<br/>
            Prezentujemy Państwu kolejne wydanie mszalika online.<br/><br />

            <strong>Co nowego</strong><br />
            - Wspomnienia są widoczne w kalendarzu i bezpośrednio pod nagłówkiem na stronie propriów.<br/><br/>

            Po więcej szczegółów odsyłamy do <MyLink href="https://github.com/mmolenda/missalemeum/releases" text="strony projektu na GitHubie" />.<br />
            Wszelkie uwagi na temat działania serwisu, sugestie, etc. są mile widziane pod adresem marcin@missalemeum.com.
          </DialogContentText>}
        </DialogContent>
      </Dialog>
  );
}