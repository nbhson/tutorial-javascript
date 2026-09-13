# Typed Arrays — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**Typed Array** là các array đặc biệt lưu trữ **dữ liệu nhị phân có kiểu cố định** (integer, float...) thay vì object thông thường. Chúng được xây dựng trên **ArrayBuffer** — vùng bộ nhớ nhị phân thuần túy — giúp thao tác với dữ liệu kích thước lớn (file, audio, image, WebGL) **hiệu quả hơn nhiều** so với array thông thường.

### Tại sao Typed Array nhanh hơn Array thông thường?

Array JS thông thường: mỗi phần tử là **object reference** trên heap — cần pointer indirection, GC tracking, boxing/unboxing khi access. Typed Array: **contiguous memory block** — giống C array, compiler JIT optimize thành SIMD instruction.

### 10 loại Typed Array phổ biến

| Typed Array | Kiểu dữ liệu | Kích thước (bytes) | Range |
|-------------|-------------|-------------------|-------|
| `Int8Array` | signed 8-bit integer | 1 | -128 đến 127 |
| `Uint8Array` | unsigned 8-bit integer | 1 | 0 đến 255 |
| `Uint8ClampedArray` | unsigned 8-bit, clamp | 1 | 0 đến 255 (clamp) |
| `Int16Array` | signed 16-bit integer | 2 | -32768 đến 32767 |
| `Uint16Array` | unsigned 16-bit integer | 2 | 0 đến 65535 |
| `Int32Array` | signed 32-bit integer | 4 | -2³¹ đến 2³¹-1 |
| `Uint32Array` | unsigned 32-bit integer | 4 | 0 đến 2³²-1 |
| `Float32Array` | IEEE 754 float | 4 | ~±3.4e38 |
| `Float64Array` | IEEE 754 double | 8 | ~±1.8e308 |
| `BigInt64Array` | signed 64-bit BigInt | 8 | -2⁶³ đến 2⁶³-1 |
| `BigUint64Array` | unsigned 64-bit BigInt | 8 | 0 đến 2⁶⁴-1 |

### ArrayBuffer — nền tảng bộ nhớ nhị phân

```js
// Tạo ArrayBuffer 8 bytes
const buf = new ArrayBuffer(8);
console.log(buf.byteLength); // 8

// Views — đọc/ghi dữ liệu từ ArrayBuffer theo kiểu cụ thể
const u8 = new Uint8Array(buf);
u8[0] = 255;   // byte 0 = 0xFF
u8[1] = 128;   // byte 1 = 0x80
console.log(u8); // Uint8Array [255, 128, 0, 0, 0, 0, 0, 0]

// Float32 view — đọc cùng 8 bytes như số float
const f32 = new Float32Array(buf);
console.log(f32[0]); // số float được encode từ 8 bytes đó
```

### DataView — precise byte-level access

```js
const buf = new ArrayBuffer(8);
const dv = new DataView(buf);

// Write bytes at specific offsets with endianness control
dv.setUint8(0, 0xFF);           // byte 0 = 255
dv.setUint16(1, 0x80, true);    // little-endian uint16 tại offset 1
dv.setInt32(5, -100, true);     // little-endian int32 tại offset 5

// Read
console.log(dv.getUint8(0));    // 255
console.log(dv.getUint16(1, true)); // 32768
console.log(dv.getInt32(5, true));  // -100
```

## 📐 Cấu trúc nhóm

```
03_data-structures/03_typed-arrays/
├── README.md         ← bài này
└── app.js            ← demo ArrayBuffer/Uint8Array/DataView
    └── index.html
```

## ✅ Điểm mạnh

- **Hiệu suất cao** — trực tiếp truy cập bộ nhớ nhị phân, không qua object overhead.
- **Bộ nhớ nhỏ gọn** — 1 byte per element (Uint8) so với 16-32 bytes per element (Array).
- **WebGL/Canvas/Image** — API chuẩn yêu cầu TypedArray cho texture, vertex data.
- **File I/O** — `FileReader`, `Blob`, `fetch()` đều return/read TypedArray.
- **Interoperability** — chung bộ nhớ với C/C++ extensions (WebAssembly).
- **Endianness control** — DataView hỗ trợ big/little endian explicit.

## ⚠️ Bẫy thường gặp

| # | Bẫy | Ví dụ | Cách tránh |
|---|-----|-------|-----------|
| 1 | **Length cố định sau khi tạo** | `arr.push(6)` → TypeError | Dùng `slice` hoặc tạo array mới |
| 2 | **`slice` khác `subarray`** | `slice` copy, `subarray` view shared buffer | Hiểu rõ: slice = independent, subarray = view |
| 3 | **Endianness với DataView** | `setInt16(0, 256, true)` vs `false` cho kết quả khác | Always specify endianness explicitly |
| 4 | **Shared buffer giữa views** | Sửa `u8` ảnh hưởng `f32` cùng buffer | Dùng buffer riêng hoặc clone |
| 5 | **`byteOffset` phải aligned với element size** | `new Int16Array(buf, 1)` → TypeError | Offset phải là bội của element size |
| 6 | **TypedArray không JSON-serializable** | `JSON.stringify(u8)` → `{}` | `Array.from(u8)` trước stringify |

## 💡 Khi nào dùng

- **WebGL rendering** — vertex buffers, texture data.
- **Audio processing** — Web Audio API raw PCM data.
- **Image manipulation** — `ImageData.data` là Uint8ClampedArray.
- **Network binary protocols** — custom binary packet parsing.
- **Large numeric arrays** — scientific computing, simulations.
- **File read/write** — `FileReader.readAsArrayBuffer()`, `Blob`.

## 🎯 Ví dụ minh họa

### Ví dụ 1: ArrayBuffer + TypedArray basic

```js
// Tạo buffer 8 bytes
const buf = new ArrayBuffer(8);
console.log(buf.byteLength); // 8

// Uint8 view
const u8 = new Uint8Array(buf);
u8[0] = 255;   // 0xFF
u8[1] = 128;   // 0x80
console.log(u8); // Uint8Array [255, 128, 0, 0, 0, 0, 0, 0]

// Float32 view trên cùng buffer
const f32 = new Float32Array(buf);
console.log(f32); // [2147483648, 0] — cùng 8 bytes, hiểu là float

// Đọc riêng view mới từ buffer (không shared)
const buf2 = new ArrayBuffer(8);
const f32_2 = new Float32Array(buf2);
f32_2[0] = 1.5;
f32_2[1] = 2.5;
console.log(f32_2); // Float32Array [1.5, 2.5]
console.log(f32_2.byteLength); // 8 bytes
```

### Ví dụ 2: DataView — precise byte access

```js
const buf = new ArrayBuffer(4);
const dv = new DataView(buf);

// Write in different formats
dv.setUint8(0, 0xFF);          // byte 0
dv.setInt16(1, -100, true);    // little-endian int16 tại offset 1
dv.setFloat32(3, 3.14, false); // big-endian float32 tại offset 3

console.log(dv.getUint8(0));   // 255
console.log(dv.getInt16(1, true));  // -100
console.log(dv.getFloat32(3, false)); // 3.14
```

### Ví dụ 3: Real use case — image pixel manipulation

```js
// Canvas ImageData.data là Uint8ClampedArray
const canvas = document.createElement("canvas");
canvas.width = 2;
canvas.height = 2;
const ctx = canvas.getContext("2d");
ctx.fillStyle = "red";
ctx.fillRect(0, 0, 2, 2);

const imageData = ctx.getImageData(0, 0, 2, 2);
const pixels = imageData.data; // Uint8ClampedArray [R,G,B,A, R,G,B,A, ...]

// Invert colors
for (let i = 0; i < pixels.length; i += 4) {
  pixels[i]     = 255 - pixels[i];     // R
  pixels[i + 1] = 255 - pixels[i + 1]; // G
  pixels[i + 2] = 255 - pixels[i + 2]; // B
  // A giữ nguyên
}
ctx.putImageData(imageData, 0, 0);
// Now canvas shows inverted red → cyan
```

### Ví dụ 4: File read as TypedArray

```js
async function readAsBuffer(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result); // ArrayBuffer
    reader.onerror = reject;
    reader.readAsArrayBuffer(file);
  });
}

async function processImage(file) {
  const buf = await readAsBuffer(file);
  const u8 = new Uint8Array(buf);
  console.log(`File size: ${buf.byteLength} bytes`);
  console.log(`First 4 bytes (magic number):`, Array.from(u8.slice(0, 4)));
  // JPEG: [255, 216, 255, 224]
  // PNG:   [137, 80, 78, 71]
}
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm | Phù hợp khi |
|-----------|---------|------------|-------------|
| **TypedArray** | Zero-copy, native binary | Fixed type/length, no JSON | WebGL, audio, file I/O |
| **Plain Array** | Flexible, JSON-serializable | High memory overhead | General purpose |
| **ArrayBuffer + DataView** | Most flexible binary access | Verbose API | Custom binary protocol parsing |
| **Base64 string** | Human-readable, JSON-safe | 33% size overhead | Transmission, storage |

## 📊 Performance & Best Practices

- **Pre-allocate buffer size** — `new ArrayBuffer(expectedBytes)` tránh resize overhead.
- **Use TypedArray constructors** `new Uint8Array(buf, offset, length)` cho view slice — zero-copy.
- **Avoid `slice` on TypedArray** — it copies; use `subarray` cho shared view.
- **Always specify endianness in DataView** — `true` = little-endian, `false` = big-endian.
- **Cache `byteLength`** — không gọi `buffer.byteLength` lặp lại trong hot loop.
- **Don't mix views on same buffer carelessly** — `u8` view and `f32` view share same bytes.
- **TypedArray from existing array** — `new Uint8Array([1,2,3])` auto-copies bytes.

## 🔗 Liên kết chéo

- Xem thêm: `03_data-structures/01_arrays/` — Array basics
- Xem thêm: `13_working-with-apis/01_fetch/` — fetch returns ArrayBuffer/Blob
- Xem thêm: `21_graphics/04_canvas/` — Canvas ImageData là Uint8ClampedArray
- Tài liệu: [MDN — TypedArray](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray), [MDN — ArrayBuffer](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/ArrayBuffer)
