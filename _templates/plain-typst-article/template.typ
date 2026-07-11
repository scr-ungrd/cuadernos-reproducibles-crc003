#import "style.typ": template, summary, diff

#show: template.with(
  title: "[-doc.title-]",
  authors: ("[# for author in doc.authors #][-author.name-][# if not loop.last #], [# endif #][# endfor #]",),
[# if doc.affiliations #]
  affiliations: "[# for affiliation in doc.affiliations #][-affiliation.value.name-][# if not loop.last #] · [# endif #][# endfor #]",
[# endif #]
[# if doc.doi #]
  doi: "[-doc.doi-]",
[# endif #]
  supertitle: "Cuaderno reproducible",
)

[-IMPORTS-]

[# if parts.abstract #]
#summary(title: "Resumen")[
[-parts.abstract-]
]
[# endif #]

[# if parts.keypoints #]
== Puntos Clave
#list(
[# for keypoint in parts.keypoints #]
  [[-keypoint-]],
[# endfor #]
)
[# endif #]

[-CONTENT-]

[# if parts.data_availability #]
== Disponibilidad de Datos
[-parts.data_availability-]
[# endif #]

[# if doc.bibliography #]
#bibliography("[- doc.bibliography | join(", ") -]", title: "References", style: "apa")
[# endif #]
