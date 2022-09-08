# -*- coding: utf-8 -*-

from operator import is_not
from odoo import http
from odoo.http import request
from urllib.request import Request
from odoo.http import request
from odoo.addons.accesscontrol.models.models import Carrera
import json
from odoo import fields, api
from datetime import datetime
from email.policy import default
from logging import warning
import requests

from requests import request
from odoo import fields, models, api
from odoo.exceptions import ValidationError
import re
from datetime import datetime
from datetime import date, datetime, timedelta
from odoo.addons.calendar.models.calendar_recurrence import weekday_to_field, RRULE_TYPE_SELECTION, END_TYPE_SELECTION, MONTH_BY_SELECTION, WEEKDAY_SELECTION, BYDAY_SELECTION
import ast
import json
from collections import defaultdict
from datetime import timedelta, datetime
from random import randint

from odoo import api, Command, fields, models, tools, SUPERUSER_ID, _, _lt
from odoo.exceptions import UserError, ValidationError, AccessError
from odoo.tools import format_amount
from odoo.osv.expression import OR

#from .project_task_recurrence import DAYS, WEEKS
#from .project_update import STATUS_COLOR

count = None



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
    name = fields.Char('Nombres y Apellidos', required=True)
    correo_docente = fields.Char('Correo', required=True)
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


    #@api.onchange('name')
    #def crearUser(self):
     #   crear_user = self.env['res.users'].sudo().create({
      #                      'name':self.name,
        #                    'login':self.correo_docente,})
       # if crear_user:
         #   print("se creo el usuario")
                 

    #@api.onchange('id_tarjeta')
    #def validate_nrotarjeta(self):
    #    if self.id_tarjeta:
     #       match = re.match('/^([a-f0-9]{6}|[a-f0-9]{3})$/', self.correo_docente)
      #      if match == None:
       #         raise ValidationError('Ingrese formato correcto')
class Estudiante(models.Model):
    _name = 'controlacceso.estudiante'
    cedula = fields.Char('Cedula', required=True)
    name = fields.Char('Nombres y Apellidos', required=True)
    id_tarjeta = fields.Char('Tarjeta', required=True)
    carrera_id = fields.Many2one(
        "controlacceso.carrera", string="Carrera",
        default=lambda self: self.env['controlacceso.carrera'].search([], limit=1),
        ondelete="cascade")
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
    
    
    def botonconfirm(self):
        datos= 'E0 3B 98 2F'
        aux = None
        lunes = None
        martes = None
        miercoles = None
        jueves = None
        viernes = None
        lab = '1'
        laboratorio = self.env['controlacceso.lab'].sudo().search([('name','=',lab)])
        hora = ( datetime.today().strftime('%H'))
        horaActual = int(hora)-5
        if horaActual >= 10:
            horaA = str(horaActual)+":"+str(min)
            #print("hora actual mayor a 10---------:"+ horaA)
        else:
            horaA = "0"+str(horaActual)+":"+str(min)
        dia = (datetime.today().strftime('%A'))
        docente = self.env['controlacceso.docente'].sudo().search([('id_tarjeta','=',datos)])
        if docente:
            buscarH = self.env['controlacceso.horario2'].sudo().search([('docente_id','=',docente.id)])
            for i in range (len(buscarH)):
                if buscarH[i].lunes and dia == 'lunes':
                    lunes = buscarH[i]
                    print("si da hoy lunes")
                if buscarH[i].martes and dia == 'martes':
                    martes = buscarH[i]
                    print("si da hoy martes")
                if buscarH[i].miercoles and dia == 'miércoles':
                    miercoles = buscarH[i]
                    print("si da hoy miercoles")
                if buscarH[i].jueves and dia == 'jueves':
                    jueves = buscarH[i]
                    print("si da hoy jueves")
                if buscarH[i].viernes and dia == 'viernes':
                    viernes = buscarH[i]
                    print("si da hoy viernes")
            if lunes != None and horaA >= lunes.hora_inicio and horaA <= lunes.hora_fin:
                m = self.env['controlacceso.materia'].sudo().search([('id','=',lunes.lunes.id)])
                self.env['controlacceso.registroasistencia'].sudo().create({
                'name':docente.name,
                'hora_ingreso':horaA,
                'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                'temperatura':'36',
                'tarjeta': datos,
                'curso_id':lunes.curso.id,
                'materia_id':m.id,
                'lab_id':laboratorio.id,})
                print('creado')
                return "registrado" 
            if martes != None and horaA >= martes.hora_inicio and horaA <= martes.hora_fin:
                m = self.env['controlacceso.materia'].sudo().search([('id','=',martes.martes.id)])
                self.env['controlacceso.registroasistencia'].sudo().create({
                'name':docente.name,
                'hora_ingreso':horaA,
                'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                'temperatura':'36',
                'tarjeta': datos,
                'curso_id':martes.curso.id,
                'materia_id':m.id,
                'lab_id':laboratorio.id,})
                print('creado')
                return "registrado" 
            if miercoles != None and horaA >= miercoles.hora_inicio and horaA <= miercoles.hora_fin:
                m = self.env['controlacceso.materia'].sudo().search([('id','=',miercoles.miercoles.id)])
                self.env['controlacceso.registroasistencia'].sudo().create({
                'name':docente.name,
                'hora_ingreso':horaA,
                'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                'temperatura':'36',
                'tarjeta': datos,
                'curso_id':miercoles.curso.id,
                'materia_id':m.id,
                'lab_id':laboratorio.id,})
                print('creado')
                return "registrado"
            else:
                print("no estas en tus horas de clases") 
            if jueves != None and horaA >= jueves.hora_inicio and horaA <= jueves.hora_fin:
                m = self.env['controlacceso.materia'].sudo().search([('id','=',jueves.jueves.id)])
                self.env['controlacceso.registroasistencia'].sudo().create({
                'name':docente.name,
                'hora_ingreso':horaA,
                'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                'temperatura':'36',
                'tarjeta': datos,
                'curso_id':jueves.curso.id,
                'materia_id':m.id,
                'lab_id':laboratorio.id,})
                print('creado')
                return "registrado" 
            if viernes != None and horaA >= viernes.hora_inicio and horaA <= viernes.hora_fin:
                m = self.env['controlacceso.materia'].sudo().search([('id','=',viernes.viernes.id)])
                self.env['controlacceso.registroasistencia'].sudo().create({
                'name':docente.name,
                'hora_ingreso':horaA,
                'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                'temperatura':'36',
                'tarjeta': datos,
                'curso_id':viernes.curso.id,
                'materia_id':m.id,
                'lab_id':laboratorio.id,})
                print('creado')
                return "registrado"  
                
            
        
        #if context is None: context = {}
        #p = self.env.context
        #nombre = p.get('active_id')
        #print('aqui esta el name', nombre)
        #if nombre is None:
         #   return ""
        #else:
            
         #   x = requests.post('http://192.168.3.11:8069/api/dost/abrir?nombre='+nombre)
          #  print(x)
        # return x
        
        #print('clickeste el boton', x, "----:",a)
        

    



class Horario(models.Model):
    _name = 'controlacceso.horario'
    hora_inicio = fields.Selection(
        selection=[("07:30", "07:30"), ("08:30", "08:30"), ("09:30", "09:30"),
                   ("10:30", "10:30"), ("11:30", "11:30"), ("12:30", "12:30")], string="Hora inicio", required=True)
    hora_fin = fields.Selection(
        selection=[("08:30", "08:30"), ("09:30", "09:30"),
                   ("10:30", "10:30"), ("11:30", "11:30"), ("12:30", "12:30"),("13:30", "13:30")], string="Hora fin", required=True)
    dia = fields.Selection(
        selection=[("lunes", "lunes"), ("martes", "martes"), ("miercoles", "miercoles"),
                   ("jueves", "jueves"), ("viernes", "viernes")], string="Dia", required=True)
    
    laboratorio_id = fields.Many2one(
        "controlacceso.lab", string="Laboratorio")
    carrera_id = fields.Many2one("controlacceso.carrera", string="Carrera",
                                 ondelete="cascade")
    materia_id = fields.Many2one("controlacceso.materia", string="Materia",
                                 ondelete="cascade")
    curso_id = fields.Many2one("controlacceso.curso", string="Curso",
                               ondelete="cascade")
    docente_id = fields.Many2one("controlacceso.docente", string="Docente",
                               ondelete="cascade")
    

 

    

   
class Practicas(models.Model):
    


    _name = 'controlacceso.practica'
    name = fields.Char('Tema de la practica', required=True, default="Uso diario")
    total_usuarios = fields.Integer('Numero usuarios')
    fecha = fields.Char('Fecha', required=True, default=datetime.today().strftime('%Y-%m-%d'))
    docente_id = fields.Many2one(
        "controlacceso.docente", string="Docente Responsable",
        default=lambda self: self.env['controlacceso.docente'].search([], limit=1),
        ondelete="cascade")
    lab_id = fields.Many2one(
        "controlacceso.lab", string="Laboratorio",
        default=lambda self: self.env['controlacceso.lab'].search([], limit=1),
        ondelete="cascade")
    curso_id = fields.Many2one("controlacceso.curso", string="Curso",
                               ondelete="cascade")

   
   

    @api.constrains('fecha')
    def contar(self):
        doc = self.docente_id
        buscarDoc =self.env['controlacceso.docente'].search([('id','=',doc.id)])
        contar =self.env['controlacceso.docente'].search_count([('id','=',doc.id)])
        print("si los cuento",contar)
        self.total_usuarios = contar
        
    @api.constrains('fecha')
    def RegistrardocenteCuenta(self):
        c = self.env.user.login
        correo= self.env['controlacceso.docente'].search([('correo_docente','=',c)])
        print("id uasriooooooo",self.env.user.login)
        self.docente_id = correo.id

    @api.constrains('fecha')
    def validate_date_practica(self):
        
        aux=None
        doc = self.env.user.login
        
        dia = (datetime.today().strftime('%A'))
        hora = ( datetime.today().strftime('%H'))
        horaActual = int(hora)-5
        min= ( datetime.today().strftime('%M')) 
        horaA = str(horaActual)+":"+str(min)
        
        
        print("esta si es la hora actual",horaA)
        
        listaHorario = self.env['controlacceso.horario2'].search([])
        for i in range(len(listaHorario)):
            print("Este es el dia",dia)
            d = self.docente_id
            buscard= self.env['controlacceso.docente'].search([('name','=',d.name)])
            buscarH=self.env['controlacceso.horario2'].search([('docente_id','=',buscard.id)])
        
            for j in range (len(buscarH)):
                if buscarH.lunes !=None and dia == 'lunes':
                    buscarM=self.env['controlacceso.materia'].search([('id','=',buscarH.lunes.id)])
                    print("Aqui da clases lunes", buscarM.name)
                    aux = buscarH[j]
                if buscarH.martes !=None and dia == 'lunes':
                    print("Aqui da clases martes", buscarH.martes)
                    aux = buscarH[j]
                if buscarH.martes !=None and dia == 'martes':
                    print("Aqui da clases martes", buscarH.martes)
                    aux = buscarH[j]
                if buscarH.miercoles !=None and dia == 'miercoles':
                    buscarM=self.env['controlacceso.materia'].search([('id','=',buscarH.lunes.id)])
                    print("Aqui da clases miercoles", buscarM.name)
                    aux = buscarH[j]
                if bool(buscarH.jueves) == True and dia == 'jueves':
                    print("Aqui da clases jueves", buscarH.martes)
                    aux = buscarH[j]
                if buscarH.viernes !=None and dia == 'viernes':
                    print("Aqui da clases viernes", buscarH.martes)
                    aux = buscarH[j]
        if aux == None:
            raise ValidationError('Se debe ingresar la practica dentro de su horario de clases')   



           # if str(dia) == str(listaHorario[i].dia):
            #    print('hay segundo match :v',listaHorario[i].dia)
             #   aux= listaHorario[i]
                
        
        #if aux is None:
         #   raise ValidationError('Se debe ingresar la practica dentro de su horario de clases')
    


    #@api.constrains('fecha')
    #def pruebaRegistro(self):
     #   print("entrol al prueb registro")
      #  doc = self.docente_id
      #  tarjeta = '8888'
       # buscarDoc =self.env['controlacceso.docente'].search([('id_tarjeta','=',tarjeta)])
       # print(buscarDoc)
        
        
        #buscarEst =self.env['controlacceso.estudiante'].search([('id_tarjeta','=',tarjeta)])
        #print(buscarEst)
        #if buscarDoc != None:
         #   buscarCarrera = self.env['controlacceso.carrera'].search([('id','=',buscarDoc.carrera_id.id)])
          #  print("Econtro docentes con sus datos", "nombre", buscarDoc.name, "carrera", buscarCarrera.name)
        #else:
         #   buscarCurso = self.env['controlacceso.curso'].search([('id','=',buscarEst.curso_id.id)])
          #  print("Econtro estudiante con su datos" , "Nombre" , buscarEst.name ,"Curso",buscarCurso.name)


class DocenteUser(models.Model):
    _inherit = "res.users"
    tarjeta = fields.Char('Nro. de tarjeta', required=True)
    curso_id = fields.Many2one("controlacceso.curso", string="Curso",
                               ondelete="cascade")
                               


class Horario2(models.Model):
    _name = 'controlacceso.horario2'
    hora_inicio = fields.Selection(
        selection=[("07:30", "07:30"), ("08:30", "08:30"), ("09:30", "09:30"),
                   ("10:30", "10:30"), ("11:30", "11:30"), ("12:30", "12:30")], string="Hora inicio", required=True)
    hora_fin = fields.Selection(
        selection=[("08:30", "08:30"), ("09:30", "09:30"),
                   ("10:30", "10:30"), ("11:30", "11:30"), ("12:30", "12:30"),("13:30", "13:30")], string="Hora fin", required=True)
    lunes = fields.Many2one("controlacceso.materia", required=False, string="Lunes",
                                 ondelete="cascade")
    martes = fields.Many2one("controlacceso.materia", required=False, string="Martes",
                                 ondelete="cascade")
    miercoles = fields.Many2one("controlacceso.materia", required=False, string="Miercoles",
                                 ondelete="cascade")
    jueves = fields.Many2one("controlacceso.materia", required=False, string="Jueves",
                                 ondelete="cascade")
    viernes = fields.Many2one("controlacceso.materia", required=False, string="Viernes",
                                 ondelete="cascade")
    laboratorio_id = fields.Many2one(
        "controlacceso.lab", string="Laboratorio")
    carrera_id = fields.Many2one("controlacceso.carrera", string="Carrera",
                                 ondelete="cascade")
  
    curso_id = fields.Many2one("controlacceso.curso", string="Curso",
                               ondelete="cascade")
    docente_id = fields.Many2one("controlacceso.docente", string="Docente",
                               ondelete="cascade")
                            
    ########################################################################

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

class registroAsistencia(models.Model):
    _name = 'controlacceso.registroasistencia'
    name = fields.Char('nombre usuario', required=True)
    hora_ingreso = fields.Char('Hora ingreso', required=True)
    fecha_ingreso = fields.Char('Fecha ingreso', required=True)
    temperatura = fields.Char('Temperatura', required=True)
    tarjeta = fields.Char('Tarjeta', required=True)
    curso_id= fields.Many2one("controlacceso.curso", string="Curso",
                               ondelete="cascade")
    materia_id= fields.Many2one("controlacceso.materia", string="Materia",
                               ondelete="cascade")
    lab_id= fields.Many2one("controlacceso.lab", string="Laboratorio",
                               ondelete="cascade")
    ingreso_usuario = fields.Selection(
                    selection=[("Si", "Si"), ("No", "No")], string="Ingreso Usuario", required=True)

    

    
    
