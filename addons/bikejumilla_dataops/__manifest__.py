{
    "name": "BikeJumilla DataOps",
    "summary": "Esqueleto didáctico para el RA3 de Sistemas de Gestión Empresarial",
    "version": "18.0.1.0.0",
    "category": "Education",
    "author": "Material docente - DAM / SGE",
    "license": "LGPL-3",
    "depends": ["base", "crm", "sale_management", "purchase", "stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/snapshot_views.xml",
        "wizard/commercial_analysis_wizard_views.xml",
        "report/commercial_summary_report.xml",
        "data/ir_cron.xml",
        "views/menu_views.xml",
    ],
    "application": True,
    "installable": True,
}
