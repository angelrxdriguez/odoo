# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LigaPartido(models.Model):
    #Nombre y descripcion del modelo
    _name = 'liga.partido'
    _description = 'Un partido de la liga'
    jornada = fields.Integer(string='Jornada')


    #Atributos del modelo


    #PARA CUANDO NO HAY UN ATRIBUTO LLAMADO NAME PARA MOSTRAR LOS Many2One en Vistas
    # https://www.odoo.com/es_ES/forum/ayuda-1/how-defined-display-name-in-custom-many2one-91657
    
   

    #Nombre del equipo que juega en casa casa
    equipo_casa = fields.Many2one(
        'liga.equipo',
        string='Equipo locaal',
    )
    #Goles equipo de casa
    goles_casa= fields.Integer()

    #Nombre del equipo que juega fuera
    equipo_fuera = fields.Many2one(
        'liga.equipo',
        string='Equipo visitantte',
    )
    #Goles equipo de casa
    goles_fuera= fields.Integer()
    #+2 goles
    def sumar_dos_locales(self):
        partidos = self.env['liga.partido'].search([])
        for partido in partidos: #saca cada partido para poder hacerlo sobre todos los registros
            partido.goles_casa = partido.goles_casa + 2 #le suma 2 goles al equipo
        self.actualizoRegistrosEquipo()
    def sumar_dos_visitantes(self):
        partidos = self.env['liga.partido'].search([])
        for partido in partidos:
            partido.goles_fuera = partido.goles_fuera + 2
        self.actualizoRegistrosEquipo()
    #Constraints de atributos
    @api.constrains('equipo_casa')
    def _check_mismo_equipo_casa(self):
        for record in self:
            if not record.equipo_casa:
                raise models.ValidationError('Debe seleccionarse un equipo locala.')
            if record.equipo_casa == record.equipo_fuera:
                raise models.ValidationError('Los equipos del partido deben serr diferentes.')


     #Constraints de atributos
    @api.constrains('equipo_fuera')
    def _check_mismo_equipo_fuera(self):
        for record in self:
            if not record.equipo_fuera:
                raise models.ValidationError('Debe seleccionarse un equipo visitante.')
            if record.equipo_fuera and record.equipo_casa == record.equipo_fuera:
                raise models.ValidationError('Los equipos del partido deben ser diferentes.')




    
    '''
    Funcion para actualizar la clasificacion de los equipos, re-calculandola entera
    '''
    def actualizoRegistrosEquipo(self):
        #Recorremos partidos y equipos
        for recordEquipo in self.env['liga.equipo'].search([]):
            #Como recalculamos todo, ponemos de cada equipo todo a cero
            recordEquipo.victorias=0
            recordEquipo.empates=0
            recordEquipo.derrotas=0
            recordEquipo.goles_a_favor=0
            recordEquipo.goles_en_contra=0
            recordEquipo.puntos=0

            for recordPartido in self.env['liga.partido'].search([]):  
                puntos_local=0 #declaro los puntos del local y visitante
                puntos_visitante=0
                #si hay empate
                if recordPartido.goles_casa==recordPartido.goles_fuera:
                    puntos_local=1
                    puntos_visitante=1
                else: #no hay empate - calculo diferencia
                    diferencia = recordPartido.goles_casa - recordPartido.goles_fuera
                #local si...
                    if diferencia>0:
                        if diferencia>=4:
                            puntos_local=4
                            puntos_visitante= -1
                        else:
                            puntos_local=3
                            puntos_visitante=0
                #visitante sino...
                    else:
                        if diferencia<=-4:
                            puntos_local=-1
                            puntos_visitante=4
                        else:
                            puntos_visitante=3
                            puntos_local=0
                #Si es el equipo de casa
                if recordPartido.equipo_casa.nombre==recordEquipo.nombre:
                    recordEquipo.puntos = recordEquipo.puntos + puntos_local
                    #Miramos si es victoria o derrota
                    if recordPartido.goles_casa>recordPartido.goles_fuera:
                        recordEquipo.victorias=recordEquipo.victorias+1
                    elif recordPartido.goles_casa<recordPartido.goles_fuera:
                        recordEquipo.derrotas=recordEquipo.derrotas+1
                    else:
                        recordEquipo.empates=recordEquipo.empates+1
                        
                    #Sumamos goles a favor y en contra
                    recordEquipo.goles_a_favor=recordEquipo.goles_a_favor+recordPartido.goles_casa
                    recordEquipo.goles_en_contra=recordEquipo.goles_en_contra+recordPartido.goles_fuera

                #Si es el equipo de fuera
                if recordPartido.equipo_fuera.nombre==recordEquipo.nombre:
                    recordEquipo.puntos = recordEquipo.puntos + puntos_visitante
                    #Miramos si es victoria o derrota
                    if recordPartido.goles_casa<recordPartido.goles_fuera:
                        recordEquipo.victorias=recordEquipo.victorias+1
                    elif recordPartido.goles_casa>recordPartido.goles_fuera:
                        recordEquipo.derrotas=recordEquipo.derrotas+1
                    else:
                        recordEquipo.empates=recordEquipo.empates+1
                    
                    #Sumamos goles a favor y en contra
                    recordEquipo.goles_a_favor=recordEquipo.goles_a_favor+recordPartido.goles_fuera
                    recordEquipo.goles_en_contra=recordEquipo.goles_en_contra+recordPartido.goles_casa




    #API onchange para cuando se modifica un partido
    #Aunque onchange envia un registro, hacemos codigo para recalcular 
    #http://www.geninit.cn/developer/reference/orm.html  
    @api.onchange('equipo_casa', 'goles_casa', 'equipo_fuera', 'goles_fuera')
    def actualizar(self):
        self.actualizoRegistrosEquipo()
    

    #Sobrescribo el borrado (unlink)
    def unlink(self):
        #Borro el registro, que es lo que hace el metodo normalmente
        result=super(LigaPartido,self).unlink()
        #Añado que llame a actualizoRegistroEquipo()
        self.actualizoRegistrosEquipo()
        return result

    #Sobreescribo el metodo crear
    @api.model
    def create(self, values):
        #hago lo normal del metodo create
        result = super().create(values)
        #Añado esto: llamo a la funcion que actualiza la clasificacion
        self.actualizoRegistrosEquipo()
        #hago lo normal del metodo create
        return result
