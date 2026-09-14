# Scripts: async, defer

> Source: [https://javascript.info/script-async-defer](https://javascript.info/script-async-defer)

<!-- fetched: 2026-09-14 -->

Trong các website hiện đại, scripts thường "nặng" hơn HTML: kích thước tải xuống lớn hơn, và thời gian xử lý cũng dài hơn.

Khi trình duyệt tải HTML và gặp thẻ `<script>...</script>`, nó không thể tiếp tục xây dựng DOM. Nó phải thực thi script ngay lập tức. Điều tương tự xảy ra với các script external `<script src="..."></script>`: trình duyệt phải chờ script tải xong, thực thi script đã tải, và chỉ sau đó mới có thể xử lý phần còn lại của trang.

Điều đó dẫn đến hai vấn đề quan trọng:

1. Scripts không thể thấy các phần tử DOM phía dưới chúng, nên không thể thêm handlers, v.v.
2. Nếu có một script lớn ở đầu trang, nó "chặn trang". Người dùng không thể thấy nội dung trang cho đến khi nó tải xong và chạy:

```
<p>...nội dung trước script...</p>

<script src="https://javascript.info/article/script-async-defer/long.js?speed=1"></script>

<!-- Chưa hiển thị cho đến khi script tải xong -->
<p>...nội dung sau script...</p>
```

Có một số workaround cho vấn đề này. Ví dụ, chúng ta có thể đặt script ở cuối trang. Sau đó nó có thể thấy các phần tử phía trên, và không chặn nội dung trang hiển thị:

```
<body>
  ...tất cả nội dung ở phía trên script...

  <script src="https://javascript.info/article/script-async-defer/long.js?speed=1"></script>
</body>
```

Nhưng giải pháp này không hoàn hảo. Ví dụ, trình duyệt chỉ nhận ra script (và có thể bắt đầu tải nó) sau khi đã tải xong full HTML document. Đối với các HTML document dài, đó có thể là một độ trễ đáng kể.

Những thứ như vậy không thể hiện rõ đối với người dùng kết nối rất nhanh, nhưng nhiều người trên thế giới vẫn có tốc độ internet chậm và sử dụng kết nối mobile internet không hoàn hảo.

May mắn thay, có hai thuộc tính `<script>` giải quyết vấn đề cho chúng ta: `defer` và `async`.

## [defer](#defer)

Thuộc tính `defer` báo trình duyệt không chờ script. Thay vào đó, trình duyệt sẽ tiếp tục xử lý HTML, xây dựng DOM. Script tải "ở chế độ background", và sau đó chạy khi DOM được xây dựng xong.

Đây là cùng ví dụ như trên, nhưng với `defer`:

```
<p>...nội dung trước script...</p>

<script defer src="https://javascript.info/article/script-async-defer/long.js?speed=1"></script>

<!-- hiển thị ngay lập tức -->
<p>...nội dung sau script...</p>
```

Nói cách khác:

- Scripts có `defer` không bao giờ chặn trang.
- Scripts có `defer` luôn thực thi khi DOM đã sẵn sàng (nhưng trước sự kiện `DOMContentLoaded`).

Ví dụ sau minh họa phần thứ hai:

```
<p>...nội dung trước scripts...</p>

<script>
  document.addEventListener('DOMContentLoaded', () => alert("DOM ready sau defer!"));
</script>

<script defer src="https://javascript.info/article/script-async-defer/long.js?speed=1"></script>

<p>...nội dung sau scripts...</p>
```

1. Nội dung trang hiển thị ngay lập tức.
2. Handler sự kiện `DOMContentLoaded` chờ script deferred. Nó chỉ kích hoạt khi script được tải và thực thi.

**Các script deferred giữ nguyên thứ tự tương đối của chúng, giống như các script thông thường.**

Giả sử chúng ta có hai script deferred: `long.js` rồi đến `small.js`:

```
<script defer src="https://javascript.info/article/script-async-defer/long.js"></script>
<script defer src="https://javascript.info/article/script-async-defer/small.js"></script>
```

Trình duyệt quét trang để tìm scripts và tải chúng song song, để cải thiện performance. Vậy trong ví dụ trên cả hai script tải song song. `small.js` có thể hoàn tất trước.

…Nhưng thuộc tính `defer`, bên cạnh việc báo trình duyệt "không chặn", đảm bảo thứ tự tương đối được giữ nguyên. Vậy mặc dù `small.js` tải trước, nó vẫn chờ và chạy sau khi `long.js` thực thi.

Điều đó có thể quan trọng trong các trường hợp khi chúng ta cần tải một thư viện JavaScript và sau đó là một script phụ thuộc vào nó.

Thuộc tính `defer` chỉ dành cho external scripts

Thuộc tính `defer` bị bỏ qua nếu thẻ `<script>` không có `src`.

## [async](#async)

Thuộc tính `async` tương tự như `defer`. Nó cũng làm cho script không chặn. Nhưng nó có các khác biệt quan trọng về behavior.

Thuộc tính `async` có nghĩa là script hoàn toàn độc lập:

- Trình duyệt không chặn trên các script `async` (giống như `defer`).
- Các script khác không chờ script `async`, và script `async` không chờ chúng.
- `DOMContentLoaded` và async scripts không chờ lẫn nhau:
  - `DOMContentLoaded` có thể xảy ra cả trước một async script (nếu một async script hoàn tất tải sau khi trang đã complete)
  - …hoặc sau một async script (nếu một async script ngắn hoặc đã trong HTTP-cache)

Nói cách khác, async scripts tải ở chế độ background và chạy khi sẵn sàng. DOM và các script khác không chờ chúng, và chúng không chờ bất cứ thứ gì. Một script hoàn toàn độc lập chạy khi được tải. Đơn giản vậy thôi, phải không?

Đây là một ví dụ tương tự những gì chúng ta đã thấy với `defer`: hai script `long.js` và `small.js`, nhưng giờ dùng `async` thay vì `defer`.

Chúng không chờ lẫn nhau. whatever tải trước (có thể là `small.js`) – chạy trước:

```
<p>...nội dung trước scripts...</p>

<script>
  document.addEventListener('DOMContentLoaded', () => alert("DOM ready!"));
</script>

<script async src="https://javascript.info/article/script-async-defer/long.js"></script>
<script async src="https://javascript.info/article/script-async-defer/small.js"></script>

<p>...nội dung sau scripts...</p>
```

- Nội dung trang hiển thị ngay lập tức: `async` không chặn nó.
- `DOMContentLoaded` có thể xảy ra cả trước và sau `async`, không có guarantee ở đây.
- Script nhỏ hơn `small.js` đứng thứ hai, nhưng có thể tải trước `long.js`, nên `small.js` chạy trước. Mặc dù, cũng có thể `long.js` tải trước nếu được cache, thì nó chạy trước. Nói cách khác, async scripts chạy theo thứ tự "tải trước – chạy trước".

Async scripts tuyệt vời khi chúng ta tích hợp một script third-party độc lập vào trang: counters, ads, và các thứ tương tự, vì chúng không phụ thuộc vào scripts của chúng ta, và scripts của chúng ta không nên chờ chúng:

```
<!-- Google Analytics thường được thêm như thế này -->
<script async src="https://google-analytics.com/analytics.js"></script>
```

Thuộc tính `async` chỉ dành cho external scripts

Giống như `defer`, thuộc tính `async` bị bỏ qua nếu thẻ `<script>` không có `src`.

## [Dynamic scripts](#dynamic-scripts)

Có một cách quan trọng khác để thêm script vào trang.

Chúng ta có thể tạo một script và append nó vào document động bằng JavaScript:

```
let script = document.createElement('script');
script.src = "/article/script-async-defer/long.js";
document.body.append(script); // (*)
```

Script bắt đầu tải ngay khi nó được append vào document `(*)`.

**Dynamic scripts hoạt động như "async" theo mặc định.**

Điều đó có nghĩa:

- Chúng không chờ gì cả, không gì chờ chúng.
- Script tải trước – chạy trước (thứ tự "load-first").

Điều này có thể thay đổi nếu chúng ta rõ ràng đặt `script.async=false`. Khi đó các script sẽ được thực thi theo thứ tự document, giống như `defer`.

Trong ví dụ này, hàm `loadScript(src)` thêm một script và cũng đặt `async` thành `false`.

Vậy `long.js` luôn chạy trước (vì nó được thêm trước):

```
function loadScript(src) {
  let script = document.createElement('script');
  script.src = src;
  script.async = false;
  document.body.append(script);
}

// long.js chạy đầu tiên vì async=false
loadScript("/article/script-async-defer/long.js");
loadScript("/article/script-async-defer/small.js");
```

Không có `script.async=false`, các script sẽ thực thi theo thứ tự mặc định, load-first (có thể là `small.js` trước).

Một lần nữa, giống như với `defer`, thứ tự quan trọng nếu chúng ta muốn tải một thư viện và sau đó là một script khác phụ thuộc vào nó.

## [Tóm tắt](#summary)

Cả `async` và `defer` có một điểm chung: việc tải các script như vậy không chặn rendering trang. Vậy người dùng có thể đọc nội dung trang và làm quen với trang ngay lập tức.

Nhưng cũng có những khác biệt quan trọng giữa chúng:

|  | Thứ tự | `DOMContentLoaded` |
| --- | --- | --- |
| `async` | *Thứ tự load-first*. Thứ tự document của chúng không quan trọng – cái nào tải trước chạy trước | Không liên quan. Có thể tải và thực thi trong khi document chưa được tải xong. Điều đó xảy ra nếu scripts nhỏ hoặc được cache, và document đủ dài. |
| `defer` | *Thứ tự document* (theo thứ tự chúng xuất hiện trong document). | Thực thi sau khi document được tải và parse xong (chúng chờ nếu cần), ngay trước `DOMContentLoaded`. |

Thực tế, `defer` được dùng cho các script cần toàn bộ DOM và/hoặc thứ tự thực thi tương đối của chúng quan trọng.

Và `async` được dùng cho các script độc lập, như counters hoặc ads. Và thứ tự thực thi tương đối của chúng không quan trọng.

Trang không có scripts nên hoạt động được

Xin lưu ý: nếu bạn đang dùng `defer` hoặc `async`, thì người dùng sẽ thấy trang *trước* khi script tải.

Trong trường hợp đó, một số components đồ họa có thể chưa được khởi tạo.

Đừng quên đặt chỉ báo "đang tải" và vô hiệu hóa các nút chưa hoạt động. Hãy để người dùng rõ ràng thấy những gì họ có thể làm trên trang, và những gì vẫn đang sẵn sàng.
