# Trang: DOMContentLoaded, load, beforeunload, unload

> Source: [https://javascript.info/onload-ondomcontentloaded](https://javascript.info/onload-ondomcontentloaded)

<!-- fetched: 2026-09-14 -->

Chu kỳ vòng đời của một trang HTML có ba sự kiện quan trọng:

- `DOMContentLoaded` – trình duyệt đã tải xong HTML và cây DOM được xây dựng, nhưng các tài nguyên bên ngoài như ảnh `<img>` và stylesheet có thể chưa tải xong.
- `load` – không chỉ HTML được tải mà còn tất cả các tài nguyên bên ngoài: ảnh, styles, v.v.
- `beforeunload/unload` – người dùng đang rời khỏi trang.

Mỗi sự kiện đều có thể hữu ích:

- Sự kiện `DOMContentLoaded` – DOM đã sẵn sàng, nên handler có thể tìm kiếm các nút DOM, khởi tạo giao diện.
- Sự kiện `load` – các tài nguyên bên ngoài đã tải xong, nên styles đã được áp dụng, kích thước ảnh đã được biết, v.v.
- Sự kiện `beforeunload` – người dùng đang rời đi: chúng ta có thể kiểm tra xem người dùng đã lưu các thay đổi hay chưa và hỏi họ có thực sự muốn rời đi không.
- `unload` – người dùng hampir rời đi, nhưng chúng ta vẫn có thể khởi động các hoạt động khác, chẳng hạn như gửi thống kê.

Hãy cùng khám phá chi tiết của các sự kiện này.

## [DOMContentLoaded](#domcontentloaded)

Sự kiện `DOMContentLoaded` xảy ra trên đối tượng `document`.

Chúng ta phải dùng `addEventListener` để bắt sự kiện này:

```
document.addEventListener("DOMContentLoaded", ready);
// không phải "document.onDOMContentLoaded = ..."
```

Ví dụ:

```
<script>
  function ready() {
    alert('DOM đã sẵn sàng');

    // ảnh chưa được tải (trừ khi đã được cache), nên kích thước là 0x0
    alert(`Kích thước ảnh: ${img.offsetWidth}x${img.offsetHeight}`);
  }

  document.addEventListener("DOMContentLoaded", ready);
</script>

<img id="img" src="https://en.js.cx/clipart/train.gif?speed=1&cache=0">
```

Trong ví dụ, handler `DOMContentLoaded` chạy khi document được tải, nên nó có thể thấy tất cả các phần tử, kể cả `<img>` ở phía dưới.

Nhưng nó không chờ ảnh tải xong. Vậy `alert` hiển thị kích thước bằng 0.

Thoạt nhìn, sự kiện `DOMContentLoaded` rất đơn giản. Cây DOM đã sẵn sàng – đó là sự kiện. Tuy nhiên có vài điểm đặc biệt.

### [DOMContentLoaded và scripts](#domcontentloaded-and-scripts)

Khi trình duyệt xử lý một HTML-document và gặp thẻ `<script>`, nó cần phải thực thi trước khi tiếp tục xây dựng DOM. Đó là một biện pháp phòng ngừa, vì scripts có thể muốn sửa đổi DOM, thậm chí `document.write` vào đó, nên `DOMContentLoaded` phải chờ.

Vậy DOMContentLoaded chắc chắn xảy ra sau các script như vậy:

```
<script>
  document.addEventListener("DOMContentLoaded", () => {
    alert("DOM đã sẵn sàng!");
  });
</script>

<script src="https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.3.0/lodash.js"></script>

<script>
  alert("Thư viện đã tải, inline script đã thực thi");
</script>
```

Trong ví dụ trên, trước tiên chúng ta thấy "Thư viện đã tải…", sau đó là "DOM đã sẵn sàng!" (tất cả scripts đều được thực thi).

Các script không chặn DOMContentLoaded

Có hai ngoại lệ từ quy tắc này:

1. Các script có thuộc tính `async`, chúng ta sẽ tìm hiểu [ở đây](/script-async-defer), không chặn `DOMContentLoaded`.
2. Các script được tạo động bằng `document.createElement('script')` rồi thêm vào trang web cũng không chặn sự kiện này.

### [DOMContentLoaded và styles](#domcontentloaded-and-styles)

External stylesheet không ảnh hưởng đến DOM, nên `DOMContentLoaded` không chờ chúng.

Nhưng có một điểm cần lưu ý. Nếu chúng ta có một script sau style, thì script đó phải chờ cho đến khi stylesheet tải xong:

```
<link type="text/css" rel="stylesheet" href="style.css">
<script>
  // script không thực thi cho đến khi stylesheet tải xong
  alert(getComputedStyle(document.body).marginTop);
</script>
```

Lý do là script có thể muốn lấy tọa độ và các thuộc tính phụ thuộc vào style khác, như trong ví dụ trên. Tất nhiên, nó phải chờ styles tải xong.

Vì `DOMContentLoaded` chờ các script, nên nó cũng chờ cả styles trước đó.

### [Tự động điền của trình duyệt](#built-in-browser-autofill)

Firefox, Chrome và Opera tự động điền form trên `DOMContentLoaded`.

Ví dụ, nếu trang có một form với login và password, và trình duyệt đã ghi nhớ các giá trị, thì trên `DOMContentLoaded` nó có thể thử tự động điền chúng (nếu người dùng đồng ý).

Vì vậy, nếu `DOMContentLoaded` bị trì hoãn bởi các script tải chậm, thì autofill cũng phải chờ. Bạn có thể đã thấy điều này trên một số trang web (nếu bạn dùng autofill của trình duyệt) – các trường login/password không được autofill ngay lập tức, mà có một độ trễ cho đến khi trang tải xong. Thực ra đó là độ trễ cho đến khi sự kiện `DOMContentLoaded` xảy ra.

## [window.onload](#window-onload)

Sự kiện `load` trên đối tượng `window` kích hoạt khi toàn bộ trang đã tải, bao gồm styles, images và các tài nguyên khác. Sự kiện này có thể truy cập qua property `onload`.

Ví dụ dưới đây hiển thị đúng kích thước ảnh, vì `window.onload` chờ tất cả ảnh:

```
<script>
  window.onload = function() { // cũng có thể dùng window.addEventListener('load', (event) => {
    alert('Trang đã tải');

    // ảnh đã được tải lúc này
    alert(`Kích thước ảnh: ${img.offsetWidth}x${img.offsetHeight}`);
  };
</script>

<img id="img" src="https://en.js.cx/clipart/train.gif?speed=1&cache=0">
```

## [window.onunload](#window-onunload)

Khi một người truy cập rời khỏi trang, sự kiện `unload` kích hoạt trên `window`. Chúng ta có thể làm một số việc không liên quan đến độ trễ, như đóng các cửa sổ popup liên quan.

Ngoại lệ đáng chú ý là gửi analytics.

Giả sử chúng ta thu thập dữ liệu về cách trang được sử dụng: các cú click chuột, cuộn trang, các vùng trang đã xem, và nhiều hơn nữa.

Tất nhiên, sự kiện `unload` là lúc người dùng rời đi, và chúng ta muốn lưu dữ liệu lên server của mình.

Có một phương thức đặc biệt gọi là `navigator.sendBeacon(url, data)` cho nhu cầu như vậy, được mô tả trong specification <https://w3c.github.io/beacon/>.

Nó gửi dữ liệu ở chế độ background. Việc chuyển sang trang khác không bị chậm: trình duyệt rời trang, nhưng vẫn thực hiện `sendBeacon`.

Cách dùng như sau:

```
let analyticsData = { /* object chứa dữ liệu đã thu thập */ };

window.addEventListener("unload", function() {
  navigator.sendBeacon("/analytics", JSON.stringify(analyticsData));
});
```

- Request được gửi dưới dạng POST.
- Chúng ta có thể gửi không chỉ string, mà còn forms và các định dạng khác, như mô tả trong chương [Fetch](/fetch), nhưng thường là một object đã được stringify.
- Dữ liệu bị giới hạn ở 64kb.

Khi request `sendBeacon` hoàn tất, trình duyệt có thể đã rời khỏi document, nên không có cách nào để nhận phản hồi từ server (thường là rỗng đối với analytics).

Cũng có flag `keepalive` để thực hiện các request "sau khi rời trang" này trong phương thức [fetch](/fetch) cho các request mạng chung. Bạn có thể tìm thêm thông tin trong chương [Fetch API](/fetch-api).

Nếu chúng ta muốn hủy chuyển hướng sang trang khác, chúng ta không thể làm điều đó ở đây. Nhưng chúng ta có thể dùng một sự kiện khác – `onbeforeunload`.

## [window.onbeforeunload](#window.onbeforeunload)

Nếu một người truy cập khởi tạo điều hướng khỏi trang hoặc cố gắng đóng cửa sổ, handler `beforeunload` yêu cầu xác nhận bổ sung.

Nếu chúng ta hủy sự kiện, trình duyệt có thể hỏi người truy cập có chắc chắn không.

Bạn có thể thử bằng cách chạy code này và sau đó tải lại trang:

```
window.onbeforeunload = function() {
  return false;
};
```

Do lý do lịch sử, việc trả về một non-empty string cũng được tính là hủy sự kiện. Cách đây không lâu, các trình duyệt thường hiển thị nó như một thông báo, nhưng theo [specification hiện đại](https://html.spec.whatwg.org/#unloading-documents), chúng không nên làm vậy.

Đây là một ví dụ:

```
window.onbeforeunload = function() {
  return "Có các thay đổi chưa lưu. Rời đi bây giờ?";
};
```

Hành vi đã được thay đổi, vì một số webmaster đã lạm dụng handler sự kiện này bằng cách hiển thị các thông báo gây hiểu lầm và khó chịu. Vì vậy hiện tại các trình duyệt cũ vẫn có thể hiển thị nó như một thông báo, nhưng ngoài ra – không có cách nào để tùy chỉnh thông báo hiển thị cho người dùng.

`event.preventDefault()` không hoạt động từ handler `beforeunload`

Nghe có vẻ kỳ lạ, nhưng hầu hết các trình duyệt bỏ qua `event.preventDefault()`.

Điều đó có nghĩa là, code sau có thể không hoạt động:

```
window.addEventListener("beforeunload", (event) => {
  // không hoạt động, nên handler sự kiện này không làm gì cả
  event.preventDefault();
});
```

Thay vào đó, trong các handler như vậy, người ta nên đặt `event.returnValue` thành một string để đạt được kết quả tương tự như code trên:

```
window.addEventListener("beforeunload", (event) => {
  // hoạt động, tương tự như trả về từ window.onbeforeunload
  event.returnValue = "Có các thay đổi chưa lưu. Rời đi bây giờ?";
});
```

## [readyState](#readystate)

Điều gì sẽ xảy ra nếu chúng ta đặt handler `DOMContentLoaded` sau khi document đã được tải?

Tất nhiên, nó sẽ không bao giờ chạy.

Có những trường hợp chúng ta không chắc document đã sẵn sàng hay chưa. Chúng ta muốn hàm của mình thực thi khi DOM được tải, dù là bây giờ hay sau này.

Property `document.readyState` cho chúng ta biết trạng thái tải hiện tại.

Có 3 giá trị có thể:

- `"loading"` – document đang tải.
- `"interactive"` – document đã được đọc xong.
- `"complete"` – document đã được đọc xong và tất cả tài nguyên (như ảnh) cũng đã tải xong.

Vậy chúng ta có thể kiểm tra `document.readyState` và thiết lập handler hoặc thực thi code ngay lập tức nếu nó đã sẵn sàng.

Như thế này:

```
function work() { /*...*/ }

if (document.readyState == 'loading') {
  // vẫn đang tải, chờ sự kiện
  document.addEventListener('DOMContentLoaded', work);
} else {
  // DOM đã sẵn sàng!
  work();
}
```

Cũng có sự kiện `readystatechange` kích hoạt khi state thay đổi, nên chúng ta có thể in tất cả các state như sau:

```
// state hiện tại
console.log(document.readyState);

// in các thay đổi state
document.addEventListener('readystatechange', () => console.log(document.readyState));
```

Sự kiện `readystatechange` là một cơ chế thay thế để theo dõi trạng thái tải document, nó xuất hiện từ lâu. Ngày nay, nó hiếm khi được sử dụng.

Hãy xem luồng sự kiện đầy đủ để completeness.

Đây là một document với `<iframe>`, `<img>` và các handler ghi lại sự kiện:

```
<script>
  log('readyState ban đầu:' + document.readyState);

  document.addEventListener('readystatechange', () => log('readyState:' + document.readyState));
  document.addEventListener('DOMContentLoaded', () => log('DOMContentLoaded'));

  window.onload = () => log('window onload');
</script>

<iframe src="iframe.html" onload="log('iframe onload')"></iframe>

<img src="https://en.js.cx/clipart/train.gif" id="img">
<script>
  img.onload = () => log('img onload');
</script>
```

Example hoạt động có [tại sandbox](https://plnkr.co/edit/AhBqQwGWWyqsYyOi?p=preview).

Output điển hình:

1. [1] initial readyState:loading
2. [2] readyState:interactive
3. [2] DOMContentLoaded
4. [3] iframe onload
5. [4] img onload
6. [4] readyState:complete
7. [4] window onload

Các số trong ngoặc vuông biểu thị thời gian gần đúng khi nó xảy ra. Các sự kiện được gán cùng một chữ số xảy ra xấp xỉ cùng thời điểm (± vài ms).

- `document.readyState` trở thành `interactive` ngay trước `DOMContentLoaded`. Hai điều này thực chất có nghĩa giống nhau.
- `document.readyState` trở thành `complete` khi tất cả tài nguyên (`iframe` và `img`) được tải xong. Ở đây chúng ta có thể thấy rằng nó xảy ra vào khoảng cùng thời điểm với `img.onload` (`img` là tài nguyên cuối cùng) và `window.onload`. Chuyển sang state `complete` có nghĩa tương tự như `window.onload`. Sự khác biệt là `window.onload` luôn chạy sau tất cả các handler `load` khác.

## [Tóm tắt](#summary)

Các sự kiện tải trang:

- Sự kiện `DOMContentLoaded` kích hoạt trên `document` khi DOM đã sẵn sàng. Chúng ta có thể áp dụng JavaScript lên các phần tử ở giai đoạn này.
  - Script như `<script>...</script>` hoặc `<script src="..."></script>` chặn DOMContentLoaded, trình duyệt chờ chúng thực thi.
  - Ảnh và các tài nguyên khác có thể vẫn đang tiếp tục tải.
- Sự kiện `load` trên `window` kích hoạt khi trang và tất cả tài nguyên đã được tải. Chúng ta hiếm khi sử dụng nó, vì thường không cần chờ lâu như vậy.
- Sự kiện `beforeunload` trên `window` kích hoạt khi người dùng muốn rời khỏi trang. Nếu chúng ta hủy sự kiện, trình duyệt sẽ hỏi liệu người dùng có thực sự muốn rời đi không (ví dụ chúng ta có các thay đổi chưa lưu).
- Sự kiện `unload` trên `window` kích hoạt khi người dùng cuối cùng đang rời đi, trong handler chúng ta chỉ có thể làm những việc đơn giản không liên quan đến độ trễ hoặc hỏi người dùng. Do hạn chế đó, nó hiếm khi được sử dụng. Chúng ta có thể gửi một network request với `navigator.sendBeacon`.
- `document.readyState` là trạng thái hiện tại của document, các thay đổi có thể được theo dõi trong sự kiện `readystatechange`:
  - `loading` – document đang tải.
  - `interactive` – document đã được parse, xảy ra vào khoảng cùng thời điểm với `DOMContentLoaded`, nhưng trước nó.
  - `complete` – document và các tài nguyên đã được tải, xảy ra vào khoảng cùng thời điểm với `window.onload`, nhưng trước nó.
