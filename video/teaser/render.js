// Renderiza video.html cuadro por cuadro (cada cuadro es función pura del tiempo).
// Uso: node render.js [--fotos t1,t2,...]   → con --fotos solo guarda esas imágenes de prueba.
const {chromium} = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const dir = __dirname;
  const fotos = process.argv.includes('--fotos') ? process.argv[process.argv.indexOf('--fotos') + 1].split(',').map(Number) : null;
  const fps = 30, duracion = 23.0;
  const navegador = await chromium.launch();
  const pagina = await navegador.newPage({viewport: {width: 1920, height: 1080}});
  await pagina.goto('file://' + path.join(dir, 'video.html'));
  await pagina.evaluate(() => window.listo);
  if (fotos) {
    for (const t of fotos) {
      await pagina.evaluate((x) => window.render(x), t);
      await pagina.screenshot({path: path.join(dir, `foto_${t.toFixed(2)}.png`)});
    }
  } else {
    const total = Math.round(fps * duracion);
    fs.mkdirSync(path.join(dir, 'frames'), {recursive: true});
    for (let i = 0; i < total; i++) {
      await pagina.evaluate((x) => window.render(x), i / fps);
      await pagina.screenshot({path: path.join(dir, 'frames', `${String(i).padStart(4, '0')}.png`)});
    }
    console.log(`${total} cuadros listos`);
  }
  await navegador.close();
})();
