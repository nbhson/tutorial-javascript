# Xử lý lỗi với promises

> Nguồn: [https://javascript.info/promise-error-handling](https://javascript.info/promise-error-handling)

<!-- fetched: 2026-09-14 -->

Chuỗi promises rất giỏi trong việc xử lý lỗi. Khi một promise reject, điều khiển nhảy đến handler rejection gần nhất. Điều đó rất tiện lợi trong thực tế.

Ví dụ, trong mã dưới đây URL để `fetch` bị sai (không có trang web đó) và `.catch` xử lý lỗi:

```
fetch('https://no-such-server.blabla') // rejects
  .then(response => response.json())
  .catch(err => alert(err)) // TypeError: failed to fetch (văn bản có thể khác)
```

Như bạn có thể thấy, `.catch` không cần phải xuất hiện ngay lập tức. Nó có thể xuất hiện sau một hoặc có lẽ nhiều `.then`.

Hoặc, có thể mọi thứ đều ổn với trang web, nhưng response không phải là JSON hợp lệ. Cách dễ nhất để bắt tất cả lỗi là thêm `.catch` vào cuối chuỗi:

```
fetch('/article/promise-chaining/user.json')
  .then(response => response.json())
  .then(user => fetch(`https://api.github.com/users/${user.name}`))
  .then(response => response.json())
  .then(githubUser => new Promise((resolve, reject) => {
    let img = document.createElement('img');
    img.src = githubUser.avatar_url;
    img.className = "promise-avatar-example";
    document.body.append(img);

    setTimeout(() => {
      img.remove();
      resolve(githubUser);
    }, 3000);
  }))
  .catch(error => alert(error.message));
```

Thông thường, `.catch` như vậy không kích hoạt ở tất cả. Nhưng nếu bất kỳ promise nào trong số đó reject (vấn đề mạng hoặc json không hợp lệ hoặc bất kỳ điều gì), thì nó sẽ bắt lỗi.

## [Implicit try…catch](#implicit-try-catch)

Mã của executor promise và các handler promise có một "implicit `try..catch`" bao quanh nó. Nếu một ngoại lệ xảy ra, nó được bắt và xử lý như một rejection.

Ví dụ, mã này:

```
new Promise((resolve, reject) => {
  throw new Error("Whoops!");
}).catch(alert); // Error: Whoops!
```

…Hoạt động chính xác giống như mã này:

```
new Promise((resolve, reject) => {
  reject(new Error("Whoops!"));
}).catch(alert); // Error: Whoops!
```

"implicit `try..catch`" bao quanh executor tự động bắt lỗi và chuyển nó thành promise rejected.

Điều này không chỉ xảy ra trong hàm executor, mà còn trong các handler của nó. Nếu chúng ta `throw` bên trong handler `.then`, đó có nghĩa là một promise rejected, vì vậy điều khiển nhảy đến handler lỗi gần nhất.

Dưới đây là một ví dụ:

```
new Promise((resolve, reject) => {
  resolve("ok");
}).then((result) => {
  throw new Error("Whoops!"); // rejects promise
}).catch(alert); // Error: Whoops!
```

Điều này xảy ra cho tất cả các lỗi, không chỉ những lỗi do câu lệnh `throw` gây ra. Ví dụ, một lỗi lập trình:

```
new Promise((resolve, reject) => {
  resolve("ok");
}).then((result) => {
  blabla(); // không có hàm như vậy
}).catch(alert); // ReferenceError: blabla is not defined
```

`.catch` cuối cùng không chỉ bắt các rejection rõ ràng, mà còn cả các lỗi tình cờ trong các handler ở trên.

## [Rethrowing](#rethrowing)

Như chúng ta đã nhận thấy, `.catch` ở cuối chuỗi giống với `try..catch`. Chúng ta có thể có bất kỳ số lượng handler `.then` nào, và sau đó sử dụng một `.catch` duy nhất ở cuối để xử lý lỗi trong tất cả chúng.

Trong `try..catch` thông thường, chúng ta có thể phân tích lỗi và có thể ném nó lại nếu không thể xử lý. Cùng một điều có thể được thực hiện cho promises.

Nếu chúng ta `throw` bên trong `.catch`, thì điều khiển đi đến handler lỗi gần nhất tiếp theo. Và nếu chúng ta xử lý lỗi và kết thúc bình thường, thì nó tiếp tục đến handler `.then` thành công gần nhất tiếp theo.

Trong ví dụ dưới đây, `.catch` đã xử lý lỗi thành công:

```
// execution: catch -> then
new Promise((resolve, reject) => {

  throw new Error("Whoops!");

}).catch(function(error) {

  alert("Lỗi đã được xử lý, tiếp tục bình thường");

}).then(() => alert("Handler thành công tiếp theo chạy"));
```

Ở đây khối `.catch` kết thúc bình thường. Vì vậy handler `.then` thành công tiếp theo được gọi.

Trong ví dụ dưới đây chúng ta thấy tình huống khác với `.catch`. Handler `(*)` bắt lỗi và chỉ không thể xử lý nó (ví dụ, nó chỉ biết cách xử lý `URIError`), vì vậy nó ném nó lại:

```
// execution: catch -> catch
new Promise((resolve, reject) => {

  throw new Error("Whoops!");

}).catch(function(error) { // (*)

  if (error instanceof URIError) {
    // xử lý nó
  } else {
    alert("Không thể xử lý lỗi như vậy");

    throw error; // ném lỗi này hoặc lỗi khác nhảy đến catch tiếp theo
  }

}).then(function() {
  /* không chạy ở đây */
}).catch(error => { // (**)

  alert(`Lỗi không xác định đã xảy ra: ${error}`);
  // không trả về gì => execution đi theo cách bình thường

});
```

Execution nhảy từ `.catch` đầu tiên `(*)` đến `.catch` tiếp theo `(**)` dọc theo chuỗi.

## [Unhandled rejections](#unhandled-rejections)

Điều gì xảy ra khi một lỗi không được xử lý? Ví dụ, chúng ta quên thêm `.catch` vào cuối chuỗi, như ở đây:

```
new Promise(function() {
  noSuchFunction(); // Lỗi ở đây (không có hàm như vậy)
})
  .then(() => {
    // các handler promise thành công, một hoặc nhiều
  }); // không có .catch ở cuối!
```

Trong trường hợp có lỗi, promise trở nên rejected, và execution nên nhảy đến handler rejection gần nhất. Nhưng không có handler nào. Vì vậy lỗi bị "bỏ quên". Không có mã để xử lý nó.

Trong thực tế, giống như với các lỗi không được xử lý thông thường trong mã, nó có nghĩa là có gì đó đã đi sai nghiêm trọng.

Điều gì xảy ra khi một lỗi thông thường xảy ra và không được bắt bởi `try..catch`? Script chết với một thông điệp trong console. Một điều tương tự xảy ra với promise rejections không được xử lý.

Engine JavaScript theo dõi các rejections như vậy và tạo ra một lỗi toàn cục trong trường hợp đó. Bạn có thể thấy nó trong console nếu bạn chạy ví dụ ở trên.

Trong trình duyệt, chúng ta có thể bắt các lỗi như vậy bằng cách sử dụng sự kiện `unhandledrejection`:

```
window.addEventListener('unhandledrejection', function(event) {
  // đối tượng event có hai thuộc tính đặc biệt:
  alert(event.promise); // [object Promise] - promise đã tạo ra lỗi
  alert(event.reason); // Error: Whoops! - đối tượng lỗi không được xử lý
});

new Promise(function() {
  throw new Error("Whoops!");
}); // không có catch để xử lý lỗi
```

Sự kiện là một phần của [HTML standard](https://html.spec.whatwg.org/multipage/webappapis.html#unhandled-promise-rejections).

Nếu một lỗi xảy ra, và không có `.catch`, handler `unhandledrejection` kích hoạt, và nhận được đối tượng `event` với thông tin về lỗi, vì vậy chúng ta có thể làm gì đó.

Thông thường các lỗi như vậy không thể khôi phục, vì vậy cách tốt nhất của chúng ta là thông báo cho user về vấn đề và có lẽ báo cáo sự cố cho server.

Trong các môi trường không phải trình duyệt như Node.js có các cách khác để theo dõi lỗi không được xử lý.

## [Tóm tắt](#summary)

- `.catch` xử lý lỗi trong tất cả các loại promises: будь nó là một lệnh gọi `reject()` hoặc một lỗi được throw trong handler.
- `.then` cũng bắt lỗi theo cách tương tự, nếu được cung cấp đối số thứ hai (là handler lỗi).
- Chúng ta nên đặt `.catch` chính xác ở những nơi chúng ta muốn xử lý lỗi và biết cách xử lý chúng. Handler nên phân tích lỗi (các class lỗi tùy chỉnh giúp) và ném lại các lỗi không biết (có lẽ đó là lỗi lập trình).
- Thật là ổn nếu không sử dụng `.catch` nói chung, nếu không có cách nào để khôi phục từ lỗi.
- Trong mọi trường hợp chúng ta nên có handler sự kiện `unhandledrejection` (đối với trình duyệt, và các bản sao cho các môi trường khác) để theo dõi các lỗi không được xử lý và thông báo cho user (và có lẽ server của chúng ta) về chúng, vì vậy ứng dụng của chúng ta không bao giờ "chết đột ngột".

---

---

## Bài tập

## [Các bài tập](#tasks)

### [Lỗi trong setTimeout](#error-in-settimeout)

Bạn nghĩ sao? `.catch` có kích hoạt không? Giải thích câu trả lời của bạn.

```
new Promise(function(resolve, reject) {
  setTimeout(() => {
    throw new Error("Whoops!");
  }, 1000);
}).catch(alert);
```

lời giải

Câu trả lời là: **không, nó sẽ không**:

```
new Promise(function(resolve, reject) {
  setTimeout(() => {
    throw new Error("Whoops!");
  }, 1000);
}).catch(alert);
```

Như đã nói trong chương, có một "implicit `try..catch`" bao quanh mã hàm. Vì vậy tất cả các lỗi synchronous đều được xử lý.

Nhưng ở đây lỗi được tạo ra không phải trong khi executor đang chạy, mà sau đó. Vì vậy promise không thể xử lý nó.
