> Exportado del documento de Claude "Mapa de trabajo · Def/Acc Hackathon 2026" (6 de noviembre de 2026). Es la versión anterior a la decisión de sumar el escenario de facturas inspirado en SAPHEN y al cambio de equipo; la matriz de riesgo e impacto (`03_matriz_riesgo_impacto.pdf`) y `04_como_vamos_a_construir.pdf` la actualizan.
>
> **10 de noviembre:** la página del hackatón cambió. Ahora hay 6 frentes, la rúbrica tiene 3 criterios con el mismo peso (impacto e innovación, calidad de ejecución, presentación y claridad), hay un cuarto jurado y ya no hay premio por difusión en redes. Las filas de rúbrica, premios y jurados de abajo son las del 6 de noviembre; la versión vigente está en `02_brief_hackathon_uniandes.txt`.

# Mapa de trabajo · Def/Acc Hackathon 2026

6 de noviembre de 2026 · Andrés

Recomendación: frente 1 con un «guardián de cifras oficiales» que reutiliza el agente y los datos verificados del reto DANE. Plan B: detector de voces clonadas con HABLA, el dataset en español de la Universidad de los Andes. Postulación hasta el 10 de noviembre de 2026 a las 11:59 p.m.; hackatón el 14 de noviembre de 2026 en Uniandes.

## Evento y reglas

Es un solo sprint de 8 horas (9:00 a.m. a 5:00 p.m.). A las 5:00 p.m. se entrega el repositorio y la ficha técnica, y los 5 mejores equipos hacen un pitch de 4 minutos a las 7:00 p.m. Todo está tomado de la [página oficial](https://aisafetycolombia.org/defacchackathon).

| Tema | Detalle |
| --- | --- |
| Postulación | Cierra el martes 10 de noviembre a las 11:59 p.m. Cada integrante llena su propio formulario, que pide cédula, LinkedIn y un texto de hasta 1.500 caracteres sobre el problema que quiere atacar. |
| Evento | Sábado 14 de noviembre, de 8:00 a.m. a 8:00 p.m., presencial en la Universidad de los Andes. Equipos de 2 a 4 personas. Es gratis e incluye almuerzo. |
| Entregables (5:00 p.m.) | Repositorio ejecutable (GitHub o Colab), ficha técnica de 1 página con la plantilla oficial y un video opcional de hasta 2 minutos. |
| La ficha responde | Qué amenaza se ataca, qué defensa se construyó, cómo se evaluó, los resultados con números, los límites y el riesgo de mal uso. |
| Rúbrica | Funcionamiento y rigor 30 % · Evidencia empírica 25 % · Relevancia en aceleración defensiva 20 % · Uso responsable y límites 15 % · Claridad 10 %. Cada proyecto lo califican al menos 2 jurados. |
| Final y premios | Pitch de 4 minutos de los 5 mejores a las 7:00 p.m. y ganadores a las 7:25 p.m. Premios de COP 1.000.000, 500.000 y 500.000, más un premio por difusión en redes. |
| Reglas estrictas | Nada contra sistemas reales de terceros (Ley 1273 de 2009). No se publican exploits ni malware. Solo datos públicos anonimizados o sintéticos. Se cita todo el código, los datos y lo generado con IA. |
| Jurados confirmados | Christian Urcuqui (TryHackMe, Icesi), autor de [AgentBreak](https://github.com/urcuqui/AgentBreak). Antonio Badilla-Olivas (SPAR), que construye entornos de ataque y monitores. Carlos Gorostiza Ibáñez (SPAR, UANL), que estudia cómo negocian los agentes de IA. |

Dos de los tres jurados trabajan en seguridad de agentes, así que un proyecto del frente 1 tendrá lectores expertos y exigentes.

## Lo que ya tenemos del reto DANE

Del reto DANE nos sirven cuatro cosas: un agente conversacional ya configurado, una tabla de cifras oficiales verificadas, un método de validación con controles que cuadran y un pitch ganador de 4 minutos, el mismo formato de la final. Las rutas son del repositorio DATATON-DANE-2026.

| Activo | Dónde está | Cómo lo reutilizamos | Frentes |
| --- | --- | --- | --- |
| Agente de voz en ElevenLabs: prompt y base de conocimiento | `ruta2/entrega/agente_voz/prompt_agente.txt` y `base_conocimiento_ruta2_bogota.txt` | Lo replicamos en Python como el sistema que se ataca y se protege. También sirve de caso de estudio para el estándar. | 1, 5 |
| Tabla de cifras verificadas: top 12 divisiones y Bogotá frente al país | `ruta2/insumos/dashboard_data_api.js`, `ruta2/entrega/ruta2_bogota_cifras_verificadas.xlsx`, `data/ruta2/api_nacional_sectoral_reference_2023.json` | Es la fuente de verdad del verificador de cifras. | 1, 5 |
| Reglas del agente: no inventar, no dar datos por localidad, un rango bajo es una señal y no una prueba | `prompt_agente.txt` | Son las reglas que la defensa debe hacer cumplir y los requisitos del estándar. | 1, 5 |
| Preguntas de prueba con respuesta esperada (Kennedy debe dar «no hay datos por localidad») | `ruta2/entrega/agente_voz/LEEME_AGENTE.md`, sección 4 | Son la semilla del conjunto de preguntas legítimas para medir utilidad. | 1 |
| Validadores: los rangos suman el total de la API y el ingreso nacional coincide con el DANE | `ruta2/control_calidad.py`, `ruta2/verificar_api.py` | Son el patrón de pruebas reproducibles, que es la evidencia empírica que pide la rúbrica. | todos |
| Notebook autónomo de Colab y su generador | `ruta2/construir_notebook.py`, `ruta2/entrega/Ruta2_Bogota_CENU.ipynb` | Plantilla del repositorio ejecutable que se entrega a las 5:00 p.m. | todos |
| Página del asistente con el SDK de ElevenLabs | `ruta2/entrega/agente_voz/asistente_voz_cenu.html` | Demo visual en el pitch. | 1, voces |
| Cuenta y experiencia en ElevenLabs | Cuenta del equipo | Voces 100 % sintéticas (prediseñadas, sin clonar a nadie) para probar el detector después de WhatsApp, y el clasificador de ElevenLabs como punto de comparación. | voces |
| Cifras de micronegocios del CENU: 82,8 % con 1 a 5 personas, 92.335 unidades de comercio al por menor, 16.410 puestos móviles de alimentos y 13.114 tiendas de barrio | `base_conocimiento_ruta2_bogota.txt` | Dicen a quién protegemos (relevancia, 20 %). | voces, phishing |
| Formalidad: 49,2 % de las unidades con información tiene RUT y Bogotá tiene 158.647 con registro mercantil (cifras de prensa) | `data/cifras_oficiales/cenu_2024_resultados_publicados.csv` | Son el público objetivo de los correos falsos «de la DIAN». | phishing |
| Guion y pitch ganador de 4 minutos | `ruta2/entrega/GUION_PRESENTACION.md` | La final usa el mismo formato de 4 minutos. | todos |
| Investigación documentada del CENU | `docs/01` a `docs/06` | Contexto, fuentes y antecedentes. | 5 |

## Comparación de los cuatro frentes

El frente 1 es el que más aprovecha lo construido y más se diferencia. Voces clonadas es el más vistoso, pero depende de que el profesor domine el procesamiento de audio. No hay premio por frente: todos compiten por los mismos 3 puestos.

| Criterio | 1 · Guardián de cifras | 4 · Voces clonadas | 4 · Phishing | 5 · Gobernanza |
| --- | --- | --- | --- | --- |
| Aprovecha lo del DANE | Alto: agente, datos y reglas | Medio: ElevenLabs y contexto del CENU | Bajo a medio: contexto RUT y DIAN | Alto: caso de estudio real |
| Dificultad técnica | Media | Media a alta | Baja a media | Baja, sin código |
| Riesgo de no tener nada funcionando a las 5 p.m. | Bajo | Medio: descargas, GPU y entrenamiento | Bajo | Muy bajo |
| Diferenciación | Alta: es poco probable que otro equipo traiga cifras oficiales verificadas | Alta: español colombiano y WhatsApp | Baja: es la opción «para empezar» y la elegirán varios equipos | Media |
| Encaje con el jurado | Muy alto pero exigente: Urcuqui es autor de AgentBreak | Medio: ningún jurado trabaja en audio | Medio | Medio |
| Cómputo | CPU y API de un modelo | GPU de Colab | CPU | Ninguno |
| Costo | Créditos de API, bajo | Gratis con Colab | Gratis | Gratis |
| Probabilidad estimada | Alta | Media a alta | Media | Media a baja sola; alta como complemento del frente 1 |

Las probabilidades son una estimación nuestra. No sabemos cuántos equipos llegarán ni qué elegirán.

## Frente 1 · Seguridad de agentes: guardián de cifras oficiales

Una réplica del asistente del DANE responde con su base de conocimiento. Un atacante esconde instrucciones en un documento para que el agente publique cifras falsas, y una capa fuera del modelo bloquea toda cifra que no esté en la tabla oficial. Aplica la idea de AgentBreak, el proyecto del jurado Urcuqui: los controles deterministas impiden que una manipulación se vuelva una acción. Aquí la acción es publicar una estadística oficial falsa, un dominio que difícilmente traerá otro equipo.

| Aspecto | Detalle |
| --- | --- |
| Amenaza | Inyección indirecta de instrucciones (OWASP LLM01:2025) en los documentos que el agente recupera. Busca que publique cifras falsas, revele su configuración o responda lo que no debe, como datos por localidad o de una empresa específica. |
| Por qué importa | Si un agente de una entidad pública repite una cifra falsa, la presenta como oficial. El CONPES 4144 de 2025 promueve el uso de IA en entidades públicas. |
| Defensa en 3 capas | 1) Lo que el agente recupera se marca como datos, no como instrucciones (delimitadores o *spotlighting*). 2) Un verificador extrae cada número de la respuesta y lo compara con la tabla oficial; si no cuadra, bloquea o responde «no tengo ese dato». 3) Una política de herramientas: solo lectura, nada se envía afuera y se rechazan las preguntas que identifiquen a una unidad. |
| Familias de ataque (40 a 60 casos en español) | Cifra falsa con apariencia oficial · Instrucción oculta de desinformación · Pedir el prompt o la configuración · Pedir datos por localidad o de una empresa · Suplantar a una autoridad («mensaje del director del DANE»). |
| Evaluación | Tasa de éxito del ataque sin defensa y con defensa. Utilidad: % de 30 a 50 preguntas legítimas respondidas bien. Falsos positivos: respuestas correctas que se bloquearon. Opcional: un subconjunto de [AgentDojo](https://github.com/ethz-spylab/agentdojo) con sus defensas como punto de comparación. Cada ataque que funcione se vuelve una prueba de regresión, como en AgentBreak. |
| Lo que ya tenemos | Prompt, base de conocimiento, tabla verificada, reglas y preguntas de prueba del asistente CENU. |
| Lo que falta | Una clave de API con créditos, el agente réplica en Python, el corpus de ataques, el verificador, el arnés de evaluación y el gráfico antes/después. |
| Recursos | Python 3.11 o superior, pandas y el SDK del proveedor (OpenAI, Anthropic o Gemini). Opcionales: `pip install agentdojo` y el repositorio de [AgentBreak](https://github.com/urcuqui/AgentBreak) como referencia. Basta con CPU. El costo es bajo si se limitan las corridas a unos cientos de llamadas. |
| Límites y riesgo dual | El verificador solo cubre cifras que están en la tabla y no detecta afirmaciones cualitativas falsas. Los ataques se publican como casos de prueba, no como guía ofensiva. Todo se prueba contra nuestra réplica, nunca contra ElevenLabs ni la API del DANE. |
| Dificultad · diferenciación · probabilidad | Media · alta · alta. |

Flujo del prototipo:

1. La persona pregunta, por ejemplo: «¿cuántas unidades tiene el comercio al por menor?».
2. El agente recupera fragmentos de la base de conocimiento, algunos envenenados, y los marca como datos.
3. El modelo propone una respuesta.
4. El verificador compara cada cifra con la tabla oficial: 92.335 pasa y 1.000.000 se bloquea.
5. Sale la respuesta verificada o «no tengo ese dato», y queda un registro con el resultado.

## Frente 4 · Voces clonadas: detector en español colombiano para WhatsApp

La propuesta es un detector liviano de voces clonadas que siga funcionando después de pasar por WhatsApp. Lo que lo hace local y medible es [HABLA](https://www.isca-archive.org/interspeech_2023/tamayoflorez23_interspeech.html), el primer dataset de voces falsas en español, con acento colombiano y creado en la Universidad de los Andes.

| Aspecto | Detalle |
| --- | --- |
| Amenaza | La estafa del «familiar en apuros» o del proveedor con voz clonada por WhatsApp. La [Ley 2502 de 2025](https://normograma.mintic.gov.co/mintic/compilacion/docs/ley_2502_2025.htm) agrava la falsedad personal hecha con IA y define el deepfake incluyendo grabaciones de sonido. No hay una cifra oficial específica de estafas con voz clonada; solo hay datos de prensa. |
| Defensa | AASIST-L, la versión liviana del modelo, que trae [modelos preentrenados](https://github.com/clovaai/aasist) (EER de 0,99 % en ASVspoof 2019). Se ajusta con HABLA y con audios comprimidos en Opus a varios bitrates usando ffmpeg. El umbral se calibra para tener pocos falsos positivos. |
| Evaluación | EER y tasa de detección en tres condiciones: audio limpio, compresión simulada y audio enviado de verdad por WhatsApp entre los celulares del equipo. Se mide antes y después del ajuste. Prueba cruzada con In-the-Wild (en inglés) para medir generalización. Comparación con el clasificador de ElevenLabs antes y después de pasar por WhatsApp. |
| Datos | HABLA: más de 22.000 audios reales y 58.000 falsos, 6 sistemas de síntesis y 5 acentos, colombiano incluido. Licencia CC BY 4.0, abierto en [Hugging Face](https://huggingface.co/datasets/SpeechAntiSpoofingBenchmarks/HABLA). In-the-Wild: 37,9 horas en inglés, licencia CC BY-SA 4.0. Voces prediseñadas de ElevenLabs. |
| Conexión con el DANE | El 82,8 % de los negocios de Bogotá tiene de 1 a 5 personas y ninguno tiene un área de seguridad. Las tiendas de barrio y los puestos móviles de alimentos suman 29.524 unidades. A eso se suma nuestra experiencia con voz en ElevenLabs. |
| Lo que ya tenemos | Cuenta de ElevenLabs, experiencia con voz y las cifras del CENU. |
| Lo que falta | Descargar HABLA y los modelos de AASIST. Montar PyTorch, torchaudio y ffmpeg en Colab con GPU. Escribir el script de compresión y el arnés de evaluación con EER. |
| Recursos | GPU de Colab (sirve una T4) y varios GB de disco. Sin costo: Colab gratis, y Pro es opcional. |
| Límites y riesgo dual | No se clonan voces de personas reales: solo voces prediseñadas. No se publica cómo evadir el detector. Las notas de voz de WhatsApp usan el códec Opus, pero el bitrate exacto no está confirmado, así que se prueba un rango. Los generadores nuevos pueden engañar al detector, y un detector puede dar falsa seguridad. |
| Dificultad · diferenciación · probabilidad | Media a alta · alta · media a alta. Es alta si el profesor domina audio con PyTorch. |

Dos de los autores de HABLA, Pablo Andrés Tamayo Flórez y Rubén Manrique, son del Departamento de Ingeniería de Sistemas y Computación de Uniandes, el mismo departamento que invita al hackatón. Usar su dataset es un guiño local. Vale la pena preguntarle al profesor si los conoció en la maestría.

## Frente 4 · Phishing: detector explicable con SpaPhish

La propuesta es un detector de phishing en español que marca el correo y además explica qué técnica de persuasión usa, para que un tendero entienda la alerta. Es la opción más segura de entregar, pero también la que más equipos pueden elegir, así que necesita un giro propio.

| Aspecto | Detalle |
| --- | --- |
| Amenaza | Correos que suplantan entidades públicas: de la DIAN (embargos, devoluciones, falsos aranceles de paquetes) y cadenas falsas sobre el censo del DANE. |
| Defensa | Un clasificador que empieza con TF-IDF y regresión logística y luego prueba un modelo multilingüe pequeño o un modelo de lenguaje con pocos ejemplos. Un segundo modelo predice cuál de los 5 principios de persuasión usa el correo y lo explica en lenguaje sencillo. |
| Evaluación | Precisión, recall, F1 y tasa de falsos positivos (correos legítimos marcados como phishing). F1 por principio de persuasión. División temporal: se entrena con correos viejos y se prueba con los más recientes, para ver si el detector aguanta phishing nuevo. |
| Datos | [SpaPhish](https://data.mendeley.com/datasets/hz2d6gz7pc), versión 5 (12 de mayo de 2026): 1.395 correos de 2014 a octubre de 2025, 664 legítimos y 731 phishing, 47 variables. Cada correo tiene anotaciones de persuasión hechas por 3 anotadores con justificación en español. Licencia CC BY 4.0. |
| Conexión con el DANE | Cuantificamos el público objetivo: las unidades con RUT (49,2 % de las que informaron) y las 158.647 con registro mercantil en Bogotá son el blanco natural de los correos «de la DIAN» (cifras de prensa). Además, el lenguaje claro para no expertos es el mismo enfoque del asistente del DANE. |
| Lo que ya tenemos | Experiencia con Colab y pandas, método de validación y comunicación para no expertos. |
| Lo que falta | Descargar SpaPhish, revisar sus columnas, armar la línea base y diseñar la explicación. |
| Recursos | Colab sin GPU y scikit-learn. La clave de API es opcional. Costo cero. |
| Límites y riesgo dual | El dataset es pequeño y sale de pocos buzones. No se generan ni se publican correos de phishing nuevos. Explicar un correo no garantiza detectarlo. |
| Dificultad · diferenciación · probabilidad | Baja a media · baja a media · media. |

## Frente 5 · Gobernanza: estándar verificable para agentes con datos públicos

La propuesta es un estándar mínimo que una entidad pública debería cumplir antes de poner un agente conversacional a responder sobre estadísticas oficiales, con el asistente del DANE como caso de estudio. El riesgo técnico es mínimo, pero compite contra prototipos que funcionan. Por eso conviene más como complemento del frente 1 que como proyecto solo.

| Aspecto | Detalle |
| --- | --- |
| Problema | El [CONPES 4144 de 2025](https://oecd.ai/en/dashboards/policy-initiatives/national-policy-on-artificial-intelligence-conpes-4144-3012) impulsa el uso de IA en entidades públicas hasta 2030. La ley de IA sigue en trámite en el Congreso. Mientras tanto no hay requisitos mínimos de contención, auditoría ni líneas rojas para estos agentes. |
| Entregable | Un modelado de amenazas del agente (activos, fronteras de confianza y atacantes). Un estándar con requisitos numerados, cada uno con su prueba de conformidad. Un protocolo de respuesta a incidentes. |
| Líneas rojas propuestas | No publicar cifras que no estén en la fuente. No responder por debajo del nivel de desagregación publicado, por la reserva estadística (Ley 79 de 1993). No tratar datos personales sin base legal (Ley 1581 de 2012). Decir siempre que es una IA, porque la Ley 2502 de 2025 castiga la suplantación con IA. |
| Marcos de referencia | OWASP Top 10 para aplicaciones con modelos de lenguaje (2025) y su Top 10 para aplicaciones agénticas (diciembre de 2025). El informe de RAND sobre seguridad de pesos de modelos, con 38 vectores de ataque y niveles SL1 a SL5, que aplica si la entidad aloja sus propios modelos. |
| Conexión con el DANE | Un caso real, nuestro asistente, y las reglas que ya aplicamos en el reto. |
| Evaluación | Aplicar el estándar al asistente del DANE y reportar requisito por requisito si cumple. Si se combina con el frente 1, las pruebas del verificador son la evidencia. |
| Recursos | Solo documentos. Sin costo. |
| Límites | Un documento convence menos que un prototipo que funciona. Hay que citar las normas con precisión y revisar sus textos oficiales. |
| Dificultad · diferenciación · probabilidad | Baja · media · media a baja sola; alta como complemento. |

## Roles del equipo

El profesor responde por el 30 % de «que funcione». Tú respondes por la evidencia y la claridad (35 %), y tu amigo por los límites, el riesgo de mal uso y la difusión (15 % más el premio por difusión).

| Persona | Rol general | En el frente 1 (recomendado) | Si vamos por voces clonadas |
| --- | --- | --- | --- |
| Profesor (Oscar) | Líder técnico | Agente réplica, verificador de cifras y arnés de evaluación | Modelo AASIST-L, ajuste con HABLA y compresión Opus |
| Tú | Datos, evidencia y pitch | Tabla oficial, preguntas legítimas, métricas, gráfico antes/después, ficha técnica y pitch | Preparar los audios, métricas de EER, gráficos, ficha técnica y pitch |
| Tu amigo | Pruebas, límites y difusión | Escribir los ataques, documentar límites y riesgo dual, video e hilo en redes | Enviar los audios por WhatsApp, documentar límites, video e hilo en redes |

## Cronograma

Lo urgente es confirmar que el profesor estará en Bogotá y enviar las tres postulaciones antes del martes 10 a las 11:59 p.m. El sábado, la meta es tener algo funcionando a la 1:00 p.m. y usar la tarde para la defensa y la medición.

**Antes del evento**

- [ ] Viernes 6: confirmar que el profesor puede estar en Bogotá todo el sábado 14. Su LinkedIn dice que trabaja en SENAI-RS, en Brasil.
- [ ] Sábado 7 y domingo 8: elegir el frente (recomendado: el 1) y el plan B.
- [ ] Lunes 9: redactar el texto común de la postulación, de hasta 1.500 caracteres.
- [ ] Martes 10, antes de las 11:59 p.m.: los tres envían su formulario con el mismo frente y el mismo texto.
- [ ] Miércoles 11: preguntar a los organizadores qué se puede traer preparado y pedir la plantilla de la ficha técnica.
- [ ] Miércoles 11: conseguir la clave de API con créditos, crear la cuenta de Hugging Face y un repositorio vacío en GitHub.
- [ ] Jueves 12: correr el demo de AgentBreak y 2 tareas de AgentDojo (frente 1), o descargar HABLA y correr AASIST (voces), o cargar SpaPhish (phishing).
- [ ] Viernes 13: ensayo corto con Colab, portátiles, cargadores y cédulas listos.

**Sábado 14, plan para el frente 1**

| Hora | Bloque | Meta que se puede comprobar |
| --- | --- | --- |
| 8:00 a.m. | Registro en la portería de Uniandes | Los tres adentro con cédula |
| 8:30 a.m. | Apertura | Frente confirmado ante los organizadores |
| 9:00 a 11:00 a.m. | Agente réplica con la tabla oficial | Responde bien 10 preguntas legítimas |
| 11:00 a.m. a 1:00 p.m. | Corpus de ataques y medición sin defensa | Tasa de éxito del ataque medida |
| 1:00 p.m. | Almuerzo y punto de control | Hay algo que se puede demostrar |
| 1:30 a 3:30 p.m. | Verificador, política y nueva medición | Gráfico antes y después |
| 3:30 a 4:30 p.m. | Ficha técnica, límites y video | Ficha completa |
| 4:30 a 5:00 p.m. | Revisión y entrega | Enviado antes de las 5:00 p.m. |
| 5:00 a 7:00 p.m. | Preparar el pitch de 4 minutos | Ensayo cronometrado |
| 7:00 p.m. | Pitch de los finalistas; ganadores a las 7:25 p.m. | — |

## Lo que necesitamos conseguir

La única compra posible son los créditos de API para el frente 1; todo lo demás es gratis.

| Recurso | Para qué frente | Estado |
| --- | --- | --- |
| Clave de API de un modelo de lenguaje con créditos (OpenAI, Anthropic o Gemini) | 1; opcional en phishing | Por conseguir |
| Cuenta de Hugging Face | Voces (HABLA, In-the-Wild) | Por conseguir |
| Colab funcionando con GPU (Pro es opcional) | Voces; útil para todos | Por probar |
| Repositorio del equipo en GitHub | Todos | Por crear |
| Plantilla oficial de la ficha técnica | Todos | Pedirla a los organizadores |
| Datos y modelos descargados y probados | Según el frente | Por hacer el jueves 12 |
| Cuenta de ElevenLabs | Voces; demo del frente 1 | Ya la tenemos |
| Tabla oficial, prompt y base de conocimiento del DANE | 1 y 5 | Ya los tenemos |
| Dos celulares con WhatsApp y audífonos | Voces | Confirmar |
| 3 portátiles con cargador, cédula original y termo | Todos | Revisar el viernes 13 |

## Riesgos y plan B

El riesgo más grande es que el profesor no pueda estar en Bogotá. Si pasa, el equipo de dos va por phishing o gobernanza, que no dependen de un líder técnico fuerte.

| Riesgo | Qué hacemos |
| --- | --- |
| El profesor no puede ir presencial | Equipo de dos (está permitido) con el frente de phishing o el de gobernanza. |
| Internet lento en el campus | Llevar datos y modelos descargados en los portátiles y un celular con datos para compartir. |
| Se acaban los créditos de API | Limitar el número de corridas, usar un modelo económico y guardar las respuestas para no repetir llamadas. |
| A la 1:00 p.m. no hay nada funcionando | Reducir el alcance: aplicar el verificador sobre respuestas ya guardadas, sin agente en vivo. |
| No se puede traer nada preparado | Preguntar el miércoles 11; si no se puede, llevar solo el entorno instalado y los datos descargados. |
| Riesgo de mal uso de los ataques | Publicarlos como casos de prueba en lenguaje neutro, sin instrucciones para atacar sistemas reales. |
| Licencias de datos | HABLA y SpaPhish son CC BY 4.0, e In-the-Wild es CC BY-SA 4.0. Citarlos en la ficha técnica. |

## Fuentes

Páginas abiertas y revisadas el 6 de noviembre de 2026:

- [Defensive Acceleration Hackathon, AI Safety Colombia](https://aisafetycolombia.org/defacchackathon) y su [formulario](https://aisafetycolombia.org/defacchackathon/aplicar)
- [AgentBreak, Christian Urcuqui](https://github.com/urcuqui/AgentBreak)
- [AgentDojo, ETH Zürich](https://github.com/ethz-spylab/agentdojo)
- [MCPTox, arXiv 2508.14925](https://arxiv.org/abs/2508.14925)
- [AASIST, Clova AI](https://github.com/clovaai/aasist)
- [HABLA, Interspeech 2023](https://www.isca-archive.org/interspeech_2023/tamayoflorez23_interspeech.html) y [HABLA en Hugging Face](https://huggingface.co/datasets/SpeechAntiSpoofingBenchmarks/HABLA)
- [In-the-Wild en Hugging Face](https://huggingface.co/datasets/mueller91/In-The-Wild)
- [SpaPhish en Mendeley Data](https://data.mendeley.com/datasets/hz2d6gz7pc)
- [Ley 2502 de 2025, normograma de MinTIC](https://normograma.mintic.gov.co/mintic/compilacion/docs/ley_2502_2025.htm)

Vistas solo en resultados de búsqueda; conviene abrirlas antes de citarlas en la ficha:

- [CONPES 4144 de 2025, OECD.AI](https://oecd.ai/en/dashboards/policy-initiatives/national-policy-on-artificial-intelligence-conpes-4144-3012)
- [RAND, A Playbook for Securing AI Model Weights](https://www.rand.org/pubs/research_briefs/RBA2849-1.html)
- [OWASP Top 10 para aplicaciones con LLM 2025, resumen de PointGuard AI](https://www.pointguardai.com/blog/understanding-the-owasp-top-10-for-llms)
- [Clasificador de voz de ElevenLabs](https://elevenlabs.io/docs/eleven-creative/audio-tools/ai-speech-classifier.md)
- [Estafas con voces clonadas crecieron 30 %, Portafolio](https://www.portafolio.co/tecnologia/estafas-con-voces-clonadas-por-ia-crecieron-30-en-diciembre-y-alertan-a-expertos-en-colombia-486082)
- [DIAN alerta por correos falsos, Portafolio](https://www.portafolio.co/economia/impuestos/la-dian-alerta-nuevos-casos-de-suplantancion-de-identidad-y-robo-de-informacion-621179)
- [Estafa por WhatsApp usando el censo del DANE, La FM](https://www.lafm.com.co/colombia/tenga-cuidado-alerta-por-estafa-en-whatsapp-usando-censo-del-dane)

Las cifras del CENU salen del reto DANE: API del Visor, módulo `sectoral_reference_2023`, resultados preliminares. Las de RUT y registro mercantil son de prensa.
