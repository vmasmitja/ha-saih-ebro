## SAIH Ebro integration for Home Assistant

Integración / Integration for Home Assistant to consume SAIH Ebro Open Data API (reservoirs, river flows and levels, meteorology, water quality, etc.).

Se distribuye como integración personalizada y está pensada para ser instalable vía HACS.

### Overview (English)

- **Domain**: `saih_ebro`
- **Platform**: `sensor`
- **Data source**: SAIH Ebro Open Data API (`https://www.saihebro.com/datos/opendata`)
- **What you can do**:
  - Select **scope** (Río, Embalse, Canal, Meteorología).
  - Select **hydrological zone** (official H1..H22 / HG map zones).
  - Pick one or more **stations** and **categories** (level, flow, temperature, etc.).
  - Optionally refine by individual **signals**.

The config flow is fully localized (Spanish + English). The English strings live in `translations/en.json` and the Spanish ones in `translations/es.json`.

### Descripción (Español)

- **Dominio**: `saih_ebro`  
- **Plataforma**: `sensor`  
- **Fuente de datos**: API Open Data de SAIH Ebro (`https://www.saihebro.com/datos/opendata`)
- **Qué permite**:
  - Elegir **ámbito** (Río, Embalse, Canal, Meteorología).
  - Elegir **zona hidrológica oficial** (H1..H22 / HG).
  - Seleccionar una o varias **estaciones** y **tipos de datos** (nivel, caudal, temperatura, etc.).
  - Opcionalmente afinar por **señales** concretas.

El asistente de configuración está traducido y pensado para poder proponerse al **core de Home Assistant** sin depender del castellano.

### Data source & attribution / Fuente de datos y atribución

This integration consumes data published by **SAIH Ebro** (Sistema Automático de Información Hidrológica del Ebro) through its Open Data API.

- **Owner of the information and associated brands (SAIH Ebro, CHE, etc.)**: [Confederación Hidrográfica del Ebro](https://chebro.es/).
- **SAIH Ebro web (basin status / maps / resources)**: `https://www.saihebro.com/homepage/estado-cuenca-ebro`
- **Open Data area / login**: `https://www.saihebro.com/datos/opendata`

Notes:
- Data shown by SAIH Ebro may be **provisional** and subject to revision (see the notices on their own website).
- This integration is **not officially affiliated** with SAIH Ebro.

### How to obtain an API Key / Cómo obtener una API Key

To use the API you need an account and explicit access to the **Open Data API**.

1. Register at: `https://www.saihebro.com/usuarios/registro`  
2. In the form, in the **Remarks / Observaciones** field, explicitly write that you request access to **Open Data API**.

If you do not have an API Key (or it is not enabled), the API may answer with an error similar to:

```text
Unauthorized, use this url (https://www.saihebro.com/datos/opendata), to know how to get data from SAIH. You need an account. You can register in url (https://www.saihebro.com/usuarios/registro). In the user registration page, write in the Remarks field that you want to access Open Data API%
```

### Logos and images / Logos e imágenes

This repository is prepared to use:

- A **project logo** for the custom integration and HACS (for example: `images/logo.png`).
- A simpler **icon** for small contexts (for example: `images/icon.png`).

You can place your own PNG/SVG assets in the `images/` folder and reference them from:
- Home Assistant / HACS metadata (standard `logo.png` / `icon.png` files).
- This README, with something like:
  - `![SAIH Ebro integration logo](images/logo.png)`

In addition, you should always mention SAIH Ebro / Confederación Hidrográfica del Ebro as the **data source**, for example:

- Text used in the sensors:  
  `Datos proporcionados por SAIH Ebro – Confederación Hidrográfica del Ebro (CHE).`
- Link to `https://chebro.es/` and/or `https://www.saihebro.com/homepage/estado-cuenca-ebro`.

On the SAIH Ebro website there is an official logo available as SVG:

- `https://www.saihebro.com/images/logo-SAIH-pie.svg`

The original logo is **not redistributed** in this repository; instead we just reference it and keep a separate, neutral logo for the Home Assistant integration.

