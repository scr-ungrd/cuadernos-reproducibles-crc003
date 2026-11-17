#import "style.typ": template, front-page, diff

// Metadata shared by the page template (masthead, header, footer) and the
// front page (title, authors, abstract...).
#let meta = (
  title: "[-doc.title-]",
  authors: ([# for au in doc.authors #](name: "[-au.name-]", affs: ([# for af in au.affiliations #]"[-af.id-]", [# endfor #])), [# endfor #]),
  affiliations: ([# for af in doc.affiliations #](id: "[-af.id-]", name: "[-af.name-]", department: "[-af.department-]", city: "[-af.city-]", country: "[-af.country-]"), [# endfor #]),
[# if doc.doi #]
  doi: "[-doc.doi-]",
[# endif #]
[# if doc.date #]
  date: (day: [-doc.date.day-], month: [-doc.date.month-], year: [-doc.date.year-]),
[# endif #]
[# if doc.license #]
  license-content: "[-doc.license.content.id-]",
  license-code: "[-doc.license.code.id-]",
[# endif #]
[# if doc.github #]
  github: "[-doc.github-]",
[# endif #]
  keywords: ([# for keyword in doc.keywords #]"[-keyword-]", [# endfor #]),
  supertitle: "Cuaderno reproducible",
  journal: "Cuadernos Reproducibles de Conocimiento del Riesgo",
[# if doc.github #]
  // Report id taken from the repository name, e.g. ".../cuadernos-reproducibles-crc001" -> "CRC001".
  report-id: "[- doc.github.split("-") | last | upper -]",
[# endif #]
)

#show: template.with(..meta)

[-IMPORTS-]

// mystmd renders tables (e.g. DataFrame outputs) with the `tablex` package and
// defines `tableStyle` and `legendStyle` in the imports above. Shadow them (and
// `tablex`) so those tables follow the article's table design (see style.typ).
#import "style.typ": tableStyle, tablex-args, wrap-table, legendStyle
#let _tablex = tablex
#let tablex(..args) = wrap-table(_tablex(..args.pos(), ..tablex-args(args.named())))

// mystmd emits a table with a legend as `subpar.grid(table, text(..legendStyle)[legend], ...)`,
// which centers everything. Shadow the `subpar` module with a wrapper that
// left-aligns the legend and brings it close to the table, and keep each table
// in one piece (with its legend).
#import "subpar-wrap.typ" as subpar
#let breakableDefault = false

// The first section of the body starts on a new page (page 2) when the document labels it:
// put `(inicio-cuerpo)=` right before its heading (mystmd turns it into the Typst label below).
#show <inicio-cuerpo>: it => {
  pagebreak(weak: true)
  it
}

// The front page is always drawn; the abstract and the key points are optional parts.
#front-page(
  ..meta,
[# if parts.abstract #]
  abstract: [
[-parts.abstract-]
  ],
[# endif #]
[# if parts.keypoints #]
  keypoints: list(
[# for keypoint in parts.keypoints #]
    [[-keypoint-]],
[# endfor #]
  ),
[# endif #]
)

[-CONTENT-]

[# if parts.data_availability #]
== Disponibilidad de Datos
[-parts.data_availability-]
[# endif #]

[# if doc.bibliography #]
#bibliography("[- doc.bibliography | join(", ") -]", title: "Referencias", style: "apa")
[# endif #]
