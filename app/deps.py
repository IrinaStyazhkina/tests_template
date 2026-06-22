from datetime import timedelta

from authx import AuthXConfig, AuthX
from pika.adapters.blocking_connection import  BlockingConnection

from configuration.rabbit_conn import init_rabbit
from config import settings
from database.repository.chat_repository import ChatRepository
from database.repository.message_repository import MessageRepository
from database.repository.transaction_repository import TransactionRepository
from database.repository.user_repository import UserRepository
from service.admin_service import AdminService
from service.auth_service import AuthService
from service.ml_service import MLService
from service.user_service import UserService

auth_config = AuthXConfig(
    JWT_SECRET_KEY= settings.JWT_SECRET_KEY,
    JWT_ACCESS_COOKIE_NAME = "access_token",
    JWT_TOKEN_LOCATION = ["cookies"],
    JWT_ACCESS_TOKEN_EXPIRES= timedelta(minutes=30),
    JWT_COOKIE_CSRF_PROTECT=False
)

auth = AuthX(config=auth_config)

user_repository = UserRepository()
transaction_repository = TransactionRepository()
chat_repository = ChatRepository()
message_repository = MessageRepository()

rabbit_connection = init_rabbit()
user_service = UserService(user_repository, transaction_repository, chat_repository)
auth_service = AuthService(user_repository, auth)
admin_service = AdminService(user_repository, transaction_repository)
ml_service = MLService(message_repository, rabbit_connection)

def get_user_service() -> UserService:
    return user_service

def get_auth_service() -> AuthService:
    return auth_service

def get_admin_service() -> AdminService:
    return admin_service

def get_ml_service() -> MLService:
    return ml_service

def get_rabbit_connection() -> BlockingConnection:
    return rabbit_connection