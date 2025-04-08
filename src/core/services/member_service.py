
#src/core/services/member_service.py
from core.repositories.member_repository import MemberRepository
from core.services.base_service import BaseService
from datetime import datetime
import base64
import os
class MemberService(BaseService):
    def __init__(self):
        self.repository = MemberRepository()
        super().__init__(self.repository)

    def get_all_by_church(self, church_id):
        return self.repository.get_all_by_church(church_id)
    
    def create(self, data):
        date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        data['date_of_birth'] = date_of_birth
        base64_string = data['base64_string']
        del data['base64_string']
        info = super().create(data)
        info_to_base64 = {'base64_string': base64_string, 'name': f"{data['cpf']}-{data['name']}"}
        self.save_base64_image( info_to_base64 )
        return info
    
    def save_base64_image(self, data):
        base64_string = data['base64_string']
        filename = data['name']
        # Verifica se a pasta img/known_faces existe, se não, cria.
        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..','img', 'known_faces'))
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Remove o cabeçalho da string, se presente
        if base64_string.startswith('data:image/jpeg;base64,'):
            base64_string = base64_string.replace('data:image/jpeg;base64,', '')

        # Decodifica a string Base64
        img_data = base64.b64decode(base64_string)

        # Cria o caminho completo do arquivo
        # Substitui espaços por underscores no nome do arquivo
        filename = f'{filename.replace(" ", "_").upper()}.jpg'
        file_path = os.path.join(directory, filename)

        # Salva a imagem no caminho especificado
        with open(file_path, 'wb') as f:
            f.write(img_data)

        print(f"Imagem salva em: {file_path}")