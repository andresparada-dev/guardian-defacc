# Teaser de 23 segundos

Video horizontal (1920×1080, 30 fps) del guardián sobre la factura sintética FE-PRUEBA-0018. Cada cuadro es una función del tiempo (`window.render(t)` en `video.html`): Playwright toma los 690 cuadros y ffmpeg los une con la música.

```bash
python scripts/generar_facturas.py                         # desde la raíz del repo
cp datos/facturas/FE-PRUEBA-0018.png video/teaser/factura.png
cd video/teaser
node render.js --fotos 3.5,6.9,15.0                        # fotos de prueba
node render.js                                             # 690 cuadros en frames/
cp frames/0450.png frames/0000.png                         # portada como primer cuadro
ffmpeg -framerate 30 -i frames/%04d.png -t 23 -i musica.mp3 \
  -filter_complex "[1:a]volume=-2dB,afade=t=out:st=21.9:d=1.1[a]" -map 0:v -map "[a]" \
  -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest guardian_teaser.mp4
```

- **Música:** "Happy Beats / Business Moves Vol. 10" de Sascha Ende ([ende.app](https://ende.app/en)), licencia CC BY 4.0. No está en el repositorio: se descarga aparte y se guarda como `musica.mp3`. Crédito obligatorio: "Música: Sascha Ende, ende.app (CC BY 4.0)".
- **Cifras:** la escena del guardián muestra la salida real del verificador con el modelo comprometido (peor caso simulado) y OCR simulado. Cuando haya resultados con Gemini, se cambian los textos de las escenas 2 y 4 por los reales.
- Estructura y reglas tomadas de la skill /brag-slim (latent-spaces/brag, MIT).
