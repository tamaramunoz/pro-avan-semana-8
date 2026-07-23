# Programación Avanzada - Semana 8

Solución práctica para la **Semana 8** de la asignatura **Programación Avanzada**. El objetivo de esta semana fue diseñar e implementar una aplicación de escritorio modularizada en Python conectada a una base de datos MySQL para el sistema de **Centro de Control de Agencias Espaciales**, permitiendo realizar el flujo completo de operaciones CRUD de manera segura e intuitiva.

## Conceptos Técnicos Aplicados

1. **Persistencia de Datos y Operaciones CRUD en MySQL:** Configuración de credenciales de acceso e integración mediante el conector de Python (`mysql.connector`) para realizar la creación (`INSERT`), lectura (`SELECT`), actualización (`UPDATE`) y eliminación (`DELETE`) de registros en la base de datos relacional.
2. **Arquitectura Modular y Separación de Responsabilidades:** Organización estructurada del proyecto mediante la segregación del código en módulos independientes (`config.py`, `database.py`, `gui.py`, `utils.py`, `styles.py` y `main.py`), desacoplando por completo la gestión de la base de datos, la interfaz gráfica y la configuración estacional de estilos.
3. **Diseño de Interfaz Gráfica e Interacción por Eventos:** Construcción de un panel interactivo en Tkinter con maquetación limpia mediante contenedores (`LabelFrame`, `Frame`), controles de interacción (`Listbox`, `Scrollbar`, `Entry`, `Button`) y enlace de eventos (*event binding*) para autocompletar formularios tras la selección de registros.

## Tecnologías utilizadas

- Python
- Tkinter
- MySQL Workbench

## Desarrollado por:

- Tamara Muñoz
