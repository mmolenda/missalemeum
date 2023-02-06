import React from 'react';
import {Link as RouterLink, useParams} from "react-router-dom";
import ContainerSimple from "./ContainerSimple";
import {Link} from "@mui/material";

export default function SupplementIndex() {
  const {lang} = useParams()
  let content
  if (lang === 'pl') {
    content = (<>
      <p>Opisy okresów liturgicznych z rozważaniem i przepisami obrzędowymi. Odnośnik do danego okresu liturgicznego wyświetla się również w opisie formularza dnia rozpoczynającego ten okres, np. Niedziela Siedemdziesiątnicy.</p>
      <Link component={RouterLink} to={{pathname: `1-wprowadzenie`, search: '?ref=supplement'}} href='#'>1-wprowadzenie</Link><br />
      <Link component={RouterLink} to={{pathname: `10-zeslanie-ducha-sw`, search: '?ref=supplement'}} href='#'>10-zeslanie-ducha-sw</Link><br />
      <Link component={RouterLink} to={{pathname: `11-okres-po-zeslaniu-ducha-sw`, search: '?ref=supplement'}} href='#'>11-okres-po-zeslaniu-ducha-sw</Link><br />
      <Link component={RouterLink} to={{pathname: `12-sancti`, search: '?ref=supplement'}} href='#'>12-sancti</Link><br />
      <Link component={RouterLink} to={{pathname: `2-adwent`, search: '?ref=supplement'}} href='#'>2-adwent</Link><br />
      <Link component={RouterLink} to={{pathname: `20-chrzest`, search: '?ref=supplement'}} href='#'>20-chrzest</Link><br />
      <Link component={RouterLink} to={{pathname: `21-pokuta`, search: '?ref=supplement'}} href='#'>21-pokuta</Link><br />
      <Link component={RouterLink} to={{pathname: `22-malzenstwo`, search: '?ref=supplement'}} href='#'>22-malzenstwo</Link><br />
      <Link component={RouterLink} to={{pathname: `3-boze-narodzenie`, search: '?ref=supplement'}} href='#'>3-boze-narodzenie</Link><br />
      <Link component={RouterLink} to={{pathname: `4-okres-po-objawieniu`, search: '?ref=supplement'}} href='#'>4-okres-po-objawieniu</Link><br />
      <Link component={RouterLink} to={{pathname: `5-przedposcie`, search: '?ref=supplement'}} href='#'>5-przedposcie</Link><br />
      <Link component={RouterLink} to={{pathname: `6-wielki-post`, search: '?ref=supplement'}} href='#'>6-wielki-post</Link><br />
      <Link component={RouterLink} to={{pathname: `7-wielki-tydzien`, search: '?ref=supplement'}} href='#'>7-wielki-tydzien</Link><br />
      <Link component={RouterLink} to={{pathname: `8-okres-meki-panskiej`, search: '?ref=supplement'}} href='#'>8-okres-meki-panskiej</Link><br />
      <Link component={RouterLink} to={{pathname: `9-okres-wielkanocny`, search: '?ref=supplement'}} href='#'>9-okres-wielkanocny</Link><br />
    </>)
  } else {
    content = (<>
      <p>1962 liturgical calendar is available in iCalendar format.</p>
      <Link component={RouterLink} to={{pathname: `advent`, search: '?ref=supplement'}} href='#'>advent</Link><br />
    </>)
  }
  return (
    <ContainerSimple title="Suplement" content={content} />
  )
}