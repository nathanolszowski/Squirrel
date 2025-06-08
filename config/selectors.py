# -*- coding: utf-8 -*-
"""
Sélecteurs CSS pour chacun des sites à scraper
"""

BNP_SELECTORS = {
    "reference": "#presentation > div > div.col.s12.offer-hero--left > div.offer-hero--left--middle > div.line.space-between.share-businessid-line.hidden-mobile.hidden-tablet > div.line.mobile-column > div.business-id > p",
    "contrat": "None",
    "actif": "None",
    "disponibilite": "#columns-container > div:nth-child(1) > ul > li > p > span",
    "surface": "#presentation > div > div.col.s12.offer-hero--left > div.offer-hero--left--middle > div.surface-block.line.no-padding.flex-column > div.surface > p > span:nth-child(1)",
    "division": "#presentation > div > div.col.s12.offer-hero--left > div.offer-hero--left--middle > div.surface-block.line.no-padding.flex-column > div.surface > p > span.divisible",
    "adresse": "#presentation > div > div.col.s12.offer-hero--left > div.offer-hero--left--middle > div.commercial-title > h1 > p",
    "nom_immeuble": "#presentation > div > div.col.s12.offer-hero--left > div.offer-hero--left--middle > div.commercial-title > h1 > span:nth-child(2)",
    "contact": "#block-bnpre-content > article > div.node__content.clearfix > div.offer-content > div > div.col.s12.l5.xl4.offer-content--right > div > div.card.card-contact > div > div:nth-child(2) > p.h3",
    "accroche": "#description > div > p:nth-child(3)",
    "amenagements": "#columns-container",
    "url_image" : "None",
    "latitude": "None",
    "longitude": "None",
    "prix_global": "#presentation > div > div.col.s12.offer-hero--left > div.offer-hero--left--bottom.hidden-mobile > div > div.block-budget.line.align-center.vente.active > div > p > span",
    "loyer_global": "#presentation > div > div.col.s12.offer-hero--left > div.offer-hero--left--bottom.hidden-mobile > div > div.block-budget.line.align-center.location.active > div > p > span",
}

JLL_SELECTORS = {
    "reference": "#propertySummary > div > div.col-span-12.lg\\:col-span-10 > div > div.flex.items-center.justify-between.gap-4.max-\\[575px\\]\\:flex-col-reverse > div.flex.items-center.justify-center.gap-4.max-\\[575px\\]\\:flex-col-reverse > span",
    "contrat": "None",
    "actif": "None",
    "disponibilite": "#propertySummary > div > div.col-span-12.lg\\:col-span-10 > div > div.mt-4.flex.items-start.sm\\:mt-9 > div.flex-1.\\[\\&\\:not\\(\\:last-child\\)\\]\\:mr-11 > ul > li:nth-child(2) > span.text-lg.text-neutral-700",
    "surface": "#propertySummary > div > div.col-span-12.lg\\:col-span-10 > div > div.mt-4.flex.items-start.sm\\:mt-9 > div.flex-1.\\[\\&\\:not\\(\\:last-child\\)\\]\\:mr-11 > ul > li:nth-child(1) > span.text-lg.text-neutral-700 > span > span:nth-child(1)",
    "division": "#propertySummary > div > div.col-span-12.lg\\:col-span-10 > div > div.mt-4.flex.items-start.sm\\:mt-9 > div.flex-1.\\[\\&\\:not\\(\\:last-child\\)\\]\\:mr-11 > ul > li:nth-child(1) > span.text-lg.text-neutral-700 > span > span:nth-child(1) > span",
    "adresse": "head > title",
    "contact": "#propertySummary > div > div.col-span-12.lg\\:col-span-10 > div > div.mt-4.flex.items-start.sm\\:mt-9 > div.inline-flex.items-center.justify-center.whitespace-nowrap.rounded.text-sm.font-semibold.ring-offset-white.transition-colors.focus-visible\\:outline-none.focus-visible\\:ring-2.focus-visible\\:ring-neutral-950.focus-visible\\:ring-offset-2.disabled\\:pointer-events-none.disabled\\:opacity-50.text-neutral-900.underline-offset-4.hover\\:underline.h-9.px-4.py-1.\\!justify-start.\\!no-underline.mb-1.h-full.w-full.\\!rounded-md.border.bg-white.px-4.py-3.hover\\:bg-white.hover\\:shadow-md.hidden.max-w-44.cursor-pointer.lg\\:block > div.overflow-hidden.text-left > p.overflow-hidden.text-ellipsis.text-base.font-bold",
    "accroche": "#description > div > div > p",
    "amenagements": "#amenities > div > ul",
    "prix_global": "#propertySummary > div > div.col-span-12.lg\\:col-span-10 > div > div.mt-4.flex.items-start.sm\\:mt-9 > div.flex-1.\\[\\&\\:not\\(\\:last-child\\)\\]\\:mr-11 > div.mb-6.flex.flex-col.flex-wrap.items-center.justify-between.text-center.sm\\:flex-row.sm\\:text-left > div.flex.items-center.justify-end.text-bronze.\\[\\&_p\\]\\:text-2xl.\\[\\&_p\\]\\:font-semibold > p",
}
CBRE_SELECTORS = {
    "reference": "None",
    "contrat": "None",
    "actif": "None",
    "disponibilite": "#contentHolder_availability",
    "surface": "#contentHolder_surface",
    "division": "#contentHolder_surfaceDiv",
    "adresse": "#contentHolder_address1",
    "contact": "#contentHolder_contactZone.row.contact-person > div.col-9.info > p:nth-child(2)",
    "accroche": "#section-description > p:nth-child(3)",
    "amenagements": "#section-feature > div > div:nth-child(1) > p",
    "prestations": "#contentHolder_featureZone > ul",
    "url_image" : "None",
    "latitude": "None",
    "longitude": "None",
    "prix_global": "#contentHolder_price",
}

ALEXBOLTON_SELECTORS = {
    "reference": "body > section.listing-header.py-md-4 > div > div > div.col-lg-5.position-relative > div > div.bolton-header-5.bolton-grey.mb-2",
    "contrat": "body > section.listing-header.py-md-4 > div > div > div.col-lg-5.position-relative > div > div.d-flex.gap-4.mb-4 > div:nth-child(1) > p:nth-child(1)",
    "actif": "None",
    "disponibilite": "body > section.listing-header.py-md-4 > div > div > div.col-lg-5.position-relative > div > div.d-flex.gap-4.mb-4 > div:nth-child(2) > p:nth-child(2)",
    "surface": "body > section.listing-header.py-md-4 > div > div > div.col-lg-5.position-relative > div > div.d-flex.gap-4.mb-4 > div:nth-child(1) > p:nth-child(4)",
    "division": "None",
    "adresse": "body > section.listing-header.py-md-4 > div > div > div.col-lg-5.position-relative > div > div.bolton-header-4.mb-4",
    "nom_immeuble": "body > section.listing-header.py-md-4 > div > div > div.col-lg-5.position-relative > div > h1",
    "accroche": "None",
    "contact": "body > section.listing-details.bolton-bg-grey.u-py-80.u-py-mobile-24 > div > div > div.col-lg-4.position-relative > div > h3",
    "amenagements": "body > section.listing-details.bolton-bg-grey.u-py-80.u-py-mobile-24 > div > div > div.col-lg-8 > div.d-flex > div > div.listing-details-description.mb-3",
    "url_image" : "None",
    "latitude": "None",
    "longitude": "None",
    "prix_global": "body > section.listing-header.py-md-4 > div > div > div.col-lg-5.position-relative > div > div.d-flex.gap-4.mb-4 > div:nth-child(1) > p:nth-child(2)",
}

CUSHMAN_SELECTORS = {
    "reference": "#js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(1) > div > header > p.u-t.u-t--sm.u-t-additional",
    "contrat": "None",
    "actif": "#js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(1) > div > header > p.c-property__category",
    "contrat": "#js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(1) > div > header > p.c-property__category",
    "disponibilite": "js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(1) > div > div:nth-child(3) > p:nth-child(3) > span.u-t--tertiary",
    "surface": "#js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(1) > div > div:nth-child(3) > p:nth-child(1) > span.u-t--tertiary",
    "division": "None",
    "adresse": "#js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(1) > div > header > h1",
    # On peut utiliser le span pour séparer nom et prénom
    "contact": "#js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(1) > div > div:nth-child(4) > div > div > div.c-contact__main > h5",
    "accroche": "#js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(2) > div > section:nth-child(5) > p",
    "amenagements": "#js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(2) > div > section:nth-child(7) > ul",
    "url_image" : "None",
    "latitude": "None",
    "longitude": "None",
    "prix_global": "#js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(1) > div > div:nth-child(3) > div > div > p > span.u-t--tertiary",
}

KNIGHTFRANK_SELECTORS = {
    "reference": "body > main > section > div.container.p-lg-0.contOMob > div > div.col-xl-7.p-xl-0.p-0 > div:nth-child(1) > div > ol > li:nth-child(5) > a > span",
    "contrat": "None",
    "actif": "None",
    "disponibilite": "body > main > section > div.container.p-lg-0.contOMob > div > div.col-xl-7.p-xl-0.p-0 > div.row.pb-4.align-items-center.p24 > div.col-xl-4.col-md-4.col-12.cDisp > div > p",
    "surface": "body > main > section > div.container.p-lg-0.contOMob > div > div.col-xl-7.p-xl-0.p-0 > div.row.pb-4.align-items-center.p24 > div.col-xl-4.col-md-4.col-auto.pe-0 > div > p.valeur-offre",
    "division": "body > main > section > div.container.p-lg-0.contOMob > div > div.col-xl-7.p-xl-0.p-0 > div.row.pb-4.align-items-center.p24 > div.col-xl-4.col-md-4.col-auto.pe-0 > div > p.post-text-offre > span",
    "adresse": "None",
    "contact": "body > main > section > div.container.p-lg-0.contOMob > div > div.d-none.col-xl-3.offset-xl-1.p-xl-0.pt-xl-4.pt-4.d-xl-flex.relative.p24 > div > div.blocAgent > div > div.offset-1.col-7.p-0.d-flex.flex-column.justify-content-center.ml-3 > p",
    "accroche": "body > main > section > div.container.p-lg-0.contOMob > div > div.col-xl-7.p-xl-0.p-0 > div:nth-child(4) > div > p.offreDesc",
    "amenagements": "body > main > section > div.container.p-lg-0.contOMob > div > div.col-xl-7.p-xl-0.p-0 > div:nth-child(8) > div > div > ul",
    "url_image" : "None",
    "latitude": "None",
    "longitude": "None",
    "prix_global": "body > main > section > div.container.p-lg-0.contOMob > div > div.col-xl-7.p-xl-0.p-0 > div.row.pb-4.align-items-center.p24 > div.col-xl-4.col-md-4.col-auto.ps-0 > div > p.valeur-offre",
}

ARTHURLOYD_SELECTORS = {
    "reference": "#advisor-brick-wrapper > div > div:nth-child(1) > div.offer-informations.d-flex.align-items-center.justify-content-between > div.reference > b",
    "contrat": "None",
    "actif": "None",
    "disponibilite": "#advisor-brick-wrapper > div > div:nth-child(1) > div:nth-child(3) > div > ul > li:nth-child(2) > span:nth-child(2)",
    "surface": "#details-desktop > div > div.col-xl-2.d-none.d-xl-block.text-end > div > div > a > div.max-surface > span",
    "division": "#details-desktop > div > div.col-xl-2.d-none.d-xl-block.text-end > div > div > a > div.d-flex.justify-content-end.min-surface > div:nth-child(1) > span.surface",
    "adresse": "#localisation > div",
    "titre": "#advisor-brick-wrapper > div > div:nth-child(1) > div.offer-title",
    "contact": "#advisor-brick-wrapper > div > div.advisor-card > div > div > div.advisor-informations > div > div:nth-child(1) > div:nth-child(1) > span",
    "accroche": "#description > div > div > div > div > div:nth-child(2) > p",
    "amenagements": "#amenities > section > div > div > div:nth-child(1) > div > ul",
    "url_image" : "None",
    "latitude": "None",
    "longitude": "None",
    "prix_global": "#advisor-brick-wrapper > div > div:nth-child(1) > div:nth-child(3) > div > ul > li:nth-child(3) > span.price",
}

""" Ajouter les sélecteurs pour les autres sites
EXEMPLE_SELECTORS = {
    "reference": "None",
    "contrat": "None",
    "actif": "None",
    "disponibilite": "None",
    "surface": "None",
    "division": "None",
    "adresse": "None",
    "contact": "None",
    "accroche": "None",
    "amenagements": "None",
    "prix_global": "None"
}
"""
