const electron = require('electron')
const path = require('path')
const url = require('url')

// Module to control application life
const app = electron.app;

// Module to create native browser window
const BrowserWindow = electron.BrowserWindow;

// Module to work with 
const ipcMain = electron.ipcMain;

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow;
let backgroundWindow;


function createWindow () {
  
  mainWindow = new BrowserWindow({width: 800, height: 600});

  mainWindow.loadURL(url.format({
    pathname: path.join(__dirname, 'index.html'),
    protocol: 'file:',
    slashes: true
  }));

  // Open the DevTools.
  mainWindow.webContents.openDevTools()

  // Emitted when the window is closed.
  mainWindow.on('closed', function () {
    mainWindow = null
  });
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow);

// Quit when all windows are closed.
app.on('window-all-closed', function () {
    if (process.platform !== 'darwin'){
        app.quit();
    }
});

app.on('activate', function () {
    if (mainWindow == null) {
        createWindow();
    }
});
