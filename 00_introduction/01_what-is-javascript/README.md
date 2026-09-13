# JavaScript là gì?

## 🔑 Khái niệm

**JavaScript** (viết tắt **JS**) là một ngôn ngữ lập trình **thông dịch cấp cao** (high-level, được *thông dịch* hoặc *biên dịch JIT*), và là một trong ba công nghệ cốt lõi của **World Wide Web**, bên cạnh **HTML** (cấu trúc) và **CSS** (trình bày). Nếu HTML là "bộ xương" và CSS là "quần áo", thì JavaScript là "bộ não" giúp trang web suy nghĩ và phản ứng lại người dùng.

Những tương tác bạn quen thuộc hằng ngày — thanh trượt, cửa sổ bật lên (alert/popup), menu đổ xuống, xác thực form ngay khi gõ, v.v. — đều được xây dựng bằng JavaScript.

Các tính chất quyết định của JavaScript:

- **First-class functions**: hàm được xử lý như một giá trị bình thường (gán cho biến, truyền vào hàm khác, trả về từ hàm) → xem thêm `01_first-class-function/`.
- **Prototype-based**: không có "class" thực sự, đối tượng kế thừa từ đối tượng khác qua chuỗi prototype → xem thêm `02_prototype-based-programming/`.
- **Garbage-collected**: bộ nhớ được quản lý tự động, lập trình viên không cần tự giải phóng.
- **Dynamic typing**: kiểu dữ liệu tự biến đổi theo giá trị gán, không khai báo kiểu tĩnh.
- **Đa mô hình**: hỗ trợ lập trình mệnh lệnh (imperative), hướng đối tượng (object-oriented) và hàm (functional).

Ngoài trình duyệt, JavaScript còn chạy ở nhiều môi trường khác: **Node.js** (máy chủ), **Electron** (app desktop), **React Native** (app di động), **Apache CouchDB**, **Adobe Acrobat**, v.v. Các môi trường này đều dùng chung một *JavaScript engine* như **V8** (Chrome/Node), **SpiderMonkey** (Firefox), **JavaScriptCore** (Safari) để thực thi mã nguồn.

## ✅ Điểm mạnh

- **Phổ biến mọi nơi**: chạy ở trình duyệt, máy chủ, di động, desktop — học một lần, dùng nhiều nơi.
- **Hệ sinh thái khổng lồ**: npm, React, Vue, Node, Electron... cộng đồng hỗ trợ rất lớn.
- **Bắt đầu nhanh**: không cần cài đặt phức tạp, mở DevTools của trình duyệt là viết được ngay.
- **Đa mô hình lập trình**: imperative, OOP, functional đều làm được, linh hoạt theo bài toán.
- **Không cần type khi khởi tạo**: phù hợp tạo prototype và MVP nhanh.

## ⚠️ Lưu ý / Hạn chế

- **Dynamic typing** đôi khi gây lỗi ở runtime mà ngôn ngữ kiểu tĩnh đã bắt được ngay; hãy cân nhắc TypeScript khi dự án lớn.
- Cơ chế ép kiểu ngầm định (`1 + "1"` = `"11"`) dễ sinh bug nếu không hiểu rõ (học kỹ ở nhóm `02_data-types/03_type-casting-and-coercion`).
- Các môi trường chạy khác nhau (trình duyệt vs Node) có các API khác nhau — `document`, `window` chỉ tồn tại trong trình duyệt.
- Lịch sử phát triển gấp gáp khiến một số hành vi lạ (như `typeof null === "object"`) trở thành "chuẩn" không thể sửa.

## 💡 Khi nào dùng

- Xây dựng tính tương tác cho website (xác thực form, cập nhật nội dung không cần reload).
- Viết API / máy chủ bằng Node.js.
- Tạo app desktop (Electron) hoặc app di động (React Native) dùng chung một ngôn ngữ.
- Lập trình robotics/IoT (JavaScriptCore, Johnny-Five) hoặc các thiết bị như Adobe Acrobat, CouchDB.

## 🎯 Ví dụ minh họa

```js
// 1. First-class function — hàm là một giá trị
const chao = (ten) => `Xin chào, ${ten}!`;
console.log(chao("Nam"));            // "Xin chào, Nam!"

// 2. Dynamic typing — tự đổi kiểu theo giá trị gán
let bien = "chuỗi";
bien = 42;                            // giờ là number, không báo lỗi
console.log(bien + 1);               // 43

// 3. Đối tượng kế thừa qua prototype
const dongVat = { tiengKeu: "..." };
const conCho = Object.create(dongVat);
conCho.ten = "Buddy";
console.log(conCho.ten);             // "Buddy"
console.log(conCho.tiengKeu);        // "..." — kế thừa từ prototype
```

## 📚 Tham khảo / Bài tập

- Vào 2 bài con để hiểu sâu 2 tính chất quan trọng nhất:
  - `01_first-class-function/` — vì sao hàm JavaScript là "first-class".
  - `02_prototype-based-programming/` — vì sao JS gọi là prototype-based.
- Tự thử: mở DevTools (F12 → Console) trong trình duyệt bất kỳ, gõ `typeof null`, `(10).toString()`, `["a","b"].map(x => x.toUpperCase())` và quan sát kết quả.
- Tài liệu: [MDN JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript), [javascript.info/intro](https://javascript.info/intro).