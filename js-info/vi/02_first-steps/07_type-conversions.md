# Chuyển đổi kiểu

> Nguồn: [https://javascript.info/type-conversions](https://javascript.info/type-conversions)

<!-- fetched: 2026-09-14 -->

Hầu hết thời gian, các toán tử và hàm tự động chuyển đổi các giá trị được đưa cho chúng sang kiểu đúng.

Ví dụ, `alert` tự động chuyển đổi bất kỳ giá trị nào thành chuỗi để hiển thị nó. Các thao tác toán học chuyển đổi giá trị thành số.

Cũng có những trường hợp khi chúng ta cần chuyển đổi rõ ràng một giá trị sang kiểu dự kiến.

Không nói về objects ngay bây giờ

Trong chương này, chúng ta sẽ không đề cập đến objects. Hiện tại, chúng ta sẽ chỉ nói về primitives.

Sau này, sau khi chúng ta học về objects, trong chương [Chuyển đổi object thành primitive](/object-toprimitive) chúng ta sẽ thấy objects phù hợp như thế nào.

## [Chuyển đổi Chuỗi](#string-conversion)

Chuyển đổi chuỗi xảy ra khi chúng ta cần dạng chuỗi của một giá trị.

Ví dụ, `alert(value)` làm điều đó để hiển thị giá trị.

Chúng ta cũng có thể gọi hàm `String(value)` để chuyển đổi một giá trị thành chuỗi:

```
let value = true;
alert(typeof value); // boolean

value = String(value); // giờ value là chuỗi "true"
alert(typeof value); // string
```

Chuyển đổi chuỗi chủ yếu là hiển nhiên. A `false` trở thành `"false"`, `null` trở thành `"null"`, v.v.

## [Chuyển đổi Số](#numeric-conversion)

Chuyển đổi số trong các hàm toán học và biểu thức xảy ra tự động.

Ví dụ, khi phép chia `/` được áp dụng cho các giá trị không phải số:

```
alert( "6" / "2" ); // 3, các chuỗi được chuyển đổi sang số
```

Chúng ta có thể sử dụng hàm `Number(value)` để chuyển đổi rõ ràng một `value` thành số:

```
let str = "123";
alert(typeof str); // string

let num = Number(str); // trở thành số 123

alert(typeof num); // number
```

Chuyển đổi rõ ràng thường được yêu cầu khi chúng ta đọc một giá trị từ một nguồn dựa trên chuỗi như form văn bản nhưng mong đợi một số được nhập.

Nếu chuỗi không phải là một số hợp lệ, kết quả của chuyển đổi như vậy là `NaN`. Ví dụ:

```
let age = Number("một chuỗi tùy ý thay vì số");

alert(age); // NaN, chuyển đổi thất bại
```

Quy tắc chuyển đổi số:

| Giá trị | Trở thành… |
| --- | --- |
| `undefined` | `NaN` |
| `null` | `0` |
| `true` và `false` | `1` và `0` |
| `string` | Dấu cách (bao gồm khoảng trống, tab `\t`, newline `\n` v.v.) từ đầu và cuối được xóa. Nếu chuỗi còn lại trống, kết quả là `0`. Ngược lại, số được “đọc” từ chuỗi. Lỗi cho `NaN`. |

Ví dụ:

```
alert( Number("   123   ") ); // 123
alert( Number("123z") );      // NaN (lỗi đọc số tại "z")
alert( Number(true) );        // 1
alert( Number(false) );       // 0
```

Xin lưu ý rằng `null` và `undefined` hành xử khác nhau ở đây: `null` trở thành không trong khi `undefined` trở thành `NaN`.

Hầu hết các toán tử toán học cũng thực hiện chuyển đổi như vậy, chúng ta sẽ thấy điều đó trong chương tiếp theo.

## [Chuyển đổi Boolean](#boolean-conversion)

Chuyển đổi boolean là đơn giản nhất.

Nó xảy ra trong các hoạt động logic (sau này chúng ta sẽ gặp các bài kiểm tra điều kiện và các thứ tương tự) nhưng cũng có thể được thực hiện rõ ràng bằng cách gọi `Boolean(value)`.

Quy tắc chuyển đổi:

- Các giá trị theo trực quan là “trống”, như `0`, chuỗi rỗng, `null`, `undefined`, và `NaN`, trở thành `false`.
- Các giá trị khác trở thành `true`.

Ví dụ:

```
alert( Boolean(1) ); // true
alert( Boolean(0) ); // false

alert( Boolean("hello") ); // true
alert( Boolean("") ); // false
```

Xin lưu ý: chuỗi với zero `"0"` là `true`

Một số ngôn ngữ (cụ thể là PHP) xử lý `"0"` như `false`. Nhưng trong JavaScript, một chuỗi không rỗng luôn là `true`.

```
alert( Boolean("0") ); // true
alert( Boolean(" ") ); // khoảng trắng, cũng true (bất kỳ chuỗi nào không rỗng đều true)
```

## [Tổng kết](#summary)

Ba chuyển đổi kiểu phổ biến nhất là sang chuỗi, sang số, và sang boolean.

**`Chuyển đổi Chuỗi`** – Xảy ra khi chúng ta xuất thứ gì đó. Có thể được thực hiện với `String(value)`. Chuyển đổi sang chuỗi thường là hiển nhiên cho các giá trị nguyên thủy.

**`Chuyển đổi Số`** – Xảy ra trong các phép toán math. Có thể được thực hiện với `Number(value)`.

Chuyển đổi tuân theo các quy tắc:

| Giá trị | Trở thành… |
| --- | --- |
| `undefined` | `NaN` |
| `null` | `0` |
| `true / false` | `1 / 0` |
| `string` | Chuỗi được đọc “nguyên vẹn”, dấu cách (bao gồm khoảng trống, tab `\t`, newline `\n` v.v.) từ cả hai bên bị bỏ qua. Chuỗi rỗng trở thành `0`. Lỗi cho `NaN`. |

**`Chuyển đổi Boolean`** – Xảy ra trong các hoạt động logic. Có thể được thực hiện với `Boolean(value)`.

Tuân theo các quy tắc:

| Giá trị | Trở thành… |
| --- | --- |
| `0`, `null`, `undefined`, `NaN`, `""` | `false` |
| bất kỳ giá trị khác | `true` |

Hầu hết các quy tắc này dễ hiểu và ghi nhớ. Các trường hợp đáng chú ý nơi mọi người thường mắc lỗi là:

- `undefined` là `NaN` như một số, không phải `0`.
- `"0"` và các chuỗi chỉ có khoảng trắng như `" "` là true như một boolean.

Objects không được đề cập ở đây. Chúng ta sẽ quay lại chúng sau trong chương [Chuyển đổi object thành primitive](/object-toprimitive) dành riêng cho objects sau khi chúng ta học thêm những điều cơ bản về JavaScript.
