# Lịch sử ngắn gọn của JavaScript

## 🔑 Khái niệm

JavaScript ra đời năm **1995**, do **Brendan Eich** tạo ra tại **Netscape** — ban đầu chỉ là một ngôn ngữ kịch bản nhỏ cho trình duyệt, được phát triển vội vàng trong khoảng **10 ngày**. Từ một công cụ khiêm tốn, nó trở thành một trong những ngôn ngữ phổ biến nhất thế giới, minh chứng cho **"Định luật Atwood"**: *"Bất kỳ ứng dụng nào có thể được viết bằng JavaScript, cuối cùng sẽ được viết bằng JavaScript."* — Jeff Atwood (đồng sáng lập Stack Overflow).

**Các mốc lịch sử chính:**

| Năm | Sự kiện |
|-----|---------|
| 1995 | Brendan Eich tạo JS tại Netscape; tên đầu là **Mocha**, rồi **LiveScript** |
| 1996 | Đổi tên thành **JavaScript** (mượn danh tiếng Java dù không liên quan); Netscape 2.0 ra mắt |
| 1997 | Gửi chuẩn hóa cho **ECMA International** → **ECMAScript 1 (ES1)** |
| 1998 | **ES2** |
| 1999 | **ES3** — thêm regex, try/catch |
| 1999–2009 | "Thập kỷ im lặng"; dự án **ES4** bị từ bỏ (chính trị + độ phức tạp) |
| 2009 | **ES5** — strict mode, JSON, Array methods; ít tiếng vang |
| 2015 | **ES6 / ES2015** — bước ngoặt lớn nhất: `let`/`const`, class, arrow, promise, module, destructuring, spread... |
| 2016 | **ES2016** — `**`, `Array.prototype.includes` |
| 2017 | **ES2017** — async/await, `Object.values()`/`Object.entries()` |

Sau ES6, TC39 chuyển sang **phát hành hằng năm** (mỗi tháng 6), và gọi các phiên bản bằng năm như *ECMAScript 2016, 2017, 2018…* thay vì số phiên bản.

**Vì sao ES4 thất bại?** Nó tham vọng quá mức (classes, modules, static typing, destructuring…), gây chia rẽ giữa các nhà cung cấp. Nhóm đối lập (Google, Microsoft, Yahoo) đề xuất **ES3.1** — một bản nâng cấp nhẹ; và sau đó chính là tiền thân của ES5. Nhiều ý tưởng của ES4 cuối cùng được "hồi sinh" vào ES6.

**Quá trình chuẩn hóa** do **ECMA International** và ủy ban **TC39** đảm trách: tạo đặc tả chung để mọi trình duyệt hiểu JavaScript giống nhau, tránh tình trạng "mỗi trình duyệt một phiên bản". Kết quả là chuẩn chính thức có tên **ECMAScript**, còn "JavaScript" là cái tên thương mại.

## ✅ Điểm mạnh

- Hiểu nguồn gốc → nắm được vì sao JS không còn phụ thuộc trình duyệt (Node.js, Electron, React Native, CouchDB).
- Biết các mốc phiên bản → dễ so sánh hỗ trợ trình duyệt khi chọn tính năng.
- Hiểu thất bại của ES4 → hiểu triết lý "thêm tính năng theo từng giai đoạn" của TC39 hiện nay.
- Nắm quá trình chuẩn hóa → giải thích được vì sao code chạy ổn định trên nhiều trình duyệt.
- Xây dựng được nhận thức rằng JS là một hệ sinh thái năng động, phát triển liên tục.

## ⚠️ Lưu ý / Hạn chế

- **JavaScript ≠ Java**: chỉ trùng tên vì mục đích marketing, hoàn toàn khác nhau về bản chất.
- Phần lớn tính năng "hiện đại" (class, module...) chỉ thực sự ổn định từ **ES6/ES2015**; code cũ hơn thiếu những cú pháp tiện lợi này.
- Do phát triển vội vàng, một số "lỗi lịch sử" (như `typeof null === "object"`) không thể sửa vì sẽ phá vỡ hàng tỉ website.
- "10 ngày thai nghén" khiến ngôn ngữ có những ngóc ngách kỳ lạ — cần học có chọn lọc, không tin toàn bộ "tips" trên mạng.

## 💡 Khi nào dùng

- Cần giải thích vì sao JS có thể chạy backend (Node.js) hay mobile (React Native).
- Bạn đọc bug báo "ES5 only" và cần quyết định dịch code (transpile) hay viết tương thích.
- Muốn theo dõi tính năng mới của JS qua quy trình TC39.
- Phỏng vấn/kỹ thuật: câu hỏi kinh điển "Nêu lịch sử và các phiên bản JavaScript".

## 🎯 Ví dụ minh họa

```js
// Cú pháp theo từng thời kỳ
// ES3 (1999): var + hàm thường
var tuoi = 30;
function chao() {
  return "Xin chào";
}

// ES5 (2009): strict mode + JSON
"use strict";
var obj = JSON.parse('{"ten": "Nam"}');

// ES6 (2015) trở đi: let/const, arrow, template string, class
let ten = "Nam";
const getTuoi = () => 30;
console.log(`Xin chào ${ten}, ${getTuoi()} tuổi`); // Xin chào Nam, 30 tuổi
```

## 📚 Tham khảo / Bài tập

- Nhóm này **chưa có file `app.js`** — hãy tự chạy các cú pháp trên ở DevTools (F12 → Console).
- Tự thử: mở một trang cũ chứa `var` và đoán phiên bản tương ứng; kiểm tra xem trình duyệt bạn đang dùng hỗ trợ ES2023/ES2024 đến đâu tại [kangax.github.io/compat-table](https://kangax.github.io/compat-table/).
- Tài liệu: [roadmap.sh — History of JavaScript](https://roadmap.sh/guides/history-of-javascript), [Educative — JS Versions History](https://www.educative.io/blog/javascript-versions-history).