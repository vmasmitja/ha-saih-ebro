## Integración SAIH Ebro para Home Assistant

Integración personalizada de Home Assistant para obtener datos de la API Open Data de SAIH Ebro (embalses, caudales, niveles, calidad del agua, etc.).

Esta primera versión expone sensores para la estación de Tortosa (temperatura del agua, nivel y caudal) y está pensada para evolucionar hacia una integración instalable vía HACS.

## Fuente de datos y atribución

Esta integración consume datos publicados por **SAIH Ebro** (Sistema Automático de Información Hidrológica del Ebro) a través de su API de Open Data.

- **Titular y propietario de la información y de las marcas asociadas (SAIH Ebro, CHE, etc.)**: [Confederación Hidrográfica del Ebro](https://chebro.es/).
- **Web SAIH Ebro (estado de cuenca / mapas / recursos)**: `https://www.saihebro.com/homepage/estado-cuenca-ebro`
- **Área Open Data / login**: `https://www.saihebro.com/datos/opendata`

Notas:
- Los datos mostrados por SAIH Ebro pueden ser **provisionales** y estar sujetos a revisión (ver avisos en su propia web).
- Esta integración **no está afiliada** oficialmente a SAIH Ebro.

## Cómo obtener una API Key

Para usar la API necesitas una cuenta y que te habiliten acceso a **Open Data API**.

1. Regístrate en: `https://www.saihebro.com/usuarios/registro`
2. En el formulario, en el campo **Remarks / Observaciones**, indica explícitamente que solicitas acceso a **Open Data API**.

Si no dispones de API Key (o no está habilitada), la API puede responder con un error similar a:

```text
Unauthorized, use this url (https://www.saihebro.com/datos/opendata), to know how to get data from SAIH. You need an account. You can register in url (https://www.saihebro.com/usuarios/registro). In the user registration page, write in the Remarks field that you want to access Open Data API%
```

## Logos e imágenes

Esta integración incluye:
- **Un logo propio** del proyecto (para Home Assistant / HACS), pensado para distinguir claramente la integración de cualquier marca oficial.
- La posibilidad de **mostrar el logo de SAIH Ebro** como referencia a la fuente de los datos, poniendo siempre de forma visible:
  - El texto “Datos proporcionados por SAIH Ebro – Confederación Hidrográfica del Ebro”.
  - Un enlace a `https://chebro.es/` y/o a la web de SAIH Ebro.

En la web de SAIH Ebro se utiliza un logo accesible en formato SVG:
- `https://www.saihebro.com/images/logo-SAIH-pie.svg`

Por indicación de SAIH Ebro/CHE en el proceso de alta de la API, se recomienda:
- Mencionar expresamente a SAIH Ebro / Confederación Hidrográfica del Ebro como **fuente de los datos**.
- Incluir referencia a `https://chebro.es/` como propietarios de la marca.

En este repositorio no se redistribuye directamente el fichero original del logo, pero se hace referencia a él (y puede mostrarse desde la propia web de SAIH Ebro) junto con el logo propio de la integración.

