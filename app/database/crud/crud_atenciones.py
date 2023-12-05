from app.database.schema.atenciones import Atenciones
from app.utils.utils import criterios_orden


class CRUDAtenciones:
    @staticmethod
    def create_object(hp=1,
                      trainer_name="test",
                      trainer_id="123",
                      cambio_estado={},
                      nivel=1,
                      pokemon_name="",
                      pokemon_id=123,
                      pokemon_info={},
                      raw_id=123,
                      user_id="",
                      turn_number=1):
        h = Atenciones(
            hp=hp,
            trainerName=trainer_name,
            trainerId=trainer_id,
            cambioEstado=cambio_estado,
            nivel=nivel,
            pokemonName=pokemon_name,
            pokemonId=pokemon_id,
            pokemonInfo=pokemon_info,
            rawId=raw_id,
            user_id=user_id,
            turnNumber=turn_number
        ).save()

        data = Atenciones.objects.filter(fechaAtencion=None)
        data = list(map(lambda transaction: transaction.to_mongo(), data))
        data = sorted(data, key=criterios_orden)

        new_turn = 1
        
        # Agrega la posición a cada elemento de la lista
        for i, objeto in enumerate(data, start=1):
            if raw_id == objeto.get("rawId"):
                new_turn = i
                
            objeto.turnNumber = i
            CRUDAtenciones.update_turn_by_id(raw_id=objeto.get("rawId"), payload={ "turnNumber": i })
        return new_turn
    

    @staticmethod
    def get_turn_number():
        try:
            new_turn = Atenciones.objects.filter(fechaAtencion=None).count()

            return new_turn + 1

        except Exception as e:
            raise e


    @staticmethod
    def update_turn_by_id(raw_id=123, payload={}):
        try:
            if not payload:
                return
            
            updator = {}
            for key in payload:
                updator[f"set__{key}"] = payload[key]

            Atenciones.objects(rawId=raw_id).update(**updator)
        except Exception as e:
            raise e
        

    @staticmethod
    def get_by_turn(turn):
        try:
            data = Atenciones.objects.filter(turnNumber=turn, fechaAtencion=None).limit(1)
            data = list(map(lambda transaction: transaction.to_mongo(), data))
            if len(data) > 0:
                return data[0]

            return None
        except Exception as e:
            raise e

    
    @staticmethod
    def get_by_id(raw_id):
        try:
            data = Atenciones.objects.filter(rawId=raw_id).limit(1)
            data = list(map(lambda transaction: transaction.to_mongo(), data))
            if len(data) > 0:
                return data[0]

            return None
        except Exception as e:
            raise e

    
    @staticmethod
    def get_items(atendidos="false"):
        try:
            filters = {}
            if atendidos.lower() == "false":
                filters["fechaAtencion"] = None
            else:
                filters["fechaAtencion__ne"] = None

            data = Atenciones.objects.filter(**filters).order_by("+turnNumber")
            return list(map(lambda transaction: transaction.to_mongo(), data))
        except Exception as e:
            raise e


