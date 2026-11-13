from odoo import api, models


class BikeJumillaCommercialSummaryReport(models.AbstractModel):
    _name = "report.bikejumilla_dataops.report_commercial_summary_document"
    _description = "BikeJumilla DataOps - Datos del informe comercial"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env["bikejumilla.commercial.analysis.wizard"].browse(docids)
        doc = docs[0]
        
        # 1. Reutilizamos el dominio del wizard
        domain = doc._build_domain()
        pedidos = self.env['sale.order'].search(domain)
        
        # 2. Preparamos las líneas del detalle
        result_lines = []
        for p in pedidos[:30]: # Limitamos a 30 para no saturar
            result_lines.append({
                'name': p.name,
                'partner': p.partner_id.name,
                'date': p.date_order.strftime('%d/%m/%Y') if p.date_order else '',
                'state': p.state,
                'amount': p.amount_total,
            })
            
        # 3. Calculamos el importe medio como indicador adicional
        total_amount = sum(pedidos.mapped('amount_total'))
        avg_amount = total_amount / len(pedidos) if pedidos else 0.0
            
        return {
            "doc_ids": docids,
            "doc_model": "bikejumilla.commercial.analysis.wizard",
            "docs": docs,
            "result_lines": result_lines,
            "result_count": len(pedidos),
            "result_amount": total_amount,
            "extra_metric": avg_amount,
        }