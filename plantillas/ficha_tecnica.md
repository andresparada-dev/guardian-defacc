# Ficha técnica · [Nombre del proyecto]

**Equipo:** [nombres] · **Frente:** 01, seguridad de agentes y defensa contra inyección de instrucciones · **Repositorio:** [enlace]

> Plantilla de trabajo. El sábado se reemplaza por la plantilla oficial de la organización, con el mismo contenido. Máximo una página.

## 1. Vector de amenaza
Inyección indirecta de instrucciones (OWASP LLM01:2025): un documento que el agente lee trae órdenes escondidas. Dos escenarios:
- **A · Cifras oficiales:** un asistente de datos del DANE publica una cifra falsa como si fuera oficial.
- **B · Facturas de pyme:** un asistente que lee facturas de WhatsApp aprueba un pago con un total falso.

## 2. Defensa
Controles por fuera del modelo:
1. **D1 · Delimitar:** el documento es dato, no orden.
2. **D2 · Forma fija:** en A, el modelo cita claves oficiales y el código pone el número; en B, un esquema estricto.
3. **D3 · Verificador y compuerta:** en A, cada cifra se compara con la tabla oficial del CENU; en B, se revisan subtotal + IVA = total, el IVA del 19 %, el dígito del NIT, una segunda lectura por OCR y el texto dirigido a la IA. Modos: aviso o bloqueo.

## 3. Metodología de evaluación
- **Casos:** [n] ataques en español en [n] familias, [n] preguntas legítimas y [n] facturas sintéticas ([n] limpias, [n] alteradas, [n] con trampa en 4 variantes).
- **Modelo:** [gemini-3.5-flash-lite o gemini-3.8-flash], temperatura 0. Referencia de peor caso: un modelo simulado que obedece todas las trampas.
- **Métricas:** % de ataques que llegan a la persona, % de casos legítimos bien resueltos y falsos positivos, por configuración.

## 4. Resultados
| Configuración | A · ataques exitosos | A · falsos positivos | B · trampas aprobadas | B · falsos positivos |
|---|---|---|---|---|
| Sin defensa | | | | |
| D1 | | | | |
| D1+D2 | | | | |
| D1+D2+D3 aviso | | | | |
| D1+D2+D3 bloqueo | | | | |

[Gráfico: resultados/<fecha>_<modelo>/grafico_ataques.png]

## 5. Límites
- El verificador de cifras no ve mentiras sin números, ni cifras oficiales reales puestas en el lugar equivocado, ni números estructurales (años, límites de rango).
- En facturas, una trampa con cifras consistentes solo se detecta con la segunda lectura por OCR.
- [n] casos, hechos por nosotros: margen de error amplio. Un integrante escribió un grupo de ataques sin ver las defensas.

## 6. Riesgo dual y uso responsable
Todo corre en local, con datos públicos del DANE y facturas sintéticas marcadas como "SIN VALIDEZ". No se atacó ningún sistema real. Los ataques se publican como casos de prueba, no como guía ofensiva.

## 7. Atribución
- **Preparado antes del evento:** [completar según lo que permita la organización].
- **Librerías:** pydantic, Pillow, pandas, matplotlib, google-genai, pytesseract.
- **Datos:** CENU 2024 (DANE), resultados preliminares.
- **Uso de IA:** [herramientas de IA usadas para escribir código o texto].
- **Referencias:** AgentBreak (C. Urcuqui), AgentDojo (ETH Zürich), OWASP Top 10 para aplicaciones con LLM.
