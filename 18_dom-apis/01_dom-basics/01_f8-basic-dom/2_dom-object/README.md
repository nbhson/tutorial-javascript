# Bài 2 — DOM Object: Thông Tin Document — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Ngoài việc lấy element, `document` còn cung cấp nhiều thuộc tính mô tả **trạng thái trang hiện tại**. Những thuộc tính này phản ánh metadata mà browser tự cập nhật — bạn chỉ cần đọc hoặc ghi. Đây là "cửa sổ" nhìn vào trạng thái hiện tại của trang.

### Bảng document properties

| Thuộc tính | Kiểu | Mô tả | Đọc/ghi? |
|---|---|---|---|
| `document.title` | `string` | Tiêu đề `<title>`, đọc/ghi được | ✅ Both |
| `document.URL` | `string` | URL đầy đủ của trang (encoded) | ✅ Read-only |
| `document.domain` | `string` | Tên miền (không có path) | ✅ Both (restricted) |
| `document.location` | `Location` object | Đối tượng Location đầy đủ, gán được để navigate | ✅ Both |
| `document.cookie` | `string` | Cookie của trang (read/write, không có HttpOnly) | ✅ Both |
| `document.referrer` | `string` | URL trang người dùng đến trước đó | ✅ Read-only |
| `document.lastModified` | `string` | Ngày sửa đổi cuối (theo UTC) | ✅ Read-only |
| `document.doctype` | `DocumentType` | Khai báo DOCTYPE (`<!DOCTYPE html>`) | ✅ Read-only |
| `document.characterSet` | `string` | Character encoding (`UTF-8`) | ✅ Read-only |
| `document.compatMode` | `string` | Rendering mode (`CSS1Compat` = standards) | ✅ Read-only |

### Đối tượng `Location`
```js
// document.location là object có nhiều property
console.log(document.location.href);      // URL đầy đủ
console.log(document.location.pathname);  // path: "/about"
console.log(document.location.search);    // query: "?q=js"
console.log(document.location.hash);      // hash: "#section"
console.log(document.location.hostname);  // hostname: "example.com"

// Redirect — gán href
document.location.href = "https://example.com";
// Hoặc ngắn gọn:
location.assign("https://example.com");
// Hoặc replace (không lưu history):
location.replace("https://example.com");
```

## 📐 Cấu trúc / Cú pháp

### Thông tin trang
```js
const info = {
  url: document.URL,
  title: document.title,
  domain: document.domain,
  charset: document.characterSet,
  lastModified: document.lastModified,
  referrer: document.referrer || "(trang mới)",
  compatMode: document.compatMode,
  cookieCount: document.cookie ? document.cookie.split(';').length : 0
};
console.table(info);
```

### Redirect động
```js
// Chuyển hướng sau 3 giây
setTimeout(() => {
  document.location.href = "https://example.com";
}, 3000);

// Redirect dựa trên điều kiện
if (!isLoggedIn()) {
  document.location.href = "/login";
}
```

### Đọc/ghi cookie
```js
// Set cookie
document.cookie = "theme=dark; max-age=86400; path=/";
document.cookie = "userId=abc123; expires=" + new Date(Date.now() + 7*24*3600*1000).toUTCString();

// Đọc cookie — parse manually
function getCookie(name) {
  const match = document.cookie.match(new RegExp('(?:^|; )' + name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '=([^;]*)'));
  return match ? decodeURIComponent(match[1]) : undefined;
}
console.log(getCookie('theme')); // "dark"
```

### Kết hợp với DOM manipulation
```js
// Đổi title và background dựa trên thời gian
const hour = new Date().getHours();
if (hour >= 22 || hour < 6) {
  document.title = "Night Mode";
  document.body.style.backgroundColor = '#1a1a2e';
} else {
  document.title = "Day Mode";
  document.body.style.backgroundColor = '#ffffff';
}
```

## ✅ Điểm mạnh

1. **Đọc/giữ được cả metadata trang** mà không cần query selector — trực tiếp từ `document`.
2. **`document.location` gán giá trị = redirect trang** — `location.href = "/new"` đơn giản, hiệu quả.
3. **`document.referrer` hữu ích** cho analytics, back button logic, "Bạn đang đến từ..." display.
4. **`document.cookie` read/write** — quản lý user preference (theme, language) mà không cần server.
5. **`document.title` read/write** — đổi tiêu đề tab động theo state (ví dụ: hiển thị notification count).
6. **`document.lastModified`** — kiểm tra trang có update không, cache invalidation logic.
7. **Không cần library** — tất cả đều là native browser API.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **`document.URL` có encode `%20` etc** — dùng `document.location.href` cho URL đã decode (readable).
2. **`document.cookie` chỉ đọc được cookie không có flag `HttpOnly`** — security restriction, không thể đọc/ghi secure cookies từ JS.
3. **`document.lastModified` có thể sai** — nếu server cache không cập nhật timestamp, hoặc dùng CDN.
4. **`document.domain` write restricted** — chỉ có thể set về domain cấp cao hơn (same origin policy).
5. **Setting `document.cookie` ghi đè** — mỗi lần set cookie mới sẽ thêm vào, không merge — cần parse old cookies nếu muốn update.
6. **`referrer` có thể empty** — direct visit, privacy settings, hoặc HTTPS→HTTP downgrade.
7. **Cookie size limit ~4KB per cookie, ~20 cookies per domain** — không lưu dữ liệu lớn.

## 💡 Khi nào dùng — Tình huống thực tế

1. **Debugging** — log metadata trang khi test (URL, title, referrer, cookie count).
2. **Redirect động** dựa trên điều kiện (user agent, time of day, auth status).
3. **Lấy referrer** để hiển thị "Bạn đang đến từ Google/Facebook...".
4. **Theme/language persistence** — lưu qua cookie, đọc khi load trang.
5. **Dynamic title** — hiển thị notification count: `document.title = \`(${unread}) New Messages\``.
6. **Cache busting** — so sánh `lastModified` với cached version.
7. **SPA route tracking** — log `location.href` changes cho analytics.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Thông tin trang hoàn chỉnh
```js
const info = {
  url: document.URL,
  title: document.title,
  domain: document.domain,
  charset: document.characterSet,
  lastModified: document.lastModified,
  referrer: document.referrer || "(trang mới)",
  cookieString: document.cookie || "(không có cookie)",
  compatMode: document.compatMode,
  elementCount: document.body?.children?.length ?? 0
};
console.table(info);
```

### Ví dụ 2: Redirect bằng location
```js
// Chuyển hướng sau 3 giây
setTimeout(() => {
  document.location.href = "https://example.com";
}, 3000);

// Hoặc dựa trên condition
if (window.location.pathname === '/old-page') {
  window.location.replace('/new-page'); // replace thay vì redirect — không lưu history
}
```

### Ví dụ 3: Đọc/ghi cookie đầy đủ
```js
// Set cookie với options
function setCookie(name, value, days = 7) {
  const expires = new Date(Date.now() + days * 86400 * 1000).toUTCString();
  document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/`;
}

// Get cookie
function getCookie(name) {
  return document.cookie.split('; ')
    .find(row => row.startsWith(name + '='))
    ?.split('=')[1];
}

// Delete cookie
function deleteCookie(name) {
  document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/`;
}

setCookie('theme', 'dark');
console.log(getCookie('theme')); // "dark"
deleteCookie('theme');
```

### Ví dụ 4: Dynamic page title với notification count
```js
let unreadCount = 5;
function updateTitle() {
  if (unreadCount > 0) {
    document.title = `(${unreadCount}) Tin mới — My App`;
  } else {
    document.title = 'My App';
  }
}
updateTitle();
// Khi đọc xong tin:
unreadCount = 0;
updateTitle(); // title revert về "My App"
```

### Ví dụ 5: Referrer-based content
```js
const referrer = document.referrer;
if (referrer.includes('google')) {
  console.log('User came from Google search');
  // Show search-result-specific content
} else if (referrer.includes('facebook')) {
  console.log('User came from Facebook');
  // Show social-proof content
} else {
  console.log('Direct visit or unknown referrer');
}
```

### Ví dụ 6: Check page state on unload
```js
window.addEventListener('beforeunload', (e) => {
  if (hasUnsavedChanges()) {
    e.preventDefault();
    e.returnValue = ''; // modern browsers require this
  }
});
```

## 🔗 Liên kết chéo

- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/1_dom-api/` — Document basics and root elements.
- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/3_element/` — element selection after knowing document.
- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/12_EventListener/` — `beforeunload` event usage.
- File tham khảo: `2.Dom-object.js` — chạy trực tiếp trong Console.
