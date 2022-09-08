# -*- coding: utf-8 -*-
{
    'name': "Control de Acceso",
    "description": "Módulo para el control de acceso de los laboratorios en la carrera de Ingeniería en Sistemas/Computación de la Universidad Nacional de Loja",
    "author": "EALeon",
   "summary": "Módulo para el control de acceso de los laboratorios en la carrera de Ingeniería en Sistemas/Computación de la Universidad Nacional de Loja",
    "author": "EALeon",
    "depends": ["base", "mail",
        'analytic',
        'base_setup',
        'portal',
        'rating',
        'resource',
        'web',
        'web_tour',
        'digest',
    ],
    "data":[
        'views/views.xml',
        'views/report.xml',
        'views/reporte_practica.xml',
        'security/ir_model_access.xml',
            
        'security/res_groups.xml',
    ]

}
