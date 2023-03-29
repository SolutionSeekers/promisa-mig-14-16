# -*- coding: utf-8 -*-
##############################################################################
#                 @author IT Admin
#
##############################################################################

{
    'name': 'Catalogos para timbrado CFDI 3.3',
    'version': '14.03',
    'description': ''' Agrega catalogos para realizar el timbrado de facturas CFDI 3.3
    ''',
    'category': 'Accounting',
    'author': 'IT Admin',
    'website': 'www.itadmin.com.mx',
    'depends': [
        'base','sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/paises_view.xml',
        'data/catalogos.paises.csv',
        'views/colonia_view.xml',
        'data/catalogos.colonias.csv',		
        'views/estados_view.xml',
        'data/catalogos.estados.csv',
        'views/localidades_view.xml',
        'data/catalogos.localidades.csv',	
        'views/municipio_view.xml',
        'data/catalogos.municipio.csv',
        'views/clave_unidad_view.xml',
        'data/catalogos.clave_unidad.csv',
        'views/clave_prodserv_view.xml',
        'data/catalogos.claveprodserv.csv',	
        'views/fraccion_arancelaria.xml',
        'data/catalogos.fraccionarancelaria.csv',
        'views/unidad_medida_aduana.xml',
        'data/catalogos.unidadmedidaaduana.csv',
        'views/banco_view.xml',
        'data/catalogos.banco.csv',
		
        #NEW DATA FOR CATALOGOS TRASLADO
        'data/cve.transporte.csv',
        'data/cve.estacion.csv',
        'data/cve.estaciones.csv',
        'data/cve.clave.unidad.csv',
        'data/cve.material.peligroso.csv',
        'data/cve.tipo.embalaje.csv',
        'data/cve.tipo.permiso.csv',
        'data/cve.conf.autotransporte.csv',
        'data/cve.remolque.semiremolque.csv',
        'data/cve.conf.maritima.csv',
        'data/cve.tipo.carga.csv',
        'data/cve.cont.maritimo.csv',
        'data/cve.autorizacion.naviera.csv',
        'data/cve.codigo.transporte.aereo.csv',
        'data/cve.clave.prod.stcc.csv',
        'data/cve.tipo.servicio.csv',
        'data/cve.derecho.paso.csv',
        'data/cve.tipo.carro.csv',
        'data/cve.contenedor.csv',
        'data/cve.figura.transporte.csv',
        'data/cve.parte.transporte.csv',

        #NEW VIEWS FOR VIEWS
        'views/cve_transporte.xml',
        'views/cve_estacion.xml',
        'views/cve_estaciones.xml',
        'views/cve_clave_unidad.xml',
        'views/cve_material_peligroso.xml',
        'views/cve_tipo_embalaje.xml',
        'views/cve_tipo_permiso.xml',
        'views/cve_conf_autotransporte.xml',
        'views/cve_remolque_semiremolque.xml',
        'views/cve_conf_maritima.xml',
        'views/cve_tipo_carga.xml',
        'views/cve_cont_maritimo.xml',
        'views/cve_autorizacion_naviera.xml',
        'views/cve_codigo_transporte_aereo.xml',
        'views/cve_clave_prod_stcc.xml',
        'views/cve_tipo_servicio.xml',
        'views/cve_derecho_paso.xml',
        'views/cve_tipo_carro.xml',
        'views/cve_contenedor.xml',
        'views/cve_figura_transporte.xml',
        'views/cve_parte_transporte.xml',
		
	],
    'application': False,
    'installable': True,
}
