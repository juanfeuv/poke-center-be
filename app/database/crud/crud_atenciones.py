from app.database.schema.atenciones import Atenciones


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
                      user_id=""):
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
            user_id=user_id
        ).save()
        return h
    

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
    def get_items(atendidos="false"):
        try:
            filters = {}
            if atendidos.lower() == "false":
                filters["fechaAtencion__exists"] = False
            else:
                filters["fechaAtencion__exists"] = True

            data = Atenciones.objects.filter(**filters).order_by("+createdAt")
            data = list(map(lambda transaction: transaction.to_mongo(), data))

            turns_with_numbers = list(filter(lambda x: x.get("turnNumber"), data))
            turns_with_numbers = list(map(lambda x: { **x, "new_turnNumber": x.get("turnNumber") - 1 }, turns_with_numbers))
            turns_with_no_numbers = list(filter(lambda x: not x.get("turnNumber"), data))

            # Sort the list of dictionaries by "turnNumber" in ascending order
            turns_with_numbers = sorted(turns_with_numbers, key=lambda x: x["turnNumber"])

            merged_list = sorted(
                turns_with_no_numbers + turns_with_numbers,
                key=lambda x: x.get("new_turnNumber", 0)  # Prioritize by turnNumber and then keep original order
            )

            return merged_list

        except Exception as e:
            raise e
