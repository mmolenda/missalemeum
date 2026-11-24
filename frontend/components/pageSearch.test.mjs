import assert from "node:assert/strict";
import {test} from "node:test";
import {findPageResults, isPageQuery} from "./pageSearch.ts";

test("a page number finds all publications and excludes longer numbers, titles and dates", () => {
  const items = [
    {title: "Msza", path: "mass/example", tags: ["Mszalik - Pallotinum s. 123"]},
    {title: "Pieśń", path: "canticum/example", tags: ["Te Deum — modlitewnik, s. 123", "Te Deum — kancjonał, s. 123"]},
    {title: "Inna strona", path: "canticum/longer", tags: ["Te Deum — kancjonał, s. 1230"]},
    {title: "Psalm 123", path: "oratio/psalm", tags: ["123"]},
    {title: "123", path: "calendar/2026-01-23", date: "2026-01-23"},
  ];
  const results = findPageResults(items, "123", "pl");
  assert.deepEqual(results.map((item) => [item.publication, item.path]), [
    ["Mszalik - Pallotinum", "mass/example"],
    ["Te Deum — kancjonał", "canticum/example"],
    ["Te Deum — modlitewnik", "canticum/example"],
  ]);
  assert.deepEqual(findPageResults(items, " 00123 ", "pl"), results);
  assert.equal(findPageResults(items, "1230", "pl")[0].path, "canticum/longer");
});

test("page search supports English missals and removes duplicate destinations per reference", () => {
  const item = {title: "Mass", path: "mass/example", tags: ["Angelus Press p. 123", "Baronius Press p. 123", "Angelus Press p. 123"]};
  const results = findPageResults([item, {...item, date: "2026-01-23"}], "123", "en");
  assert.deepEqual(results.map((item) => item.publication), ["Angelus Press", "Baronius Press"]);
});

test("all page results are returned even when more than thirty items share a page", () => {
  const items = Array.from({length: 40}, (_, index) => ({title: `Pieśń ${index}`, path: `canticum/${index}`, tags: ["Te Deum — modlitewnik, s. 218"]}));
  assert.equal(findPageResults(items, "218", "pl").length, 40);
});

test("only an integer query switches to page search", () => {
  for (const query of ["", " ", "Te Deum", "s. 123", "2026-01-23", "123.0", "123 tekst"]) {
    assert.equal(isPageQuery(query), false);
    assert.deepEqual(findPageResults([], query, "pl"), []);
  }
  assert.equal(isPageQuery("123"), true);
});
