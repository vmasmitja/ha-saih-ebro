[![SAIH Ebro integration logo](https://raw.githubusercontent.com/vmasmitja/ha-saih-ebro/master/custom_components/saih_ebro/brand/logo.png)](https://www.saihebro.com/homepage/estado-cuenca-ebro)

[![HACS][hacs-badge]](https://hacs.xyz/)
[![Home Assistant][ha-badge]](https://www.home-assistant.io/)
[![GitHub release][release-badge]](https://github.com/vmasmitja/ha-saih-ebro/releases)

# SAIH Ebro (Open Data) for Home Assistant

## English

Integrate **SAIH Ebro Open Data API** in Home Assistant to expose measurements from river gauges, reservoirs and canal stations, plus meteorology.

### ⚙️ Configuration

1. Install via **HACS**.
2. Add the integration in Home Assistant.
3. Use the config wizard:
   - **API Key**: paste your personal Open Data API key.
   - **Scope**: choose `River`, `Reservoir`, `Canal` or `Meteorology`.
   - **Zone**: choose one official SAIH hydrological zone (H1..H22 / HG).
   - **Stations**: pick one or more stations inside that zone.
   - **Data types**: pick the measurements you want (level, flow, precipitation, etc.).
   - **Signals (optional)**: further refine by specific signals.

The wizard is localized using your Home Assistant language. In English it shows **River** (not “Río”).
Zone and station names are proper nouns and keep their official spelling.

### ⬇️ Installation & ♻️ Update (HACS)

Use HACS to install / update this integration. The repository is configured for HACS releases.

### 🔑 How to obtain an API Key

To use the Open Data API you need an account with explicit access.

1. Register: `https://www.saihebro.com/usuarios/registro`
2. In the form, write in **Remarks / Observaciones** that you want access to **Open Data API**.

### 📊 Provided entities

This integration creates a `sensor` entity **for each selected signal**.
The available measurement families currently exposed by the catalog are:

| Category | Applies to scope | Measurement | Unit |
|---|---|---:|---|
| Nivel río | Río | River level | m |
| Caudal río | Río | River flow | m³/s |
| Nivel embalse | Embalse | Reservoir level | msnm |
| Volumen embalse | Embalse | Reservoir volume | hm³ |
| % volumen embalse | Embalse | Reservoir volume percentage | % |
| Nivel canal | Canal | Canal level | m |
| Cota lámina | Canal | Water surface elevation | m |
| Caudal canal | Canal | Canal flow | m³/s |
| Nivel piezométrico | Canal | Piezometric level | m |
| Temperatura | Meteorología | Temperature | º C |
| Precipitación QM | Meteorología | Precipitation (QM) | mm |
| Precipitación 24h | Meteorología | 24h precipitation | mm |
| Precipitación acumulada | Meteorología | Accumulated precipitation | mm |
| Velocidad racha | Meteorología | Wind gust speed | m/s |
| Insolación acumulada | Meteorología | Accumulated insolation | h |
| Equivalente en agua | Meteorología | Water equivalent | mm |
| Altura de nieve | Meteorología | Snow height | cm |

### 🌍 Hydrological zones (full basin map + official zones)

![SAIH Ebro hydrological zones map](https://www.saihebro.com/images/mapas_hidrologia/mapaHG.jpg)

Official hydrological zones used by the integration wizard:

| Code | Zone name |
|---|---|
| H1 | Alto Ebro (M.I.) |
| H2 | Semi Alta (Miranda) |
| H3 | Aragón-Irati |
| H4 | Medio Ebro (M.I.) |
| H5 | Gállego |
| H6 | Bajo Cinca |
| H7 | Segre |
| H8 | Bajo Ebro |
| H9 | Guadalope-Martín |
| H10 | Bajo Jalón |
| H11 | Semi Alta (Logroño) |
| H12 | Arga |
| H13 | Nogueras |
| H15 | Alto Ebro (M.D.) |
| H16 | Alto Aragón |
| H17 | Alto Cinca |
| H18 | Esera |
| H19 | Huerva-Aguas Vivas |
| H20 | Alto Jalón |
| H21 | Medio Ebro (M.D.) |
| H22 | Garona |
| HG | Toda la Cuenca |

### Data source & attribution

This integration consumes data published by **SAIH Ebro** through its Open Data API.

- Owner / associated brands: [Confederación Hidrográfica del Ebro (CHE)](https://chebro.es/)
- SAIH Ebro web: `https://www.saihebro.com/homepage/estado-cuenca-ebro`
- Open Data area / login: `https://www.saihebro.com/datos/opendata`

Notes:
- Data may be **provisional** and subject to revision.
- This integration is **not officially affiliated** with SAIH Ebro.

## Español

Integra la **API Open Data de SAIH Ebro** en Home Assistant para exponer mediciones de estaciones de río, embalses y canales, además de meteorología.

### ⚙️ Configuración

1. Instala mediante **HACS**.
2. Añade la integración en Home Assistant.
3. Usa el asistente de configuración:
   - **API Key**: pega tu clave personal de Open Data API.
   - **Ámbito / Scope**: elige `Río`, `Embalse`, `Canal` o `Meteorología` (o **River/Reservoir/Canal/Meteorology** en inglés).
   - **Zona**: selecciona una zona hidrológica oficial de SAIH (H1..H22 / HG).
   - **Estaciones**: elige una o varias estaciones dentro de esa zona.
   - **Tipos de datos**: elige las mediciones deseadas (nivel, caudal, precipitación, etc.).
   - **Señales (opcional)**: afina por señales concretas.

El asistente está traducido usando el idioma de tu Home Assistant. En inglés muestra **River** (no “Río”).  
Los nombres de zonas y estaciones son propios y mantienen su ortografía oficial.

### ⬇️ Instalación & ♻️ Actualización (HACS)

Usa HACS para instalar / actualizar esta integración. El repo está preparado con releases para HACS.

### 🔑 Cómo obtener una API Key

Para usar la Open Data API necesitas una cuenta con acceso explícito:

1. Regístrate: `https://www.saihebro.com/usuarios/registro`
2. En el formulario, en **Remarks / Observaciones**, indica que quieres acceso a **Open Data API**.

### 📊 Entidades proporcionadas

Esta integración crea una entidad `sensor` **por cada señal seleccionada**.
Las familias de medición disponibles en el catálogo son:

| Categoría | Ámbito | Medición | Unidad |
|---|---|---:|---|
| Nivel río | Río | Nivel de río | m |
| Caudal río | Río | Caudal de río | m³/s |
| Nivel embalse | Embalse | Nivel de embalse | msnm |
| Volumen embalse | Embalse | Volumen de embalse | hm³ |
| % volumen embalse | Embalse | % de volumen de embalse | % |
| Nivel canal | Canal | Nivel de canal | m |
| Cota lámina | Canal | Cota de lámina de agua | m |
| Caudal canal | Canal | Caudal de canal | m³/s |
| Nivel piezométrico | Canal | Nivel piezométrico | m |
| Temperatura | Meteorología | Temperatura | º C |
| Precipitación QM | Meteorología | Precipitación QM | mm |
| Precipitación 24h | Meteorología | Precipitación 24h | mm |
| Precipitación acumulada | Meteorología | Precipitación acumulada | mm |
| Velocidad racha | Meteorología | Rachas de viento | m/s |
| Insolación acumulada | Meteorología | Insolación acumulada | h |
| Equivalente en agua | Meteorología | Equivalente en agua | mm |
| Altura de nieve | Meteorología | Altura de nieve | cm |

### 🌍 Zonas hidrológicas (mapa completo + zonas oficiales)

![Mapa de zonas hidrológicas SAIH Ebro](https://www.saihebro.com/images/mapas_hidrologia/mapaHG.jpg)

Las zonas hidrológicas oficiales usadas por el asistente son:

| Código | Zona |
|---|---|
| H1 | Alto Ebro (M.I.) |
| H2 | Semi Alta (Miranda) |
| H3 | Aragón-Irati |
| H4 | Medio Ebro (M.I.) |
| H5 | Gállego |
| H6 | Bajo Cinca |
| H7 | Segre |
| H8 | Bajo Ebro |
| H9 | Guadalope-Martín |
| H10 | Bajo Jalón |
| H11 | Semi Alta (Logroño) |
| H12 | Arga |
| H13 | Nogueras |
| H15 | Alto Ebro (M.D.) |
| H16 | Alto Aragón |
| H17 | Alto Cinca |
| H18 | Esera |
| H19 | Huerva-Aguas Vivas |
| H20 | Alto Jalón |
| H21 | Medio Ebro (M.D.) |
| H22 | Garona |
| HG | Toda la Cuenca |

### Fuente de datos y atribución

Esta integración consume datos publicados por **SAIH Ebro** a través de su API Open Data.

- Propietario / marcas asociadas: [Confederación Hidrográfica del Ebro (CHE)](https://chebro.es/)
- Web SAIH Ebro: `https://www.saihebro.com/homepage/estado-cuenca-ebro`
- Área Open Data / login: `https://www.saihebro.com/datos/opendata`

Notas:
- Los datos pueden ser **provisionales** y sujetos a revisión.
- Esta integración no está afiliada oficialmente a SAIH Ebro.

---

[hacs-badge]: https://img.shields.io/badge/HACS-Frontend-yellow.svg?style=for-the-badge
[ha-badge]: https://img.shields.io/badge/Home%20Assistant-2026.2.0-blue.svg?style=for-the-badge
[release-badge]: https://img.shields.io/github/v/release/vmasmitja/ha-saih-ebro?style=for-the-badge

