# BikeJumilla DataOps — Esqueleto inicial (Odoo 18)

Punto de partida de la práctica del RA3 de Sistemas de Gestión Empresarial.

## Objetivo docente
El proyecto está preparado para instalarse, pero la lógica evaluable está sin resolver. Buscar `TODO` para localizar el trabajo del alumnado.

## Dependencias
`base`, `crm`, `sale_management`, `purchase`, `stock`.

## Instalación
1. Copiar `bikejumilla_dataops` a una ruta incluida en `addons_path`.
2. Reiniciar Odoo.
3. Actualizar la lista de aplicaciones.
4. Instalar **BikeJumilla DataOps**.

Ejemplo habitual durante desarrollo:
```bash
./odoo-bin -d NOMBRE_BD -u bikejumilla_dataops --stop-after-init
```
El comando exacto dependerá del despliegue del aula.

## Se proporciona
- Modelo persistente `bikejumilla.dataops.snapshot`.
- Wizard `bikejumilla.commercial.analysis.wizard`.
- Acción y plantilla QWeb para el informe.
- Acción planificada instalada desactivada.
- Menús y permisos mínimos.

## NO está resuelto
- Dominios y consultas ORM.
- Agregaciones.
- Presentación real de resultados.
- Líneas y métricas reales del informe.
- Extracción automática.
- Exportaciones.
- Profiling.
- Interpretación empresarial.
