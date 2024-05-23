{
    "name": "Real Estate Ads",
    "description": "Real estate module to show available properties",
    "version": "1.0",
    "author": "Farhat Shahir Zim",
    "category": "Sales",
    "depends": ["base"],
    "data": [
        # security
        "security/ir.model.access.csv",

        # views
        "views/property_view.xml",
        "views/property_type_view.xml",
        "views/property_tag_view.xml",
        "views/property_offer_view.xml",
        "views/menu_items.xml",
        "data/property_type.xml",

        # data
        # either data/file.xml or file.csv should be used
        # "data/property_tag.xml",
        "data/property_tag.csv",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3"
}