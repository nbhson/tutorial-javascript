# File và FileReader

> Source: [https://javascript.info/file](https://javascript.info/file)

<!-- fetched: 2026-09-14 -->

Đối tượng [File](https://www.w3.org/TR/FileAPI/#dfn-file) kế thừa từ `Blob` và được mở rộng với các khả năng liên quan đến filesystem.

Có hai cách để có được nó.

Đầu tiên, có constructor, tương tự như `Blob`:

```
new File(fileParts, fileName, [options])
```

- **`fileParts`** – là mảng các giá trị Blob/BufferSource/String.
- **`fileName`** – chuỗi tên tệp.
- **`options`** – đối tượng tùy chọn:
  - **`lastModified`** – dấu thời gian (ngày nguyên) của lần sửa đổi cuối cùng.

Thứ hai, thường xuyên hơn chúng ta nhận được tệp từ `<input type="file">` hoặc drag'n'drop hoặc các giao diện trình duyệt khác. Trong trường hợp đó, tệp nhận thông tin này từ OS.

Vì `File` kế thừa từ `Blob`, các đối tượng `File` có cùng thuộc tính, cộng thêm:

- `name` – tên tệp,
- `lastModified` – dấu thời gian của lần sửa đổi cuối cùng.

Đây là cách chúng ta có thể lấy đối tượng `File` từ `<input type="file">`:

```
<input type="file" onchange="showFile(this)">

<script>
function showFile(input) {
  let file = input.files[0];

  alert(`Tên tệp: ${file.name}`); // ví dụ my.png
  alert(`Sửa đổi lần cuối: ${file.lastModified}`); // ví dụ 1552830408824
}
</script>
```

Xin lưu ý:

Input có thể chọn nhiều tệp, vì vậy `input.files` là một đối tượng giống mảng với chúng. Ở đây chúng ta có một tệp, vì vậy chúng ta chỉ lấy `input.files[0]`.

## [FileReader](#filereader)

[FileReader](https://www.w3.org/TR/FileAPI/#dfn-filereader) là một đối tượng với mục đích duy nhất là đọc dữ liệu từ các đối tượng `Blob` (và do đó `File` cũng vậy).

Nó cung cấp dữ liệu bằng sự kiện, vì đọc từ đĩa có thể mất thời gian.

Constructor:

```
let reader = new FileReader(); // không có đối số
```

Các phương thức chính:

- **`readAsArrayBuffer(blob)`** – đọc dữ liệu ở định dạng nhị phân `ArrayBuffer`.
- **`readAsText(blob, [encoding])`** – đọc dữ liệu như một chuỗi văn bản với encoding đã cho (`utf-8` mặc định).
- **`readAsDataURL(blob)`** – đọc dữ liệu nhị phân và mã hóa nó thành data url base64.
- **`abort()`** – hủy thao tác.

Lựa chọn phương thức `read*` phụ thuộc vào định dạng chúng ta thích, cách chúng ta sẽ sử dụng dữ liệu.

- `readAsArrayBuffer` – cho các tệp nhị phân, để thực hiện các thao tác nhị phân cấp thấp. Cho các thao tác cấp cao, như slicing, `File` kế thừa từ `Blob`, vì vậy chúng ta có thể gọi chúng trực tiếp, mà không cần đọc.
- `readAsText` – cho các tệp văn bản, khi chúng ta muốn nhận được một chuỗi.
- `readAsDataURL` – khi chúng ta muốn sử dụng dữ liệu này trong `src` cho `img` hoặc thẻ khác. Có một cách thay thế để đọc tệp cho việc đó, như đã thảo luận trong chương [Blob](/blob): `URL.createObjectURL(file)`.

Khi quá trình đọc đang diễn ra, có các sự kiện:

- `loadstart` – đang bắt đầu tải.
- `progress` – xảy ra trong quá trình đọc.
- `load` – không có lỗi, đọc hoàn tất.
- `abort` – `abort()` được gọi.
- `error` – lỗi đã xảy ra.
- `loadend` – đọc kết thúc với thành công hoặc thất bại.

Khi quá trình đọc kết thúc, chúng ta có thể truy cập kết quả như:

- `reader.result` là kết quả (nếu thành công)
- `reader.error` là lỗi (nếu thất bại).

Các sự kiện được sử dụng rộng rãi nhất chắc chắn là `load` và `error`.

Đây là một ví dụ về đọc tệp:

```
<input type="file" onchange="readFile(this)">

<script>
function readFile(input) {
  let file = input.files[0];

  let reader = new FileReader();

  reader.readAsText(file);

  reader.onload = function() {
    console.log(reader.result);
  };

  reader.onerror = function() {
    console.log(reader.error);
  };

}
</script>
```

`FileReader` cho blobs

Như đã đề cập trong chương [Blob](/blob), `FileReader` có thể đọc không chỉ các tệp, mà bất kỳ blobs nào.

Chúng ta có thể sử dụng nó để chuyển đổi blob sang định dạng khác:

- `readAsArrayBuffer(blob)` – sang `ArrayBuffer`,
- `readAsText(blob, [encoding])` – sang chuỗi (một cách thay thế cho `TextDecoder`),
- `readAsDataURL(blob)` – sang data url base64.

`FileReaderSync` có sẵn trong Web Workers

Đối với Web Workers, cũng tồn tại một biến thể đồng bộ của `FileReader`, gọi là [FileReaderSync](https://www.w3.org/TR/FileAPI/#FileReaderSync).

Các phương thức đọc `read*` của nó không tạo sự kiện, mà trả về kết quả, như các hàm thông thường làm.

Điều đó chỉ tồn tại trong Web Worker, vì độ trễ trong các cuộc gọi đồng bộ, có thể xảy ra khi đọc từ tệp, trong Web Workers ít quan trọng hơn. Chúng không ảnh hưởng đến trang.

## [Tóm tắt](#summary)

Các đối tượng `File` kế thừa từ `Blob`.

Ngoài các phương thức và thuộc tính `Blob`, các đối tượng `File` cũng có các thuộc tính `name` và `lastModified`, cộng với khả năng nội bộ để đọc từ filesystem. Chúng ta thường nhận được các đối tượng `File` từ đầu vào của người dùng, như `<input>` hoặc các sự kiện Drag'n'Drop (`ondragend`).

Các đối tượng `FileReader` có thể đọc từ một tệp hoặc blob, ở một trong ba định dạng:

- Chuỗi (`readAsText`).
- `ArrayBuffer` (`readAsArrayBuffer`).
- Data url, base-64 encoded (`readAsDataURL`).

Trong nhiều trường hợp, chúng ta không phải đọc nội dung tệp. Giống như chúng ta đã làm với blobs, chúng ta có thể tạo một url ngắn với `URL.createObjectURL(file)` và gán nó cho `<a>` hoặc `<img>`. Bằng cách này, tệp có thể được tải xuống hoặc hiển thị như một hình ảnh, như một phần của canvas, v.v.

Và nếu chúng ta định gửi một `File` qua mạng, đó cũng là điều dễ dàng: API mạng như `XMLHttpRequest` hoặc `fetch` chấp nhận native các đối tượng `File`.
