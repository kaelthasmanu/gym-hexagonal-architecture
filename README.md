# Sistema de Gestión de Gimnasios - Módulo de Membresías

## Descripción

Este proyecto es un **Sistema de Gestión de Gimnasios** desarrollado con FastAPI que implementa una arquitectura hexagonal (también conocida como puertos y adaptadores) para el módulo de membresías. El sistema permite gestionar múltiples gimnasios, cada uno con sus propios clientes, membresías, pagos y operaciones administrativas.

## Arquitectura Hexagonal

El proyecto sigue los principios de la **Arquitectura Hexagonal** (Ports & Adapters) para el módulo de membresías, lo que proporciona:

- **Desacoplamiento** entre la lógica de negocio y la infraestructura
- **Testabilidad** mejorada mediante el uso de interfaces
- **Mantenibilidad** al separar claramente las responsabilidades
- **Flexibilidad** para cambiar implementaciones de infraestructura sin afectar el dominio

## Estructura del Proyecto

```
.
├── features/
│   └── membership/               # Módulo de membresías (hexagonal)
│       ├── __init__.py
│       ├── application/          # Casos de uso y servicios de aplicación
│       ├── domain/               # Entidades, value objects y reglas de negocio
│       └── infrastructure/       # Implementaciones concretas (repositorios, APIs, etc.)
├── dev_utils/                    # Utilidades para desarrollo y pruebas
│   ├── dev_database.py          # Configuración de base de datos para desarrollo
│   ├── dev_gym_model.py         # Modelos de gimnasio para desarrollo
│   ├── dev_models.py            # Modelos Pydantic y SQLAlchemy para desarrollo
│   ├── dev_security.py          # Utilidades de autenticación y autorización para desarrollo
│   └── seed_data.py             # Datos de prueba para desarrollo
├── main.py                      # Punto de entrada de la aplicación
└── requirements.txt             # Dependencias del proyecto
```

## Propósito de los Archivos en `dev_utils/`

Los archivos en el directorio `dev_utils/` son componentes de desarrollo que se utilizan para:

### 1. `dev_database.py`
- Configura la conexión a la base de datos PostgreSQL para desarrollo
- Proporciona utilidades para la gestión de sesiones asíncronas
- Incluye funciones para inicializar y restablecer la base de datos
- **Uso**: Se utiliza durante el desarrollo para configurar el entorno de base de datos sin necesidad de modificar el código de producción

### 2. `dev_gym_model.py`
- Contiene modelos de gimnasio para desarrollo y pruebas
- **Uso**: Proporciona datos de gimnasio ficticios para pruebas y desarrollo

### 3. `dev_models.py`
- Define modelos Pydantic y entidades SQLAlchemy para desarrollo
- Incluye modelos como `User`, `Membership`, `MembershipCreate`, etc.
- **Uso**: Se utiliza para pruebas y desarrollo sin depender de los modelos de producción

### 4. `dev_security.py`
- Implementa un sistema de autenticación y autorización simulado para desarrollo
- Incluye usuarios de prueba con diferentes roles (superadmin, admin, worker)
- **Uso**: Permite probar los endpoints protegidos sin necesidad de un sistema de autenticación completo

### 5. `seed_data.py`
- Contiene datos de ejemplo para poblar la base de datos durante el desarrollo
- **Uso**: Inicializa la base de datos con datos de prueba para facilitar el desarrollo


## Instalación

1. Clonar el repositorio
2. Crear un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Configurar variables de entorno (ver `.env.example`)
5. Inicializar la base de datos:
   ```bash
   python -m dev_utils.dev_database init_db
   ```

## Uso

1. Iniciar el servidor de desarrollo:
   ```bash
   uvicorn main:app --reload
   ```
2. Acceder a la documentación interactiva de la API en:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Estructura del Código

### Capa de Dominio (`domain/`)
- Contiene la lógica de negocio central
- Incluye entidades, value objects y reglas de negocio
- No tiene dependencias externas

### Capa de Aplicación (`application/`)
- Orquesta el flujo de datos entre la interfaz de usuario y el dominio
- Implementa los casos de uso
- Define interfaces (puertos) que serán implementadas por la capa de infraestructura

### Capa de Infraestructura (`infrastructure/`)
- Implementaciones concretas de las interfaces definidas en la capa de aplicación
- Incluye acceso a base de datos, APIs externas, etc.
- Depende de la capa de dominio

## Integración con el Código Existente

El módulo de membresías está diseñado para integrarse con el sistema existente de la siguiente manera:

1. **Autenticación y Autorización**: Utiliza el sistema de autenticación existente a través de los adaptadores en `dev_security.py`
2. **Base de Datos**: Se conecta a la misma base de datos PostgreSQL que el resto de la aplicación
3. **API REST**: Expone endpoints RESTful que siguen las convenciones del sistema existente
