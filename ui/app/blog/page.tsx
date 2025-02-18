import LikeButton from "@/testcomponents/button";


function Header({ title }) {
  return <h1>{title ? title : 'Default title'}</h1>;
}

export default function Page() {
  const names = ['Ada Lovelace', 'Grace Hopper', 'Margaret Hamilton'];
  let titles = []

    fetch("http://localhost:8000/pl/api/v5/calendar", {mode: "cors"})
    .then(response => {
        return response.json()
    })
    .then(json => {


    })



  return (
    <div>
      <Header title="Develop. Preview. Ship." />
      <ul>
        {names.map((name) => (
          <li key={name}>{name}</li>
        ))}
      </ul>

      <LikeButton />
    </div>
  );
}