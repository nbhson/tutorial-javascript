const buf = new ArrayBuffer(8);
const u8 = new Uint8Array(buf);
u8[0]=255; u8[1]=128;
console.log(u8, buf.byteLength);
const f32 = new Float32Array([1.5,2.5]);
console.log(f32, f32.BYTES_PER_ELEMENT);
const dv = new DataView(buf);
dv.setInt16(0, 0x1234, true);
console.log(dv.getInt16(0, true).toString(16));
