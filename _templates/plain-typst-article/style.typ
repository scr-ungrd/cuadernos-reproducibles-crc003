// Plain academic article style (unbranded).
//
// Adapted from the "cellpress-unofficial" Typst template by Robin Eklind
// (https://github.com/mewmew/cellpress-unofficial, 0BSD license). The Cell
// Press logo and fixed journal branding (Elsevier/Cell Press trademarks)
// have been removed so this can be used as a generic, unbranded article
// layout.
//
// Page design: accent bar on top of every page, running header, footer with
// page number, sans-serif text throughout (Liberation Sans) and a single
// accent colour (links keep their own blue).

// Font. "Liberation Sans" is installed explicitly in CI (fonts-liberation) so
// the PDF renders the same locally and on GitHub Actions.
#let font-sans-serif = "Liberation Sans"

// Colours: one accent (bar, rules, headings), one link colour, neutral greys.
#let accent       = rgb("#0a2f5c")
#let link-blue    = rgb("#0296d3")
#let neutral-gray = luma(45%)
#let rule-gray    = luma(80%)
#let heading-red  = rgb("#a93b45") // section headings
#let header-fill  = luma(87%) // table header row
#let zebra-fill   = luma(94%) // alternate table rows
#let dark-rule    = luma(15%) // heavy rules of tables
#let code-fill    = rgb("#f1f4f9") // soft tint of the accent, for code cells

// mystmd's LaTeX-to-Typst math converter emits the bare identifier `diff`
// for \partial, which is not a builtin symbol in current Typst releases.
// Shim it so partial-derivative equations compile.
#let diff = "∂"

// --- [ tables ] --------------------------------------------------------------

#let toprule(color: accent) = {
	table.hline(stroke: 0.7pt + color)
}

#let bottomrule(color: accent) = {
	table.hline(stroke: 0.7pt + color)
}

#let midrule(color: accent) = {
	table.hline(stroke: 0.5pt + color)
}

#let tabsubhdr(content, colspan: 3, color: accent) = table.header(
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

// Table design (after Nature Reviews "Table 3"): a thin rule above the bold
// caption, grey header row in bold, alternate rows in light grey with no lines
// between rows, top-aligned small sans-serif text and a thin closing rule.
// The caption itself is styled by the generic `figure.caption` rule in
// `template` (shared with figures).
#let style-table(body) = {
	// mystmd emits captioned tables as `figure(kind: "table")` (a string), Typst's
	// own tables as `kind: table`; handle both.
	show figure.where(kind: "table"): set figure.caption(position: top)
	show figure.where(kind: table): set figure.caption(position: top)
	show figure.where(kind: "table"): set block(breakable: true, above: 14pt, below: 14pt)
	// Table, title and legend are left-aligned (a figure centers its body).
	show figure.where(kind: "table"): it => {
		show align: a => if a.alignment == left { a } else { align(left, a.body) }
		it
	}
	show figure.where(kind: table): set block(breakable: true, above: 14pt, below: 14pt)
	show table: set table(
		columns: 1fr,
		align: left + top,
		fill: (_, y) => if y == 0 { header-fill } else if calc.even(y) { zebra-fill },
		stroke: none,
		inset: (x: 5pt, y: 4pt),
	)
	show table: set text(font: font-sans-serif, size: 7.5pt)
	show table: set par(justify: false)
	show table.cell.where(y: 0): set text(weight: "bold")
	show table: it => block(
		width: 100%,
		stroke: (bottom: 0.75pt + dark-rule),
		// Inset keeps the cell fills from painting over the closing rule.
		inset: (bottom: 1pt),
		it,
	)

	body
}

// Legend (notes) under a table, like the notes of a Nature table: small and
// plain. mystmd emits it as `text(..legendStyle)[...]` below the table.
#let legendStyle = (size: 6.5pt, fill: black, style: "normal")

// Same table design for tables that mystmd emits through `tablex` (named
// arguments spread into every `tablex(...)` call by the generated document).
#let tableStyle = (
	width: 100%,
	align: left + top,
	inset: (x: 5pt, y: 4pt),
	auto-lines: false,
)

// Completes the arguments of a `tablex(...)` call: equal-width columns so the
// table spans the text width, and header/zebra fills and bold header text that
// respect the number of header rows (`header-rows`).
#let tablex-args(named) = {
	let named = named
	let cols = named.at("columns", default: none)
	if type(cols) == int { named.insert("columns", (1fr,) * cols) }
	let hr = named.at("header-rows", default: 1)
	named.insert("fill", (_, row) => if row < hr { header-fill } else if calc.odd(row - hr) { zebra-fill })
	named.insert("map-rows", (row, cells) => cells.map(c => if c == none { c } else if row < hr {
		(..c, content: strong(c.content))
	} else { c }))
	named
}

// Wraps a `tablex` call: small sans-serif text and a thin closing rule.
#let wrap-table(tbl) = {
	set text(font: font-sans-serif, size: 7.5pt)
	set par(justify: false)
	block(
		width: 100%,
		above: 1em,
		below: 1em,
		stroke: (bottom: 0.75pt + dark-rule),
		inset: (bottom: 1pt),
		tbl,
	)
}

// --- [ template ] ------------------------------------------------------------

// Horizontal page margins and the resulting text width.
#let margin-left  = 3.5cm
#let margin-right = 3.5cm
#let text-width   = 8.5in - margin-left - margin-right

// The page design follows the layout of a Nature Climate Change article
// (all vertical distances in pt, measured on that PDF): accent bar, journal
// masthead, "article type + DOI" row between hairlines, title, two-column
// front matter (metadata rows | authors + abstract), affiliations above the
// footer on page 1, and a "label + DOI" running header on later pages.
#let hairline = 0.35pt + black

#let months-es = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre")
#let fmt-date(d) = str(d.day) + " de " + months-es.at(d.month - 1) + " de " + str(d.year)
#let fmt-month-year(d) = months-es.at(d.month - 1) + " de " + str(d.year)

// Authors with superscript affiliation numbers, e.g. "A. Autor¹, B. Autora¹ˑ²".
#let author-line(authors, affiliations) = {
	let ids = affiliations.map(a => a.id)
	authors.map(a => {
		let idx = a.affs.map(id => str(ids.position(x => x == id) + 1))
		a.name
		if idx.len() > 0 { super(idx.join(",")) }
	}).join(", ", last: " y ")
}

// "¹Institution, department, city, country. ²…" for the footnote of page 1.
#let affiliation-text(affiliations) = affiliations.enumerate().map(((i, a)) => {
	let parts = (a.name, a.department, a.city, a.country).filter(x => x != "")
	super(str(i + 1)) + parts.join(", ") + "."
}).join(" ")

// Key points: list inside a box with the grey background of the "Highlights" box of a Cell Press article.
#let keypoints-fill = rgb("#ebebec")
#let keypoints-box(title: "Puntos clave", body) = block(
	width: 100%,
	fill: keypoints-fill,
	radius: 3pt,
	inset: (x: 8pt, y: 7pt),
	{
		set par(justify: false)
		set list(indent: 0pt, body-indent: 4pt, spacing: 0.7em)
		text(size: 8pt, weight: "extrabold", fill: heading-red)[#title]
		v(6pt)
		set text(size: 7.5pt)
		body
	},
)

#let print-doi(doi, size: 8pt) = {
	set text(font: font-sans-serif, size: size, fill: link-blue)
	link("https://doi.org/" + doi)
}

// Page 1 "masthead", drawn on the page background at absolute positions:
// accent bar, journal name and the "article type + DOI" row over a hairline.
#let page1-masthead(journal, supertitle, doi) = {
	set text(font: font-sans-serif)
	place(top + left, dx: margin-left, dy: 34pt, rect(width: text-width, height: 3.5pt, fill: heading-red, stroke: none))
	if journal != none {
		place(top + left, dx: margin-left, dy: 41pt, text(size: 14pt, weight: "bold", tracking: -0.2pt, top-edge: "ascender")[#journal])
	}
	place(top + left, dx: margin-left, dy: 95pt, block(width: text-width, grid(
		columns: (1fr, auto),
		align: bottom,
		text(size: 10pt, weight: "bold")[#supertitle],
		if doi != none { print-doi(doi) },
	)))
	place(top + left, dx: margin-left, dy: 109.1pt, line(length: text-width, stroke: hairline))
}

// Running header of pages 2+: label on the left, DOI on the right, hairline below.
#let print-header(supertitle, doi) = context {
	if counter(page).get().first() > 1 {
		set text(font: font-sans-serif)
		set block(spacing: 0pt)
		grid(
			columns: (1fr, auto),
			align: bottom,
			text(size: 10pt, weight: "bold")[#supertitle],
			if doi != none { print-doi(doi) },
		)
		v(6.6pt)
		line(length: 100%, stroke: hairline)
	}
}

// Footer: hairline, "journal | report id (links to the repo) | date" on the left,
// bold page number on the right.
#let print-footer(journal, report-id, date, github) = {
	set text(font: font-sans-serif, size: 8pt)
	set block(spacing: 0pt)
	line(length: 100%, stroke: hairline)
	v(7pt)
	let parts = ()
	if report-id != none {
		// The report id links to the GitHub repository when its URL is known.
		parts.push(if github != none { link(github, text(fill: link-blue)[#report-id]) } else { report-id })
	}
	if date != none { parts.push(fmt-month-year(date)) }
	grid(
		columns: (1fr, auto),
		align: (left, right),
		{
			if journal != none { text(fill: heading-red)[#journal] }
			for p in parts [ | #p]
		},
		strong(context counter(page).display()),
	)
}

// front-page places the page-1 front matter: title between hairlines, then two
// columns (metadata rows + key points | abstract + keywords), and
// the affiliations footnote at the bottom of the page.
#let front-page(
	title:           "",
	authors:         (),
	affiliations:    (),
	date:            none,
	license-content: none,
	license-code:    none,
	github:          none,
	abstract:        none,
	keywords:        (),
	keypoints:       none,
	..args,
) = {
	let left-w = 0.319 * text-width
	let gutter = 0.022 * text-width
	let row(body) = block(width: 100%, height: 19.7pt, stroke: (bottom: hairline), inset: (top: 5.3pt), body)

	place(top + left, float: true, scope: "parent", clearance: 16pt)[
		#set par(justify: false)
		#set block(spacing: 0pt)
		// Title cap-height starts ~6 pt under the hairline of the masthead.
		#v(65.5pt)
		#block(width: 100%, {
			set text(font: font-sans-serif, size: 22pt, weight: "bold", tracking: -0.5pt)
			set par(leading: 8.25pt)
			title
		})
		// Authors right under the title, full width (as in Trends in Ecology & Evolution).
		#v(16pt)
		#text(size: 9pt, weight: "bold")[#author-line(authors, affiliations)]
		#v(21pt)
		#line(length: 100%, stroke: hairline)
		#grid(
			columns: (left-w, gutter, 1fr),
			{
				set text(size: 8pt, weight: "medium")
				if date != none { row[Publicado: #fmt-date(date)] }
				if license-content != none { row[Contenido: #license-content] }
				if license-code != none { row[Código: #license-code] }
				if github != none { row[#link(github)[Repositorio en GitHub]] }
				if keypoints != none {
					v(12pt)
					keypoints-box(title: "Puntos clave", keypoints)
				}
			},
			[],
			{
				v(5.3pt)
				if abstract != none {
					set text(size: 9.5pt)
					set par(leading: 6.5pt)
					abstract
				}
				if keywords.len() > 0 {
					v(8pt)
					text(size: 8pt)[*Palabras clave:* #keywords.join(" · ")]
				}
			},
		)
	]

	place(bottom + left, float: true, clearance: 10pt)[
		#set par(justify: false)
		#set block(spacing: 0pt)
		#line(length: 100%, stroke: hairline)
		#v(2pt)
		#text(size: 7.5pt)[#affiliation-text(affiliations)]
	]
}

// template applies the article format to the document: page geometry,
// masthead / header / footer, and the text, caption, code and heading styles.
#let template(
	journal:      none,
	supertitle:   "Cuaderno reproducible",
	report-id:    none,
	title:        "Paper Title",
	authors:      (),
	affiliations: (),
	doi:          none,
	date:         none,
	github:       none,
	..args,
	body
) = {
	set page(
		width: 8.5in,
		height: 11in,
		margin: (
			left: margin-left,
			right: margin-right,
			top: 49.5pt,
			bottom: 45pt,
		),
		columns: 1,
		background: context {
			if counter(page).get().first() == 1 { page1-masthead(journal, supertitle, doi) }
		},
		header: print-header(supertitle, doi),
		header-ascent: 11pt,
		footer: print-footer(journal, report-id, date, github),
		footer-descent: 8.6pt,
	)
	set par(justify: true)
	set text(font: font-sans-serif, size: 8.4pt, lang: "es")

	show ref: set text(fill: link-blue)
	show link: set text(fill: link-blue)
	show cite: set text(fill: link-blue)
	show footnote: set text(fill: link-blue)

	show: style-table

	// Captions for figures and tables: "Figura 1 | text" / "Tabla 1 | text",
	// sans-serif, small, left-aligned, only the label in bold.
	show figure.caption: it => {
		set align(left)
		if it.kind == table or it.kind == "table" {
			// Table titles: bold, one block under a thin rule (like Nature "Table 3").
			set text(font: font-sans-serif, size: 8.5pt, weight: "bold")
			set par(leading: 0.45em, justify: false)
			block(
				width: 100%,
				above: 6pt,
				below: 6pt,
				stroke: (top: 0.75pt + dark-rule),
				inset: (top: 5pt),
			)[
				Tabla #context it.counter.display(it.numbering)#h(0.3em)|#h(0.3em)#it.body
			]
		} else {
			set text(font: font-sans-serif, size: 7.5pt)
			set par(leading: 0.5em)
			let label = if it.kind == image or it.kind == "figure" { [Figura] } else { it.supplement }
			block(width: 100%, above: 6pt, below: 6pt)[
				#strong[#label #context it.counter.display(it.numbering)]#h(0.3em)|#h(0.3em)#it.body
			]
		}
	}

	// Other fenced blocks (e.g. the Stack box, lang "text") get a soft tinted
	// background and no side bar.
	show raw.where(block: true): it => if it.lang == "python" or it.lang == none {
		// The PDF omits the code cells (lang "python") and their text outputs
		// (no lang); both are available in the web version.
		none
	} else {
		let is-code = it.lang != none
		block(
			width: 100%,
			fill: if is-code { code-fill },
			stroke: if is-code { none } else { (left: 2pt + rule-gray) },
			inset: (left: 8pt, right: 6pt, y: 6pt),
			radius: if is-code { 2pt } else { (right: 2pt) },
			above: 0.9em,
			below: 0.9em,
			it,
		)
	}

	// All headings use the sans-serif face. Levels 1 and 2: space above 15.15 pt
	// (+50 % over the 10.1 pt paragraph spacing) and below 11.7 pt (-25 % of 15.6 pt).
	show heading: set text(font: font-sans-serif)
	show heading.where(level: 1): it => {
		set text(size: 8.4pt, weight: "extrabold", tracking: -0.2pt, fill: heading-red)
		set block(above: 15.15pt, below: 11.7pt)
		scale(origin: left+horizon, x: 110%)[#upper(it)]
	}
	show heading.where(level: 2): it => {
		set text(size: 8.4pt, weight: "extrabold", tracking: -0.2pt, fill: heading-red)
		set block(above: 15.15pt, below: 11.7pt)
		scale(origin: left+horizon, x: 110%)[#it]
	}
	show heading.where(level: 3): it => {
		set text(size: 9pt, weight: "bold")
		set block(above: 1em, below: 0.5em)
		it
	}

	body
}
