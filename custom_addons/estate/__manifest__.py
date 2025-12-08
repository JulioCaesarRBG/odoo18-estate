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
        "views/real_estate_tag_view.xml",
        "views/real_estate_type_view.xml",
        "views/real_estate_offer_view.xml",
        "views/real_estate_users_view.xml",
        
        #controller actions
        "views/controller_actions.xml",
        
        #templates
        "views/templates.xml",
        
        #reports
        "reports/real_estate_report_template.xml",
        "reports/real_estate_custom_report_template.xml",
        
        #wizards
        # "wizard/real_estate_batch_report_wizard_view.xml",
        
        #menus
        "views/estate_menus.xml",

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