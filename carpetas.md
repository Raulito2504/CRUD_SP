# Estructura de Carpetas del Proyecto

A continuación se detalla la responsabilidad de cada directorio en la arquitectura del proyecto:

- **`api/routes/`**
  Solo define los endpoints de la API, nada más. Su única responsabilidad es recibir la *request* HTTP y llamar al *service* correspondiente.

- **`services/`**
  Aquí vive toda la lógica de negocio. Es la capa encargada de ejecutar los Procedimientos Almacenados (SP's) utilizando la conexión a la base de datos.

- **`db/`**
  Maneja exclusivamente la conexión a la base de datos (SQL Server). Al tenerlo centralizado, es el único lugar que necesitas modificar si en algún momento decides migrar a otro motor de base de datos.

- **`schemas/`**
  Contiene los modelos de validación de datos basados en **Pydantic**. Actúan como contratos que validan la estructura de lo que entra (requests) y lo que sale (responses) de tu API.

- **`core/`**
  Almacena la configuración global de la aplicación, como la gestión y carga de variables de entorno utilizando `pydantic-settings`.