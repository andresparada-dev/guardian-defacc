# Video de 45 segundos · estilo lanzamiento de producto

Video corto del Guardián para redes y para abrir el pitch. 1920×1080 a 30 fps, con textos en pantalla y música, sin locución.

Toma el **estilo** de un video de lanzamiento de producto que nos compartieron como referencia: fondo de ciudad en trama de puntos (día, noche y color de marca), una línea fina que guía la mirada, textos cortos con la palabra clave resaltada, una caja de chat que se escribe sola, tarjetas que flotan y una disolución en píxeles antes del logo. No usa nada de esa marca: el skyline es el de Bogotá (Colpatria, Avianca, BD Bacatá, Atrio y los cerros con Monserrate), dibujado en código, y el color es el verde del Guardián.

## Guion

| Tiempo | Escena |
|---|---|
| 0:00 | 30 facturas por WhatsApp. Una trae una orden escondida. La IA la aprobó sola. |
| 0:04 | El total pasa de $ 8.532.300 a $ 90.000. Revisión humana: ninguna. (Se hace de noche.) |
| 0:08 | Caja de chat: "Hay una forma más segura". |
| 0:11 | Fondo verde con el panel del Guardián: cada documento, revisado antes de que decida la IA. |
| 0:15 | Revisa cada… factura, cifra, documento. |
| 0:19 | Diagrama: las entradas pasan por las firmas y las reglas, fuera del modelo. La IA propone; el código decide. |
| 0:24 | Verificación de FE-PRUEBA-0018: firmas F05 y F09, subtotal + IVA, segunda lectura por OCR y NIT. Decisión: revisión humana. |
| 0:29 | Detéctalo. Bloquéalo. |
| 0:34 | Tú eliges el modo: apagada, aviso o bloqueo. |
| 0:37 | Ataques que llegan: de 93 % a 7 % (peor caso simulado). "Bloqueada. Nada se pagó." |
| 0:41 | Logo sobre el skyline: "Guardián · def/acc Hackathon 2026". |

Las cifras salen del repositorio: la factura sintética FE-PRUEBA-0018 (total real $ 8.532.300, total falso $ 90.000), lo que reporta el verificador sobre ella y los resultados del peor caso simulado del 10 de noviembre (cifras: 14 de 15 ataques sin defensa y 1 de 15 con firmas y reglas). **No son resultados de Gemini.** Cuando estén las mediciones reales, se cambian los números en `video.html` y se vuelve a renderizar.

## Cómo se genera

Necesita las facturas sintéticas (`python scripts/generar_facturas.py`), Node con Playwright y ffmpeg.

```bash
cd video/estilo
node render.js --fotos 2.4,12,26,41.1                                     # fotos de prueba
for r in "0 338" "338 676" "676 1014" "1014 1350"; do set -- $r; node render.js --desde $1 --hasta $2 & done; wait
ffmpeg -framerate 30 -i frames/%04d.png -t 45 -i musica.mp3 \
  -filter_complex "[1:a]volume=0.85,afade=t=in:st=0:d=0.5,afade=t=out:st=42.5:d=2.5[a]" \
  -map 0:v -map "[a]" -c:v libx264 -pix_fmt yuv420p -crf 20 -preset slow \
  -c:a aac -b:a 192k -movflags +faststart -shortest guardian_estilo_45s.mp4
```

- **Música:** "Happy Beats / Business Moves Vol. 12" de Sascha Ende ([ende.app](https://ende.app/en)), CC BY 4.0. Se guarda aparte como `musica.mp3`. El crédito va en el cierre del video y hay que repetirlo al publicarlo.
- **Fuente:** Inter.
