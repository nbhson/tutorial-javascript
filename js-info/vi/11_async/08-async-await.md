# Async/await

> Nguồn: [https://javascript.info/async-await](https://javascript.info/async-await)

<!-- fetched: 2026-09-14 -->

Có một cú pháp đặc biệt để làm việc với promises theo cách thoải mái hơn, được gọi là "async/await". Nó rất dễ hiểu và sử dụng.

## [Async functions](#async-functions)

Hãy bắt đầu với từ khóa `async`. Nó có thể được đặt trước một hàm, như thế này:

```
async function f() {
  return 1;
}
```

Từ "async" trước một hàm có nghĩa một thứ đơn giản: một hàm luôn trả về một promise. Các giá trị khác được gói gọn trong một promise đã resolved tự động.

Ví dụ, hàm này trả về một promise đã resolved với kết quả của `1`; hãy kiểm tra nó:

```
async function f() {
  return 1;
}

f().then(alert); // 1
```

…Chúng ta có thể explicitly return một promise, điều đó sẽ giống nhau:

```
async function f() {
  return Promise.resolve(1);
}

f().then(alert); // 1
```

Vì vậy, `async` đảm bảo rằng hàm trả về một promise, và gói các non-promise trong đó. Đơn giản đủ, phải không? Nhưng không chỉ có vậy. Có một từ khóa khác, `await`, chỉ hoạt động bên trong các hàm `async`, và nó rất tuyệt.

## [Await](#await)

Cú pháp:

```
// chỉ hoạt động bên trong các hàm async
let value = await promise;
```

Từ khóa `await` làm cho JavaScript chờ cho đến khi promise settle và trả về kết quả của nó.

Dưới đây là một ví dụ với một promise resolve sau 1 giây:

```
async function f() {

  let promise = new Promise((resolve, reject) => {
    setTimeout(() => resolve("done!"), 1000)
  });

  let result = await promise; // chờ cho đến khi promise resolve (*)

  alert(result); // "done!"
}

f();
```

Execution của hàm "dừng lại" ở dòng `(*)` và tiếp tục khi promise settle, với `result` trở thành kết quả của nó. Vì vậy mã ở trên hiển thị "done!" trong một giây.

Hãy nhấn mạnh: `await` về mặt ngữ nghĩa làm tạm dừng execution của hàm cho đến khi promise settle, và sau đó tiếp tục nó với kết quả promise. Điều đó không tiêu tốn bất kỳ tài nguyên CPU nào, vì engine JavaScript có thể làm các công việc khác trong thời gian đó: thực thi các script khác, xử lý events, v.v.

Nó chỉ là một cú pháp thanh lịch hơn để nhận kết quả promise so với `promise.then`. Và, dễ đọc và viết hơn.

Không thể sử dụng `await` trong các hàm thông thường

Nếu chúng ta cố gắng sử dụng `await` trong một hàm không phải async, sẽ có một syntax error:

```
function f() {
  let promise = Promise.resolve(1);
  let result = await promise; // Syntax error
}
```

Chúng ta có thể nhận được lỗi này nếu chúng ta quên đặt `async` trước một hàm. Như đã nêu trước đó, `await` chỉ hoạt động bên trong một hàm `async`.

Hãy lấy ví dụ `showAvatar()` từ chương [Chuỗi Promises](/promise-chaining) và viết lại nó bằng cách sử dụng `async/await`:

1. Chúng ta sẽ cần thay thế các cuộc gọi `.then` với `await`.
2. Cũng nên làm cho hàm `async` để chúng hoạt động.

```
async function showAvatar() {

  // đọc JSON của chúng ta
  let response = await fetch('/article/promise-chaining/user.json');
  let user = await response.json();

  // đọc github user
  let githubResponse = await fetch(`https://api.github.com/users/${user.name}`);
  let githubUser = await githubResponse.json();

  // hiển thị avatar
  let img = document.createElement('img');
  img.src = githubUser.avatar_url;
  img.className = "promise-avatar-example";
  document.body.append(img);

  // chờ 3 giây
  await new Promise((resolve, reject) => setTimeout(resolve, 3000));

  img.remove();

  return githubUser;
}

showAvatar();
```

Rất sạch và dễ đọc, phải không? Tốt hơn nhiều so với trước đây.

Trình duyệt hiện đại cho phép top-level `await` trong modules

Trong các trình duyệt hiện đại, `await` ở top level hoạt động tốt, khi chúng ta đang ở bên trong một module. Chúng ta sẽ đề cập đến modules trong bài viết [Modules, introduction](/modules-intro).

Ví dụ:

```
// chúng ta giả sử mã này chạy ở top level, bên trong một module
let response = await fetch('/article/promise-chaining/user.json');
let user = await response.json();

console.log(user);
```

Nếu chúng ta không sử dụng modules, hoặc phải hỗ trợ [các trình duyệt cũ](https://caniuse.com/mdn-javascript_operators_await_top_level), có một công thức phổ quát: gói vào một anonymous async function.

Như thế này:

```
(async () => {
  let response = await fetch('/article/promise-chaining/user.json');
  let user = await response.json();
  ...
})();
```

`await` chấp nhận "thenables"

Giống như `promise.then`, `await` cho phép chúng ta sử dụng các đối tượng thenable (những cái có phương thức `then` có thể gọi được). Ý tưởng là một đối tượng của bên thứ ba có thể không phải là promise, nhưng tương thích promise: nếu nó hỗ trợ `.then`, điều đó là đủ để sử dụng nó với `await`.

Dưới đây là một lớp `Thenable` demo; `await` bên dưới chấp nhận các instances của nó:

```
class Thenable {
  constructor(num) {
    this.num = num;
  }
  then(resolve, reject) {
    alert(resolve);
    // resolve với this.num*2 sau 1000ms
    setTimeout(() => resolve(this.num * 2), 1000); // (*)
  }
}

async function f() {
  // chờ 1 giây, sau đó result trở thành 2
  let result = await new Thenable(1);
  alert(result);
}

f();
```

Nếu `await` nhận được một đối tượng non-promise với `.then`, nó gọi phương thức đó cung cấp các hàm tích hợp `resolve` và `reject` như các đối số (giống như nó làm cho executor `Promise` thông thường). Sau đó `await` chờ cho đến khi một trong số chúng được gọi (trong ví dụ ở trên nó xảy ra ở dòng `(*)`) và sau đó tiếp tục với kết quả.

Async class methods

Để khai báo một async class method, chỉ cần thêm `async` trước nó:

```
class Waiter {
  async wait() {
    return await Promise.resolve(1);
  }
}

new Waiter()
  .wait()
  .then(alert); // 1 (điều này giống như (result => alert(result)))
```

Ý nghĩa là giống nhau: nó đảm bảo rằng giá trị trả về là một promise và kích hoạt `await`.

## [Xử lý lỗi](#error-handling)

Nếu một promise resolve bình thường, thì `await promise` trả về kết quả. Nhưng trong trường hợp rejection, nó ném lỗi, giống như nếu có một câu lệnh `throw` ở dòng đó.

Mã này:

```
async function f() {
  await Promise.reject(new Error("Whoops!"));
}
```

…Giống như mã này:

```
async function f() {
  throw new Error("Whoops!");
}
```

Trong các tình huống thực tế, promise có thể mất một số thời gian trước khi nó reject. Trong trường hợp đó sẽ có một độ trễ trước khi `await` ném lỗi.

Chúng ta có thể bắt lỗi đó bằng cách sử dụng `try..catch`, giống như một `throw` thông thường:

```
async function f() {

  try {
    let response = await fetch('http://no-such-url');
  } catch(err) {
    alert(err); // TypeError: failed to fetch
  }
}

f();
```

Trong trường hợp có lỗi, điều khiển nhảy đến khối `catch`. Chúng ta cũng có thể gói nhiều dòng:

```
async function f() {

  try {
    let response = await fetch('/no-user-here');
    let user = await response.json();
  } catch(err) {
    // bắt lỗi cả trong fetch và response.json
    alert(err);
  }
}

f();
```

Nếu chúng ta không có `try..catch`, thì promise được tạo bởi cuộc gọi của hàm async `f()` sẽ trở nên rejected. Chúng ta có thể thêm `.catch` để xử lý nó:

```
async function f() {
  let response = await fetch('http://no-such-url');
}

// f() trở thành một promise rejected
f().catch(alert); // TypeError: failed to fetch // (*)
```

Nếu chúng ta quên thêm `.catch` ở đó, thì chúng ta nhận được một lỗi promise không được xử lý (có thể xem trong console). Chúng ta có thể bắt các lỗi như vậy bằng cách sử dụng handler sự kiện toàn cục `unhandledrejection` như được mô tả trong chương [Xử lý lỗi với promises](/promise-error-handling).

`async/await` và `promise.then/catch`

Khi chúng ta sử dụng `async/await`, chúng ta hiếm khi cần `.then`, vì `await` xử lý việc chờ đợi cho chúng ta. Và chúng ta có thể sử dụng `try..catch` thông thường thay vì `.catch`. Điều đó thường (nhưng không phải lúc nào) thuận tiện hơn.

Nhưng ở top level của mã, khi chúng ta đang ngoài bất kỳ hàm `async` nào, chúng ta không thể sử dụng `await` về mặt cú pháp, vì vậy đó là một practice thông thường để thêm `.then/catch` để xử lý kết quả cuối cùng hoặc lỗi tràn, như trong dòng `(*)` của ví dụ ở trên.

`async/await` hoạt động tốt với `Promise.all`

Khi chúng ta cần chờ nhiều promise, chúng ta có thể gói chúng trong `Promise.all` và sau đó `await`:

```
// chờ mảng kết quả
let results = await Promise.all([
  fetch(url1),
  fetch(url2),
  ...
]);
```

Trong trường hợp có lỗi, nó được propagate như thông thường, từ promise thất bại đến `Promise.all`, và sau đó trở thành exception mà chúng ta có thể bắt bằng cách sử dụng `try..catch` xung quanh cuộc gọi.

## [Tóm tắt](#summary)

Từ khóa `async` trước một hàm có hai tác dụng:

1. Làm cho nó luôn trả về một promise.
2. Cho phép `await` được sử dụng trong nó.

Từ khóa `await` trước một promise làm cho JavaScript chờ cho đến khi promise settle, và sau đó:

1. Nếu đó là lỗi, một exception được tạo — giống như nếu `throw error` được gọi tại chỗ đó.
2. Nếu không, nó trả về kết quả.

Kết hợp với nhau chúng cung cấp một framework tuyệt vời để viết mã không đồng bộ dễ đọc và viết.

Với `async/await` chúng ta hiếm khi cần viết `promise.then/catch`, nhưng chúng ta vẫn không nên quên rằng chúng dựa trên promises, vì đôi khi (ví dụ trong outermost scope) chúng ta phải sử dụng các methods này. Cũng `Promise.all` rất hữu ích khi chúng ta chờ nhiều task cùng lúc.

---

---

## Bài tập

## [Các bài tập](#tasks)

### [Viết lại bằng async/await](#rewrite-using-async-await)

Viết lại mã ví dụ từ chương [Chuỗi Promises](/promise-chaining) bằng cách sử dụng `async/await` thay vì `.then/catch`:

```
function loadJson(url) {
  return fetch(url)
    .then(response => {
      if (response.status == 200) {
        return response.json();
      } else {
        throw new Error(response.status);
      }
    });
}

loadJson('https://javascript.info/no-such-user.json')
  .catch(alert); // Error: 404
```

lời giải

Các ghi chú ở dưới mã:

```
async function loadJson(url) { // (1)
  let response = await fetch(url); // (2)

  if (response.status == 200) {
    let json = await response.json(); // (3)
    return json;
  }

  throw new Error(response.status);
}

loadJson('https://javascript.info/no-such-user.json')
  .catch(alert); // Error: 404 (4)
```

Ghi chú:

1. Hàm `loadJson` trở thành `async`.
2. Tất cả `.then` bên trong được thay thế bằng `await`.
3. Chúng ta có thể `return response.json()` thay vì awaiting cho nó, như thế này:

   ```
   if (response.status == 200) {
     return response.json(); // (3)
   }
   ```

   Sau đó mã bên ngoài sẽ phải `await` cho promise đó resolve. Trong trường hợp của chúng ta nó không quan trọng.
4. Lỗi được throw từ `loadJson` được xử lý bởi `.catch`. Chúng ta không thể sử dụng `await loadJson(…)`) ở đó, vì chúng ta không ở trong một hàm `async`.

### [Viết lại "rethrow" bằng async/await](#rewrite-rethrow-with-async-await)

Dưới đây bạn có thể tìm thấy ví dụ "rethrow". Viết lại nó bằng cách sử dụng `async/await` thay vì `.then/catch`.

Và loại bỏ đệ quy thay thế bằng một loop trong `demoGithubUser`: với `async/await` điều đó trở nên dễ dàng.

```
class HttpError extends Error {
  constructor(response) {
    super(`${response.status} for ${response.url}`);
    this.name = 'HttpError';
    this.response = response;
  }
}

function loadJson(url) {
  return fetch(url)
    .then(response => {
      if (response.status == 200) {
        return response.json();
      } else {
        throw new HttpError(response);
      }
    });
}

// Hỏi tên user cho đến khi github trả về một user hợp lệ
function demoGithubUser() {
  let name = prompt("Nhập tên?", "iliakan");

  return loadJson(`https://api.github.com/users/${name}`)
    .then(user => {
      alert(`Tên đầy đủ: ${user.name}.`);
      return user;
    })
    .catch(err => {
      if (err instanceof HttpError && err.response.status == 404) {
        alert("Không có user này, vui lòng nhập lại.");
        return demoGithubUser();
      } else {
        throw err;
      }
    });
}

demoGithubUser();
```

lời giải

Không có mẹo gì ở đây. Chỉ cần thay thế `.catch` bằng `try..catch` bên trong `demoGithubUser` và thêm `async/await` nơi cần thiết:

```
class HttpError extends Error {
  constructor(response) {
    super(`${response.status} for ${response.url}`);
    this.name = 'HttpError';
    this.response = response;
  }
}

async function loadJson(url) {
  let response = await fetch(url);
  if (response.status == 200) {
    return response.json();
  } else {
    throw new HttpError(response);
  }
}

// Hỏi tên user cho đến khi github trả về một user hợp lệ
async function demoGithubUser() {

  let user;
  while(true) {
    let name = prompt("Nhập tên?", "iliakan");

    try {
      user = await loadJson(`https://api.github.com/users/${name}`);
      break; // không có lỗi, thoát khỏi loop
    } catch(err) {
      if (err instanceof HttpError && err.response.status == 404) {
        // loop tiếp tục sau alert
        alert("Không có user này, vui lòng nhập lại.");
      } else {
        // lỗi không xác định, ném lại
        throw err;
      }
    }
  }

  alert(`Tên đầy đủ: ${user.name}.`);
  return user;
}

demoGithubUser();
```

### [Gọi async từ non-async](#call-async-from-non-async)

Chúng ta có một hàm "thông thường" được gọi là `f`. Bạn có thể gọi hàm `async wait()` và sử dụng kết quả của nó bên trong `f` như thế nào?

```
async function wait() {
  await new Promise(resolve => setTimeout(resolve, 1000));

  return 10;
}

function f() {
  // ...bạn nên viết gì ở đây?
  // chúng ta cần gọi async wait() và chờ để nhận 10
  // nhớ rằng, chúng ta không thể sử dụng "await"
}
```

P.S. Bài tập về mặt kỹ thuật rất đơn giản, nhưng câu hỏi khá phổ biến cho các nhà phát triển mới với async/await.

lời giải

Đó là trường hợp khi biết cách nó hoạt động bên trong là hữu ích.

Chỉ cần xử lý cuộc gọi `async` như promise và attach `.then` vào nó:

```
async function wait() {
  await new Promise(resolve => setTimeout(resolve, 1000));

  return 10;
}

function f() {
  // hiển thị 10 sau 1 giây
  wait().then(result => alert(result));
}

f();
```

### [Dangerous Promise.all](#dangerous-promise-all)

`Promise.all` là một cách tuyệt vời để parallelize nhiều hoạt động. Nó đặc biệt hữu ích khi chúng ta cần thực hiện các yêu cầu song song đến nhiều dịch vụ.

Tuy nhiên, có một nguy hiểm ẩn giấu. Chúng ta sẽ xem một ví dụ trong bài tập này và khám phá cách tránh nó.

Giả sử chúng ta có một kết nối đến một dịch vụ từ xa, chẳng hạn như cơ sở dữ liệu.

Có hai hàm: `connect()` và `disconnect()`.

Khi đã kết nối, chúng ta có thể gửi các yêu cầu bằng cách sử dụng `database.query(...)` — một async function thường trả về kết quả nhưng cũng có thể ném lỗi.

Dưới đây là một implementation đơn giản:

```
let database;

function connect() {
  database = {
    async query(isOk) {
      if (!isOk) throw new Error('Query failed');
    }
  };
}

function disconnect() {
  database = null;
}

// intended usage:
// connect()
// ...
// database.query(true) để mô phỏng một cuộc gọi thành công
// database.query(false) để mô phỏng một cuộc gọi thất bại
// ...
// disconnect()
```

Bây giờ đây là vấn đề.

Chúng ta đã viết mã để kết nối và gửi 3 queries song song (tất cả đều mất thời gian khác nhau, ví dụ 100, 200 và 300ms), sau đó disconnect:

```
// Helper function để gọi async function `fn` sau `ms` milliseconds
function delay(fn, ms) {
  return new Promise((resolve, reject) => {
    setTimeout(() => fn().then(resolve, reject), ms);
  });
}

async function run() {
  connect();

  try {
    await Promise.all([
      // 3 jobs song song này mất thời gian khác nhau: 100, 200 và 300 ms
      // chúng ta sử dụng helper `delay` để đạt được hiệu ứng này
      delay(() => database.query(true), 100),
      delay(() => database.query(false), 200),
      delay(() => database.query(false), 300)
    ]);
  } catch(error) {
    console.log('Lỗi đã được xử lý (hay là vậy?)');
  }

  disconnect();
}

run();
```

Hai trong số các queries này không thành công, nhưng chúng ta đủ thông minh để gói cuộc gọi `Promise.all` vào một khối `try..catch`.

Tuy nhiên, điều đó không giúp gì! Script này thực sự dẫn đến một lỗi không được catch trong console!

Tại sao? Làm thế nào để tránh nó?

lời giải

Gốc rễ của vấn đề là `Promise.all` ngay lập tức reject khi một trong các promise của nó reject, nhưng nó không làm gì để hủy các promise khác.

Trong trường hợp của chúng ta, query thứ hai thất bại, vì vậy `Promise.all` reject, và khối `try...catch` bắt lỗi này.Trong khi đó, các promise khác *không bị ảnh hưởng* – chúng độc lập tiếp tục thực thi. Trong trường hợp của chúng ta, query thứ ba ném một lỗi của riêng nó sau một chút thời gian. Và lỗi đó không bao giờ được catch, chúng ta có thể thấy nó trong console.

Vấn đề đặc biệt nguy hiểm trong các môi trường server-side, chẳng hạn như Node.js, khi một lỗi không được catch có thể gây ra process crash.

Làm thế nào để sửa nó?

Một giải pháp lý tưởng sẽ là hủy tất cả các query chưa hoàn thành khi một trong số chúng thất bại. Cách này chúng ta tránh được bất kỳ lỗi tiềm ẩn nào.

Tuy nhiên, tin xấu là các service calls (như `database.query`) thường được thực hiện bởi một thư viện bên thứ ba không hỗ trợ cancellation. Sau đó không có cách nào để hủy một cuộc gọi.

Như một giải pháp thay thế, chúng ta có thể viết wrapper function của riêng chúng ta xung quanh `Promise.all` thêm một handler `then/catch` tùy chỉnh cho mỗi promise để theo dõi chúng: kết quả được thu thập và, nếu có lỗi xảy ra, tất cả các promise tiếp theo bị bỏ qua.

```
function customPromiseAll(promises) {
  return new Promise((resolve, reject) => {
    const results = [];
    let resultsCount = 0;
    let hasError = false; // chúng ta sẽ đặt nó thành true upon first error

    promises.forEach((promise, index) => {
      promise
        .then(result => {
          if (hasError) return; // bỏ qua promise nếu đã errored
          results[index] = result;
          resultsCount++;
          if (resultsCount === promises.length) {
            resolve(results); // khi tất cả kết quả sẵn sàng - success
          }
        })
        .catch(error => {
          if (hasError) return; // bỏ qua promise nếu đã errored
          hasError = true; // wops, lỗi!
          reject(error); // fail với rejection
        });
    });
  });
}
```

Cách tiếp cận này có một vấn đề của riêng nó – thường không mong muốn để `disconnect()` khi queries vẫn đang trong quá trình.

Có thể quan trọng là tất cả các queries hoàn thành, đặc biệt nếu một số trong số chúng thực hiện các cập nhật quan trọng.

Vì vậy chúng ta nên chờ cho đến khi tất cả các promise settle trước khi tiếp tục với execution và cuối cùng disconnect.

Dưới đây là một implementation khác. Nó hoạt động tương tự như `Promise.all` – cũng resolve với lỗi đầu tiên, nhưng chờ cho đến khi tất cả các promise settle.

```
function customPromiseAllWait(promises) {
  return new Promise((resolve, reject) => {
    const results = new Array(promises.length);
    let settledCount = 0;
    let firstError = null;

    promises.forEach((promise, index) => {
      Promise.resolve(promise)
        .then(result => {
          results[index] = result;
        })
        .catch(error => {
          if (firstError === null) {
            firstError = error;
          }
        })
        .finally(() => {
          settledCount++;
          if (settledCount === promises.length) {
            if (firstError !== null) {
              reject(firstError);
            } else {
              resolve(results);
            }
          }
        });
    });
  });
}
```

Bây giờ `await customPromiseAllWait(...)` sẽ stall execution cho đến khi tất cả queries được xử lý.

Đây là một cách tiếp cận đáng tin cậy hơn, vì nó đảm bảo một luồng execution dự đoán được.

Cuối cùng, nếu chúng ta muốn xử lý tất cả lỗi, chúng ta có thể sử dụng `Promise.allSettled` hoặc viết một wrapper xung quanh nó để thu thập tất cả lỗi trong một đối tượng [AggregateError](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/AggregateError) duy nhất và reject với nó.

```
// chờ tất cả promises settle
// trả về kết quả nếu không có lỗi
// throw AggregateError với tất cả lỗi nếu có bất kỳ
function allOrAggregateError(promises) {
  return Promise.allSettled(promises).then(results => {
    const errors = [];
    const values = [];

    results.forEach((res, i) => {
      if (res.status === 'fulfilled') {
        values[i] = res.value;
      } else {
        errors.push(res.reason);
      }
    });

    if (errors.length > 0) {
      throw new AggregateError(errors, 'One or more promises failed');
    }

    return values;
  });
}
```
