{
    "name": "Real Estate",
    "summary": "Test module",
    "version": "18.0.0.0.0",
    "license": "OEEL-1",
    "application": True,
    "depends": ["crm"],
    "data":[
        #security
        "security/res_groups.xml",
        "security/ir.model.access.csv",

        #views
        "views/real_estate_views.xml",
        "views/estate_menus.xml",
        "views/real_estate_tag_view.xml",
        "views/real_estate_type_view.xml",
        "views/real_estate_offer_view.xml",
        "views/real_estate_users_view.xml",
        # "views/estate_property_views.xml",
        # "views/estates_menu.xml",
        #menus

    ],
    "demo": [
        "demo/demo.xml"
        ],
    "assets": {
        "web.assets_backend": [
            "estate/static/src/css/estate.css",
        ],
    }
}