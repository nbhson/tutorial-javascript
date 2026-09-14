# Promisification

> Nguồn: [https://javascript.info/promisify](https://javascript.info/promisify)

<!-- fetched: 2026-09-14 -->

"Promisification" là một từ dài cho một phép biến đổi đơn giản. Đó là chuyển đổi một hàm chấp nhận callback thành một hàm trả về promise.

Các phép biến đổi như vậy thường được yêu cầu trong thực tế, vì nhiều hàm và thư viện dựa trên callback. Nhưng promises thuận tiện hơn, vì vậy có ý nghĩa để promisifying chúng.

Để hiểu rõ hơn, hãy xem một ví dụ.

Ví dụ, chúng ta có `loadScript(src, callback)` từ chương [Giới thiệu: callbacks](/callbacks).

```
function loadScript(src, callback) {
  let script = document.createElement('script');
  script.src = src;

  script.onload = () => callback(null, script);
  script.onerror = () => callback(new Error(`Lỗi tải script cho ${src}`));

  document.head.append(script);
}

// cách sử dụng:
// loadScript('path/script.js', (err, script) => {...})
```

Hàm tải một script với `src` đã cho, và sau đó gọi `callback(err)` trong trường hợp có lỗi, hoặc `callback(null, script)` trong trường hợp tải thành công. Đó là một quy ước phổ biến để sử dụng callbacks, chúng ta đã thấy trước đó.

Hãy promisifying nó.

Chúng ta sẽ tạo một hàm mới `loadScriptPromise(src)`, làm giống nhau (tải script), nhưng trả về một promise thay vì sử dụng callbacks.

Nói cách khác, chúng ta chỉ chuyển nó `src` (không có `callback`) và nhận được một promise làm kết quả, resolve với `script` khi tải thành công, và reject với lỗi nếu không.

Dưới đây là nó:

```
let loadScriptPromise = function(src) {
  return new Promise((resolve, reject) => {
    loadScript(src, (err, script) => {
      if (err) reject(err);
      else resolve(script);
    });
  });
};

// cách sử dụng:
// loadScriptPromise('path/script.js').then(...)
```

Như chúng ta có thể thấy, hàm mới là một wrapper xung quanh hàm `loadScript` gốc. Nó gọi nó cung cấp callback tùy chỉnh của nó mà chuyển đổi thành promise `resolve/reject`.

Bây giờ `loadScriptPromise` phù hợp với mã dựa trên promise. Nếu chúng ta thích promises hơn callbacks (và sớm chúng ta sẽ thấy nhiều lý do hơn cho điều đó), thì chúng ta sẽ sử dụng nó thay thế.

Trong thực tế chúng ta có thể cần promisifying nhiều hơn một hàm, vì vậy có ý nghĩa để sử dụng một helper.

Chúng ta sẽ gọi nó là `promisify(f)`: nó nhận một hàm để promisifies `f` và trả về wrapper function.

```
function promisify(f) {
  return function (...args) { // return wrapper-function (*)
    return new Promise((resolve, reject) => {
      function callback(err, result) { // callback tùy chỉnh của chúng ta cho f (**)
        if (err) {
          reject(err);
        } else {
          resolve(result);
        }
      }

      args.push(callback); // append callback tùy chỉnh của chúng ta vào cuối các đối số của f

      f.call(this, ...args); // gọi hàm gốc
    });
  };
}

// cách sử dụng:
let loadScriptPromise = promisify(loadScript);
loadScriptPromise(...).then(...);
```

Mã có thể trông hơi phức tạp, nhưng về cơ bản là cùng thứ mà chúng ta đã viết ở trên, trong khi promisifying hàm `loadScript`.

Một cuộc gọi đến `promisify(f)` trả về một wrapper xung quanh `f` `(*)`. Wrapper đó trả về một promise và chuyển tiếp cuộc gọi đến `f` gốc, theo dõi kết quả trong callback tùy chỉnh `(**)`.

Ở đây, `promisify` giả định rằng hàm gốc mong đợi một callback với chính xác hai đối số `(err, result)`. Đó là những gì chúng ta gặp phải nhiều nhất. Sau đó callback tùy chỉnh của chúng ta có chính xác định dạng đúng, và `promisify` hoạt động tuyệt vời cho trường hợp như vậy.

Nhưng nếu `f` gốc mong đợi một callback với nhiều đối số `callback(err, res1, res2, ...)`?

Chúng ta có thể cải thiện helper của chúng ta. Hãy làm một phiên bản `promisify` nâng cao hơn.

- Khi được gọi là `promisify(f)` nó nên hoạt động tương tự như phiên bản ở trên.
- Khi được gọi là `promisify(f, true)`, nó nên trả về promise resolve với mảng các kết quả callback. Đó chính xác là cho các callback với nhiều đối số.

```
// promisify(f, true) để nhận mảng kết quả
function promisify(f, manyArgs = false) {
  return function (...args) {
    return new Promise((resolve, reject) => {
      function callback(err, ...results) { // callback tùy chỉnh của chúng ta cho f
        if (err) {
          reject(err);
        } else {
          // resolve với tất cả kết quả callback nếu manyArgs được chỉ định
          resolve(manyArgs ? results : results[0]);
        }
      }

      args.push(callback);

      f.call(this, ...args);
    });
  };
}

// cách sử dụng:
f = promisify(f, true);
f(...).then(arrayOfResults => ..., err => ...);
```

Như bạn có thể thấy, nó về cơ bản giống như ở trên, nhưng `resolve` được gọi với chỉ một hoặc tất cả các đối số tùy thuộc vào việc `manyArgs` có truthy hay không.

Đối với các định dạng callback kỳ lạ hơn, như những cái không có `err` nói chung: `callback(result)`, chúng ta có thể promisifying các hàm như vậy thủ công mà không sử dụng helper.

Cũng có các module với các hàm promisification linh hoạt hơn một chút, ví dụ [es6-promisify](https://github.com/digitaldesignlabs/es6-promisify). Trong Node.js, có một hàm tích hợp `util.promisify` cho mục đích đó.

Xin lưu ý:

Promisification là một cách tiếp cận tuyệt vời, đặc biệt khi bạn sử dụng `async/await` (được đề cập sau trong chương [Async/await](/async-await)), nhưng không phải là sự thay thế hoàn toàn cho callbacks.

Hãy nhớ rằng, một promise chỉ có thể có một kết quả, nhưng một callback về mặt kỹ thuật có thể được gọi nhiều lần.

Vì vậy promisification chỉ dành cho các hàm gọi callback một lần. Các cuộc gọi tiếp theo sẽ bị bỏ qua.
