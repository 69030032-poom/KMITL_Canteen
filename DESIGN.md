# KMITL Canteen UI

Approved direction: original orange desktop layout, warm cream background and faint canteen line illustration.

- Customer: menu list in the centre, independent option panel on the right. Price and add action remain outside the scrolling options. Shop cart summary remains visible.
- Merchant: order list on the left, selected order on the right, status action fixed below details. Filters and selected order survive automatic updates.
- Narrow windows show one menu column; wider menu areas show two. Minimum window 900x600 logical pixels.
- Palette: orange #C94716, hover #A93810, cream #FFF8F0, peach #FCE6D7, text #28231F, muted #6F6258, border #E9DED3.
- Menu images are AI-generated illustrations, labeled as illustrations in the app; they are not photographs supplied by the shops.
- Hide nonfunctional search and favorites. No new merchant menu-management feature is implied by the visual draft.
- Actual data and access rules remain in Backend and SQLite. UI is on branch ui.

## Background asset
assets/canteen_background.png was generated with the built-in image tool as a decorative illustration, not a real photo of the campus.
Prompt: Landscape warm ivory #FFF8F0 canvas, delicate very pale peach-orange architectural line art of a Thai university canteen pavilion, students at tables, trees, noodle bowl and cup; pavilion bottom left; upper area almost empty; subtle thin contours; no text, logos, buttons, shadows or gradients.

## Verification
20 automated tests including customer noodle/drink choices, fixed action visibility, cart navigation, merchant filters/status changes and original backend regression cases. Actual Windows screenshots inspected at 1000x680 logical pixels. GUI tests use an isolated database and do not create real orders.
