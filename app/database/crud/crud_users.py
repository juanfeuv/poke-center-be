import datetime

from app.database.schema.users import Users


POKER_CENTER = "POKE-CENTER"


class CRUDUsers:
    @staticmethod
    def create_object(username, password,
                      status="active",
                      created_by=POKER_CENTER,
                      modified_by=POKER_CENTER,
                      created_date=datetime.datetime.now,
                      modified_date=datetime.datetime.now):
        h = Users(
            username=username,
            password=password,
            status=status,
            createdBy=created_by,
            modifiedBy=modified_by,
            createdDate=created_date,
            modifiedDate=modified_date,
        ).save()
        return h
    

    @staticmethod
    def get_by_username(username, status="active"):
        try:
            obj = Users.objects.filter(
                username=username, status=status).limit(1)
            if obj:
                return obj[0]
            else:
                raise Exception("UserNotFound")
        except Exception as e:
            print(f"Error: {e}")
            raise e
        
    
    @staticmethod
    def user_already_exist(username, status="active"):
        try:
            obj = Users.objects.filter(
                username=username, status=status).limit(1)
            if obj:
                return True
            return False
        except Exception as e:
            print(f"Error: {e}")
            raise e