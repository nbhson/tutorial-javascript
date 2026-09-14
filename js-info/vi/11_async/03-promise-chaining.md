# Chuỗi Promises

> Nguồn: [https://javascript.info/promise-chaining](https://javascript.info/promise-chaining)

<!-- fetched: 2026-09-14 -->

Hãy quay lại vấn đề được đề cập trong chương [Giới thiệu: callbacks](/callbacks): chúng ta có một chuỗi các tác vụ không đồng bộ cần được thực hiện nối tiếp — ví dụ, tải script. Làm thế nào để chúng ta mã hóa nó tốt?

Promises cung cấp một vài công thức để làm điều đó.

Trong chương này chúng ta sẽ tìm hiểu về chuỗi promises.

Nó trông như thế này:

```
new Promise(function(resolve, reject) {

  setTimeout(() => resolve(1), 1000); // (*)

}).then(function(result) { // (**)

  alert(result); // 1
  return result * 2;

}).then(function(result) { // (***)

  alert(result); // 2
  return result * 2;

}).then(function(result) {

  alert(result); // 4
  return result * 2;

});
```

Ý tưởng là kết quả được truyền qua chuỗi các handler `.then`.

Luồng ở đây là:

1. Promise ban đầu resolve sau 1 giây `(*)`,
2. Sau đó handler `.then` được gọi `(**)`, mà tự nó tạo ra một promise mới (được resolve với giá trị `2`).
3. `then` tiếp theo `(***)` nhận kết quả từ cái trước, xử lý nó (nhân đôi) và truyền nó đến handler tiếp theo.
4. …và cứ thế.

Khi kết quả được truyền dọc theo chuỗi các handler, chúng ta có thể thấy một chuỗi các cuộc gọi `alert`: `1` → `2` → `4`.

![](/article/promise-chaining/promise-then-chain.svg)

Toàn bộ mọi thứ hoạt động, vì mọi cuộc gọi đến `.then` đều trả về một promise mới, vì vậy chúng ta có thể gọi `.then` tiếp theo trên nó.

Khi một handler trả về một giá trị, nó trở thành kết quả của promise đó, vì vậy `.then` tiếp theo được gọi với nó.

**Một lỗi kinh điển của người mới: về mặt kỹ thuật chúng ta cũng có thể thêm nhiều `.then` vào một promise đơn. Đây không phải là chaining.**

Ví dụ:

```
let promise = new Promise(function(resolve, reject) {
  setTimeout(() => resolve(1), 1000);
});

promise.then(function(result) {
  alert(result); // 1
  return result * 2;
});

promise.then(function(result) {
  alert(result); // 1
  return result * 2;
});

promise.then(function(result) {
  alert(result); // 1
  return result * 2;
});
```

Những gì chúng ta làm ở đây chỉ là thêm nhiều handler vào một promise. Chúng không truyền kết quả cho nhau; thay vào đó chúng xử lý nó một cách độc lập.

Dưới đây là hình ảnh (so sánh nó với chaining ở trên):

![](/article/promise-chaining/promise-then-many.svg)

Tất cả `.then` trên cùng một promise đều nhận được cùng một kết quả – kết quả của promise đó. Vì vậy trong mã ở trên tất cả `alert` đều hiển thị cùng một: `1`.

Trong thực tế chúng ta hiếm khi cần nhiều handler cho một promise. Chaining được sử dụng thường xuyên hơn nhiều.

## [Returning promises](#returning-promises)

Một handler, được sử dụng trong `.then(handler)` có thể tạo và trả về một promise.

Trong trường hợp đó các handler tiếp theo sẽ chờ cho đến khi nó settled, và sau đó nhận kết quả của nó.

Ví dụ:

```
new Promise(function(resolve, reject) {

  setTimeout(() => resolve(1), 1000);

}).then(function(result) {

  alert(result); // 1

  return new Promise((resolve, reject) => { // (*)
    setTimeout(() => resolve(result * 2), 1000);
  });

}).then(function(result) { // (**)

  alert(result); // 2

  return new Promise((resolve, reject) => {
    setTimeout(() => resolve(result * 2), 1000);
  });

}).then(function(result) {

  alert(result); // 4

});
```

Ở đây `.then` đầu tiên hiển thị `1` và trả về `new Promise(…)` ở dòng `(*)`. Sau một giây nó resolve, và kết quả (đối số của `resolve`, ở đây là `result * 2`) được truyền đến handler của `.then` thứ hai. Handler đó nằm ở dòng `(**)`, nó hiển thị `2` và làm同じ的事情。

Vì vậy, đầu ra giống như trong ví dụ trước: 1 → 2 → 4, nhưng bây giờ với độ trễ 1 giây giữa các cuộc gọi `alert`.

Trả về promises cho phép chúng ta xây dựng chuỗi các hành động không đồng bộ.

## [Ví dụ: loadScript](#example-loadscript)

Hãy sử dụng tính năng này với `loadScript` đã được promisified, được định nghĩa trong [chương trước](/promise-basics#loadscript), để tải script từng cái một, theo thứ tự tuần tự:

```
loadScript("/article/promise-chaining/one.js")
  .then(function(script) {
    return loadScript("/article/promise-chaining/two.js");
  })
  .then(function(script) {
    return loadScript("/article/promise-chaining/three.js");
  })
  .then(function(script) {
    // sử dụng các hàm được khai báo trong scripts
    // để cho thấy rằng chúng thực sự đã được tải
    one();
    two();
    three();
  });
```

Mã này có thể được viết ngắn gọn hơn một chút với arrow functions:

```
loadScript("/article/promise-chaining/one.js")
  .then(script => loadScript("/article/promise-chaining/two.js"))
  .then(script => loadScript("/article/promise-chaining/three.js"))
  .then(script => {
    // scripts đã được tải, chúng ta có thể sử dụng các hàm được khai báo ở đó
    one();
    two();
    three();
  });
```

Ở đây mỗi cuộc gọi `loadScript` trả về một promise, và `.then` tiếp theo chạy khi nó resolve. Sau đó nó khởi động việc tải script tiếp theo. Vì vậy scripts được tải nối tiếp nhau.

Chúng ta có thể thêm nhiều hành động không đồng bộ hơn vào chuỗi. Xin lưu ý rằng mã vẫn "phẳng" — nó phát triển xuống, không sang phải. Không có dấu hiệu của "tháp thảm họa".

Về mặt kỹ thuật, chúng ta có thể thêm `.then` trực tiếp vào mỗi `loadScript`, như thế này:

```
loadScript("/article/promise-chaining/one.js").then(script1 => {
  loadScript("/article/promise-chaining/two.js").then(script2 => {
    loadScript("/article/promise-chaining/three.js").then(script3 => {
      // hàm này có quyền truy cập vào các biến script1, script2 và script3
      one();
      two();
      three();
    });
  });
});
```

Mã này làm giống nhau: tải 3 scripts theo thứ tự tuần tự. Nhưng nó "phát triển sang phải". Vì vậy chúng ta có cùng vấn đề như với callbacks.

Những người bắt đầu sử dụng promises đôi khi không biết về chaining, vì vậy họ viết nó theo cách này. Nói chung, chaining được ưa chuộng hơn.

Đôi khi cũng ổn để viết `.then` trực tiếp, vì hàm lồng nhau có quyền truy cập vào phạm vi bên ngoài. Trong ví dụ ở trên callback lồng nhau nhất có quyền truy cập vào tất cả các biến `script1`, `script2`, `script3`. Nhưng đó là ngoại lệ chứ không phải quy tắc.

Thenables

Để chính xác, một handler có thể không trả về chính xác một promise, mà là một đối tượng gọi là "thenable" — một đối tượng tùy ý có phương thức `.then`. Nó sẽ được xử lý giống như một promise.

Ý tưởng là các thư viện của bên thứ ba có thể thực hiện các đối tượng "tương thích promise" của riêng họ. Chúng có thể có một tập hợp các phương thức mở rộng, nhưng cũng tương thích với native promises, vì chúng thực hiện `.then`.

Dưới đây là một ví dụ về đối tượng thenable:

```
class Thenable {
  constructor(num) {
    this.num = num;
  }
  then(resolve, reject) {
    alert(resolve); // function() { native code }
    // resolve với this.num*2 sau 1 giây
    setTimeout(() => resolve(this.num * 2), 1000); // (**)
  }
}

new Promise(resolve => resolve(1))
  .then(result => {
    return new Thenable(result); // (*)
  })
  .then(alert); // hiển thị 2 sau 1000ms
```

JavaScript kiểm tra đối tượng được trả về bởi handler `.then` ở dòng `(*)`: nếu nó có một phương thức có thể gọi được tên là `then`, thì nó gọi phương thức đó cung cấp các hàm native `resolve`, `reject` như các đối số (tương tự như executor) và chờ cho đến khi một trong số chúng được gọi. Trong ví dụ ở trên `resolve(2)` được gọi sau 1 giây `(**)`. Sau đó kết quả được truyền tiếp xuống chuỗi.

Tính năng này cho phép chúng ta tích hợp các đối tượng tùy chỉnh với chuỗi promises mà không cần kế thừa từ `Promise`.

## [Ví dụ lớn hơn: fetch](#bigger-example-fetch)

Trong lập trình frontend, promises thường được sử dụng cho các yêu cầu mạng. Vì vậy hãy xem một ví dụ mở rộng về điều đó.

Chúng ta sẽ sử dụng phương thức [fetch](/fetch) để tải thông tin về user từ máy chủ từ xa. Nó có nhiều tham số tùy chọn được bao phủ trong [các chương riêng biệt](/fetch), nhưng cú pháp cơ bản khá đơn giản:

```
let promise = fetch(url);
```

Điều này thực hiện một yêu cầu mạng đến `url` và trả về một promise. Promise resolve với một đối tượng `response` khi máy chủ từ xa phản hồi với các header, nhưng *trước khi bản đầy đủ được tải xuống*.

Để đọc bản đầy đủ, chúng ta nên gọi phương thức `response.text()`: nó trả về một promise resolve khi văn bản đầy đủ được tải xuống từ máy chủ từ xa, với văn bản đó làm kết quả.

Mã dưới đây thực hiện yêu cầu đến `user.json` và tải văn bản của nó từ máy chủ:

```
fetch('/article/promise-chaining/user.json')
  // .then bên dưới chạy khi máy chủ từ xa phản hồi
  .then(function(response) {
    // response.text() trả về một promise mới resolve với văn bản phản hồi đầy đủ
    // khi nó tải xong
    return response.text();
  })
  .then(function(text) {
    // ...và đây là nội dung của file từ xa
    alert(text); // {"name": "iliakan", "isAdmin": true}
  });
```

Đối tượng `response` được trả về từ `fetch` cũng bao gồm phương thức `response.json()` đọc dữ liệu từ xa và phân tích nó dưới dạng JSON. Trong trường hợp của chúng ta điều đó thậm chí còn thuận tiện hơn, vì vậy hãy chuyển sang nó.

Chúng ta cũng sẽ sử dụng arrow functions để viết ngắn gọn:

```
// giống như ở trên, nhưng response.json() phân tích nội dung từ xa dưới dạng JSON
fetch('/article/promise-chaining/user.json')
  .then(response => response.json())
  .then(user => alert(user.name)); // iliakan, đã lấy được tên user
```

Bây giờ hãy làm gì đó với user đã tải.

Ví dụ, chúng ta có thể thực hiện một yêu cầu nữa đến GitHub, tải profile user và hiển thị avatar:

```
// Thực hiện yêu cầu cho user.json
fetch('/article/promise-chaining/user.json')
  // Tải nó dưới dạng json
  .then(response => response.json())
  // Thực hiện yêu cầu đến GitHub
  .then(user => fetch(`https://api.github.com/users/${user.name}`))
  // Tải response dưới dạng json
  .then(response => response.json())
  // Hiển thị ảnh avatar (githubUser.avatar_url) trong 3 giây (có thể animate nó)
  .then(githubUser => {
    let img = document.createElement('img');
    img.src = githubUser.avatar_url;
    img.className = "promise-avatar-example";
    document.body.append(img);

    setTimeout(() => img.remove(), 3000); // (*)
  });
```

Mã hoạt động; xem comments về chi tiết. Tuy nhiên, có một vấn đề tiềm ẩn trong nó, một lỗi điển hình cho những người bắt đầu sử dụng promises.

Hãy nhìn vào dòng `(*)`: làm thế nào để chúng ta làm gì đó *sau* khi avatar đã hoàn thành hiển thị và bị xóa? Ví dụ, chúng ta muốn hiển thị một biểu mẫu để chỉnh sửa user đó hoặc một thứ gì khác. Cho đến nay, không có cách nào.

Để làm cho chuỗi có thể mở rộng, chúng ta cần trả về một promise resolve khi avatar hoàn thành hiển thị.

Như thế này:

```
fetch('/article/promise-chaining/user.json')
  .then(response => response.json())
  .then(user => fetch(`https://api.github.com/users/${user.name}`))
  .then(response => response.json())
  .then(githubUser => new Promise(function(resolve, reject) { // (*)
    let img = document.createElement('img');
    img.src = githubUser.avatar_url;
    img.className = "promise-avatar-example";
    document.body.append(img);

    setTimeout(() => {
      img.remove();
      resolve(githubUser); // (**)
    }, 3000);
  }))
  // kích hoạt sau 3 giây
  .then(githubUser => alert(`Hoàn thành hiển thị ${githubUser.name}`));
```

Tức là, handler `.then` ở dòng `(*)` bây giờ trả về `new Promise`, mà chỉ settled sau khi gọi `resolve(githubUser)` trong `setTimeout` `(**)`. `.then` tiếp theo trong chuỗi sẽ chờ đợi điều đó.

Như một practice tốt, một hành động không đồng bộ nên luôn trả về một promise. Điều đó làm cho các hành động sau nó có thể được lên kế hoạch; ngay cả khi chúng ta không lên kế hoạch mở rộng chuỗi bây giờ, chúng ta có thể cần nó sau này.

Cuối cùng, chúng ta có thể tách mã thành các hàm có thể tái sử dụng:

```
function loadJson(url) {
  return fetch(url)
    .then(response => response.json());
}

function loadGithubUser(name) {
  return loadJson(`https://api.github.com/users/${name}`);
}

function showAvatar(githubUser) {
  return new Promise(function(resolve, reject) {
    let img = document.createElement('img');
    img.src = githubUser.avatar_url;
    img.className = "promise-avatar-example";
    document.body.append(img);

    setTimeout(() => {
      img.remove();
      resolve(githubUser);
    }, 3000);
  });
}

// Sử dụng chúng:
loadJson('/article/promise-chaining/user.json')
  .then(user => loadGithubUser(user.name))
  .then(showAvatar)
  .then(githubUser => alert(`Hoàn thành hiển thị ${githubUser.name}`));
  // ...
```

## [Tóm tắt](#summary)

Nếu handler `.then` (hoặc `catch/finally`, không quan trọng) trả về một promise, phần còn lại của chuỗi sẽ chờ cho đến khi nó settled. Khi nó làm vậy, kết quả của nó (hoặc lỗi) được truyền tiếp.

Dưới đây là bức tranh đầy đủ:

![](/article/promise-chaining/promise-handler-variants.svg)

---

---

## Bài tập

## [Các bài tập](#tasks)

### [Promise: then versus catch](#promise-then-versus-catch)

Các fragment mã này có bằng nhau không? Nói cách khác, chúng có hành xử giống nhau trong mọi hoàn cảnh, cho bất kỳ hàm handler nào?

```
promise.then(f1).catch(f2);
```

So với:

```
promise.then(f1, f2);
```

lời giải

Câu trả lời ngắn gọn là: **không, chúng không bằng nhau**:

Sự khác biệt là nếu một lỗi xảy ra trong `f1`, thì nó được xử lý bởi `.catch` ở đây:

```
promise
  .then(f1)
  .catch(f2);
```

…Nhưng không ở đây:

```
promise
  .then(f1, f2);
```

Đó là vì một lỗi được truyền dọc theo chuỗi, và trong đoạn mã thứ hai không có chuỗi bên dưới `f1`.

Nói cách khác, `.then` truyền kết quả/lỗi đến `.then/catch` tiếp theo. Vì vậy trong ví dụ đầu tiên, có một `catch` bên dưới, và trong ví dụ thứ hai không có, vì vậy lỗi không được xử lý.
