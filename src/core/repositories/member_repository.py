#src/core/repositories/member_repository.py
from config.database.models.type_person import TypePerson
from core.repositories.repository import Repository
from config.database.models import Member
from sqlalchemy.orm import joinedload

class MemberRepository(Repository):
    def __init__(self):
        super().__init__(Member)

    def get_all_by_church(self, church_id):
        # Se um church_id for fornecido, filtra os membros por essa igreja
        query = self.model.query
        if church_id:
            query = query.filter_by(church_id=church_id)
        
        # Carrega as relações de church e type_person
        models = query.options(joinedload(Member.church), joinedload(Member.type_person)).all()
        return [
        {
            'id': model.id,
            'name': model.name,
            'church': model.church.name,  # Acessando o nome da igreja
            'type_person': model.type_person.name  # Acessando o nome do tipo de pessoa
        }
        for model in models
    ]
        
    
    