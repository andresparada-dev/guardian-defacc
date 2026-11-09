// Renderiza video.html cuadro por cuadro (cada cuadro es función pura del tiempo).
// Uso: node render.js --fotos t1,t2           (imágenes de prueba)
//      node render.js --desde 0 --hasta 900   (rango de cuadros, para repartir el trabajo)
const {chromium} = require('playwright');
const path = require('path');
const fs = require('fs');

const arg = (k, def) => (process.argv.includes(k) ? process.argv[process.argv.indexOf(k) + 1] : def);
(async () => {
  const dir = __dirname, fps = 30, duracion = 120.0;
  const total = Math.round(fps * duracion);
  const navegador = await chromium.launch();
  const pagina = await navegador.newPage({viewport: {width: 1920, height: 1080}});
  await pagina.goto('file://' + path.join(dir, 'video.html'));
  await pagina.evaluate(() => window.listo);
  const fotos = arg('--fotos', null);
  if (fotos) {
    for (const t of fotos.split(',').map(Number)) {
      await pagina.evaluate((x) => window.render(x), t);
      await pagina.screenshot({path: path.join(dir, `foto_${t.toFixed(2)}.png`)});
    }
  } else {
    const desde = Number(arg('--desde', 0)), hasta = Math.min(Number(arg('--hasta', total)), total);
    fs.mkdirSync(path.join(dir, 'frames'), {recursive: true});
    for (let i = desde; i < hasta; i++) {
      await pagina.evaluate((x) => window.render(x), i / fps);
      await pagina.screenshot({path: path.join(dir, 'frames', `${String(i).padStart(4, '0')}.png`)});
    }
    console.log(`cuadros ${desde}-${hasta - 1} listos`);
  }
  await navegador.close();
})();
