# Promise API

> Nguồn: [https://javascript.info/promise-api](https://javascript.info/promise-api)

<!-- fetched: 2026-09-14 -->

Có 6 static methods trong class `Promise`. Chúng ta sẽ nhanh chóng đề cập đến các trường hợp sử dụng của chúng ở đây.

## [Promise.all](#promise-all)

Giả sử chúng ta muốn nhiều promise thực hiện song song và chờ đến khi tất cả chúng sẵn sàng.

Ví dụ, tải nhiều URL song song và xử lý nội dung một khi tất cả chúng đều xong.

Đó là mục đích của `Promise.all`.

Cú pháp là:

```
let promise = Promise.all(iterable);
```

`Promise.all` nhận một iterable (thường là một mảng các promise) và trả về một promise mới.

Promise mới resolve khi tất cả các promise được liệt kê được resolve, và mảng các kết quả của chúng trở thành kết quả của nó.

Ví dụ, `Promise.all` dưới đây settle sau 3 giây, và sau đó kết quả của nó là một mảng `[1, 2, 3]`:

```
Promise.all([
  new Promise(resolve => setTimeout(() => resolve(1), 3000)), // 1
  new Promise(resolve => setTimeout(() => resolve(2), 2000)), // 2
  new Promise(resolve => setTimeout(() => resolve(3), 1000))  // 3
]).then(alert); // 1,2,3 khi các promise sẵn sàng: mỗi promise đóng góp một thành viên mảng
```

Xin lưu ý rằng thứ tự của các thành viên mảng kết quả giống như trong các promise nguồn của nó. Mặc dù promise đầu tiên mất nhiều thời gian nhất để resolve, nó vẫn là đầu tiên trong mảng kết quả.

Một mẹo phổ biến là ánh xạ một mảng dữ liệu công việc vào một mảng các promise, và sau đó gói nó vào `Promise.all`.

Ví dụ, nếu chúng ta có một mảng các URL, chúng ta có thể fetch tất cả chúng như thế này:

```
let urls = [
  'https://api.github.com/users/iliakan',
  'https://api.github.com/users/remy',
  'https://api.github.com/users/jeresig'
];

// ánh xạ mỗi url thành promise của fetch
let requests = urls.map(url => fetch(url));

// Promise.all chờ cho đến khi tất cả công việc được resolve
Promise.all(requests)
  .then(responses => responses.forEach(
    response => alert(`${response.url}: ${response.status}`)
  ));
```

Một ví dụ lớn hơn với việc fetch thông tin user cho một mảng các user GitHub theo tên của họ (chúng ta có thể fetch một mảng goods theo id của chúng, logic giống hệt nhau):

```
let names = ['iliakan', 'remy', 'jeresig'];

let requests = names.map(name => fetch(`https://api.github.com/users/${name}`));

Promise.all(requests)
  .then(responses => {
    // tất cả responses được resolve thành công
    for(let response of responses) {
      alert(`${response.url}: ${response.status}`); // hiển thị 200 cho mỗi url
    }

    return responses;
  })
  // ánh xạ mảng responses thành mảng response.json() để đọc nội dung của chúng
  .then(responses => Promise.all(responses.map(r => r.json())))
  // tất cả các câu trả lời JSON đã được parse: "users" là mảng của chúng
  .then(users => users.forEach(user => alert(user.name)));
```

**Nếu bất kỳ promise nào bị reject, promise được trả về bởi `Promise.all` ngay lập tức reject với lỗi đó.**

Ví dụ:

```
Promise.all([
  new Promise((resolve, reject) => setTimeout(() => resolve(1), 1000)),
  new Promise((resolve, reject) => setTimeout(() => reject(new Error("Whoops!")), 2000)),
  new Promise((resolve, reject) => setTimeout(() => resolve(3), 3000))
]).catch(alert); // Error: Whoops!
```

Ở đây promise thứ hai reject sau hai giây. Điều đó dẫn đến immediate rejection của `Promise.all`, vì vậy `.catch` thực thi: rejection error trở thành kết quả của toàn bộ `Promise.all`.

Trong trường hợp có lỗi, các promise khác bị bỏ qua

Nếu một promise reject, `Promise.all` ngay lập tức reject, hoàn toàn quên các promise khác trong danh sách. Kết quả của chúng bị bỏ qua.

Ví dụ, nếu có nhiều lệnh gọi `fetch`, như trong ví dụ ở trên, và một cái thất bại, những cái khác sẽ tiếp tục thực thi, nhưng `Promise.all` sẽ không theo dõi chúng nữa. Chúng sẽ cuối cùng settle, nhưng kết quả của chúng sẽ bị bỏ qua.

`Promise.all(iterable)` không làm gì để hủy chúng, vì không có khái niệm "cancellation" trong promises. Trong [chương khác](/fetch-abort) chúng ta sẽ đề cập đến `AbortController` có thể giúp đỡ với điều đó, nhưng nó không phải là một phần của Promise API.

`Promise.all(iterable)` cho phép các giá trị "thông thường" không phải promise trong `iterable`

Thông thường, `Promise.all(...)` chấp nhận một iterable (trong hầu hết các trường hợp là một mảng) các promise. Nhưng nếu bất kỳ đối tượng nào trong số đó không phải là promise, nó được chuyển đến mảng kết quả "như nó là".

Ví dụ, ở đây các kết quả là `[1, 2, 3]`:

```
Promise.all([
  new Promise((resolve, reject) => {
    setTimeout(() => resolve(1), 1000)
  }),
  2,
  3
]).then(alert); // 1, 2, 3
```

Vì vậy chúng ta có thể chuyển các giá trị sẵn có đến `Promise.all` khi tiện lợi.

## [Promise.allSettled](#promise-allsettled)

Một bổ sung gần đây

Đây là một bổ sung gần đây cho ngôn ngữ.
Các trình duyệt cũ có thể cần [polyfills](https://javascript.info/polyfills).

`Promise.all` reject như một tổng thể nếu bất kỳ promise nào reject. Điều đó tốt cho các trường hợp "all or nothing", khi chúng ta cần *tất cả* kết quả thành công để tiếp tục:

```
Promise.all([
  fetch('/template.html'),
  fetch('/style.css'),
  fetch('/data.json')
]).then(render); // phương thức render cần kết quả của tất cả fetches
```

`Promise.allSettled` chỉ chờ tất cả promises settle, bất kể kết quả. Mảng kết quả có:

- `{status:"fulfilled", value:result}` cho các phản hồi thành công,
- `{status:"rejected", reason:error}` cho các lỗi.

Ví dụ, chúng ta muốn tải thông tin về nhiều user. Ngay cả khi một yêu cầu thất bại, chúng ta vẫn quan tâm đến các yêu cầu khác.

Hãy sử dụng `Promise.allSettled`:

```
let urls = [
  'https://api.github.com/users/iliakan',
  'https://api.github.com/users/remy',
  'https://no-such-url'
];

Promise.allSettled(urls.map(url => fetch(url)))
  .then(results => { // (*)
    results.forEach((result, num) => {
      if (result.status == "fulfilled") {
        alert(`${urls[num]}: ${result.value.status}`);
      }
      if (result.status == "rejected") {
        alert(`${urls[num]}: ${result.reason}`);
      }
    });
  });
```

`results` ở dòng `(*)` ở trên sẽ là:

```
[
  {status: 'fulfilled', value: ...response...},
  {status: 'fulfilled', value: ...response...},
  {status: 'rejected', reason: ...error object...}
]
```

Vì vậy cho mỗi promise chúng ta nhận được trạng thái và `value/error` của nó.

### [Polyfill](#polyfill)

Nếu trình duyệt không hỗ trợ `Promise.allSettled`, dễ dàng để polyfill:

```
if (!Promise.allSettled) {
  const rejectHandler = reason => ({ status: 'rejected', reason });

  const resolveHandler = value => ({ status: 'fulfilled', value });

  Promise.allSettled = function (promises) {
    const convertedPromises = promises.map(p => Promise.resolve(p).then(resolveHandler, rejectHandler));
    return Promise.all(convertedPromises);
  };
}
```

Trong mã này, `promises.map` nhận các giá trị đầu vào, biến đổi chúng thành promises (chỉ để phòng trường hợp một non-promise đã được chuyển) với `p => Promise.resolve(p)`, và sau đó thêm handler `.then` cho mỗi cái.

Handler đó biến một kết quả thành công `value` thành `{status:'fulfilled', value}`, và một lỗi `reason` thành `{status:'rejected', reason}`. Đó chính xác là định dạng của `Promise.allSettled`.

Bây giờ chúng ta có thể sử dụng `Promise.allSettled` để nhận kết quả của *tất cả* các promise đã cho, ngay cả khi một số trong số chúng reject.

## [Promise.race](#promise-race)

Giống như `Promise.all`, nhưng chỉ chờ promise settle đầu tiên và nhận kết quả (hoặc lỗi) của nó.

Cú pháp là:

```
let promise = Promise.race(iterable);
```

Ví dụ, ở đây kết quả sẽ là `1`:

```
Promise.race([
  new Promise((resolve, reject) => setTimeout(() => resolve(1), 1000)),
  new Promise((resolve, reject) => setTimeout(() => reject(new Error("Whoops!")), 2000)),
  new Promise((resolve, reject) => setTimeout(() => resolve(3), 3000))
]).then(alert); // 1
```

Promise đầu tiên ở đây nhanh nhất, vì vậy nó trở thành kết quả. Sau khi promise đã settled đầu tiên "chiến thắng cuộc đua", tất cả các kết quả/lỗi tiếp theo bị bỏ qua.

## [Promise.any](#promise-any)

Giống như `Promise.race`, nhưng chỉ chờ promise fulfilled đầu tiên và nhận kết quả của nó. Nếu tất cả các promise đã cho đều reject, thì promise được trả về bị reject với [`AggregateError`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/AggregateError) — một đối tượng lỗi đặc biệt lưu trữ tất cả các lỗi promise trong thuộc tính `errors` của nó.

Cú pháp là:

```
let promise = Promise.any(iterable);
```

Ví dụ, ở đây kết quả sẽ là `1`:

```
Promise.any([
  new Promise((resolve, reject) => setTimeout(() => reject(new Error("Whoops!")), 1000)),
  new Promise((resolve, reject) => setTimeout(() => resolve(1), 2000)),
  new Promise((resolve, reject) => setTimeout(() => resolve(3), 3000))
]).then(alert); // 1
```

Promise đầu tiên ở đây nhanh nhất, nhưng nó bị reject, vì vậy promise thứ hai trở thành kết quả. Sau khi promise fulfilled đầu tiên "chiến thắng cuộc đua", tất cả các kết quả tiếp theo bị bỏ qua.

Dưới đây là một ví dụ khi tất cả các promise thất bại:

```
Promise.any([
  new Promise((resolve, reject) => setTimeout(() => reject(new Error("Ouch!")), 1000)),
  new Promise((resolve, reject) => setTimeout(() => reject(new Error("Error!")), 2000))
]).catch(error => {
  console.log(error.constructor.name); // AggregateError
  console.log(error.errors[0]); // Error: Ouch!
  console.log(error.errors[1]); // Error: Error!
});
```

Như bạn có thể thấy, các đối tượng lỗi cho các promise thất bại có sẵn trong thuộc tính `errors` của đối tượng `AggregateError`.

## [Promise.resolve/reject](#promise-resolve-reject)

Các phương thức `Promise.resolve` và `Promise.reject` hiếm khi cần trong mã hiện đại, vì cú pháp `async/await` (chúng ta sẽ đề cập đến nó [một chút sau](/async-await)) làm cho chúng hơi lỗi thời.

Chúng ta đề cập đến chúng ở đây cho đầy đủ và cho những người không thể sử dụng `async/await` vì lý do nào đó.

### [Promise.resolve](#promise-resolve)

`Promise.resolve(value)` tạo một promise đã resolved với kết quả `value`.

Giống như:

```
let promise = new Promise(resolve => resolve(value));
```

Phương thức được sử dụng cho tương thích, khi một hàm được mong đợi trả về một promise.

Ví dụ, hàm `loadCached` dưới đây fetch một URL và ghi nhớ (cache) nội dung của nó. Cho các cuộc gọi sau đó với cùng URL nó ngay lập tức nhận nội dung trước đó từ cache, nhưng sử dụng `Promise.resolve` để tạo một promise của nó, vì vậy giá trị trả về luôn là một promise:

```
let cache = new Map();

function loadCached(url) {
  if (cache.has(url)) {
    return Promise.resolve(cache.get(url)); // (*)
  }

  return fetch(url)
    .then(response => response.text())
    .then(text => {
      cache.set(url,text);
      return text;
    });
}
```

Chúng ta có thể viết `loadCached(url).then(…)`, vì hàm được đảm bảo trả về một promise. Chúng ta luôn có thể sử dụng `.then` sau `loadCached`. Đó là mục đích của `Promise.resolve` ở dòng `(*)`.

### [Promise.reject](#promise-reject)

`Promise.reject(error)` tạo một promise đã rejected với `error`.

Giống như:

```
let promise = new Promise((resolve, reject) => reject(error));
```

Trong thực tế, phương thức này hầu như không bao giờ được sử dụng.

## [Tóm tắt](#summary)

Có 6 static methods của class `Promise`:

1. `Promise.all(promises)` – chờ tất cả promises resolve và trả về một mảng các kết quả của chúng. Nếu bất kỳ promise nào trong số các promise đã cho reject, nó trở thành lỗi của `Promise.all`, và tất cả các kết quả khác bị bỏ qua.
2. `Promise.allSettled(promises)` (phương thức được thêm gần đây) – chờ tất cả promises settle và trả về các kết quả của chúng dưới dạng một mảng các đối tượng với:
   - `status`: `"fulfilled"` hoặc `"rejected"`
   - `value` (nếu fulfilled) hoặc `reason` (nếu rejected).
3. `Promise.race(promises)` – chờ promise đầu tiên settle, và kết quả/lỗi của nó trở thành kết quả.
4. `Promise.any(promises)` (phương thức được thêm gần đây) – chờ promise đầu tiên fulfill, và kết quả của nó trở thành kết quả. Nếu tất cả các promise đã cho đều reject, [`AggregateError`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/AggregateError) trở thành lỗi của `Promise.any`.
5. `Promise.resolve(value)` – tạo một promise đã resolved với giá trị đã cho.
6. `Promise.reject(error)` – tạo một promise đã rejected với lỗi đã cho.

Trong tất cả những cái này, `Promise.all` có lẽ là phổ biến nhất trong thực tế.
