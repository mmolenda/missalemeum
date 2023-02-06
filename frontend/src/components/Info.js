import React from 'react';
import {useParams} from "react-router-dom";
import ContainerSimple from "./ContainerSimple";

export default function Info() {
  const {lang} = useParams()
  let content
  if (lang === 'pl') {
    content = 'Strona Missale Meum (dawniej Mszał Rzymski) powstała na chwałę Boską i pożytek ludzki'
  } else {
    content = 'Missale Meum has been built for the greater glory of God and for peoples advance'
  }
  return (
    <ContainerSimple title="Info" content={content} />
  )
}