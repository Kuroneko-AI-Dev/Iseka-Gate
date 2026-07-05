
## Ganti model live2d
Kalau mau ganti model Live2D, tidak perlu ubah React (App.jsx, AvatarStage.jsx, Live2DCanvas.jsx). Yang diganti hanya folder model dan path di konfigurasi.

Alurnya:

React
 ↓
Live2DCanvas.jsx
 ↓
LAppDelegate
 ↓
LAppLive2DManager
 ↓
LAppModel
 ↓
model3.json
 ↓
moc3 + texture + motion
1. Masukkan model baru

Misal sekarang:

public/
└── live2d/
    └── Epsilon/
        ├── Epsilon.model3.json
        ├── Epsilon.moc3
        ├── Epsilon.1024/
        ├── motion/
        └── expressions/

Ganti jadi:

public/
└── live2d/
    └── Hiyori/
        ├── Hiyori.model3.json
        ├── Hiyori.moc3
        ├── Hiyori.2048/
        ├── motion/
        └── expressions/
2. Ubah path model

File:

src/live2d/app/lappdefine.ts

Cari:

export const ResourcesPath = '/live2d/';

export const ModelDir = "Epsilon";

atau yang mirip:

export const Model = [
    "Epsilon"
];

ubah:

export const Model = [
    "Hiyori"
];
3. Ubah nama file model

File:

src/live2d/app/lappdefine.ts

cari:

export const ModelDir =
"../../assets/live2d/Epsilon";

## fix error ketika mengganti karakter

Nah ini menarik. Berarti model sebenarnya punya parameter mulut, hanya nama parameternya bukan nama default Live2D.

jika belum ada tambahkan secara manual:
 "Groups": [
    {
      "Target": "Parameter",
      "Name": "EyeBlink",
      "Ids": [
        "ParamEyeLOpen",
        "ParamEyeROpen"
      ]
    },
    {
      "Target": "Parameter",
      "Name": "LipSync",
      "Ids": [
        "ParamMouthOpenY"
      ]
    }
  ],
  "HitAreas": []
}

## cara mengatasi bg hitam
Background hitam WebGL

File:

frontend/src/live2d/app/lappsubdelegate.ts
Sekitar baris 140

Sekarang ada:

gl.clearColor(0.0, 0.0, 0.0, 1.0);

Ganti menjadi:

gl.clearColor(0.0, 0.0, 0.0, 0.0);

Perhatikan angka terakhir:

1.0  -> 0.0

Artinya canvas menjadi transparan sehingga gambar HTML di belakangnya bisa terlihat.

## untuk mengatur scale ukuran karakter di file lappdefine.ts

## untuk mengeser kamera di file lappview.ts
 */
  public initialize(subdelegate: LAppSubdelegate): void {
    this._subdelegate = subdelegate;
    const { width, height } = subdelegate.getCanvas();

    const ratio: number = width / height;
    const left: number = -ratio;
    const right: number = ratio;
    const bottom: number = LAppDefine.ViewLogicalLeft;
    const top: number = LAppDefine.ViewLogicalRight;

    this._viewMatrix.setScreenRect(left, right, bottom, top); // デバイスに対応する画面の範囲。 Xの左端、Xの右端、Yの下端、Yの上端
    this._viewMatrix.scale(LAppDefine.ViewScale, LAppDefine.ViewScale);

    // Geser kamera ke bawah
    this._viewMatrix.translateRelative(0.0, -0.20);


## FIX FROTEND LIVE2D CUBISM

## Tahap 1 - Import SDK Live2D
Status

✅ Berhasil

Perubahan

Menyalin source SDK dari:

CubismSdkForWeb-5-r.5/
└── Samples/
    └── TypeScript/
        └── Demo/
            └── src/

ke project:

frontend/
└── src/
    └── live2d/
        ├── app/
        ├── shaders/
        ├── manager/
        └── hooks/



Fungsi:

- Membuat element canvas
- Menghubungkan React dengan Cubism SDK
- Menjalankan render loop Live2D


Kode:

```jsx
import { useEffect, useRef } from "react";
import { LAppDelegate } from "../live2d/app/lappdelegate";


export default function Live2DCanvas(){

    const canvasRef = useRef(null);


    useEffect(()=>{

        const delegate =
        LAppDelegate.getInstance();


        delegate.initialize();

        delegate.run();


    },[]);



    return (

        <canvas

            id="live2d"

            ref={canvasRef}

            style={{
                width:"100%",
                height:"100%",
                display:"block"
            }}

        />

    );

}


2. Menghubungkan Canvas React ke Cubism

File:

src/live2d/app/lappdelegate.ts

Pada fungsi:

initializeSubdelegates()

ditambahkan pencarian canvas React:

const canvas =
document.getElementById("live2d")
as HTMLCanvasElement;


if(!canvas){

    console.error(
    "Canvas #live2d tidak ditemukan"
    );

    return;

}


this._canvases = [canvas];


const subdelegate =
new LAppSubdelegate();


subdelegate.initialize(canvas);


this._subdelegates =
[subdelegate];


Tujuan:

React membuat canvas,
Cubism SDK memakai canvas tersebut untuk WebGL rendering.

3. Membuat akses ke Live2D Manager

File:

src/live2d/app/lappdelegate.ts

Tambahkan sebelum:

private release()

kode:

public getSubdelegate(){

    return this._subdelegates[0];

}

Fungsi:

Memberikan akses dari luar
ke:

Live2D Manager
Model
Audio handler
4. Menambahkan akses Model

File:

src/live2d/app/lapplive2dmanager.ts

Tambahkan:

public getModel():LAppModel {

    return this._models[0];

}

Fungsi:

Mengambil model Live2D yang sedang aktif.

Contoh:

manager.getModel()
5. Persiapan LipSync

File:

src/live2d/app/lappmodel.ts

Setelah fungsi:

public startRandomMotion()

ditambahkan:

/*
 Connect external audio to Live2D LipSync
*/


public startLipSync(
audioPath:string
):void {


    console.log(
        "[LIPSYNC AUDIO]",
        audioPath
    );


    this._wavFileHandler
    .start(audioPath);


}


Fungsi:

Menerima file audio
Mengirim audio ke WavFileHandler
Membaca RMS suara
6. Model3.json harus memiliki LipSync Parameter

File:

Epsilon.model3.json

Harus ada:

{
"Target":"Parameter",
"Name":"LipSync",
"Ids":[
"PARAM_MOUTH_OPEN_Y"
]
}

Parameter ini yang membuat mulut Live2D bisa membuka.

Debug masalah sebelum berhasil
Error:
Failed to resolve import @framework

Penyebab:

Alias Vite belum diarahkan.

Fix:

vite.config.js

resolve:{
 alias:{
 "@framework":
 path.resolve(
 __dirname,
 "src/live2d/framework"
 )
 }
}

Model tidak muncul

Penyebab:

Canvas React tidak tersambung ke Cubism.

Fix:

Pastikan:

<canvas id="live2d">

dan:

document.getElementById("live2d")

menghasilkan canvas.

Live2D tampil tetapi tidak ada suara/mulut bergerak

Penyebab:

LipSync belum dipanggil.

Flow:

Audio
↓
startLipSync()
↓
WavFileHandler
↓
RMS
↓
PARAM_MOUTH_OPEN_Y


## untuk mematikan background bawaan live2d cubism

// Background bawaan Live2D dinonaktifkan.//
    /*
    imageName = LAppDefine.BackImageName;

    // 非同期なのでコールバック関数を作成
    const initBackGroundTexture = (textureInfo: TextureInfo): void => {
      const x: number = width * 0.5;
      const y: number = height * 0.5;

      const fheight = height * 0.95;
      const ratio = fheight / textureInfo.height;
      const fwidth = textureInfo.width * ratio;
      this._back = new LAppSprite(x, y, fwidth, fheight, textureInfo.id);
      this._back.setSubdelegate(this._subdelegate);
    };

    textureManager.createTextureFromPngFile(
      resourcesPath + imageName,
      false,
      initBackGroundTexture
    );
    */
    // Background memakai React <img>.//


## Live2D model hitam di HP ##

Penyebab

Texture berukuran

8192 x 8192

terlalu besar untuk GPU Android.

Walaupun browser melaporkan

MAX_TEXTURE_SIZE = 16384

banyak GPU Android gagal merender texture 8192 dengan stabil.

Solusi

Texture diubah menjadi

4096 x 4096

menggunakan GIMP.


## problem yg mungkin akan muncul

Login Google gagal di HP

Penyebab

Frontend masih mengirim request ke

http://127.0.0.1:8000

yang hanya berlaku untuk localhost.

Solusi

Menggunakan

VITE_API_URL=http://192.168.1.3:8000 > ipqonfig

dan seluruh request menggunakan

import.meta.env.VITE_API_URL
✅ 3. Firebase Authorized Domain

Menambahkan domain deployment Firebase agar login Google dapat bekerja.

✅ 4. Backend tidak bisa diakses dari HP

Penyebab

Backend belum dijalankan pada semua interface.

Solusi

Menjalankan

uvicorn main:app --host 0.0.0.0 --port 8000


## jika terjadi fliker fix di file lappsubdelegate

// 画面の初期化
    gl.clearColor(0.0, 0.0, 0.0, 0.1);