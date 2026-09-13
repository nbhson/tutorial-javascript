# XMLHttpRequest (XHR) — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**XMLHttpRequest** là API **tiền thân của fetch**, cho phép gửi HTTP request từ JS — dù tên có "XML" nhưng nó xử lý được mọi định dạng (JSON, text, binary...). XHR dựa trên **callback**: bạn gán các handler `onload`, `onerror`, `onprogress`... rồi gọi `send()`.

Khác biệt cốt lõi so với fetch:
- **fetch**: Promise-based, cú pháp gọn, quản lý bằng `.then()`.
- **XHR**: callback-based, dài dòng, nhưng theo dõi được **tiến trình upload/download** (`upload.onprogress`) — fetch không có tính năng này.

Ngày nay nên dùng **fetch**; chỉ giữ XHR khi cần tương thích rất cũ hoặc theo dõi tiến trình tải file.

## 📐 Cấu trúc / Cú pháp

### XHR basic pattern

```js
const xhr = new XMLHttpRequest();

// 1. Configure
xhr.open(method, url, async=true);  // method: GET/POST/PUT/DELETE
                                     // async: true (default) hoặc false

// 2. Set headers (phải sau open, trước send)
xhr.setRequestHeader("Content-Type", "application/json");
xhr.setRequestHeader("Authorization", "Bearer token");

// 3. Setup handlers
xhr.onload = function() {
  // chạy khi response nhận ĐỦ (dù status 200 hay 404)
  console.log("Status:", xhr.status);
  console.log("Response:", xhr.responseText);
};

xhr.onerror = function() {
  // chỉ chạy khi NETWORK error
  console.error("Network error");
};

xhr.onprogress = function(event) {
  // tiến trình download
  if (event.lengthComputable) {
    const percent = (event.loaded / event.total) * 100;
    console.log(`Downloaded ${percent.toFixed(1)}%`);
  }
};

xhr.upload.onprogress = function(event) {
  // tiến trình upload
  if (event.lengthComputable) {
    const percent = (event.loaded / event.total) * 100;
    console.log(`Uploaded ${percent.toFixed(1)}%`);
  }
};

xhr.ontimeout = function() {
  console.error("Request timed out");
};

// 4. Send
xhr.timeout = 5000; // ms
xhr.send(body); // body: string, FormData, ArrayBuffer, null
```

### XHR vs Fetch comparison table

| Đặc tính | XMLHttpRequest | Fetch API |
|----------|---------------|-----------|
| Callback vs Promise | Callback-based | Promise-based |
| Syntax | Dài, verbose | Ngắn, gọn |
| Progress tracking | ✅ `onprogress` | ❌ Không có |
| Timeout | ✅ `.timeout` property | AbortController |
| Abort | `.abort()` | AbortController |
| Response types | `.responseText`, `.responseXML`, `.response` (blob/arraybuffer) | `.text()`, `.json()`, `.blob()`, `.formData()` |
| CORS | ✅ | ✅ |
| Modern browsers | All | All modern |

### XHR readyState values

| Value | Name | Meaning |
|-------|------|---------|
| 0 | `UNSENT` | Created, chưa open() |
| 1 | `OPENED` | open() được gọi |
| 2 | `HEADERS_RECEIVED` | Headers nhận được |
| 3 | `LOADING` | Data đang nhận |
| 4 | `DONE` | Hoàn tất |

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Hỗ trợ mọi trình duyệt từ lâu đời** — IE6+, safe cho legacy projects.
2. **Theo dõi tiến trình tải lên/tải xuống** (`progress` event) — fetch không có sẵn.
3. **Hỗ trợ `overrideMimeType`** — ép decode content type khác.
4. **Timeout trực tiếp** qua `.timeout` property — đơn giản hơn AbortController.
5. **Nền tảng để hiểu lịch sử evolution** của web HTTP APIs.
6. **Binary response** dễ dàng — `.responseType = "blob|arraybuffer"`.
7. **CORS preflight** tự động — XHR xử lý automatic.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: `onload` chạy cả với HTTP error (404, 500)

```js
xhr.onload = function() {
  // CHẠY ngay cả khi status 404!
  if (xhr.status >= 200 && xhr.status < 300) {
    console.log("Success:", xhr.responseText);
  } else {
    console.error("HTTP error:", xhr.status);
  }
};
```

### Bẫy 2: `onerror` chỉ bắt network error, KHÔNG bắt HTTP error

```js
xhr.onerror = function() {
  // Chỉ chạy khi network down, CORS blocked, aborted
  // KHÔNG chạy khi server trả 404/500!
};
```

### Bẫy 3: `setRequestHeader` phải gọi sau `open()`, trước `send()`

```js
xhr.open("POST", url);
xhr.setRequestHeader("Content-Type", "application/json"); // ✅ đúng
// xhr.open(...) phải trước setRequestHeader
```

### Bẫy 4: `send()` không tự stringify body — phải tự làm

```js
// ❌ Sai
xhr.send({ name: "John" }); // → "[object Object]"

// ✅ Đúng
xhr.send(JSON.stringify({ name: "John" }));
```

### Bẫy 5: Async=false bị deprecate — không nên dùng

```js
// ❌ Sai — synchronous XHR chặn main thread
xhr.open("GET", url, false); // false = sync
xhr.send();
// Modern browsers warn/deprecated
```

### Bẫy 6: Response type mặc định là text — cần set cho binary

```js
xhr.responseType = "blob"; // hoặc "arraybuffer", "document", "json"
xhr.send();
// xhr.response sẽ là blob thay vì text
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Tải file có thanh tiến trình upload/download** — progress listening.
2. **Hệ thống codebase cũ** đang dùng XHR — refactor dần.
3. **So sánh để hiểu** vì sao fetch tốt hơn.
4. **Legacy browser support** — IE11 không có fetch.
5. **Streaming binary data** — download large files với progress.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Basic GET với XHR

```js
const xhr = new XMLHttpRequest();
xhr.open("GET", "https://jsonplaceholder.typicode.com/posts/1");
xhr.onload = () => {
  if (xhr.status >= 200 && xhr.status < 300) {
    const post = JSON.parse(xhr.responseText);
    console.log("Title:", post.title);
  } else {
    console.error("HTTP error:", xhr.status);
  }
};
xhr.onerror = () => console.error("Network error");
xhr.send();
```

### Ví dụ 2: XHR vs Fetch — cùng endpoint

```js
// XHR version
const xhr = new XMLHttpRequest();
xhr.open("GET", "https://jsonplaceholder.typicode.com/posts/1");
xhr.onload = () =>
  console.log("XHR status", xhr.status, xhr.responseText.slice(0, 100));
xhr.onerror = () => console.log("XHR error");
xhr.send();

// Fetch equivalent
fetch("https://jsonplaceholder.typicode.com/posts/1")
  .then((r) => r.text())
  .then((t) => console.log("fetch", t.slice(0, 100)));
```

### Ví dụ 3: POST với XHR

```js
const xhr = new XMLHttpRequest();
xhr.open("POST", "https://jsonplaceholder.typicode.com/posts");
xhr.setRequestHeader("Content-Type", "application/json");
xhr.onload = function() {
  if (xhr.status >= 200 && xhr.status < 300) {
    const newPost = JSON.parse(xhr.responseText);
    console.log("Created:", newPost.id);
  }
};
xhr.onerror = () => console.error("Error");
xhr.send(JSON.stringify({
  title: "Foo",
  body: "bar",
  userId: 1
}));
```

### Ví dụ 4: Progress tracking (download)

```js
const xhr = new XMLHttpRequest();
xhr.open("GET", "/large-file.zip");

xhr.onprogress = (event) => {
  if (event.lengthComputable) {
    const percent = (event.loaded / event.total) * 100;
    console.log(`Downloaded: ${percent.toFixed(1)}% (${event.loaded}/${event.total})`);
  }
};

xhr.onload = () => {
  if (xhr.status >= 200 && xhr.status < 300) {
    console.log("Download complete");
  }
};

xhr.onerror = () => console.error("Download failed");
xhr.send();
```

### Ví dụ 5: Upload với progress

```js
const xhr = new XMLHttpRequest();
xhr.open("POST", "/api/upload");

xhr.upload.onprogress = (event) => {
  if (event.lengthComputable) {
    const percent = (event.loaded / event.total) * 100;
    console.log(`Uploading: ${percent.toFixed(1)}%`);
  }
};

xhr.onload = () => {
  if (xhr.status >= 200 && xhr.status < 300) {
    console.log("Upload successful");
  }
};

xhr.send(new FormData(document.getElementById("upload-form")));
```

### Ví dụ 6: Timeout handling

```js
const xhr = new XMLHttpRequest();
xhr.open("GET", "https://slow-api.com/data");
xhr.timeout = 3000; // 3 seconds

xhr.ontimeout = () => console.error("Timeout after 3s");
xhr.onload = () => {
  if (xhr.status >= 200 && xhr.status < 300) {
    console.log(JSON.parse(xhr.responseText));
  }
};
xhr.onerror = () => console.error("Network error");
xhr.send();
```

### Ví dụ 7: Abort XHR

```js
const xhr = new XMLHttpRequest();
xhr.open("GET", "/api/slow-request");

xhr.onload = () => console.log(JSON.parse(xhr.responseText));
xhr.send();

// Abort after 5 seconds
setTimeout(() => {
  xhr.abort();
  console.log("Request aborted");
}, 5000);
```

### Ví dụ 8: XHR với JSON responseType

```js
const xhr = new XMLHttpRequest();
xhr.open("GET", "https://jsonplaceholder.typicode.com/posts/1");
xhr.responseType = "json"; // parse automatic

xhr.onload = () => {
  if (xhr.status >= 200 && xhr.status < 300) {
    console.log("Title:", xhr.response.title); // direct object, no JSON.parse needed
  }
};
xhr.send();
```

### Ví dụ 9: Wrap XHR in Promise (bridge to modern API)

```js
function xhrRequest(method, url, data = null) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open(method, url);
    xhr.setRequestHeader("Content-Type", "application/json");
    
    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(JSON.parse(xhr.responseText));
      } else {
        reject(new Error(`HTTP ${xhr.status}`));
      }
    };
    xhr.onerror = () => reject(new Error("Network error"));
    xhr.ontimeout = () => reject(new Error("Timeout"));
    
    xhr.timeout = 5000;
    xhr.send(data ? JSON.stringify(data) : null);
  });
}

// Sử dụng như fetch
xhrRequest("GET", "https://jsonplaceholder.typicode.com/posts/1")
  .then(post => console.log(post.title))
  .catch(err => console.error(err));
```

## 🔬 So sánh với alternatives

| API | Syntax style | Progress | Timeout | Modern? |
|-----|-------------|----------|---------|---------|
| XHR | Callback | ✅ | ✅ `.timeout` | ❌ Legacy |
| Fetch | Promise | ❌ | AbortController | ✅ Modern |
| Axios | Promise | ✅ | `timeout` option | ✅ Library |

## 📊 Performance & Best Practices

- **Prefers fetch** cho code mới — ngắn gọn, promise-based.
- **Dùng XHR** khi cần progress tracking hoặc legacy support.
- **Always check `xhr.status`** trong `onload` — onload không phân biệt success/error HTTP.
- **Set `xhr.responseType`** khi cần binary/JSON auto-parse.
- **Wrap XHR in Promise** nếu muốn dùng với async/await.
- **Clear timeout** khi unmount/component destroy.

## 🔗 Liên kết chéo

- **Xem thêm:** `13_working-with-apis/01_fetch` — modern replacement for XHR
- **Xem thêm:** `13_working-with-apis/05_crud` — CRUD with fetch (modern approach)
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/01_promise-theory` — promise wrapping
- **Xem thêm:** `13_working-with-apis/README` — APIs overview
