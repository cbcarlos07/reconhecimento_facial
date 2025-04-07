
from passlib.hash import pbkdf2_sha256
from core.repositories.user_repository import UserRepository
from core.services.base_service import BaseService

class UserService(BaseService):
    def __init__(self):
        self.user_repository = UserRepository()
        super().__init__(self.user_repository)

    def create(self, data):
        password = self.gerar_hash_senha(data['password'])
        data['password'] = password
        return super().create(data)

    def gerar_hash_senha(self, senha):
        """Gera um hash seguro para a senha usando bcrypt."""
        return pbkdf2_sha256.hash(senha)
    
    def verificar_senha(self, senha, hashed_password):
        """Verifica se a senha fornecida corresponde ao hash."""
        return pbkdf2_sha256.verify(senha, hashed_password)
    
    