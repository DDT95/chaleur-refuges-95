# Design QA

- Source visual truth: `reference-template.png` (carte Nature · adaptation existante)
- Implementation: `implementation-desktop.png`
- Atlas integration: `atlas-understand-desktop.png`
- Viewport: 1280 × 720 CSS px, device pixel ratio 2
- Source pixels: 1440 × 900 capture; implementation pixels: 1440 × 900 capture
- State: carte chargée, aléa de jour actif, trois familles de refuges actives

## Full-view comparison evidence

The implementation preserves the source composition: 104 px institutional header, fixed left reading panel, rounded map shell, top-right legend, bottom-left status, and right-side detail drawer. The new heat palette and point markers are intentional thematic substitutions. The Atlas integration shows seven cards in a four-column grid, producing two rows with reduced visual headers.

## Focused comparison evidence

Focused checks covered the header/logo lockup, sidebar cards and switches, map legend, status chip, commune detail drawer, and Atlas “Comprendre” grid. No additional crop was required because these surfaces remain readable in the desktop captures.

## Required fidelity surfaces

- Fonts and typography: Marianne assets and the source hierarchy are preserved; headings, labels and small metadata wrap without clipping.
- Spacing and layout rhythm: header, 330 px sidebar, map shell, 18–27 px radii and panel spacing match the existing template.
- Colors and tokens: institutional navy remains dominant; heat red/orange, night violet, refuge green/blue and water cyan are semantic and contrast sufficiently.
- Image and asset fidelity: the official Préfet du Val-d’Oise vector asset is reused unchanged. The cartography uses source data layers rather than decorative placeholder imagery.
- Copy and content: all user-facing text distinguishes modeled heat risk from measured temperature and labels refuges as potential resources requiring local verification.

## Interaction and console checks

- heatmap day/night switch: passed;
- heatmap masking: present;
- three refuge filters: passed on initial render;
- commune search and Pontoise detail drawer: passed;
- departmental synthesis and methodology dialogs: present and wired;
- map loads 5,938 cells and 927 potential resources after the public-access filter;
- browser console errors on clean load: none;
- Atlas build and seven-card grid: passed.

## Comparison history

1. P1: the initial heat layer called an unsupported `bringToBack` method, stopping markers, commune geometry and interaction binding. Fix: removed the unsupported call. Post-fix evidence: clean browser load, populated markers, working search/detail drawer and no console errors.
2. P2: the previous six-card Atlas layout could not accommodate the seventh entry as requested. Fix: changed the desktop grid to four columns, reduced visual header height and card density. Post-fix evidence: `atlas-understand-desktop.png` shows four cards on the first row and three on the second.
3. P1: point-based heat rendering produced isolated halos and kernel artefacts, while the first polygon pass lacked an explanatory legend. Fix: point heat rendering was removed entirely. Every scale now uses the 28,105 official morphoclimatic islands with a stable six-class blue-to-red palette and a labelled legend. Post-fix evidence: `implementation-desktop.png` and `implementation-zoom.png` show the same graphic language before and after four zoom levels, with no console errors.
4. P1: generic OSM swimming-pool geometries included residential pools. Fix: private/forbidden access is excluded globally and pools now require a name plus an explicit public, customer/member or operator signal. The resource set fell from 2,370 to 927, including one documented pool.

## Follow-up polish

- The in-app browser did not honor its temporary mobile viewport override during this run; mobile behavior relies on the inherited, already-used 700 px breakpoint from the reference template and should receive a device check in a later polish pass.

final result: passed
