# -*- coding: utf-8 -*-

# from odoo import models, fields, api
from email.policy import default
from logging import warning
from odoo import fields, models, api
from odoo.exceptions import ValidationError
import re

# class control_acceso(models.Model):
#     _name = 'control_acceso.control_acceso'
#     _description = 'control_acceso.control_acceso'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class Carrera(models.Model):
    _name = 'controlacceso.carrera'
    _description = 'registro de carreras'
    name = fields.Char('Carrera', required=True)

class Curso(models.Model):
    _name = 'controlacceso.curso'
    name = fields.Char('Nombre curso', required=True)
    carrera_id = fields.Many2one(
        "controlacceso.carrera", string="Carrera",
        default=lambda self: self.env['controlacceso.carrera'].search([], limit=1),
        ondelete="cascade")
    carrera =  fields.Char(related='carrera_id.name', string="Nombre Carrera",) 

class Materia(models.Model):
    _name = 'controlacceso.materia'
    name = fields.Char('Nombre materia', required=True)
    carrera_id = fields.Many2one(
        "controlacceso.carrera", string="Carrera",
        default=lambda self: self.env['controlacceso.carrera'].search([], limit=1),
        ondelete="cascade")

class Docente(models.Model):
    _name = 'controlacceso.docente'
    cedula = fields.Char('Cedula', required=True)
    nombre_docente = fields.Char('Nombres', required=True)
    apellido_docente = fields.Char('Apellidos', required=True)
    correo_docente = fields.Char('Correo', required=True)
    estado = fields.Boolean('Estado', default=True)
    id_tarjeta = fields.Char('Tarjeta', required=True)
    carrera_id = fields.Many2one(
        "controlacceso.carrera", string="Carrera",
        default=lambda self: self.env['controlacceso.carrera'].search([], limit=1),
        ondelete="cascade")
    
    @api.constrains('cedula')
    def vcedula(self):
    # sin ceros a la izquierda
        nocero = self.cedula.strip("0")
        
        cedula = int(nocero,0)
        verificador = cedula%10
        numero = cedula//10
        
        # mientras tenga números
        suma = 0
        while (numero > 0):
            
            # posición impar
            posimpar = numero%10
            numero   = numero//10
            posimpar = 2*posimpar
            if (posimpar  > 9):
                posimpar = posimpar-9
            
            # posición par
            pospar = numero%10
            numero = numero//10
            
            suma = suma + posimpar + pospar
        
        decenasup = suma//10 + 1
        calculado = decenasup*10 - suma
        if (calculado  >= 10):
            calculado = calculado - 10

        if (calculado == verificador):
            validado = 1
        else:
            validado = 0
            raise ValidationError("Ingrese una cedula valida")
        return (validado)
    @api.onchange('correo_docente')
    def validate_mail(self):
        if self.correo_docente:
            match = re.match('.+@unl.edu\.ec', self.correo_docente)
            if match == None:
                raise ValidationError('Solo se aceptan direcciones de correo pertenecientes a @unl.edu.ec')
                

class Estudiante(models.Model):
    _name = 'controlacceso.estudiante'
    nombre_estudiante = fields.Char('Nombres', required=True)
    apellido_estudiante = fields.Char('Apellidos', required=True)
    estado = fields.Boolean('Estado', default=True)
    id_tarjeta = fields.Char('Tarjeta', required=True)
    curso_id = fields.Many2one(
        "controlacceso.curso", string="curso",
        default=lambda self: self.env['controlacceso.curso'].search([], limit=1),
        ondelete="cascade")

class Laboratorio(models.Model):
    _name = 'controlacceso.lab'
    codigo_lab = fields.Char('Codigo del Laboratorio', required=True)
    name = fields.Char('Nombre', required=True)
    estado_puerta = fields.Selection(
        selection=[("abierto", "abierto"), ("cerrado", "cerrado")],
        string="Estado puerta", required=True)
    clave_llave = fields.Char('Clave Llave', required=True)

class Horario(models.Model):
    _name = 'controlacceso.horario'
    