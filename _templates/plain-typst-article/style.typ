// Plain two-column academic article style.
//
// Adapted from the "cellpress-unofficial" Typst template by Robin Eklind
// (https://github.com/mewmew/cellpress-unofficial, 0BSD license). The Cell
// Press logo and fixed journal branding (Elsevier/Cell Press trademarks)
// have been removed so this can be used as a generic, unbranded two-column
// article layout.

#let font-sans-serif = "Helvetica Neue"

// Colours (kept from the source template, renamed to be brand-neutral).
#let zebra-gray  = rgb(luma(95.25%))
#let accent-red   = rgb("#a93b45")
#let accent-blue  = rgb("#0296d3")
#let accent-grey  = rgb("#b3b3b3")
#let summary-blue = rgb("#0a2f5c")

// mystmd's LaTeX-to-Typst math converter emits the bare identifier `diff`
// for \partial, which is not a builtin symbol in current Typst releases.
// Shim it so partial-derivative equations compile.
#let diff = "∂"

// --- [ tables ] --------------------------------------------------------------

#let toprule(color: accent-red) = {
	table.hline(stroke: 0.7pt + color)
}

#let bottomrule(color: accent-red) = {
	table.hline(stroke: 0.7pt + color)
}

#let midrule(color: accent-red) = {
	table.hline(stroke: 0.5pt + color)
}

#let tabsubhdr(content, colspan: 3, color: accent-red) = table.header(
	level: 2,
	table.cell(
		colspan: colspan,
		inset: (y: 5pt),
		fill: none,
		{
			set text(fill: color)
			show text: emph
			content
		}
	)
)

#let style-table(body) = {
	show figure.where(kind: table): set figure.caption(position: top, separator: [. ])
	show figure.where(kind: table): set block(breakable: true, above: 14pt, below: 14pt)
	show figure.where(kind: table): outer => {
		show figure.caption: it => align(
			center,
			[
				#strong[#it.supplement #context it.counter.display(it.numbering)#it.separator]
				#it.body
			]
		)
		outer
	}
	show table: set table(
		stroke: none,
		align: left,
		columns: 1fr,
		fill: (_, y) => {
			if y != 0 and not calc.odd(y) {
				zebra-gray
			}
		},
		inset: (x, y) => {
			let y_pad = 3pt
			if y == 0 {
				y_pad = 4pt
			}
			(x: 2.5pt, y: y_pad)
		}
	)
	show table: set text(size: 6pt)
	show table.cell.where(y: 0): it => {
		show text: strong
		set text(fill: accent-red)
		it
	}

	body
}

// --- [ template ] ------------------------------------------------------------

// summary displays a floating highlighted box (used for the abstract).
#let summary(title: "Summary", body) = {
	place(
		top,
		float: true,
		scope: "parent",
	)[
		#v(2mm)
		#heading(level: 1, outlined: false)[#title]
		#set text(font: font-sans-serif, size: 9.9pt, weight: "semibold", fill: summary-blue)
		#set par(
			leading: 0.33em,
		)
		#block(below: 3mm, body)
	]
}

#let print-supertitle(supertitle) = {
	set text(font: font-sans-serif, size: 13.9pt, weight: "extrabold", tracking: -0.1pt, fill: accent-grey)
	block(scale(origin: left+horizon, x: 110%)[#supertitle])
}

#let print-title(title) = {
	set text(font: font-sans-serif, size: 20pt, weight: "bold", tracking: -0.5pt)
	set par(
		justify: false,
		leading: 0.33em,
	)
	block(width: 75%, title)
}

#let print-authors(authors) = {
	let authors-str = authors
	if type(authors) == array {
		authors-str = authors.join(", ", last: " and ")
	}
	set text(font: font-sans-serif, size: 9pt, weight: "semibold")
	block(scale(origin: left+horizon, x: 97%)[#authors-str])
}

#let print-affiliations(affiliations) = {
	let affiliations-str = affiliations
	if type(affiliations) == array {
		affiliations-str = affiliations.join(" · ")
	}
	set text(font: font-sans-serif, size: 7.5pt, fill: accent-grey)
	block(affiliations-str)
}

#let print-doi(doi) = {
	set text(font: font-sans-serif, size: 7.9pt)
	block(link("https://doi.org/" + doi))
}

// template applies the plain single-column article format to the document.
// `journal` and `supertitle` are optional small masthead labels (no logo,
// no fixed publisher branding) shown in the page header.
#let template(
	journal:      none,
	supertitle:   "Cuaderno reproducible",
	title:        "Paper Title",
	authors:      ("John Doe", "Jane Rue"),
	affiliations: none,
	doi:          none,
	date:         datetime.today(),
	body
) = {
	set page(
		width: 8.5in,
		height: 11in,
		margin: (
			left: 2.5cm,
			right: 2.5cm,
			top: 3.555cm,
			bottom: 2.5cm,
		),
		columns: 1,
		header: context {
			if journal != none {
				grid(
					columns: (1fr, 1fr),
					align: (left, right),
					[
						#block(text(font: font-sans-serif, size: 19pt, weight: "bold", tracking: -1pt, fill: accent-blue)[#journal])
					],
					[],
				)
			}
		},
		header-ascent: 20%,
	)
	set par(justify: true)
	set text(font: font-sans-serif, size: 8.4pt)

	show ref: set text(fill: accent-blue)
	show link: set text(fill: accent-blue)
	show cite: set text(fill: accent-blue)
	show footnote: set text(fill: accent-blue)

	show: style-table

	show heading.where(level: 1): it => {
		set text(font: font-sans-serif, size: 8.4pt, weight: "extrabold", tracking: -0.2pt, fill: accent-red)
		set block(below: 0.55cm)
		scale(origin: left+horizon, x: 110%)[#upper(it)]
	}
	show heading.where(level: 2): it => {
		set text(font: font-sans-serif, size: 8.4pt, weight: "extrabold", tracking: -0.2pt, fill: accent-red)
		set block(below: 0.55cm)
		scale(origin: left+horizon, x: 110%)[#it]
	}

	place(
		top+left,
		scope: "parent",
		float: true,
	)[
		#print-supertitle(supertitle)
		#v(-6.5mm)
		#print-title(title)
		#v(-2mm)
		#print-authors(authors)
		#if affiliations != none {
			print-affiliations(affiliations)
		}
		#if doi != none {
			print-doi(doi)
		}
	]

	body
}
