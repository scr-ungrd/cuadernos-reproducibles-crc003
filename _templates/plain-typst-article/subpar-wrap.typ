// Wrapper of the `subpar` package used by mystmd for tables/figures with a
// legend: it emits `subpar.grid(table, text(..legendStyle)[legend], ...)`, which
// centers everything. This module exposes a `grid` with the same interface that
// left-aligns the legend and brings it close to the table.
#import "@preview/subpar:0.2.2" as _subpar

#let grid(..args) = _subpar.grid(
  ..args.named(),
  grid-styles: it => {
    set std.grid(gutter: 3pt)
    it
  },
  ..args.pos().map(item => // `text(..legendStyle)[..]` is a "styled" element (it carries text set rules);
  // the table (a wrapped `tablex` block) goes through the same path harmlessly.
  if type(item) == content and repr(item.func()) == "styled" {
    block(width: 100%, {
      set par(justify: false)
      align(left, item)
    })
  } else { item }),
)
