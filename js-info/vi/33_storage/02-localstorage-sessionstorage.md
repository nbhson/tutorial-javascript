# LocalStorage và sessionStorage

> Source: [https://javascript.info/localstorage](https://javascript.info/localstorage)

<!-- fetched: 2026-09-14 -->

Các đối tượng web storage `localStorage` và `sessionStorage` cho phép lưu trữ các cặp key/value trong trình duyệt.

Điều thú vị về chúng là dữ liệu sống sót qua việc làm mới trang (với `sessionStorage`) và thậm chí qua việc khởi động lại trình duyệt hoàn toàn (với `localStorage`). Chúng ta sẽ sớm thấy điều đó.

Chúng ta đã có cookies. Tại sao cần thêm các đối tượng?

- Không giống cookies, các đối tượng web storage không được gửi lên server với mỗi request. Vì vậy, chúng ta có thể lưu trữ nhiều hơn. Hầu hết các trình duyệt hiện đại cho phép ít nhất 5 megabyte dữ liệu (hoặc nhiều hơn) và có các cài đặt để cấu hình điều đó.
- Ngoài ra, khác với cookies, server không thể thao tác với các đối tượng storage qua HTTP header. Mọi thứ đều được thực hiện bằng JavaScript.
- Storage gắn với origin (bộ ba domain/giao thức/cổng). Nghĩa là, các giao thức hoặc subdomain khác tạo ra các đối tượng storage khác nhau, chúng không thể truy cập dữ liệu của nhau.

Cả hai đối tượng storage cung cấp cùng các phương thức và thuộc tính:

- `setItem(key, value)` – lưu cặp key/value.
- `getItem(key)` – lấy giá trị theo key.
- `removeItem(key)` – xóa key cùng giá trị của nó.
- `clear()` – xóa mọi thứ.
- `key(index)` – lấy key tại vị trí cho trước.
- `length` – số lượng mục đã lưu.

Như bạn có thể thấy, nó giống như tập hợp `Map` (`setItem/getItem/removeItem`), nhưng cũng cho phép truy cập theo index bằng `key(index)`.

Hãy xem cách nó hoạt động.

## [localStorage demo](#localstorage-demo)

Các tính năng chính của `localStorage` là:

- Chia sẻ giữa tất cả các tab và cửa sổ cùng origin.
- Dữ liệu không hết hạn. Nó còn lại sau khi khởi động lại trình duyệt và thậm chí sau khi khởi động lại hệ điều hành.

Ví dụ, nếu bạn chạy mã này…

```
localStorage.setItem('test', 1);
```

…Và đóng/mở trình duyệt hoặc chỉ mở cùng trang trong một cửa sổ khác, thì bạn có thể lấy nó như thế này:

```
alert( localStorage.getItem('test') ); // 1
```

Chúng ta chỉ cần ở cùng origin (domain/cổng/giao thức), path của url có thể khác nhau.

`localStorage` được chia sẻ giữa tất cả các cửa sổ có cùng origin, vì vậy nếu chúng ta đặt dữ liệu trong một cửa sổ, thay đổi sẽ hiển thị trong cửa sổ khác.

## [Truy cập kiểu đối tượng](#object-like-access)

Chúng ta cũng có thể dùng cách truy cập đối tượng thông thường để lấy/đặt keys, như sau:

```
// set key
localStorage.test = 2;

// get key
alert( localStorage.test ); // 2

// remove key
delete localStorage.test;
```

Điều đó được cho phép vì lý do lịch sử, và phần lớn hoạt động, nhưng nhìn chung không được khuyến khích, vì:

1. Nếu key do người dùng tạo, nó có thể là bất kỳ thứ gì, như `length` hoặc `toString`, hoặc một phương thức khác có sẵn của `localStorage`. Trong trường hợp đó `getItem/setItem` hoạt động tốt, trong khi truy cập kiểu đối tượng thất bại:

   ```
   let key = 'length';
   localStorage[key] = 5; // Error, can't assign length
   ```
2. Có sự kiện `storage`, nó kích hoạt khi chúng ta sửa dữ liệu. Sự kiện đó không xảy ra với truy cập kiểu đối tượng. Chúng ta sẽ thấy điều đó sau trong chương này.

## [Lặp qua các key](#looping-over-keys)

Như chúng ta đã thấy, các phương thức cung cấp chức năng "lấy/đặt/xóa theo key". Nhưng làm thế nào để lấy tất cả các giá trị hoặc keys đã lưu?

Tiếc rằng, các đối tượng storage không thể lặp được.

Một cách là lặp qua chúng như với mảng:

```
for(let i=0; i<localStorage.length; i++) {
  let key = localStorage.key(i);
  alert(`${key}: ${localStorage.getItem(key)}`);
}
```

Cách khác là sử dụng vòng lặp `for key in localStorage`, giống như chúng ta làm với các đối tượng thường.

Nó lặp qua các keys, nhưng cũng in ra một vài trường có sẵn mà chúng ta không cần:

```
// bad try
for(let key in localStorage) {
  alert(key); // shows getItem, setItem and other built-in stuff
}
```

…Vì vậy chúng ta cần lọc các trường từ prototype bằng kiểm tra `hasOwnProperty`:

```
for(let key in localStorage) {
  if (!localStorage.hasOwnProperty(key)) {
    continue; // skip keys like "setItem", "getItem" etc
  }
  alert(`${key}: ${localStorage.getItem(key)}`);
}
```

…Hoặc chỉ cần lấy các keys "riêng" bằng `Object.keys` và sau đó lặp qua chúng nếu cần:

```
let keys = Object.keys(localStorage);
for(let key of keys) {
  alert(`${key}: ${localStorage.getItem(key)}`);
}
```

Cách sau hoạt động, vì `Object.keys` chỉ trả về các keys thuộc về đối tượng, bỏ qua prototype.

## [Chỉ chuỗi](#strings-only)

Vui lòng lưu ý rằng cả key và value đều phải là chuỗi.

Nếu chúng thuộc bất kỳ kiểu nào khác, như số hoặc đối tượng, chúng sẽ được chuyển đổi thành chuỗi tự động:

```
localStorage.user = {name: "John"};
alert(localStorage.user); // [object Object]
```

Tuy nhiên, chúng ta có thể dùng `JSON` để lưu các đối tượng:

```
localStorage.user = JSON.stringify({name: "John"});

// sometime later
let user = JSON.parse( localStorage.user );
alert( user.name ); // John
```

Ngoài ra, cũng có thể stringify toàn bộ đối tượng storage, ví dụ cho mục đích debug:

```
// added formatting options to JSON.stringify to make the object look nicer
alert( JSON.stringify(localStorage, null, 2) );
```

## [sessionStorage](#sessionstorage)

Đối tượng `sessionStorage` được dùng ít thường xuyên hơn `localStorage`.

Các thuộc tính và phương thức giống hệt nhau, nhưng nó bị giới hạn nhiều hơn:

- `sessionStorage` chỉ tồn tại trong tab trình duyệt hiện tại.
  - Một tab khác với cùng trang sẽ có storage khác.
  - Nhưng nó được chia sẻ giữa các iframe trong cùng tab (giả sử chúng đến từ cùng origin).
- Dữ liệu sống sót qua việc làm mới trang, nhưng không qua việc đóng/mở tab.

Hãy xem điều đó trong thực tế.

Chạy mã này…

```
sessionStorage.setItem('test', 1);
```

…Sau đó làm mới trang. Bây giờ bạn vẫn có thể lấy dữ liệu:

```
alert( sessionStorage.getItem('test') ); // after refresh: 1
```

…Nhưng nếu bạn mở cùng trang trong tab khác, và thử lại ở đó, mã trên sẽ trả về `null`, nghĩa là "không tìm thấy gì".

Chính xác là vì `sessionStorage` gắn không chỉ với origin, mà còn với tab trình duyệt. Vì lý do đó, `sessionStorage` được sử dụng thưa thớt.

## [Sự kiện storage](#storage-event)

Khi dữ liệu được cập nhật trong `localStorage` hoặc `sessionStorage`, sự kiện [storage](https://html.spec.whatwg.org/multipage/webstorage.html#the-storageevent-interface) kích hoạt, với các thuộc tính:

- `key` – key đã bị thay đổi (`null` nếu `.clear()` được gọi).
- `oldValue` – giá trị cũ (`null` nếu key mới được thêm).
- `newValue` – giá trị mới (`null` nếu key bị xóa).
- `url` – url của tài liệu nơi cập nhật diễn ra.
- `storageArea` – đối tượng `localStorage` hoặc `sessionStorage` nơi cập nhật diễn ra.

Điều quan trọng là: sự kiện kích hoạt trên tất cả các đối tượng `window` nơi storage có thể truy cập được, trừ đối tượng đã gây ra nó.

Hãy làm rõ điều đó.

Hãy tưởng tượng bạn có hai cửa sổ với cùng trang web trong mỗi cửa sổ. Vì vậy `localStorage` được chia sẻ giữa chúng.

Bạn có thể muốn mở trang này trong hai cửa sổ trình duyệt để kiểm tra mã bên dưới.

Nếu cả hai cửa sổ đều lắng nghe `window.onstorage`, thì mỗi cửa sổ sẽ phản ứng với các cập nhật diễn ra ở cửa sổ kia.

```
// triggers on updates made to the same storage from other documents
window.onstorage = event => { // can also use window.addEventListener('storage', event => {
  if (event.key != 'now') return;
  alert(event.key + ':' + event.newValue + " at " + event.url);
};

localStorage.setItem('now', Date.now());
```

Vui lòng lưu ý rằng sự kiện cũng chứa: `event.url` – url của tài liệu nơi dữ liệu được cập nhật.

Ngoài ra, `event.storageArea` chứa đối tượng storage – sự kiện giống nhau cho cả `sessionStorage` và `localStorage`, vì vậy `event.storageArea` tham chiếu đến đối tượng đã bị sửa đổi. Chúng ta thậm chí có thể muốn đặt lại thứ gì đó vào nó, để "phản ứng" với thay đổi.

**Điều đó cho phép các cửa sổ khác từ cùng origin trao đổi thông điệp với nhau.**

Các trình duyệt hiện đại cũng hỗ trợ [Broadcast channel API](https://developer.mozilla.org/en-US/docs/Web/api/Broadcast_Channel_API), API đặc biệt cho liên lạc giữa các cửa sổ cùng origin, nó đầy đủ tính năng hơn nhưng ít được hỗ trợ hơn. Có các thư viện polyfill API đó, dựa trên `localStorage`, giúp nó có sẵn ở khắp nơi.

## [Tóm tắt](#summary)

Các đối tượng web storage `localStorage` và `sessionStorage` cho phép lưu trữ các cặp key/value trong trình duyệt.

- Cả `key` và `value` đều phải là chuỗi.
- Giới hạn là 5mb+, phụ thuộc vào trình duyệt.
- Chúng không hết hạn.
- Dữ liệu gắn với origin (domain/cổng/giao thức).

| `localStorage` | `sessionStorage` |
| --- | --- |
| Chia sẻ giữa tất cả tab và cửa sổ cùng origin | Hiển thị trong một tab trình duyệt, bao gồm cả iframe từ cùng origin |
| Sống sót khi khởi động lại trình duyệt | Sống sót khi làm mới trang (nhưng không khi đóng tab) |

API:

- `setItem(key, value)` – lưu cặp key/value.
- `getItem(key)` – lấy giá trị theo key.
- `removeItem(key)` – xóa key cùng giá trị của nó.
- `clear()` – xóa mọi thứ.
- `key(index)` – lấy key số `index`.
- `length` – số lượng mục đã lưu.
- Dùng `Object.keys` để lấy tất cả các keys.
- Chúng ta truy cập keys như thuộc tính của đối tượng, trong trường hợp đó sự kiện `storage` không kích hoạt.

Sự kiện storage:

- Kích hoạt với các gọi `setItem`, `removeItem`, `clear`.
- Chứa tất cả dữ liệu về thao tác (`key/oldValue/newValue`), `url` của tài liệu và đối tượng storage `storageArea`.
- Kích hoạt trên tất cả các đối tượng `window` có quyền truy cập storage, trừ đối tượng đã tạo ra nó (trong tab với `sessionStorage`, toàn cục với `localStorage`).

---

---

## Bài tập

## [Bài tập](#tasks)

### [Tự động lưu trường form](#autosave-a-form-field)

Tạo một trường `textarea` "tự động lưu" giá trị của nó mỗi khi thay đổi.

Vậy, nếu người dùng vô tình đóng trang, và mở lại, anh ta sẽ thấy phần nhập liệu chưa hoàn thành của mình vẫn còn đó.

Như thế này:

[Mở sandbox cho bài tập.](https://plnkr.co/edit/Qib2uOppF9MWGXW5?p=preview)

solution

[Mở lời giải trong sandbox.](https://plnkr.co/edit/tJq9Clang0uVVLTH?p=preview)
