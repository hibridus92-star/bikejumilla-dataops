from odoo import api, models


class BikeJumillaCommercialSummaryReport(models.AbstractModel):
    _name = "report.bikejumilla_dataops.report_commercial_summary_document"
    _description = "BikeJumilla DataOps - Datos del informe comercial"

    @api.model
    def _get_report_values(self, docids, data=None):
        """TODO RA3 / CE a-c-h: sustituir placeholders por datos calculados."""
        docs = self.env["bikejumilla.commercial.analysis.wizard"].browse(docids)
        return {
            "doc_ids": docids,
            "doc_model": "bikejumilla.commercial.analysis.wizard",
            "docs": docs,
            "result_lines": [],
            "result_count": 0,
            "result_amount": 0.0,
            "extra_metric": None,
        }
