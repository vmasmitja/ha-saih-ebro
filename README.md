## Integración SAIH Ebro para Home Assistant

Integración personalizada de Home Assistant para obtener datos de la API Open Data de SAIH Ebro (embalses, caudales, niveles, calidad del agua, etc.).

Esta primera versión expone sensores para la estación de Tortosa (temperatura del agua, nivel y caudal) y está pensada para evolucionar hacia una integración instalable vía HACS.

## Fuente de datos y atribución

Esta integración consume datos publicados por **SAIH Ebro** (Sistema Automático de Información Hidrológica del Ebro) a través de su API de Open Data.

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

Esta integración se preparará para incluir:
- **Un logo propio** del proyecto (para Home Assistant / HACS).
- Referencias a la identidad visual de SAIH Ebro **solo** de forma compatible con los derechos de marca/autor.

En la web de SAIH Ebro se utiliza un logo accesible en formato SVG:
- `https://www.saihebro.com/images/logo-SAIH-pie.svg`

Recomendación: por defecto **no incluimos** ese archivo dentro del repositorio hasta confirmar que el uso y redistribución del logo está permitido por sus condiciones legales. Mientras tanto, podemos enlazarlo o mantenerlo como recurso opcional.

