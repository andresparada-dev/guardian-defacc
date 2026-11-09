# Video de demostración de 2 minutos

Es el entregable opcional del hackatón ("video de hasta 2 minutos mostrando el prototipo en funcionamiento"). Formato 1920×1080 a 30 fps, con textos en pantalla y música, sin locución.

| Tiempo | Escena |
|---|---|
| 0:00 | Apertura y título |
| 0:10 | La amenaza: inyección indirecta de instrucciones, en los dos escenarios |
| 0:22 | Escenario A en funcionamiento: cifra falsa sin defensa, bloqueada con el guardián, y pregunta legítima |
| 0:46 | Escenario B: factura con trampa simple y factura con trampa consistente (la detecta la segunda lectura por OCR) |
| 1:10 | Cómo funciona: flujo y defensas D1, D2 y D3 |
| 1:24 | La medición: terminal, gráfico y cifras clave |
| 1:42 | Límites y uso responsable |
| 1:52 | Cierre |

## Cómo regenerarlo

```bash
python scripts/generar_facturas.py                                  # desde la raíz del repo
cp datos/facturas/FE-PRUEBA-0016.png video/demo/factura16.png
cp datos/facturas/FE-PRUEBA-0018.png video/demo/factura18.png
python scripts/medir.py --modelo comprometido --ocr simulado        # copia el gráfico a video/demo/grafico.png
cd video/demo
node render.js --fotos 31.5,56.5,100                                # fotos de prueba
for r in "0 900" "900 1800" "1800 2700" "2700 3600"; do set -- $r; node render.js --desde $1 --hasta $2 & done; wait
cp frames/1695.png frames/0000.png                                  # portada como primer cuadro
ffmpeg -framerate 30 -i frames/%04d.png -t 120 -i musica.mp3 \
  -filter_complex "[1:a]volume=-3dB,afade=t=out:st=118.3:d=1.7[a]" -map 0:v -map "[a]" \
  -c:v libx264 -crf 19 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest guardian_demo_2min.mp4
```

- **Resultados:** la escena 1:24 muestra la medición con el modelo comprometido (peor caso simulado). Cuando haya resultados con Gemini, se cambian el comando y las líneas de `SALIDA`, los datos `f3` a `f5` y el gráfico, y se vuelve a generar.
- **Música:** "Happy Beats / Business Moves Vol. 1" de Sascha Ende ([ende.app](https://ende.app/en)), CC BY 4.0. Se guarda aparte como `musica.mp3`. El crédito va en el cierre del video.
