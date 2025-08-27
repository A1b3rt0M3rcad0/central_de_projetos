# Guia de Implementação do Padrão Cache-Aside

## 📋 Visão Geral

Este guia explica como implementar o padrão **Cache-Aside** nas rotas da API usando Redis como camada de cache. O padrão melhora significativamente a performance das consultas mais frequentes.

## 🔄 Como Funciona o Cache-Aside

### Fluxo Básico:

1. **Primeira requisição**: Busca no cache → Cache miss → Busca no banco → Armazena no cache → Retorna dados
2. **Requisições subsequentes**: Busca no cache → Cache hit → Retorna dados (muito mais rápido)

### Vantagens:

- ✅ **Performance**: Reduz drasticamente o tempo de resposta para dados frequentemente acessados
- ✅ **Escalabilidade**: Reduz a carga no banco de dados
- ✅ **Disponibilidade**: Se o cache falhar, o sistema continua funcionando com o banco
- ✅ **Flexibilidade**: Fácil de implementar e manter

## 🛠️ Implementação

### 1. Estrutura de Arquivos

Para implementar cache em uma nova entidade (ex: `empresa`), você precisa criar:

```
src/
├── presentation/controllers/cache/
│   └── empresa/
│       ├── get/
│       │   └── find_empresa_by_name_cached_controller.py
│       └── set/
│           └── set_empresa_by_name_cached_controller.py
├── main/composers/cache/
│   └── empresa/
│       ├── get/
│       │   └── get_empresa_by_name_cached_composer.py
│       └── set/
│           └── set_empresa_by_name_cached_composer.py
└── main/routes/api/
    └── empresa/
        └── empresa_routes.py (modificado)
```

### 2. Controllers de Cache

#### Controller GET (Buscar no Cache)

```python
from src.presentation.interface.async_controller_interface import AsyncControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_get_cached_value import IGetCachedValue

class FindEmpresaByNameCachedController(AsyncControllerInterface):
    def __init__(self, get_cached_value: IGetCachedValue):
        self.get_cached_value = get_cached_value

    async def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            name = path_params['empresa_name']
            result = await self.get_cached_value.get(key=name)
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Empresa Founded',
                    'content': result
                }
            )
        except Exception as e:
            raise e from e
```

#### Controller SET (Armazenar no Cache)

```python
from src.presentation.interface.async_controller_interface import AsyncControllerInterface
from src.domain.use_cases.i_set_cached_value import ISetCachedValue
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class SetEmpresaByNameCachedController(AsyncControllerInterface):
    def __init__(self, set_cached_value: ISetCachedValue):
        self.set_cached_value = set_cached_value

    async def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            body = http_request.body
            name = path_params['empresa_name']
            await self.set_cached_value.set(key=name, value=body)
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Empresa set successfully',
                    'content': {'name': name}
                }
            )
        except Exception as e:
            raise e from e
```

### 3. Composers de Cache

#### Composer GET

```python
from src.infra.redis.config.connection.redis_url_connection import RedisUrlConnection
from src.infra.redis.config.connection.redis_connection_handler import RedisConnectionHandler
from src.infra.redis.repositories.cache_repository import CacheRepository
from src.data.use_cases.get_cached_value import GetCachedValue
from src.presentation.controllers.cache.empresa.get.find_empresa_by_name_cached_controller import FindEmpresaByNameCachedController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def get_empresa_by_name_cached_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindEmpresaByNameCachedController(
        get_cached_value=GetCachedValue(
            cache_repository=CacheRepository(
                redis_connection_handler=RedisConnectionHandler(
                    redis_url_connection=RedisUrlConnection()
                )
            )
        )
    ).handle
```

#### Composer SET

```python
from src.infra.redis.config.connection.redis_connection_handler import RedisConnectionHandler
from src.infra.redis.config.connection.redis_url_connection import RedisUrlConnection
from src.infra.redis.repositories.cache_repository import CacheRepository
from src.data.use_cases.set_cached_value import SetCachedValue
from src.presentation.controllers.cache.empresa.set.set_empresa_by_name_cached_controller import SetEmpresaByNameCachedController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

async def set_empresa_by_name_cached_composer() -> Callable[[HttpRequest], HttpResponse]:
    return SetEmpresaByNameCachedController(
        set_cached_value=SetCachedValue(
            cache_repository=CacheRepository(
                redis_connection_handler=RedisConnectionHandler(
                    redis_url_connection=RedisUrlConnection()
                )
            )
        )
    ).handle
```

### 4. Modificação da Rota

```python
from src.main.adapters.simple_cache_aside_adapter import simple_cache_aside_adapter
from src.main.composers.cache.empresa.get.get_empresa_by_name_cached_composer import get_empresa_by_name_cached_composer
from src.main.composers.cache.empresa.set.set_empresa_by_name_cached_composer import set_empresa_by_name_cached_composer

@routes.get('/{empresa_name}', response_model=FindEmpresaResponse, responses=generate_error_responses())
async def find_empresa(empresa_name, request:Request, user=Security(role_required(["VEREADOR", "ADMIN", "ASSESSOR"]))):
    """
    Endpoint para buscar uma empresa específica pelo nome exato.
    Implementa cache-aside: primeiro busca no Redis, se não encontrar busca no banco.
    """
    try:
        # Usa o cache-aside adapter para implementar o padrão cache
        http_response = await simple_cache_aside_adapter(
            framework_request=request,
            cache_get_controller=get_empresa_by_name_cached_composer(),
            db_controller=find_empresa_by_exact_name_composer(),
            cache_set_controller=set_empresa_by_name_cached_composer(),
            cache_key='empresa_name'
        )

        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            logger_name=PREFIX,
            http_response=http_response,
            request=request
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            logger_name=PREFIX,
            http_response=error_result,
            request=request
        )
        return response_adapter(error_result)
```

## 🎯 Casos de Uso Recomendados

### ✅ Implementar Cache Para:

- **Consultas por ID/Nome**: `GET /bairro/{name}`, `GET /empresa/{name}`
- **Dados estáticos**: Configurações, listas de tipos, status
- **Dados frequentemente acessados**: Usuários ativos, projetos em andamento
- **Contadores**: Total de registros, estatísticas

### ❌ Não Implementar Cache Para:

- **Dados que mudam frequentemente**: Logs, métricas em tempo real
- **Dados sensíveis**: Senhas, tokens de acesso
- **Dados muito grandes**: Arquivos, imagens (use CDN)
- **Consultas complexas**: Relatórios, análises

## 🔧 Configuração do Redis

### Variáveis de Ambiente (.env)

```env
REDIS_URL=redis://localhost:6379
REDIS_PORT=6379
REDIS_PASSWORD=your_password
REDIS_DECODE_RESPONSES=True
REDIS_NAMESPACE=IMBITUBA
REDIS_TTL=3600
```

### Configuração de TTL (Time To Live)

```python
# No CacheRepository, você pode configurar TTL específico
cache_repository = CacheRepository(
    redis_connection_handler=RedisConnectionHandler(
        redis_url_connection=RedisUrlConnection()
    ),
    ttl=3600  # 1 hora em segundos
)
```

## 📊 Monitoramento e Métricas

### Logs Recomendados

```python
# Log de cache hit
log_http(
    level='INFO',
    logger_name='CACHE',
    message=f'Cache HIT for key: {cache_key}',
    request=request
)

# Log de cache miss
log_http(
    level='INFO',
    logger_name='CACHE',
    message=f'Cache MISS for key: {cache_key}, fetching from database',
    request=request
)
```

### Métricas Úteis

- **Cache Hit Rate**: Porcentagem de requisições atendidas pelo cache
- **Cache Miss Rate**: Porcentagem de requisições que precisaram ir ao banco
- **Response Time**: Tempo de resposta com e sem cache
- **Memory Usage**: Uso de memória do Redis

## 🚀 Performance Esperada

### Antes do Cache:

- **Primeira requisição**: ~50-100ms (banco de dados)
- **Requisições subsequentes**: ~50-100ms (banco de dados)

### Depois do Cache:

- **Primeira requisição**: ~50-100ms (banco de dados + cache)
- **Requisições subsequentes**: ~5-10ms (apenas cache)

### Melhoria:

- **Cache Hit**: 80-90% de redução no tempo de resposta
- **Redução de carga no banco**: 70-80% menos consultas
- **Melhor experiência do usuário**: Respostas mais rápidas

## 🔄 Invalidação de Cache

### Estratégias de Invalidação:

1. **TTL (Time To Live)**: Dados expiram automaticamente
2. **Invalidação manual**: Quando dados são atualizados
3. **Invalidação por padrão**: Usando wildcards

### Exemplo de Invalidação Manual:

```python
# Após atualizar uma empresa, invalidar o cache
async def update_empresa(empresa_name: str, new_data: dict):
    # Atualiza no banco
    await update_empresa_in_database(empresa_name, new_data)

    # Invalida o cache
    cache_key = f"empresa:{empresa_name}"
    await cache_repository.delete(cache_key)
```

## 🧪 Testes

### Testes Recomendados:

- ✅ Cache hit (dados encontrados no cache)
- ✅ Cache miss (dados não encontrados, busca no banco)
- ✅ Cache exception (cache falha, fallback para banco)
- ✅ Cache set failure (falha ao armazenar, não quebra a requisição)
- ✅ Performance tests (comparar tempos com e sem cache)

## 📝 Checklist de Implementação

- [ ] Criar controllers de cache (GET e SET)
- [ ] Criar composers de cache
- [ ] Modificar a rota para usar o adapter
- [ ] Configurar TTL apropriado
- [ ] Implementar logs de cache
- [ ] Criar testes unitários
- [ ] Testar performance
- [ ] Documentar a implementação

## 🎉 Benefícios Alcançados

Com esta implementação, você terá:

- **Performance otimizada** para consultas frequentes
- **Arquitetura escalável** que suporta crescimento
- **Experiência do usuário melhorada** com respostas mais rápidas
- **Redução de custos** com menor uso do banco de dados
- **Sistema resiliente** que funciona mesmo se o cache falhar
