import datetime, os
import logging, grpc, jwt
import user_service_pb2, user_service_pb2_grpc
from concurrent import futures
from werkzeug.security import generate_password_hash, check_password_hash
from providers.mongo_provider import MongoDBProvider
from dotenv import load_dotenv

def parse_create_req(request):
    return {'data':(request.username,request.email,
                    generate_password_hash(request.password),request.role,)}

def gen_auth_token(user_id: 'str', role: 'str'):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=7200),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id,
        'role': role
    }
    return jwt.encode(
        payload,
        os.getenv('SECRET_KEY'),   # generated randomly
        algorithm='HS256'
    )

class UserMgtServicer(user_service_pb2_grpc.UserMgtServicer):
    def __init__(self) -> None:
        self.provider = MongoDBProvider()
        self.provider.connect()
    
    def CreateUser(self, request, context):
        data = parse_create_req(request)
        response = self.provider.create(location="",data=data)
        return user_service_pb2.DBUserResponse(status=response[0],
                                                message=response[1])

    def ReadUser(self, request, context):
        email, password = request.email, request.password
        _ii, _i, user_dict = self.provider.read(location=email)
        user_list = user_dict.get('list')
        if user_list.__len__() == 0:
            return user_service_pb2.DBUserResponse(status=False,
                                    message='Unknown email, Please sign up')
        elif not check_password_hash(user_list[0].get('password'), password):
            return user_service_pb2.DBUserResponse(status=False,
                                    message='Invalid password')
        else:
            message = gen_auth_token(email,user_list[0].get('role'))    
            return user_service_pb2.DBUserResponse(status=True,
                                                message=message)

def server():
    load_dotenv()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_service_pb2_grpc.add_UserMgtServicer_to_server(UserMgtServicer(),server)
    server.add_insecure_port('[::]:40051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    server()