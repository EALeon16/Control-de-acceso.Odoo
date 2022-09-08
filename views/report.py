from reportlab.pdfbase.pdfutils import _fusc

from odoo import models, api
from datetime import datetime

class SolicitudMatricula(models.AbstractModel):
    _name = "report.control_acceso_registroasistencia.report_registroasistencia"

    @api.model
    def _get_report_values(self, docids, data=None):
        print("ingresa despues de la funcion")
        docs = self.env["controlacceso.registroasistencia"].browse(docids)
        docargs = {
            "docs": docs,
        }
        return docargs


class ReportePracticas(models.AbstractModel):
    print("ingresa despues de la clase")
    _name = "reporte_practica.control_acceso_practicas.report_practica"
    print("ingresa despues del _name")
    @api.model
    def _get_report_values(self, docids, data=None):
        print("ingresa despues de la funcion")
        docs = self.env["controlacceso.practica"].browse(docids)
        asistencia = self.env["controlacceso.registroasistencia"].sudo().search(['fecha_ingreso','=',docs.fecha])
        docargs = {
            "docs": docs,
            "a": asistencia,
        }
        print("+++++++++++++++++++++++++++++++++++++", docs.name)
        return docargs