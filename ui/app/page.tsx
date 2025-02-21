import Link from "next/link";

export default async function Page({params}) {
  return (
    <div>
        <Link href="/pl">Go to app</Link>
    </div>
  );
}