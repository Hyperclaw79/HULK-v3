// Refer Nextron for docs.

import { app, BrowserWindow, ipcMain } from 'electron';
import serve from 'electron-serve';
import { createWindow } from './helpers';

const isProd: boolean = process.env.NODE_ENV === 'production';

if (isProd) {
  serve({ directory: 'app' });
} else {
  app.setPath('userData', `${app.getPath('userData')} (development)`);
}

(async () => {
  await app.whenReady();

  const mainWindow = createWindow('main', {
    width: 1920,
    height: 1080,
    show: false
  });
  mainWindow.maximize();
  mainWindow.show();


  if (isProd) {
    await mainWindow.loadURL('app://./index.html');
  } else {
    const port = process.argv[2];
    await mainWindow.loadURL(`http://localhost:${port}`);
  }

  ipcMain.on('request-reload', (event) => {
      const webWin = BrowserWindow.fromWebContents(event.sender);
      console.log('Refresh requested by the renderer.');
      webWin?.reload();
  });
})();

app.on('window-all-closed', () => {
  app.quit();
});
