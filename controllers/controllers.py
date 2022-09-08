# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from urllib.request import Request
from odoo.http import request
from odoo.addons.accesscontrol.models.models import Carrera
import json
from odoo import fields, api
from datetime import datetime
import requests
from odoo.addons.control_acceso.models.models import Laboratorio









class ApiController(http.Controller):
    
    @http.route('/api/dost/', methods=['post'], auth='public', csrf=False)
    def create_order(self, **kwargs):
        # Play with stuff, E.g:
        temperatura = 38
        aux = None
        materia2 = None 
        martes = None 
        miercoles = None 
        jueves = None 
        viernes = None 
        datos = kwargs
        lab = datos["lab"]
        print("laaab"+ lab)
        hora = ( datetime.today().strftime('%H'))
        horaActual = int(hora)-5
        #horaActual = '09:00'
        dia = (datetime.today().strftime('%A'))
        #dia = "jueves"
        min= ( datetime.today().strftime('%M')) 
        if horaActual >= 10:
            horaA = str(horaActual)+":"+str(min)
            #print("hora actual mayor a 10---------:"+ horaA)
        else:
            horaA = "0"+str(horaActual)+":"+str(min)
            #print("hora actual menor a 10---------:" + horaA)
        estudiante = request.env['controlacceso.estudiante'].sudo().search([('id_tarjeta','=',datos['pass'])])
        docente = request.env['controlacceso.docente'].sudo().search([('id_tarjeta','=',datos['pass'])])
        curso = request.env['controlacceso.curso'].sudo().search([('id','=',estudiante.curso_id.id)])
        laboratorio = request.env['controlacceso.lab'].sudo().search([('name','=',lab)])
        carrera = request.env['controlacceso.carrera'].sudo().search([('id','=',curso.id)])
        materia = request.env['controlacceso.materia'].sudo().search([('carrera_id','=',carrera.id)])
        #print("carrea: ", carrera, "materia: ", materia)
        #print("laboratorio id", laboratorio.id, "dia" , dia)
        if estudiante:
            buscarH = request.env['controlacceso.horario2'].sudo().search([('curso_id','=',estudiante.curso_id.id)])
            #print("estos veces esta el curso en el horario", buscarH.curso_id)
            aux = buscarH
            #print("aqui esta el curso del estudiante", aux.curso_id)
        for i in range (len(aux)):
            if aux[i].lunes and dia == 'lunes':
                materia2 = aux[i]
            if aux[i].martes and dia == 'martes':
                martes = aux[i]
            if aux[i].miercoles and dia == 'miércoles':
                miercoles = aux[i]
            if aux[i].jueves and dia == 'jueves':
                jueves = aux[i]
            if aux[i].viernes and dia == 'viernes':
                viernes = aux[i]
        if materia2 != None:
            m = request.env['controlacceso.materia'].sudo().search([('id','=',materia2.lunes.id)])
            if temperatura <= 37:
                request.env['controlacceso.registroasistencia'].sudo().create({
                                'name':estudiante.name,
                                'hora_ingreso':horaA,
                                'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                                'temperatura':temperatura,
                                'tarjeta':datos["pass"],
                                'curso_id':curso.id,
                                'materia_id':m.id,
                                'ingreso_usuario':"Si",
                                'lab_id':laboratorio.id,})
            else:
                request.env['controlacceso.registroasistencia'].sudo().create({
                                'name':estudiante.name,
                                'hora_ingreso':horaA,
                                'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                                'temperatura':temperatura,
                                'tarjeta':datos["pass"],
                                'curso_id':curso.id,
                                'materia_id':m.id,
                                'ingreso_usuario':"No",
                                'lab_id':laboratorio.id,})

            print('creado')
            return "registrado"
        if martes != None and horaA >= martes.hora_inicio and horaA <= martes.hora_fin:
            m = request.env['controlacceso.materia'].sudo().search([('id','=',martes.martes.id)])
            request.env['controlacceso.registroasistencia'].sudo().create({
                            'name':estudiante.name,
                            'hora_ingreso':horaA,
                            'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                            'temperatura':'36',
                            'tarjeta':datos["pass"],
                            'curso_id':curso.id,
                            'materia_id':m.id,
                            'lab_id':laboratorio.id,})
            print('creado')
            return "registrado"
        if miercoles != None and horaA >= miercoles.hora_inicio and horaA <= miercoles.hora_fin:
            m = request.env['controlacceso.materia'].sudo().search([('id','=',miercoles.miercoles.id)])
            request.env['controlacceso.registroasistencia'].sudo().create({
                            'name':estudiante.name,
                            'hora_ingreso':horaA,
                            'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                            'temperatura':'36',
                            'tarjeta':datos["pass"],
                            'curso_id':curso.id,
                            'materia_id':m.id,
                            'lab_id':laboratorio.id,})
            print('creado')
            return "registrado"
        if jueves != None and horaA >= jueves.hora_inicio and horaA <= jueves.hora_fin:
            m = request.env['controlacceso.materia'].sudo().search([('id','=',jueves.jueves.id)])
            request.env['controlacceso.registroasistencia'].sudo().create({
                            'name':estudiante.name,
                            'hora_ingreso':horaA,
                            'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                            'temperatura':'36',
                            'tarjeta':datos["pass"],
                            'curso_id':curso.id,
                            'materia_id':m.id,
                            'lab_id':laboratorio.id,})
            print('creado')
            return "registrado"
        if viernes != None:
            m = request.env['controlacceso.materia'].sudo().search([('id','=',viernes.viernes.id)])
            request.env['controlacceso.registroasistencia'].sudo().create({
                            'name':estudiante.name,
                            'hora_ingreso':horaA,
                            'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                            'temperatura':'36',
                            'tarjeta':datos["pass"],
                            'curso_id':curso.id,
                            'materia_id':m.id,
                            'lab_id':laboratorio.id,})
            print('creado')
            return "registrado"
            

                
                    
        if docente:
            request.env['controlacceso.registroasistencia'].sudo().create({
                'name':docente.name,
                'hora_ingreso':horaA,
                'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                'temperatura':'36',
                'tarjeta': datos['pass'],
                'curso_id':curso.id,
                'materia_id':'',
                'lab_id':laboratorio.id,})
            print('creado')
            return "registrado"    
        else:
            print('no creado')
            return "no registrado"
        # and other parameters, please read Odoo document
        return "se conecto con odoo"
    
    
        

    



