# TextDecoder và TextEncoder

> Source: [https://javascript.info/text-decoder](https://javascript.info/text-decoder)

<!-- fetched: 2026-09-14 -->

Sao nếu dữ liệu nhị phân thực ra là một chuỗi? Ví dụ, chúng ta nhận được một tệp với dữ liệu văn bản.

Đối tượng tích hợp [TextDecoder](https://encoding.spec.whatwg.org/#interface-textdecoder) cho phép đọc giá trị vào chuỗi JavaScript thực tế, đã cho buffer và encoding.

Chúng ta trước tiên cần tạo nó:

```
let decoder = new TextDecoder([label], [options]);
```

- **`label`** – encoding, `utf-8` mặc định, nhưng `big5`, `windows-1251` và nhiều cái khác cũng được hỗ trợ.
- **`options`** – đối tượng tùy chọn:
  - **`fatal`** – boolean, nếu `true` thì ném lỗi ngoại lệ cho các ký tự không hợp lệ (không thể giải mã), nếu không (mặc định) thay thế chúng bằng ký tự `\uFFFD`.
  - **`ignoreBOM`** – boolean, nếu `true` thì bỏ qua BOM (dấu thứ tự byte Unicode tùy chọn), hiếm khi cần.

…Sau đó giải mã:

```
let str = decoder.decode([input], [options]);
```

- **`input`** – `BufferSource` để giải mã.
- **`options`** – đối tượng tùy chọn:
  - **`stream`** – true cho việc giải mã stream, khi `decoder` được gọi nhiều lần với các chunk dữ liệu đến. Trong trường hợp đó, một ký tự nhiều byte đôi khi bị chia cắt giữa các chunk. Tùy chọn này bảo `TextDecoder` ghi nhớ các ký tự "chưa hoàn thành" và giải mã chúng khi chunk tiếp theo đến.

Ví dụ:

```
let uint8Array = new Uint8Array([72, 101, 108, 108, 111]);

alert( new TextDecoder().decode(uint8Array) ); // Hello
```

```
let uint8Array = new Uint8Array([228, 189, 160, 229, 165, 189]);

alert( new TextDecoder().decode(uint8Array) ); // 你好
```

Chúng ta có thể giải mã một phần của buffer bằng cách tạo view subarray cho nó:

```
let uint8Array = new Uint8Array([0, 72, 101, 108, 108, 111, 0]);

// chuỗi ở giữa
// tạo view mới trên đó, không sao chép bất cứ thứ gì
let binaryString = uint8Array.subarray(1, -1);

alert( new TextDecoder().decode(binaryString) ); // Hello
```

## [TextEncoder](#textencoder)

[TextEncoder](https://encoding.spec.whatwg.org/#interface-textencoder) làm ngược lại – chuyển đổi một chuỗi thành các byte.

Cú pháp là:

```
let encoder = new TextEncoder();
```

Encoding duy nhất nó hỗ trợ là "utf-8".

Nó có hai phương thức:

- **`encode(str)`** – trả về `Uint8Array` từ một chuỗi.
- **`encodeInto(str, destination)`** – mã hóa `str` vào `destination` phải là `Uint8Array`.

```
let encoder = new TextEncoder();

let uint8Array = encoder.encode("Hello");
alert(uint8Array); // 72,101,108,108,111
```
