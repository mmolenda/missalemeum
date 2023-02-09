import * as React from 'react';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import {IconButton} from "@mui/material";
import CloseIcon from '@mui/icons-material/Close';

export default function NewReleaseDialog(props) {
  const [open, setOpen] = React.useState(localStorage.getItem("releaseDialogSeen") !== props.version || props.debug === true)
  const handleClose = () => {
    localStorage.setItem("releaseDialogSeen", props.version)
    setOpen(false);
  };

  return (
      <Dialog
        open={open}
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
        <DialogTitle id="alert-dialog-title">{(props.lang === "pl") ? "Missale Meum w nowej odsłonie" : "Missale Meum in a new version"}</DialogTitle>
        <DialogContent>
          {(props.lang === "en")
            ? <DialogContentText id="alert-dialog-description">
            Laudetur Iesus Christus!<br/>
            We are happy to present you with the next edition of the online missal.<br/><br />

            <strong>What's new</strong><br />
            - Refreshed design<br/>
            - Added several popular songs and prayers in English and in Latin, with the same language switch as in masses<br/><br/>

            Although the list of new features is not spectacular, over the last few months we have made thorough changes
              to the application that will facilitate further development and work on new functionalities that we hope
              will start to appear soon.<br /><br />
            Any comments on the operation of the new website, suggestions, etc. are welcome at   marcin@missalemeum.com.
          </DialogContentText>
          : <DialogContentText id="alert-dialog-description">
            Laudetur Iesus Christus!<br/>
            Prezentujemy Państwu kolejne wydanie mszalika online.<br/><br />

            <strong>Co nowego</strong><br />
            - Odświeżony wygląd<br/>
            - Pieśni i modlitwy polsko-łacińskie mają przełącznik języka, tak jak msze<br/>
            - Komentarze do ewanelii przeniesione do aplikacji (zamiast linku do zewnętrznego źródła)<br/><br />

            Chociaż lista nowości nie jest spektakularna, przez ostatnich kilka miesięcy przeprowadziliśmy
            gruntowne zmiany w aplikaci, które ułatwią dalszy rozwój i prace nad nowymi funkcjonalnościami,
            które, mamy nadzieję, wkrótce zaczną się pojawiać.<br /><br />
            Wszelkie uwagi na temat działania nowego serwisu, sugestie, etc. są mile widziane pod adresem marcin@missalemeum.com.
          </DialogContentText>}
        </DialogContent>
      </Dialog>
  );
}