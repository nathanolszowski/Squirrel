# -*- coding: utf-8 -*-
"""
Sélecteurs CSS pour chaque site
"""

BNP_SELECTORS = {
    "reference": "#presentation > div > div.col.s12.offer-hero--left > div.offer-hero--left--middle > div.line.space-between.share-businessid-line.hidden-mobile.hidden-tablet > div.line.mobile-column > div.business-id > p",
    "disponibilite": "#columns-container > div:nth-child(1) > ul > li > p > span",
    "surface": "#presentation > div > div.col.s12.offer-hero--left > div.offer-hero--left--middle > div.surface-block.line.no-padding.flex-column > div.surface > p > span:nth-child(1)",
    "division": "#presentation > div > div.col.s12.offer-hero--left > div.offer-hero--left--middle > div.surface-block.line.no-padding.flex-column > div.surface > p > span.divisible",
    "adresse": "#presentation > div > div.col.s12.offer-hero--left > div.offer-hero--left--middle > div.commercial-title > h1 > p",
    "nom_immeuble" : "#presentation > div > div.col.s12.offer-hero--left > div.offer-hero--left--middle > div.commercial-title > h1 > span:nth-child(2)",
    "contact": "#block-bnpre-content > article > div.node__content.clearfix > div.offer-content > div > div.col.s12.l5.xl4.offer-content--right > div > div.card.card-contact > div > div:nth-child(2) > p.h3",
    "accroche": "#description > div > p:nth-child(3)",
    "amenagements": "#columns-container",
    "prix_global" : "#presentation > div > div.col.s12.offer-hero--left > div.offer-hero--left--bottom.hidden-mobile > div > div.block-budget.line.align-center.vente.active > div > p > span",
    "loyer_global": "#presentation > div > div.col.s12.offer-hero--left > div.offer-hero--left--bottom.hidden-mobile > div > div.block-budget.line.align-center.location.active > div > p > span"
}

JLL_SELECTORS = {
    "reference": "#propertySummary > div > div.col-span-12.lg\\:col-span-10 > div > div.flex.items-center.justify-between.gap-4.max-\\[575px\\]\\:flex-col-reverse > div.flex.items-center.justify-center.gap-4.max-\\[575px\\]\\:flex-col-reverse > span",
    "disponibilite": "#propertySummary > div > div.col-span-12.lg\\:col-span-10 > div > div.mt-4.flex.items-start.sm\\:mt-9 > div.flex-1.\\[\\&\\:not\\(\\:last-child\\)\\]\\:mr-11 > ul > li:nth-child(2) > span.text-lg.text-neutral-700",
    "surface": "#propertySummary > div > div.col-span-12.lg\\:col-span-10 > div > div.mt-4.flex.items-start.sm\\:mt-9 > div.flex-1.\\[\\&\\:not\\(\\:last-child\\)\\]\\:mr-11 > ul > li:nth-child(1) > span.text-lg.text-neutral-700 > span > span:nth-child(1)",
    "division": "#propertySummary > div > div.col-span-12.lg\\:col-span-10 > div > div.mt-4.flex.items-start.sm\\:mt-9 > div.flex-1.\\[\\&\\:not\\(\\:last-child\\)\\]\\:mr-11 > ul > li:nth-child(1) > span.text-lg.text-neutral-700 > span > span:nth-child(1) > span",
    "adresse": "head > title",
    "contact": "#propertySummary > div > div.col-span-12.lg\\:col-span-10 > div > div.mt-4.flex.items-start.sm\\:mt-9 > div.inline-flex.items-center.justify-center.whitespace-nowrap.rounded.text-sm.font-semibold.ring-offset-white.transition-colors.focus-visible\\:outline-none.focus-visible\\:ring-2.focus-visible\\:ring-neutral-950.focus-visible\\:ring-offset-2.disabled\\:pointer-events-none.disabled\\:opacity-50.text-neutral-900.underline-offset-4.hover\\:underline.h-9.px-4.py-1.\\!justify-start.\\!no-underline.mb-1.h-full.w-full.\\!rounded-md.border.bg-white.px-4.py-3.hover\\:bg-white.hover\\:shadow-md.hidden.max-w-44.cursor-pointer.lg\\:block > div.overflow-hidden.text-left > p.overflow-hidden.text-ellipsis.text-base.font-bold",
    "accroche": "#description > div > div > p",
    "amenagements": "#amenities > div > ul",
    "prix_global": "#propertySummary > div > div.col-span-12.lg\\:col-span-10 > div > div.mt-4.flex.items-start.sm\\:mt-9 > div.flex-1.\\[\\&\\:not\\(\\:last-child\\)\\]\\:mr-11 > div.mb-6.flex.flex-col.flex-wrap.items-center.justify-between.text-center.sm\\:flex-row.sm\\:text-left > div.flex.items-center.justify-end.text-bronze.\\[\\&_p\\]\\:text-2xl.\\[\\&_p\\]\\:font-semibold > p"
}
CBRE_SELECTORS = {
    "disponibilite": "#contentHolder_availability",
    "surface": "#contentHolder_surface",
    "division": "#contentHolder_surfaceDiv",
    "adresse": "#contentHolder_address1",
    "contact": "#contentHolder_contactZone > div.col-md-7.info > p:nth-of-type(2)",
    "accroche": "#section-description > p:nth-child(3)",
    "amenagements": "#section-feature > div > div:nth-child(1) > p",
    "prestations" : "#contentHolder_featureZone > ul",
    "prix_global": "#contentHolder_price"
}

ALEXBOLTON_SELECTORS = {
    "reference": "body > section.listing-header.py-md-4 > div > div > div.col-lg-5.position-relative > div > div.bolton-header-5.bolton-grey.mb-2",
    "contrat" : "body > section.listing-header.py-md-4 > div > div > div.col-lg-5.position-relative > div > div.d-flex.gap-4.mb-4 > div:nth-child(1) > p:nth-child(1)",
    "disponibilite": "body > section.listing-header.py-md-4 > div > div > div.col-lg-5.position-relative > div > div.d-flex.gap-4.mb-4 > div:nth-child(2) > p:nth-child(2)",
    "surface": "body > section.listing-header.py-md-4 > div > div > div.col-lg-5.position-relative > div > div.d-flex.gap-4.mb-4 > div:nth-child(1) > p:nth-child(4)",
    "adresse": "body > section.listing-header.py-md-4 > div > div > div.col-lg-5.position-relative > div > div.bolton-header-4.mb-4",
    "nom_immeuble" : "body > section.listing-header.py-md-4 > div > div > div.col-lg-5.position-relative > div > h1",
    "contact": "body > section.listing-details.bolton-bg-grey.u-py-80.u-py-mobile-24 > div > div > div.col-lg-4.position-relative > div > h3",
    "amenagements": "body > section.listing-details.bolton-bg-grey.u-py-80.u-py-mobile-24 > div > div > div.col-lg-8 > div.d-flex > div > div.listing-details-description.mb-3",
    "prix_global": "body > section.listing-header.py-md-4 > div > div > div.col-lg-5.position-relative > div > div.d-flex.gap-4.mb-4 > div:nth-child(1) > p:nth-child(2)"
}

CUSHMAN_SELECTORS = {
    "reference": "#js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(1) > div > header > p.u-t.u-t--sm.u-t-additional",
    "actif" : "#js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(1) > div > header > p.c-property__category",
    "contrat": "#js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(1) > div > header > p.c-property__category",
    "disponibilite": "js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(1) > div > div:nth-child(3) > p:nth-child(3) > span.u-t--tertiary",
    "surface": "#js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(1) > div > div:nth-child(3) > p:nth-child(1) > span.u-t--tertiary",
    "adresse": "#js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(1) > div > header > h1",
    # On peut utiliser le span pour séparer nom et prénom
    "contact": "#js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(1) > div > div:nth-child(4) > div > div > div.c-contact__main > h5",
    "accroche": "#js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(2) > div > section:nth-child(5) > p",
    "amenagements": "#js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(2) > div > section:nth-child(7) > ul",
    "prix_global": "#js-page > div.c-page__inner > main > div.o-container > article > div.o-grid.u-fxd\\(column\\)\\@phone.u-fxw\\(nowrap\\)\\@phone > div:nth-child(2) > div:nth-child(1) > div > div:nth-child(3) > div > div > p > span.u-t--tertiary"
}

""" Ajouter les sélecteurs pour les autres sites
EXEMPLE_SELECTORS = {
    "reference": "",
    "disponibilite": "",
    "surface": "",
    "division": "",
    "adresse": "",
    "contact": "",
    "accroche": "",
    "amenagements": "",
    "prix_global": ""
}
"""