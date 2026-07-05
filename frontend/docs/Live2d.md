# Live2D Cubism Integration Documentation

Dokumen ini berisi seluruh proses integrasi Live2D Cubism SDK ke project Raphael beserta catatan debugging yang berguna jika membuat project lain di masa depan.

---

# Struktur SDK

```
src/

└── live2d/

    ├── app/

    ├── framework/

    ├── shaders/

    ├── manager/

    └── hooks/
```

---

# Flow Rendering

```
React

↓

Live2DCanvas

↓

LAppDelegate

↓

LAppSubdelegate

↓

LAppView

↓

LAppLive2DManager

↓

LAppModel

↓

CubismRenderer_WebGL

↓

WebGL
```

---

# Canvas

Canvas dibuat oleh React.

File

```
src/components/Live2DCanvas.jsx
```

Canvas harus memiliki id

```html
<canvas id="live2d"></canvas>
```

---

# Delegate

File

```
src/live2d/app/lappdelegate.ts
```

Delegate bertugas

* membuat Subdelegate
* membuat WebGL Context
* menjalankan Render Loop

---

# LAppSubdelegate

Mengatur

* WebGL
* Texture Manager
* View
* Live2D Manager

---

# LAppView

Mengatur

* Camera
* Zoom
* Drag
* Tap

---

# Scale

File

```
src/live2d/app/lappdefine.ts
```

Parameter

```ts
ViewScale
```

Semakin besar nilainya

↓

Model semakin dekat

Contoh

```
1.5

↓

lebih kecil
```

```
2.0

↓

lebih besar
```

---

# Posisi Kamera

File

```
src/live2d/app/lappview.ts
```

Pada

```ts
initialize()
```

gunakan

```ts
this._viewMatrix.translateRelative(
    0.0,
    -0.30
);
```

Nilai negatif

↓

kamera turun

Nilai positif

↓

kamera naik

---

# Mengganti Model

Masukkan model

```
public/live2d/
```

Kemudian ubah

```
lappdefine.ts
```

```ts
export const Model = [
    "NamaModel"
];
```

---

# EyeBlink

Model harus memiliki

```json
{
  "Target":"Parameter",
  "Name":"EyeBlink",
  "Ids":[
      "ParamEyeLOpen",
      "ParamEyeROpen"
  ]
}
```

Jika kosong

↓

kedipan otomatis tidak akan bekerja.

---

# LipSync

Model harus memiliki

```json
{
  "Target":"Parameter",
  "Name":"LipSync",
  "Ids":[
      "ParamMouthOpenY"
  ]
}
```

Jika model memiliki

```
ParamMouthForm
```

maka AI juga dapat mengubah ekspresi mulut.

---

# Shader

Folder

```
src/live2d/shaders/
```

berisi

```
.vert
.frag
```

Shader dimuat oleh

```
CubismShader_WebGL
```

---

# Texture

Texture diambil dari

```
model3.json

↓

Textures

↓

texture_00.png
```

---

# Motion

Urutan loading

```
Expression

↓

Physics

↓

Pose

↓

EyeBlink

↓

Breath

↓

Motion

↓

Texture

↓

CompleteSetup
```

Jika state sudah

```
CompleteSetup
```

berarti model siap dirender.

---

# Debugging Checklist

## Model tidak muncul

Periksa

* model3.json
* moc3
* texture
* shader
* WebGL

---

## Texture putih

Periksa path

```
Textures
```

pada model3.json

---

## Shader gagal

Periksa

```
ShaderPath
```

dan pastikan semua file shader berhasil dimuat (HTTP 200).

---

## EyeBlink tidak bekerja

Periksa

```
Groups

↓

EyeBlink
```

---

## LipSync tidak bekerja

Periksa

```
Groups

↓

LipSync
```

dan parameter

```
ParamMouthOpenY
```

---

## Drag tidak bekerja

Periksa

```
ParamAngleX

ParamAngleY

ParamBodyAngleX

ParamEyeBallX

ParamEyeBallY
```

---

## Tap tidak bekerja

Periksa

```
HitAreas
```

pada model3.json.

---

# Catatan

Selama integrasi Raphael seluruh sistem shader, texture, renderer, motion, physics, pose, expression, WebGL, dan loading pipeline telah berhasil berjalan dengan benar. Dokumentasi ini dapat dijadikan acuan untuk integrasi Live2D pada project lain di masa mendatang.
