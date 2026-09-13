# XMLHttpRequest (XHR)

## 🔑 Khái niệm

**XMLHttpRequest** là API **tiền thân của fetch**, cho phép gửi HTTP request từ JS — dù tên có "XML" nhưng nó xử lý được mọi định dạng (JSON, text...). XHR dựa trên **callback**: bạn gán các handler `onload`, `onerror`, `onprogress...` rồi gọi `send()`.

Luồng cơ bản:

```js
const xhr = new XMLHttpRequest();
xhr.open("GET", url);          // cấu hình phương thức + URL
xhr.onload = () => {           // chạy khi response về ĐỦ
  console.log(xhr.status);     // 200
  console.log(xhr.responseText); // nội dung (string)
};
xhr.onerror = () => console.log("network error");
xhr.send();                    // bắt đầu gửi
```

Khác biệt cốt lõi so với fetch:

- **fetch**: Promise-based, cú pháp gọn, quản lý bằng `.then()`.
- **XHR**: callback-based, dài dòng, nhưng theo dõi được **tiến trình upload/download** (`upload.onprogress`).

Ngày nay nên dùng **fetch**; chỉ giữ XHR khi cần tương thích rất cũ hoặc theo dõi tiến trình.

## ✅ Điểm mạnh

- Hỗ trợ mọi trình duyệt từ lâu đời.
- Theo dõi tiến trình tải lên/tải xuống (progress event) — fetch không có sẵn.
- Hỗ trợ `overrideMimeType`, timeout, abort.
- Làm nền tảng để hiểu lịch sử evolution của web.

## ⚠️ Lưu ý / Hạn chế

- Cú pháp dài, nhiều callback → khó đọc, dễ callback hell.
- Không trả Promise — khó kết hợp với async/await (trừ khi tự wrap).
- `responseText` là chuỗi — phải tự `JSON.parse`.
- Bị CORS hạn chế như fetch; đã cũ nhưng vẫn hoạt động.

## 💡 Khi nào dùng

- Tải file có thanh tiến trình upload (progress listening).
- Hệ thống codebase cũ đang dùng XHR.
- Khi muốn so sánh để hiểu vì sao fetch tốt hơn.

## 🎯 Ví dụ minh họa

```js
const xhr = new XMLHttpRequest();
xhr.open("GET", "https://jsonplaceholder.typicode.com/posts/1");
xhr.onload = () =>
  console.log("XHR status", xhr.status, xhr.responseText.slice(0, 100));
xhr.onerror = () => console.log("XHR error");
xhr.send();

// Tương đương với fetch
fetch("https://jsonplaceholder.typicode.com/posts/1")
  .then((r) => r.text())
  .then((t) => console.log("fetch", t.slice(0, 100)));
```

## 📚 Tham khảo / Bài tập

- Chạy `02_xmlhttprequest/app.js` qua `index.html` hoặc `node app.js`: cùng một endpoint, xem cả output của XHR (`XHR status 200 ...`) lẫn fetch.
- Tự thử: dùng `xhr.open("POST", ...)` + `xhr.setRequestHeader("Content-Type", "application/json")` + `xhr.send(JSON.stringify(data))` để POST — so với fetch POST ở folder `05_crud` xem cách nào gọn hơn.