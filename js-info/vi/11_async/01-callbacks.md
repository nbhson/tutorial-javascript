# Giới thiệu: callbacks

> Nguồn: [https://javascript.info/callbacks](https://javascript.info/callbacks)

<!-- fetched: 2026-09-14 -->

Chúng ta sử dụng các phương thức trình duyệt trong các ví dụ ở đây

Để minh họa cách sử dụng callbacks, promises và các khái niệm trừu tượng khác, chúng ta sẽ sử dụng một số phương thức trình duyệt: cụ thể là tải script và thực hiện các thao tác đơn giản trên document.

Nếu bạn chưa quen với các phương thức này, và cách sử dụng chúng trong các ví dụ gây bối rối, bạn có thể muốn đọc một vài chương từ [phần tiếp theo](/document) của hướng dẫn.

Tuy nhiên, chúng ta sẽ cố gắng làm rõ mọi thứ. Sẽ không có gì phức tạp liên quan đến trình duyệt.

Nhiều hàm được cung cấp bởi môi trường JavaScript host cho phép bạn lập lịch *các hành động không đồng bộ*. Nói cách khác, là các hành động mà chúng ta khởi tạo ngay bây giờ, nhưng chúng sẽ hoàn thành sau đó.

Ví dụ, một trong những hàm như vậy là hàm `setTimeout`.

Có nhiều ví dụ khác về các hành động không đồng bộ trong thực tế, ví dụ như tải script và module (chúng ta sẽ đề cập đến chúng ở các chương sau).

Hãy xem xét hàm `loadScript(src)`, hàm tải một script với `src` đã cho:

```
function loadScript(src) {
  // tạo một thẻ <script> và thêm nó vào trang
  // điều này khiến script với src đã cho bắt đầu tải và chạy khi hoàn thành
  let script = document.createElement('script');
  script.src = src;
  document.head.append(script);
}
```

Hàm này chèn vào document một thẻ `<script src="…">` được tạo động với `src` đã cho. Trình duyệt tự động bắt đầu tải nó và thực thi khi hoàn thành.

Chúng ta có thể sử dụng hàm này như sau:

```
// tải và thực thi script tại đường dẫn đã cho
loadScript('/my/script.js');
```

Script được thực thi "theo cách không đồng bộ", vì nó bắt đầu tải ngay bây giờ, nhưng chạy sau đó, khi hàm đã kết thúc.

Nếu có bất kỳ mã nào bên dưới `loadScript(…)`, nó sẽ không chờ cho đến khi script tải xong.

```
loadScript('/my/script.js');
// mã bên dưới loadScript
// không chờ script tải xong
// ...
```

Giả sử chúng ta cần sử dụng script mới ngay khi nó tải xong. Nó khai báo các hàm mới, và chúng ta muốn chạy chúng.

Nhưng nếu chúng ta làm điều đó ngay sau khi gọi `loadScript(…)`, thì sẽ không hoạt động:

```
loadScript('/my/script.js'); // script có "function newFunction() {…}"

newFunction(); // không có hàm như vậy!
```

Tất nhiên, trình duyệt có thể chưa kịp tải script. Cho đến nay, hàm `loadScript` không cung cấp cách nào để theo dõi việc hoàn thành tải. Script tải và cuối cùng sẽ chạy, đó là tất cả. Nhưng chúng ta muốn biết khi nào điều đó xảy ra, để sử dụng các hàm và biến mới từ script đó.

Hãy thêm hàm `callback` là đối số thứ hai cho `loadScript` sẽ được thực thi khi script tải xong:

```
function loadScript(src, callback) {
  let script = document.createElement('script');
  script.src = src;

  script.onload = () => callback(script);

  document.head.append(script);
}
```

Sự kiện `onload` được mô tả trong bài viết [Resource loading: onload and onerror](/onload-onerror#loading-a-script), về cơ bản nó thực thi một hàm sau khi script được tải và thực thi.

Bây giờ nếu chúng ta muốn gọi các hàm mới từ script, chúng ta nên viết điều đó trong callback:

```
loadScript('/my/script.js', function() {
  // callback chạy sau khi script được tải
  newFunction(); // vì vậy bây giờ nó hoạt động
  ...
});
```

Đó là ý tưởng: đối số thứ hai là một hàm (thường là ẩn danh) chạy khi hành động hoàn thành.

Dưới đây là một ví dụ có thể chạy được với script thật:

```
function loadScript(src, callback) {
  let script = document.createElement('script');
  script.src = src;
  script.onload = () => callback(script);
  document.head.append(script);
}

loadScript('https://cdnjs.cloudflare.com/ajax/libs/lodash.js/3.2.0/lodash.js', script => {
  alert(`Cool, script ${script.src} đã được tải`);
  alert( _ ); // _ là hàm được khai báo trong script đã tải
});
```

Điều này được gọi là phong cách lập trình không đồng bộ "dựa trên callback". Một hàm thực hiện một việc gì đó không đồng bộ nên cung cấp đối số `callback` nơi chúng ta đặt hàm cần chạy sau khi hoàn thành.

Ở đây chúng ta đã làm điều đó trong `loadScript`, nhưng tất nhiên đó là một phương pháp chung.

## [Callback trong callback](#callback-in-callback)

Làm thế nào để tải hai script theo thứ tự tuần tự: cái này trước, rồi cái kia sau?

Giải pháp tự nhiên sẽ là đặt cuộc gọi `loadScript` thứ hai bên trong callback, như sau:

```
loadScript('/my/script.js', function(script) {

  alert(`Cool, ${script.src} đã được tải, hãy tải thêm một cái nữa`);

  loadScript('/my/script2.js', function(script) {
    alert(`Cool, script thứ hai đã được tải`);
  });

});
```

Sau khi `loadScript` bên ngoài hoàn thành, callback sẽ khởi tạo callback bên trong.

Giả sử chúng ta muốn thêm một script nữa…?

```
loadScript('/my/script.js', function(script) {

  loadScript('/my/script2.js', function(script) {

    loadScript('/my/script3.js', function(script) {
      // ...tiếp tục sau khi tất cả script được tải
    });

  });

});
```

Vì vậy, mỗi hành động mới nằm bên trong một callback. Điều đó ổn cho vài hành động, nhưng không tốt cho nhiều hành động, vì vậy chúng ta sẽ thấy các biến thể khác sớm.

## [Xử lý lỗi](#handling-errors)

Trong các ví dụ trên, chúng ta không xem xét lỗi. Nếu việc tải script thất bại thì sao? Callback của chúng ta nên có khả năng phản ứng với điều đó.

Dưới đây là phiên bản cải tiến của `loadScript` theo dõi lỗi tải:

```
function loadScript(src, callback) {
  let script = document.createElement('script');
  script.src = src;

  script.onload = () => callback(null, script);
  script.onerror = () => callback(new Error(`Lỗi tải script cho ${src}`));

  document.head.append(script);
}
```

Nó gọi `callback(null, script)` cho trường hợp tải thành công và `callback(error)` trong các trường hợp khác.

Cách sử dụng:

```
loadScript('/my/script.js', function(error, script) {
  if (error) {
    // xử lý lỗi
  } else {
    // script đã tải thành công
  }
});
```

Một lần nữa, công thức mà chúng ta đã sử dụng cho `loadScript` thực sự khá phổ biến. Nó được gọi là phong cách "error-first callback".

Quy ước là:

1. Đối số thứ nhất của `callback` được dành cho lỗi nếu nó xảy ra. Sau đó `callback(err)` được gọi.
2. Đối số thứ hai (và các đối số tiếp theo nếu cần) là cho kết quả thành công. Sau đó `callback(null, result1, result2…)` được gọi.

Vì vậy, hàm `callback` đơn được sử dụng cho cả việc báo cáo lỗi và truyền lại kết quả.

## [Pyramid of Doom (Tháp thảm họa)](#pyramid-of-doom)

Thoạt nhìn, nó có vẻ là một cách tiếp cận khả thi cho việc mã hóa không đồng bộ. Và đúng là như vậy. Đối với một hoặc có lẽ hai lệnh gọi lồng nhau, nó trông ổn.

Nhưng đối với nhiều hành động không đồng bộ xảy ra sau nhau, chúng ta sẽ có mã như thế này:

```
loadScript('1.js', function(error, script) {

  if (error) {
    handleError(error);
  } else {
    // ...
    loadScript('2.js', function(error, script) {
      if (error) {
        handleError(error);
      } else {
        // ...
        loadScript('3.js', function(error, script) {
          if (error) {
            handleError(error);
          } else {
            // ...tiếp tục sau khi tất cả script được tải (*)
          }
        });

      }
    });
  }
});
```

Trong mã ở trên:

1. Chúng ta tải `1.js`, sau đó nếu không có lỗi…
2. Chúng ta tải `2.js`, sau đó nếu không có lỗi…
3. Chúng ta tải `3.js`, sau đó nếu không có lỗi – làm điều gì đó khác `(*)`.

Khi các lệnh gọi trở nên lồng nhau hơn, mã trở nên sâu hơn và ngày càng khó quản lý hơn, đặc biệt nếu chúng ta có mã thực tế thay vì `...` có thể bao gồm nhiều vòng lặp, câu lệnh điều kiện và các thứ khác.

Điều đó đôi khi được gọi là "callback hell" (Địa ngục callback) hoặc "pyramid of doom" (Tháp thảm họa).

![](/article/callbacks/callback-hell.svg)

"Tháp" các lệnh gọi lồng nhau phát triển sang phải với mỗi hành động không đồng bộ.很快 nó sẽ xoắn ra khỏi tầm kiểm soát.

Vì vậy, cách mã hóa này không tốt lắm.

Chúng ta có thể cố gắng giảm bớt vấn đề bằng cách tạo mỗi hành động thành một hàm độc lập, như thế này:

```
loadScript('1.js', step1);

function step1(error, script) {
  if (error) {
    handleError(error);
  } else {
    // ...
    loadScript('2.js', step2);
  }
}

function step2(error, script) {
  if (error) {
    handleError(error);
  } else {
    // ...
    loadScript('3.js', step3);
  }
}

function step3(error, script) {
  if (error) {
    handleError(error);
  } else {
    // ...tiếp tục sau khi tất cả script được tải (*)
  }
}
```

Thấy không? Nó làm cùng một thứ, và không có lồng nhau sâu bây giờ vì chúng ta đã tạo mỗi hành động thành một hàm riêng biệt ở mức cao nhất.

Nó hoạt động, nhưng mã trông như một bảng tính bị xé toang. Khó đọc, và bạn có thể nhận thấy rằng người đọc cần phải nhảy mắt giữa các phần khi đọc nó. Điều đó bất tiện, đặc biệt nếu người đọc không quen với mã và không biết phải nhảy mắt đến đâu.

Ngoài ra, các hàm có tên `step*` 모두 được tạo chỉ để sử dụng một lần, chúng được tạo ra chỉ để tránh "tháp thảm họa". Không ai sẽ tái sử dụng chúng bên ngoài chuỗi hành động. Vì vậy, có một chút lộn xộn namespace ở đây.

Chúng ta muốn có thứ gì đó tốt hơn.

May mắn thay, có những cách khác để tránh các tháp như vậy. Một trong những cách tốt nhất là sử dụng "promises", được mô tả ở chương tiếp theo.
