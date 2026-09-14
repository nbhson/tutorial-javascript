# Iteration bất đồng bộ và Generators

> Nguồn: [https://javascript.info/async-iterators-generators](https://javascript.info/async-iterators-generators)

<!-- fetched: 2026-09-14 -->

Asynchronous iteration cho phép chúng ta iterate qua dữ liệu đến không đồng bộ, theo yêu cầu. Ví dụ, khi chúng ta tải một thứ gì đó từng chunk qua mạng. Và async generators làm cho nó thậm chí thuận tiện hơn.

Hãy xem một ví dụ đơn giản trước, để nắm bắt cú pháp, và sau đó xem xét một trường hợp sử dụng thực tế.

## [Nhắc lại iterables](#recall-iterables)

Hãy nhắc lại chủ đề về iterables.

Ý tưởng là chúng ta có một đối tượng, như `range` ở đây:

```
let range = {
  from: 1,
  to: 5
};
```

…Và chúng ta muốn sử dụng vòng lặp `for..of` trên nó, như `for(value of range)`, để nhận các giá trị từ `1` đến `5`.

Nói cách khác, chúng ta muốn thêm *khả năng iteration* cho đối tượng.

Điều đó có thể được thực hiện bằng cách sử dụng một phương thức đặc biệt với tên `Symbol.iterator`:

- Phương thức này được gọi bởi cấu trúc `for..of` khi vòng lặp bắt đầu, và nó nên trả về một đối tượng có phương thức `next`.
- Cho mỗi iteration, phương thức `next()` được invoke để nhận giá trị tiếp theo.
- `next()` nên trả về một giá trị dưới dạng `{done: true/false, value:<loop value>}`, trong đó `done:true` có nghĩa là kết thúc vòng lặp.

Dưới đây là một implementation cho iterable `range`:

```
let range = {
  from: 1,
  to: 5,

  [Symbol.iterator]() { // được gọi một lần, ở đầu for..of
    return {
      current: this.from,
      last: this.to,

      next() { // được gọi trên mỗi iteration, để nhận giá trị tiếp theo
        if (this.current <= this.last) {
          return { done: false, value: this.current++ };
        } else {
          return { done: true };
        }
      }
    };
  }
};

for(let value of range) {
  alert(value); // 1 sau đó 2, sau đó 3, sau đó 4, sau đó 5
}
```

Nếu có điều gì không rõ, xin hãy ghé thăm chương [Iterables](/iterable), nó cung cấp tất cả chi tiết về iterables thông thường.

## [Iterables không đồng bộ](#async-iterables)

Asynchronous iteration cần thiết khi các giá trị đến không đồng bộ: sau `setTimeout` hoặc một loại delay khác.

Trường hợp phổ biến nhất là đối tượng cần thực hiện một yêu cầu mạng để cung cấp giá trị tiếp theo, chúng ta sẽ thấy một ví dụ thực tế của nó một chút sau.

Để làm cho một đối tượng iterable một cách asynchronous:

1. Sử dụng `Symbol.asyncIterator` thay vì `Symbol.iterator`.
2. Phương thức `next()` nên trả về một promise (để fulfill với giá trị tiếp theo).
   - Từ khóa `async` xử lý nó, chúng ta chỉ cần làm `async next()`.
3. Để iterate qua đối tượng như vậy, chúng ta nên sử dụng vòng lặp `for await (let item of iterable)`.
   - Lưu ý từ `await`.

Như một ví dụ bắt đầu, hãy tạo một đối tượng iterable `range`, giống như cái trước, nhưng bây giờ nó sẽ trả về giá trị không đồng bộ, một cái mỗi giây.

Tất cả những gì chúng ta cần làm là thực hiện một vài thay thế trong mã ở trên:

```
let range = {
  from: 1,
  to: 5,

  [Symbol.asyncIterator]() { // (1)
    return {
      current: this.from,
      last: this.to,

      async next() { // (2)

        // lưu ý: chúng ta có thể sử dụng "await" bên trong async next:
        await new Promise(resolve => setTimeout(resolve, 1000)); // (3)

        if (this.current <= this.last) {
          return { done: false, value: this.current++ };
        } else {
          return { done: true };
        }
      }
    };
  }
};

(async () => {

  for await (let value of range) { // (4)
    alert(value); // 1,2,3,4,5
  }

})();
```

Như chúng ta có thể thấy, cấu trúc tương tự như các iterator thông thường:

1. Để làm cho một đối tượng asynchronously iterable, nó phải có phương thức `Symbol.asyncIterator` `(1)`.
2. Phương thức này phải trả về đối tượng có phương thức `next()` trả về một promise `(2)`.
3. Phương thức `next()` không nhất thiết phải `async`, nó có thể là một phương thức thông thường trả về promise, nhưng `async` cho phép chúng ta sử dụng `await`, vì vậy thuận tiện. Ở đây chúng ta chỉ delay trong một giây `(3)`.
4. Để iterate, chúng ta sử dụng `for await(let value of range)` `(4)`, cụ thể là thêm "await" sau "for". Nó gọi `range[Symbol.asyncIterator]()` một lần, và sau đó `next()` của nó cho các giá trị.

Dưới đây là một bảng nhỏ với các khác biệt:

|  | Iterators | Async iterators |
| --- | --- | --- |
| Object method để cung cấp iterator | `Symbol.iterator` | `Symbol.asyncIterator` |
| Giá trị trả về của `next()` là | any value | `Promise` |
| để loop, sử dụng | `for..of` | `for await..of` |

Cú pháp spread `...` không hoạt động asynchronous

Các tính năng yêu cầu các iterator regular, synchronous, không hoạt động với các async iterator.

Ví dụ, cú pháp spread sẽ không hoạt động:

```
alert( [...range] ); // Error, không có Symbol.iterator
```

Điều đó tự nhiên, vì nó mong đợi tìm thấy `Symbol.iterator`, không phải `Symbol.asyncIterator`.

Cũng đúng cho `for..of`: cú pháp không có `await` cần `Symbol.iterator`.

## [Nhắc lại generators](#recall-generators)

Bây giờ hãy nhắc lại generators, vì chúng cho phép làm cho mã iteration ngắn hơn nhiều. Hầu hết thời gian, khi chúng ta muốn tạo một iterable, chúng ta sẽ sử dụng generators.

Vì sự đơn giản thuần túy, bỏ qua một số thứ quan trọng, chúng là "các hàm tạo ra (yield) các giá trị". Chúng được giải thích chi tiết trong chương [Generators](/generators).

Generators được đánh dấu với `function*` (lưu ý ngôi sao) và sử dụng `yield` để tạo ra giá trị, sau đó chúng ta có thể sử dụng `for..of` để loop qua chúng.

Ví dụ này tạo ra một sequence của các giá trị từ `start` đến `end`:

```
function* generateSequence(start, end) {
  for (let i = start; i <= end; i++) {
    yield i;
  }
}

for(let value of generateSequence(1, 5)) {
  alert(value); // 1, sau đó 2, sau đó 3, sau đó 4, sau đó 5
}
```

Như chúng ta đã biết, để làm cho một đối tượng iterable, chúng ta nên thêm `Symbol.iterator` vào nó.

```
let range = {
  from: 1,
  to: 5,
  [Symbol.iterator]() {
    return <đối tượng với next để làm range iterable>
  }
};
```

Practice phổ biến cho `Symbol.iterator` là trả về một generator, nó làm cho mã ngắn hơn, như bạn có thể thấy:

```
let range = {
  from: 1,
  to: 5,

  *[Symbol.iterator]() { // shorthand cho [Symbol.iterator]: function*()
    for(let value = this.from; value <= this.to; value++) {
      yield value;
    }
  }
};

for(let value of range) {
  alert(value); // 1, sau đó 2, sau đó 3, sau đó 4, sau đó 5
}
```

Xin xem chương [Generators](/generators) nếu bạn muốn thêm chi tiết.

Trong các generator thông thường chúng ta không thể sử dụng `await`. Tất cả các giá trị phải đến synchronous, như yêu cầu bởi cấu trúc `for..of`.

Nếu chúng ta muốn tạo ra giá trị một cách asynchronous? Từ các yêu cầu mạng, ví dụ.

Hãy chuyển sang async generators để làm cho điều đó có thể.

## [Async generators (cuối cùng)](#async-generators-finally)

Đối với hầu hết các ứng dụng thực tế, khi chúng ta muốn tạo một đối tượng async tạo ra một sequence của các giá trị, chúng ta có thể sử dụng một async generator.

Cú pháp đơn giản: thêm `async` trước `function*`. Điều đó làm cho generator trở nên asynchronous.

Và sau đó sử dụng `for await (...)` để iterate qua nó, như thế này:

```
async function* generateSequence(start, end) {

  for (let i = start; i <= end; i++) {

    // Wow, có thể sử dụng await!
    await new Promise(resolve => setTimeout(resolve, 1000));

    yield i;
  }

}

(async () => {

  let generator = generateSequence(1, 5);
  for await (let value of generator) {
    alert(value); // 1, sau đó 2, sau đó 3, sau đó 4, sau đó 5 (với delay giữa)
  }

})();
```

Vì generator là asynchronous, chúng ta có thể sử dụng `await` bên trong nó, dựa vào promises, thực hiện các yêu cầu mạng và vân vân.

Under-the-hood difference

Về mặt kỹ thuật, nếu bạn là một người đọc nâng cao nhớ các chi tiết về generators, có một sự khác biệt nội bộ.

Đối với async generators, phương thức `generator.next()` là asynchronous, nó trả về promises.

Trong một generator thông thường chúng ta sẽ sử dụng `result = generator.next()` để nhận giá trị. Trong một async generator, chúng ta nên thêm `await`, như thế này:

```
result = await generator.next(); // result = {value: ..., done: true/false}
```

Đó là lý do tại sao async generators hoạt động với `for await...of`.

### [Range iterable không đồng bộ](#async-iterable-range)

Generators thông thường có thể được sử dụng như `Symbol.iterator` để làm cho mã iteration ngắn hơn.

Tương tự như vậy, async generators có thể được sử dụng như `Symbol.asyncIterator` để thực hiện asynchronous iteration.

Ví dụ, chúng ta có thể làm cho đối tượng `range` tạo ra giá trị một cách asynchronous, một lần mỗi giây, bằng cách thay thế `Symbol.iterator` synchronous bằng `Symbol.asyncIterator` asynchronous:

```
let range = {
  from: 1,
  to: 5,

  // dòng này giống như [Symbol.asyncIterator]: async function*() {
  async *[Symbol.asyncIterator]() {
    for(let value = this.from; value <= this.to; value++) {

      // tạo pause giữa các giá trị, chờ đợi điều gì đó
      await new Promise(resolve => setTimeout(resolve, 1000));

      yield value;
    }
  }
};

(async () => {

  for await (let value of range) {
    alert(value); // 1, sau đó 2, sau đó 3, sau đó 4, sau đó 5
  }

})();
```

Bây giờ các giá trị đến với độ trễ 1 giây giữa chúng.

Xin lưu ý:

Về mặt kỹ thuật, chúng ta có thể thêm cả `Symbol.iterator` và `Symbol.asyncIterator` vào đối tượng, vì vậy nó vừa synchronously iterable (`for..of`) vừa asynchronously iterable (`for await..of`).

Trong thực tế, điều đó sẽ là một điều kỳ lạ để làm.

## [Ví dụ thực tế: paginated data](#real-life-example-paginated-data)

Cho đến nay chúng ta đã thấy các ví dụ cơ bản, để có được sự hiểu biết. Bây giờ hãy xem xét một trường hợp sử dụng thực tế.

Có nhiều dịch vụ online cung cấp dữ liệu phân trang. Ví dụ, khi chúng ta cần một danh sách user, một request trả về một count được định trước (ví dụ 100 users) — "một trang", và cung cấp một URL đến trang tiếp theo.

Mẫu này rất phổ biến. Đó không phải là về user, mà chỉ về bất kỳ thứ gì.

Ví dụ, GitHub cho phép chúng ta truy xuất commits theo cách phân trang tương tự:

- Chúng ta nên thực hiện yêu cầu đến `fetch` dưới dạng `https://api.github.com/repos/<repo>/commits`.
- Nó phản hồi với một JSON của 30 commits, và cũng cung cấp một liên kết đến trang tiếp theo trong header `Link`.
- Sau đó chúng ta có thể sử dụng liên kết đó cho yêu cầu tiếp theo, để nhận thêm commits, và cứ thế.

Đối với mã của chúng ta, chúng ta muốn có một cách đơn giản hơn để nhận commits.

Hãy tạo một hàm `fetchCommits(repo)` nhận commits cho chúng ta, thực hiện các yêu cầu bất cứ khi nào cần. Và để nó lo lắng về tất cả các thứ pagination. Đối với chúng ta sẽ là async iteration `for await..of` đơn giản.

Vì vậy cách sử dụng sẽ giống như thế này:

```
for await (let commit of fetchCommits("username/repository")) {
  // xử lý commit
}
```

Dưới đây là hàm như vậy, được implement dưới dạng async generator:

```
async function* fetchCommits(repo) {
  let url = `https://api.github.com/repos/${repo}/commits`;

  while (url) {
    const response = await fetch(url, { // (1)
      headers: {'User-Agent': 'Our script'}, // github cần bất kỳ user-agent header nào
    });

    const body = await response.json(); // (2) response là JSON (mảng các commits)

    // (3) URL của trang tiếp theo nằm trong headers, extract nó
    let nextPage = response.headers.get('Link').match(/<(.*?)>; rel="next"/);
    nextPage = nextPage?.[1];

    url = nextPage;

    for(let commit of body) { // (4) yield commits từng cái một, cho đến khi trang kết thúc
      yield commit;
    }
  }
}
```

Giải thích thêm về cách nó hoạt động:

1. Chúng ta sử dụng phương thức browser [fetch](/fetch) để tải các commits.

   - URL ban đầu là `https://api.github.com/repos/<repo>/commits`, và trang tiếp theo sẽ nằm trong header `Link` của response.
   - Phương thức `fetch` cho phép chúng ta cung cấp authorization và các header khác nếu cần – ở đây GitHub yêu cầu `User-Agent`.
2. Các commits được trả về dưới dạng JSON.
3. Chúng ta nên nhận URL trang tiếp theo từ header `Link` của response. Nó có một định dạng đặc biệt, vì vậy chúng ta sử dụng regular expression cho điều đó (chúng ta sẽ học tính năng này trong [Regular expressions](/regular-expressions)).

   - URL trang tiếp theo có thể trông như `https://api.github.com/repositories/93253246/commits?page=2`. Nó được tạo bởi chính GitHub.
4. Sau đó chúng ta yield các commits đã nhận từng cái một, và khi chúng kết thúc, iteration `while(url)` tiếp theo sẽ kích hoạt, thực hiện một yêu cầu khác.

Một ví dụ về sử dụng (hiển thị tác giả commits trong console):

```
(async () => {

  let count = 0;

  for await (const commit of fetchCommits('javascript-tutorial/en.javascript.info')) {

    console.log(commit.author.login);

    if (++count == 100) { // hãy dừng ở 100 commits
      break;
    }
  }

})();

// Lưu ý: Nếu bạn đang chạy điều này trong một sandbox bên ngoài, bạn cần dán ở đây hàm fetchCommits được mô tả ở trên
```

Đó chính xác là những gì chúng ta muốn.

Cơ chế nội bộ của các yêu cầu phân trang là vô hình từ bên ngoài. Đối với chúng ta đó chỉ là một async generator trả về các commits.

## [Tóm tắt](#summary)

Các iterator và generator thông thường hoạt động tốt với dữ liệu không mất thời gian để tạo.

Khi chúng ta mong đợi dữ liệu đến không đồng bộ, với delays, các async counterparts của chúng có thể được sử dụng, và `for await..of` thay vì `for..of`.

Khác biệt cú pháp giữa async và regular iterators:

|  | Iterable | Async Iterable |
| --- | --- | --- |
| Method để cung cấp iterator | `Symbol.iterator` | `Symbol.asyncIterator` |
| Giá trị trả về của `next()` là | `{value:…, done: true/false}` | `Promise` resolve đến `{value:…, done: true/false}` |

Khác biệt cú pháp giữa async và regular generators:

|  | Generators | Async generators |
| --- | --- | --- |
| Declaration | `function*` | `async function*` |
| Giá trị trả về của `next()` là | `{value:…, done: true/false}` | `Promise` resolve đến `{value:…, done: true/false}` |

Trong web-development chúng ta thường gặp streams dữ liệu, khi nó chảy từng chunk. Ví dụ, tải xuống hoặc tải lên một file lớn.

Chúng ta có thể sử dụng async generators để xử lý dữ liệu như vậy. Cũng đáng lưu ý là trong một số environments, như trong browsers, có một API khác được gọi là Streams, cung cấp các interfaces đặc biệt để làm việc với các streams như vậy, để transform dữ liệu và để truyền nó từ stream này sang stream khác (ví dụ tải xuống từ một nơi và ngay lập tức gửi đến nơi khác).
