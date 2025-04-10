
#src/core/services/member_service.py
import json
from core.repositories.member_repository import MemberRepository
from core.services.base_service import BaseService
from datetime import datetime
import base64
import os
class MemberService(BaseService):
    def __init__(self):
        repository = MemberRepository()
        self.directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..','img', 'known_faces'))
        super().__init__(repository)

    def get_all_by_church(self, church_id):
        return self.repository.get_all_by_church(church_id)
    
    def create(self, data):
        values = self.prepare_new_data(data)
            
        info = super().create(values['newData'])
        
        if 'info_to_base64' in values:
            self.save_base64_image( values.get('info_to_base64') )
            
        return info
    
    def update(self, id, data):
        # Verifica se 'base64_string' está nos dados
        if 'base64_string' not in data and not data:
            return {'error': 'No data provided for update'}
        
        values_old = self.get_by_id( id )
        values = self.prepare_new_data(data)
        
        info = None
        newData = None
        try:
             # Atualiza os dados, se existirem
            if values.get('newData'):
                newData = values.get('newData')
                info = super().update(id, values['newData'])
            
            
            if 'info_to_base64' in values:
                info_to_base64 = values.get('info_to_base64')
                name = info_to_base64.get('name')
                get_info = self.get_by_id( id )
                
                if 'name' in info_to_base64 and info_to_base64['name'] is None:
                    newName = get_info['name']
                    cpf = get_info['cpf']
                    name = f"{cpf}-{newName}"
                elif len(info_to_base64['name'].split('-')) == 1 and not info_to_base64['name'].isnumeric():
                    newName = info_to_base64['name'].split('-')[0]
                    cpf = get_info['cpf'] 
                    name = f"{cpf}-{newName}"

                
                info_to_base64['name'] = name
                self.save_base64_image( info_to_base64 )
                if newData.get('cpf') != values_old.get('cpf'):
                    self.deletePicture(values_old.get('cpf'))
                info = info if info is not None else get_info

            return info
        except Exception as e:
            error_message = f"Ocorreu um erro inesperado: {str(e)}"
            return {'error': error_message}
        
    
    def prepare_new_data(self, data):
        base64_string = None
        
        if 'date_of_birth' in data:
            date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
            data['date_of_birth'] = date_of_birth

        if 'base64_string' in data:
            base64_string = data['base64_string']
            del data['base64_string']

        name = None
        if 'name' in data:
            name = data['name']
            if 'cpf' in data:
                name = f"{data['cpf']}-{name}"
            
        
        info_to_base64 = None
        if base64_string:
            info_to_base64 = {'base64_string': base64_string, 'name': name}
            
        return {"newData": data, 'info_to_base64': info_to_base64 }

    
    def save_base64_image(self, data):
        base64_string = data['base64_string']
        filename = data['name']
        # Verifica se a pasta img/known_faces existe, se não, cria.
        
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        # Remove o cabeçalho da string, se presente
        if base64_string.startswith('data:image/jpeg;base64,'):
            base64_string = base64_string.replace('data:image/jpeg;base64,', '')

        # Decodifica a string Base64
        img_data = base64.b64decode(base64_string)

        # Cria o caminho completo do arquivo
        # Substitui espaços por underscores no nome do arquivo
        filename = f'{filename.replace(" ", "_").upper()}.jpg'
        file_path = os.path.join(self.directory, filename)

        # Verifica se já existe um arquivo que começa com os 11 primeiros dígitos e remove-o
        prefix = filename.split('-')[0]  # Obtém os 11 primeiros dígitos do nome do arquivo
        self.deletePicture(prefix)

        # Salva a imagem no caminho especificado
        with open(file_path, 'wb') as f:
            f.write(img_data)

        print(f"Imagem salva em: {file_path}")

    def deletePicture(self, prefix):
        for existing_file in os.listdir(self.directory):
            if existing_file.startswith(prefix):
                os.remove(os.path.join(self.directory, existing_file))
                print(f"Arquivo removido: {existing_file}")