import os
import importlib
import inspect
import pkgutil

class RouteRegistry:
    @staticmethod
    def register_routes(app):
        """
        Registra automaticamente todas as classes de rotas encontradas nos arquivos 
        dentro do diretório routes/default e seus subdiretórios.
        """
        # Obtém o diretório atual (routes)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        default_dir = os.path.join(current_dir, 'default')
        
        # Verifica se o diretório default existe
        if not os.path.isdir(default_dir):
            print(f"Aviso: Diretório {default_dir} não encontrado.")
            return
        
        # Importa o pacote default
        default_package = importlib.import_module('api.routes.default')
        
        # Percorre todos os módulos no pacote default e seus subpacotes
        for _, module_name, is_pkg in pkgutil.walk_packages(default_package.__path__, default_package.__name__ + '.'):
            if not is_pkg:  # Se não for um pacote (ou seja, é um arquivo Python)
                try:
                    # Importa o módulo
                    module = importlib.import_module(module_name)
                    
                    # Encontra todas as classes no módulo
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        # Verifica se a classe pertence ao módulo atual (não é importada)
                        if obj.__module__ == module_name:
                            # Verifica se o nome da classe termina com 'Routes'
                            if name.endswith('Routes'):
                                # Inicializa a classe de rota com a aplicação
                                route_instance = obj(app)
                                route_instance.configure_routes()
                                print(f"Registradas rotas de: {name} do módulo {module_name}")
                except Exception as e:
                    print(f"Erro ao carregar o módulo {module_name}: {e}")

# Exporta a função para fácil importação
def register_all_routes(app):
    RouteRegistry.register_routes(app)