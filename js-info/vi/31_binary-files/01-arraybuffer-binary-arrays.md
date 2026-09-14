# ArrayBuffer, mảng nhị phân

> Source: [https://javascript.info/arraybuffer-binary-arrays](https://javascript.info/arraybuffer-binary-arrays)

<!-- fetched: 2026-09-14 -->

Trong phát triển web, chúng ta thường gặp dữ liệu nhị phân chủ yếu khi làm việc với tệp (tạo, tải lên, tải xuống). Một trường hợp sử dụng phổ biến khác là xử lý hình ảnh.

Tất cả những điều này đều có thể thực hiện được trong JavaScript, và các phép toán nhị phân có hiệu suất cao.

Tuy nhiên, có một chút nhầm lẫn vì có nhiều lớp đối tượng. Hãy điểm qua vài cái:

- `ArrayBuffer`, `Uint8Array`, `DataView`, `Blob`, `File`, v.v.

Dữ liệu nhị phân trong JavaScript được triển khai theo cách không tiêu chuẩn, so với các ngôn ngữ khác. Nhưng khi chúng ta nắm rõ mọi thứ, mọi thứ trở nên khá đơn giản.

**Đối tượng nhị phân cơ bản là `ArrayBuffer` – một tham chiếu đến một vùng bộ nhớ liên tục có độ dài cố định.**

Chúng ta tạo nó như sau:

```
let buffer = new ArrayBuffer(16); // tạo buffer có độ dài 16
alert(buffer.byteLength); // 16
```

Điều này phân bổ một vùng bộ nhớ liên tục 16 byte và điền sẵn bằng giá trị 0.

`ArrayBuffer` không phải là một mảng của cái gì đó

Hãy loại bỏ một nguồn nhầm lẫn có thể. `ArrayBuffer` không có gì chung với `Array`:

- Nó có độ dài cố định, chúng ta không thể tăng hoặc giảm nó.
- Nó chiếm đúng khoảng không gian đó trong bộ nhớ.
- Để truy cập vào từng byte, cần một đối tượng "view" khác, không phải `buffer[index]`.

`ArrayBuffer` là một vùng bộ nhớ. Dữ liệu lưu trữ trong đó là gì? Nó không biết. Chỉ là một dãy byte thô.

**Để thao tác với `ArrayBuffer`, chúng ta cần sử dụng đối tượng "view".**

Một đối tượng view không lưu trữ gì riêng biệt. Nó là "kính mát" đưa ra cách diễn giải các byte được lưu trữ trong `ArrayBuffer`.

Ví dụ:

- **`Uint8Array`** – xử lý mỗi byte trong `ArrayBuffer` như một số riêng biệt, với giá trị có thể từ 0 đến 255 (một byte là 8-bit, vì vậy nó chỉ có thể giữ giá trị đó). Giá trị như vậy được gọi là "số nguyên không dấu 8-bit".
- **`Uint16Array`** – xử lý mỗi 2 byte như một số nguyên, với giá trị có thể từ 0 đến 65535. Đó được gọi là "số nguyên không dấu 16-bit".
- **`Uint32Array`** – xử lý mỗi 4 byte như một số nguyên, với giá trị có thể từ 0 đến 4294967295. Đó được gọi là "số nguyên không dấu 32-bit".
- **`Float64Array`** – xử lý mỗi 8 byte như một số thập phân với giá trị có thể từ `5.0x10-324` đến `1.8x10308`.

Vì vậy, dữ liệu nhị phân trong một `ArrayBuffer` 16 byte có thể được diễn giải là 16 "số nhỏ", hoặc 8 số lớn hơn (mỗi số 2 byte), hoặc 4 số thậm chí lớn hơn (mỗi số 4 byte), hoặc 2 giá trị thập phân có độ chính xác cao (mỗi số 8 byte).

![](/article/arraybuffer-binary-arrays/arraybuffer-views.svg)

`ArrayBuffer` là đối tượng cốt lõi, là gốc rễ của mọi thứ, là dữ liệu nhị phân thô.

Nhưng nếu chúng ta muốn ghi vào đó, hoặc lặp qua nó, về cơ bản là cho hầu hết mọi thao tác – chúng ta phải sử dụng view, ví dụ:

```
let buffer = new ArrayBuffer(16); // tạo buffer có độ dài 16

let view = new Uint32Array(buffer); // xử lý buffer như một dãy các số nguyên 32-bit

alert(Uint32Array.BYTES_PER_ELEMENT); // 4 byte cho mỗi số nguyên

alert(view.length); // 4, nó lưu trữ bấy nhiêu số nguyên
alert(view.byteLength); // 16, kích thước tính bằng byte

// hãy ghi một giá trị
view[0] = 123456;

// lặp qua các giá trị
for(let num of view) {
  alert(num); // 123456, sau đó là 0, 0, 0 (tổng cộng 4 giá trị)
}
```

## [TypedArray](#typedarray)

Thuật ngữ chung cho tất cả các view này (`Uint8Array`, `Uint32Array`, v.v.) là [TypedArray](https://tc39.github.io/ecma262/#sec-typedarray-objects). Chúng chia sẻ cùng một tập hợp các phương thức và thuộc tính.

Xin lưu ý, không có constructor tên là `TypedArray`, đó chỉ là thuật ngữ "bao trùm" chung để đại diện cho một trong các view trên `ArrayBuffer`: `Int8Array`, `Uint8Array` và cứ thế, danh sách đầy đủ sẽ theo sau.

Khi bạn thấy thứ gì đó như `new TypedArray`, nó có nghĩa là bất kỳ `new Int8Array`, `new Uint8Array`, v.v.

Các mảng kiểu (typed arrays) hoạt động giống như mảng thông thường: có chỉ mục và có thể lặp qua.

Constructor của mảng kiểu (dù là `Int8Array` hay `Float64Array`) hoạt động khác nhau tùy thuộc vào kiểu đối số.

Có 5 biến thể của đối số:

```
new TypedArray(buffer, [byteOffset], [length]);
new TypedArray(object);
new TypedArray(typedArray);
new TypedArray(length);
new TypedArray();
```

1. Nếu đối số `ArrayBuffer` được cung cấp, view sẽ được tạo trên nó. Chúng ta đã sử dụng cú pháp đó.

   Tùy chọn, chúng ta có thể cung cấp `byteOffset` để bắt đầu (mặc định là 0) và `length` (tới cuối buffer mặc định), khi đó view sẽ chỉ bao phủ một phần của `buffer`.
2. Nếu một `Array`, hoặc bất kỳ đối tượng giống mảng nào được đưa ra, nó sẽ tạo một mảng kiểu có cùng độ dài và sao chép nội dung.

   Chúng ta có thể sử dụng nó để điền sẵn mảng với dữ liệu:

   ```
   let arr = new Uint8Array([0, 1, 2, 3]);
   alert( arr.length ); // 4, tạo mảng nhị phân có cùng độ dài
   alert( arr[1] ); // 1, được điền với 4 byte (số nguyên không dấu 8-bit) với các giá trị đã cho
   ```
3. Nếu một `TypedArray` khác được cung cấp, nó làm điều tương tự: tạo một mảng kiểu có cùng độ dài và sao chép các giá trị. Các giá trị được chuyển đổi sang kiểu mới trong quá trình này, nếu cần.

   ```
   let arr16 = new Uint16Array([1, 1000]);
   let arr8 = new Uint8Array(arr16);
   alert( arr8[0] ); // 1
   alert( arr8[1] ); // 232, cố sao chép 1000, nhưng không vừa 1000 vào 8 bit (giải thích bên dưới)
   ```
4. Đối với đối số số `length` – tạo mảng kiểu chứa bấy nhiêu phần tử. Độ dài byte của nó sẽ là `length` nhân với số byte trong một mục `TypedArray.BYTES_PER_ELEMENT`:

   ```
   let arr = new Uint16Array(4); // tạo mảng kiểu cho 4 số nguyên
   alert( Uint16Array.BYTES_PER_ELEMENT ); // 2 byte cho mỗi số nguyên
   alert( arr.byteLength ); // 8 (kích thước tính bằng byte)
   ```
5. Không có đối số, tạo mảng kiểu có độ dài 0.

Chúng ta có thể tạo `TypedArray` trực tiếp, mà không đề cập đến `ArrayBuffer`. Nhưng một view không thể tồn tại mà không có `ArrayBuffer` nền, nên nó được tạo tự động trong tất cả các trường hợp ngoại trừ trường hợp đầu tiên (khi được cung cấp).

Để truy cập `ArrayBuffer` nền, có các thuộc tính sau trong `TypedArray`:

- `buffer` – tham chiếu đến `ArrayBuffer`.
- `byteLength` – độ dài của `ArrayBuffer`.

Vì vậy, chúng ta luôn có thể di chuyển từ view này sang view khác:

```
let arr8 = new Uint8Array([0, 1, 2, 3]);

// view khác trên cùng dữ liệu
let arr16 = new Uint16Array(arr8.buffer);
```

Đây là danh sách các mảng kiểu:

- `Uint8Array`, `Uint16Array`, `Uint32Array` – cho số nguyên 8, 16 và 32 bit.
  - `Uint8ClampedArray` – cho số nguyên 8-bit, "làm méo" chúng khi gán (xem bên dưới).
- `Int8Array`, `Int16Array`, `Int32Array` – cho số nguyên có dấu (có thể âm).
- `Float32Array`, `Float64Array` – cho số thập phân có dấu 32 và 64 bit.

Không có `int8` hoặc các kiểu đơn giá trị tương tự

Xin lưu ý, bất chấp các tên như `Int8Array`, không có kiểu đơn giá trị như `int`, hoặc `int8` trong JavaScript.

Điều đó là hợp lý, vì `Int8Array` không phải là mảng của các giá trị riêng lẻ này, mà là một view trên `ArrayBuffer`.

### [Hành vi vượt giới hạn](#out-of-bounds-behavior)

Sao nếu chúng ta cố gắng ghi một giá trị vượt giới hạn vào mảng kiểu? Sẽ không có lỗi. Nhưng các bit thừa sẽ bị cắt bỏ.

Ví dụ, hãy thử đặt 256 vào `Uint8Array`. Ở dạng nhị phân, 256 là `100000000` (9 bit), nhưng `Uint8Array` chỉ cung cấp 8 bit cho mỗi giá trị, phạm vi có sẵn là từ 0 đến 255.

Đối với các số lớn hơn, chỉ 8 bit bên phải (ít quan trọng hơn) được lưu trữ, và phần còn lại bị cắt bỏ:

![](/article/arraybuffer-binary-arrays/8bit-integer-256.svg)

Vì vậy, chúng ta sẽ nhận được 0.

Đối với 257, dạng nhị phân là `100000001` (9 bit), 8 bit bên phải được lưu trữ, vì vậy chúng ta sẽ có `1` trong mảng:

![](/article/arraybuffer-binary-arrays/8bit-integer-257.svg)

Nói cách khác, số modulo 2^8 được lưu.

Đây là bản demo:

```
let uint8array = new Uint8Array(16);

let num = 256;
alert(num.toString(2)); // 100000000 (biểu diễn nhị phân)

uint8array[0] = 256;
uint8array[1] = 257;

alert(uint8array[0]); // 0
alert(uint8array[1]); // 1
```

`Uint8ClampedArray` đặc biệt trong khía cạnh này, hành vi của nó khác biệt. Nó lưu 255 cho bất kỳ số nào lớn hơn 255, và 0 cho bất kỳ số âm nào. Hành vi đó hữu ích cho xử lý hình ảnh.

## [Phương thức TypedArray](#typedarray-methods)

`TypedArray` có các phương thức `Array` thông thường, với vài ngoại lệ đáng chú ý.

Chúng ta có thể lặp qua, `map`, `slice`, `find`, `reduce`, v.v.

Có vài thứ chúng ta không thể làm:

- Không có `splice` – chúng ta không thể "xóa" một giá trị, vì mảng kiểu là view trên một buffer, và những thứ này là các vùng bộ nhớ liên tục cố định. Tất cả những gì chúng ta có thể làm là gán bằng 0.
- Không có phương thức `concat`.

Có hai phương thức bổ sung:

- `arr.set(fromArr, [offset])` sao chép tất cả các phần tử từ `fromArr` vào `arr`, bắt đầu tại vị trí `offset` (mặc định là 0).
- `arr.subarray([begin, end])` tạo một view mới cùng kiểu từ `begin` đến `end` (không bao gồm). Điều đó tương tự như phương thức `slice` (cũng được hỗ trợ), nhưng không sao chép bất cứ thứ gì – chỉ tạo view mới, để thao tác trên đoạn dữ liệu đã cho.

Các phương thức này cho phép chúng ta sao chép mảng kiểu, trộn chúng, tạo mảng mới từ các mảng hiện có, và cứ thế.

## [DataView](#dataview)

[DataView](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DataView) là một "untyped" view đặc biệt siêu linh hoạt trên `ArrayBuffer`. Nó cho phép truy cập dữ liệu ở bất kỳ offset nào với bất kỳ định dạng nào.

- Đối với mảng kiểu, constructor quy định định dạng là gì. Toàn bộ mảng được cho là đồng nhất. Số thứ i là `arr[i]`.
- Với `DataView`, chúng ta truy cập dữ liệu bằng các phương thức như `.getUint8(i)` hoặc `.getUint16(i)`. Chúng ta chọn định dạng tại thời điểm gọi phương thức thay vì thời điểm tạo.

Cú pháp:

```
new DataView(buffer, [byteOffset], [byteLength])
```

- **`buffer`** – `ArrayBuffer` nền. Khác với mảng kiểu, `DataView` không tự tạo buffer. Chúng ta cần phải có nó sẵn.
- **`byteOffset`** – vị trí byte bắt đầu của view (mặc định là 0).
- **`byteLength`** – độ dài byte của view (mặc định tới cuối `buffer`).

Ví dụ, ở đây chúng ta trích xuất các số ở các định dạng khác nhau từ cùng một buffer:

```
// mảng nhị phân 4 byte, tất cả đều có giá trị tối đa 255
let buffer = new Uint8Array([255, 255, 255, 255]).buffer;

let dataView = new DataView(buffer);

// lấy số 8-bit tại offset 0
alert( dataView.getUint8(0) ); // 255

// bây giờ lấy số 16-bit tại offset 0, gồm 2 byte, cùng được diễn giải là 65535
alert( dataView.getUint16(0) ); // 65535 (số nguyên không dấu 16-bit lớn nhất)

// lấy số 32-bit tại offset 0
alert( dataView.getUint32(0) ); // 4294967295 (số nguyên không dấu 32-bit lớn nhất)

dataView.setUint32(0, 0); // đặt số 4 byte bằng 0, do đó đặt tất cả các byte bằng 0
```

`DataView` rất tuyệt khi chúng ta lưu trữ dữ liệu hỗn hợp định dạng trong cùng một buffer. Ví dụ, khi chúng ta lưu trữ một dãy các cặp (số nguyên 16-bit, số thập phân 32-bit), `DataView` cho phép truy cập chúng một cách dễ dàng.

## [Tóm tắt](#summary)

`ArrayBuffer` là đối tượng cốt lõi, một tham chiếu đến vùng bộ nhớ liên tục có độ dài cố định.

Để thực hiện hầu hết mọi thao tác trên `ArrayBuffer`, chúng ta cần một view.

- Đó có thể là một `TypedArray`:
  - `Uint8Array`, `Uint16Array`, `Uint32Array` – cho số nguyên không dấu 8, 16, và 32 bit.
  - `Uint8ClampedArray` – cho số nguyên 8-bit, "làm méo" chúng khi gán.
  - `Int8Array`, `Int16Array`, `Int32Array` – cho số nguyên có dấu (có thể âm).
  - `Float32Array`, `Float64Array` – cho số thập phân có dấu 32 và 64 bit.
- Hoặc một `DataView` – view sử dụng các phương thức để chỉ định định dạng, ví dụ `getUint8(offset)`.

Trong hầu hết các trường hợp, chúng ta tạo và thao tác trực tiếp trên mảng kiểu, để `ArrayBuffer` ở chế độ ẩn, như một "ước chung lớn nhất". Chúng ta có thể truy cập nó như `.buffer` và tạo một view khác nếu cần.

Có hai thuật ngữ bổ sung nữa, được sử dụng trong mô tả các phương thức hoạt động trên dữ liệu nhị phân:

- `ArrayBufferView` là thuật ngữ bao trùm cho tất cả các loại view này.
- `BufferSource` là thuật ngữ bao trùm cho `ArrayBuffer` hoặc `ArrayBufferView`.

Chúng ta sẽ thấy các thuật ngữ này trong các chương tiếp theo. `BufferSource` là một trong những thuật ngữ phổ biến nhất, vì nó có nghĩa là "bất kỳ loại dữ liệu nhị phân nào" – một `ArrayBuffer` hoặc view trên nó.

Đây là bảng tra cứu nhanh:

![](/article/arraybuffer-binary-arrays/arraybuffer-view-buffersource.svg)

---

---

## Bài tập

## [Bài tập](#tasks)

### [Ghép các mảng kiểu](#concatenate-typed-arrays)

Cho một mảng các `Uint8Array`, viết hàm `concat(arrays)` trả về kết quả ghép các mảng đó thành một mảng duy nhất.

[Mở sandbox với tests.](https://plnkr.co/edit/RzzerzPQiF4cqQJR?p=preview)

solution

```
function concat(arrays) {
  // tổng độ dài của các mảng con
  let totalLength = arrays.reduce((acc, value) => acc + value.length, 0);

  let result = new Uint8Array(totalLength);

  if (!arrays.length) return result;

  // cho mỗi mảng - sao chép nó vào result
  // mảng tiếp theo được sao chép ngay sau mảng trước đó
  let length = 0;
  for(let array of arrays) {
    result.set(array, length);
    length += array.length;
  }

  return result;
}
```

[Mở lời giải với tests trong sandbox.](https://plnkr.co/edit/3J5jU9DQeDSsRfdq?p=preview)
