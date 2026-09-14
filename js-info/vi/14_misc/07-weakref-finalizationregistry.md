# WeakRef và FinalizationRegistry

> Source: [https://javascript.info/weakref-finalizationregistry](https://javascript.info/weakref-finalizationregistry)

<!-- fetched: 2026-09-14 -->

Các tính năng "ẩn" của ngôn ngữ

Bài viết này đề cập đến một chủ đề rất tập trung, mà hầu hết các nhà phát triển hiếm khi gặp phải trong thực tế (và có thể không even biết về sự tồn tại của nó).

Chúng tôi khuyên bạn bỏ qua chương này nếu bạn mới bắt đầu học JavaScript.

Nhớ lại khái niệm cơ bản của *nguyên lý reachability* từ chương [Garbage collection](/garbage-collection),
chúng ta có thể nhận thấy rằng engine JavaScript được đảm bảo giữ các giá trị trong bộ nhớ có thể truy cập hoặc đang sử dụng.

Ví dụ:

```
//  biến user giữ một strong reference đến đối tượng
let user = { name: "John" };

// hãy ghi đè giá trị của biến user
user = null;

// reference bị mất và đối tượng sẽ bị xóa khỏi bộ nhớ
```

Hoặc một mã tương tự, nhưng phức tạp hơn một chút với hai strong references:

```
//  biến user giữ một strong reference đến đối tượng
let user = { name: "John" };

// copied strong reference đến đối tượng vào biến admin
let admin = user;

// hãy ghi đè giá trị của biến user
user = null;

// đối tượng vẫn có thể truy cập được thông qua biến admin
```

Đối tượng `{ name: "John" }` sẽ chỉ bị xóa khỏi bộ nhớ nếu không có strong references nào đến nó (nếu chúng ta cũng ghi đè giá trị của biến `admin`).

Trong JavaScript, có một khái niệm được gọi là `WeakRef`, hoạt động hơi khác trong trường hợp này.

Các thuật ngữ: "Strong reference", "Weak reference"

**Strong reference** – là một reference đến một đối tượng hoặc giá trị, ngăn chúng bị xóa bởi garbage collector. Nhờ đó, giữ đối tượng hoặc giá trị trong bộ nhớ, nơi nó trỏ đến.

Điều đó có nghĩa là, đối tượng hoặc giá trị vẫn ở trong bộ nhớ và không được garbage collector thu thập cho đến khi có active strong references đến nó.

Trong JavaScript, các reference thông thường đến các đối tượng là strong references. Ví dụ:

```
// biến user giữ một strong reference đến đối tượng này
let user = { name: "John" };
```

**Weak reference** – là một reference đến một đối tượng hoặc giá trị, không *ngăn* chúng bị xóa bởi garbage collector.
Một đối tượng hoặc giá trị có thể bị xóa bởi garbage collector nếu, các reference còn lại đến chúng chỉ là weak references.

## [WeakRef](#weakref)

Lưu ý thận trọng

Trước khi chúng ta đi sâu vào nó, đáng chú ý rằng việc sử dụng đúng các cấu trúc được thảo luận trong bài viết này đòi hỏi suy nghĩ rất cẩn thận, và chúng tốt nhất nên tránh nếu có thể.

`WeakRef` – là một đối tượng, chứa một weak reference đến một đối tượng khác, được gọi là `target` hoặc `referent`.

Đặc tính của `WeakRef` là nó không ngăn garbage collector xóa đối tượng referent của nó. Nói cách khác, một đối tượng `WeakRef` không giữ đối tượng `referent` sống.

Giờ hãy lấy biến `user` làm "referent" và tạo một weak reference từ nó đến biến `admin`.
Để tạo một weak reference, bạn cần sử dụng constructor `WeakRef`, truyền vào đối tượng target (đối tượng bạn muốn có weak reference đến).

Trong trường hợp của chúng ta – đây là biến `user`:

```
//  biến user giữ một strong reference đến đối tượng
let user = { name: "John" };

//  biến admin giữ một weak reference đến đối tượng
let admin = new WeakRef(user);
```

Sơ đồ dưới đây mô tả hai loại references: một strong reference sử dụng biến `user` và một weak reference sử dụng biến `admin`:

![](/article/weakref-finalizationregistry/weakref-finalizationregistry-01.svg)

Sau đó, tại một số điểm, chúng ta ngừng sử dụng biến `user` – nó được ghi đè, đi ra khỏi scope, v.v., trong khi vẫn giữ instance `WeakRef` trong biến `admin`:

```
// hãy ghi đè giá trị của biến user
user = null;
```

Một weak reference đến một đối tượng không đủ để giữ nó "sống". Khi chỉ còn lại các weak references đến một đối tượng referent, garbage collector tự do phá hủy đối tượng này và sử dụng bộ nhớ của nó cho mục đích khác.

Tuy nhiên, cho đến khi đối tượng thực sự bị phá hủy, weak reference có thể trả về nó, ngay cả khi không còn strong references nào đến đối tượng đó.
Nghĩa là, đối tượng của chúng ta trở thành một loại "[Schrödinger's cat](https://en.wikipedia.org/wiki/Schr%C3%B6dinger%27s_cat)" – chúng ta không thể biết chắc chắn rằng nó "sống" hay "chết":

![](/article/weakref-finalizationregistry/weakref-finalizationregistry-02.svg)

Tại thời điểm này, để nhận đối tượng từ instance `WeakRef`, chúng ta sẽ sử dụng phương thức `deref()` của nó.

Phương thức `deref()` trả về đối tượng referent mà `WeakRef` trỏ đến, nếu đối tượng vẫn ở trong bộ nhớ. Nếu đối tượng đã bị garbage collector xóa, thì phương thức `deref()` sẽ trả về `undefined`:

```
let ref = admin.deref();

if (ref) {
  // đối tượng vẫn có thể truy cập được: chúng ta có thể thực hiện bất kỳ thao tác nào với nó
} else {
  // đối tượng đã bị garbage collector thu thập
}
```

## [Các trường hợp sử dụng WeakRef](#weakref-use-cases)

`WeakRef` thường được sử dụng để tạo caches hoặc [associative arrays](https://en.wikipedia.org/wiki/Associative_array) lưu trữ các đối tượng tốn nhiều tài nguyên.
Điều đó cho phép tránh ngăn cản các đối tượng này bị thu thập bởi garbage collector chỉ dựa trên sự hiện diện của chúng trong cache hoặc associative array.

Một trong những ví dụ chính – là tình huống khi chúng ta có vô số các đối tượng hình ảnh nhị phân (chẳng hạn, được biểu diễn dưới dạng `ArrayBuffer` hoặc `Blob`), và chúng ta muốn associate một tên hoặc path với mỗi hình ảnh.
Các cấu trúc dữ liệu hiện có không hoàn toàn phù hợp cho các mục đích này:

- Sử dụng `Map` để tạo associations giữa tên và hình ảnh, hoặc ngược lại, sẽ giữ các đối tượng hình ảnh trong bộ nhớ vì chúng hiện diện trong `Map` dưới dạng keys hoặc values.
- `WeakMap` không phù hợp cho mục tiêu này: vì các đối tượng được biểu diễn dưới dạng keys của `WeakMap` sử dụng weak references, và không được bảo vệ khỏi bị xóa bởi garbage collector.

Nhưng, trong tình huống này, chúng ta cần một cấu trúc dữ liệu sẽ sử dụng weak references trong các values của nó.

Cho mục đích này, chúng ta có thể sử dụng một collection `Map`, có các values là các instance `WeakRef` trỏ đến các đối tượng lớn mà chúng ta cần.
Do đó, chúng ta sẽ không giữ các đối tượng lớn và không cần thiết này trong bộ nhớ lâu hơn chúng nên.

Nếu không, đây là một cách để nhận đối tượng hình ảnh từ cache nếu nó vẫn có thể truy cập được.
Nếu nó đã bị garbage collected, chúng ta sẽ re-generate hoặc re-download nó một lần nữa.

Bằng cách đó, ít bộ nhớ được sử dụng trong một số tình huống.

## [Ví dụ №1: sử dụng WeakRef cho caching](#example-1-using-weakref-for-caching)

Dưới đây là một đoạn mã demonstrata kỹ thuật sử dụng `WeakRef`.

Nói ngắn gọn, chúng ta sử dụng một `Map` với các key string và các đối tượng `WeakRef` làm values của chúng.
Nếu đối tượng `WeakRef` chưa bị garbage collector thu thập, chúng ta nhận nó từ cache.
Nếu không, chúng ta re-download nó một lần nữa và đặt nó vào cache để tái sử dụng sau:

```
function fetchImg() {
    // abstract function for downloading images...
}

function weakRefCache(fetchImg) { // (1)
    const imgCache = new Map(); // (2)

    return (imgName) => { // (3)
        const cachedImg = imgCache.get(imgName); // (4)

        if (cachedImg?.deref()) { // (5)
            return cachedImg?.deref();
        }

        const newImg = fetchImg(imgName); // (6)
        imgCache.set(imgName, new WeakRef(newImg)); // (7)

        return newImg;
    };
}

const getCachedImg = weakRefCache(fetchImg);
```

Hãy đi sâu vào chi tiết về những gì đã xảy ra ở đây:

1. `weakRefCache` – là một higher-order function nhận một hàm khác, `fetchImg`, làm đối số. Trong ví dụ này, chúng ta có thể bỏ qua mô tả chi tiết của hàm `fetchImg`, vì nó có thể là bất kỳ logic nào để tải xuống hình ảnh.
2. `imgCache` – là một cache của hình ảnh, lưu trữ kết quả đã cache của hàm `fetchImg`, dưới dạng các key string (tên hình ảnh) và các đối tượng `WeakRef` làm values của chúng.
3. Trả về một anonymous function nhận tên hình ảnh làm đối số. Đối số này sẽ được sử dụng làm key cho hình ảnh đã cache.
4. Cố gắng nhận kết quả đã cache từ cache, sử dụng key đã cung cấp (tên hình ảnh).
5. Nếu cache chứa một value cho key đã chỉ định, và đối tượng `WeakRef` chưa bị garbage collector xóa, trả về kết quả đã cache.
6. Nếu không có entry trong cache với key được yêu cầu, hoặc phương thức `deref()` trả về `undefined` (có nghĩa là đối tượng `WeakRef` đã bị garbage collected), hàm `fetchImg` tải xuống hình ảnh một lần nữa.
7. Đặt hình ảnh đã tải xuống vào cache dưới dạng một đối tượng `WeakRef`.

Giờ chúng ta có một collection `Map`, nơi keys – là tên hình ảnh dưới dạng strings, và values – là các đối tượng `WeakRef` chứa chính hình ảnh.

Kỹ thuật này giúp tránh phân bổ một lượng lớn bộ nhớ cho các đối tượng tốn nhiều tài nguyên, mà không ai sử dụng nữa.
Nó cũng tiết kiệm bộ nhớ và thời gian trong trường hợp tái sử dụng các đối tượng đã cache.

Đây là biểu diễn trực quan của những gì mã này trông như thế nào:

![](/article/weakref-finalizationregistry/weakref-finalizationregistry-03.svg)

Nhưng, implementation này có các nhược điểm của nó: theo thời gian, `Map` sẽ được điền với các strings làm keys, trỏ đến một `WeakRef`, có đối tượng referent đã bị garbage collected:

![](/article/weakref-finalizationregistry/weakref-finalizationregistry-04.svg)

Một cách để xử lý vấn đề này – là dọn dẹp cache định kỳ và xóa các entries "chết".
Một cách khác – là sử dụng các finalizers, mà chúng ta sẽ khám phá tiếp theo.

## [Ví dụ №2: Sử dụng WeakRef để theo dõi các đối tượng DOM](#example-2-using-weakref-to-track-dom-objects)

Một trường hợp sử dụng khác cho `WeakRef` – là theo dõi các đối tượng DOM.

Hãy tưởng tượng một tình huống khi một số mã hoặc thư viện của bên thứ ba tương tác với các phần tử trên trang của chúng ta miễn là chúng tồn tại trong DOM.
Chẳng hạn, đó có thể là một utility bên ngoài để giám sát và thông báo về trạng thái của hệ thống (thường được gọi là "logger" – một chương trình gửi các thông tin được gọi là "logs").

Ví dụ tương tác:

Result

index.js

index.css

index.html

```
const startMessagesBtn = document.querySelector('.start-messages'); // (1)
const closeWindowBtn = document.querySelector('.window__button'); // (2)
const windowElementRef = new WeakRef(document.querySelector(".window__body")); // (3)

startMessagesBtn.addEventListener('click', () => { // (4)
    startMessages(windowElementRef);
    startMessagesBtn.disabled = true;
});

closeWindowBtn.addEventListener('click', () =>  document.querySelector(".window__body").remove()); // (5)

const startMessages = (element) => {
    const timerId = setInterval(() => { // (6)
        if (element.deref()) { // (7)
            const payload = document.createElement("p");
            payload.textContent = `Message: System status OK: ${new Date().toLocaleTimeString()}`;
            element.deref().append(payload);
        } else { // (8)
            alert("The element has been deleted."); // (9)
            clearInterval(timerId);
        }
    }, 1000);
};
```

```
.app {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.start-messages {
    width: fit-content;
}

.window {
    width: 100%;
    border: 2px solid #464154;
    overflow: hidden;
}

.window__header {
    position: sticky;
    padding: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #736e7e;
}

.window__title {
    margin: 0;
    font-size: 24px;
    font-weight: 700;
    color: white;
    letter-spacing: 1px;
}

.window__button {
    padding: 4px;
    background: #4f495c;
    outline: none;
    border: 2px solid #464154;
    color: white;
    font-size: 16px;
    cursor: pointer;
}

.window__body {
    height: 250px;
    padding: 16px;
    overflow: scroll;
    background-color: #736e7e33;
}
```

```
<!DOCTYPE HTML>
<html lang="en">

<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="index.css">
  <title>WeakRef DOM Logger</title>
</head>

<body>

<div class="app">
  <button class="start-messages">Start sending messages</button>
  <div class="window">
    <div class="window__header">
      <p class="window__title">Messages:</p>
      <button class="window__button">Close</button>
    </div>
    <div class="window__body">
      No messages.
    </div>
  </div>
</div>

<script type="module" src="index.js"></script>
</body>
</html>
```

Khi nút "Start sending messages" được click, trong cửa sổ hiển thị "logs" (một phần tử với class `.window__body`), các thông báo (logs) bắt đầu xuất hiện.

Nhưng, ngay khi phần tử này bị xóa khỏi DOM, logger nên dừng gửi thông báo.
Để tái tạo việc xóa phần tử này, chỉ cần click nút "Close" ở góc trên bên phải.

Để không làm phức tạp công việc của chúng ta, và không phải thông báo cho mã của bên thứ ba mỗi khi DOM-element của chúng ta có sẵn, và khi nó không có, sẽ đủ để tạo một weak reference đến nó bằng cách sử dụng `WeakRef`.

Một khi phần tử bị xóa khỏi DOM, logger sẽ nhận ra điều đó và dừng gửi thông báo.

Giờ hãy xem xét kỹ hơn source code (*tab `index.js`*):

1. Lấy DOM-element của nút "Start sending messages".
2. Lấy DOM-element của nút "Close".
3. Lấy DOM-element của cửa sổ hiển thị logs bằng cách sử dụng constructor `new WeakRef()`. Bằng cách đó, biến `windowElementRef` giữ một weak reference đến DOM-element.
4. Thêm event listener trên nút "Start sending messages", chịu trách nhiệm bắt đầu logger khi được click.
5. Thêm event listener trên nút "Close", chịu trách nhiệm đóng cửa sổ hiển thị logs khi được click.
6. Sử dụng `setInterval` để bắt đầu hiển thị một thông báo mới mỗi giây.
7. Nếu DOM-element của cửa sổ hiển thị logs vẫn có thể truy cập được và được giữ trong bộ nhớ, tạo và gửi một thông báo mới.
8. Nếu phương thức `deref()` trả về `undefined`, có nghĩa là DOM-element đã bị xóa khỏi bộ nhớ. Trong trường hợp này, logger dừng hiển thị thông báo và xóa timer.
9. `alert`, sẽ được gọi, sau khi DOM-element của cửa sổ hiển thị logs bị xóa khỏi bộ nhớ (tức là sau khi click nút "Close"). **Lưu ý, việc xóa khỏi bộ nhớ có thể không xảy ra ngay lập tức, vì nó phụ thuộc chỉ vào các cơ chế nội bộ của garbage collector.**

   Chúng ta không thể kiểm soát quá trình này trực tiếp từ mã. Tuy nhiên, bất chấp điều đó, chúng ta vẫn có tùy chọn ép garbage collection từ trình duyệt.

   Trong Google Chrome, chẳng hạn, để làm điều đó, bạn cần mở các công cụ developer (`Ctrl` + `Shift` + `J` trên Windows/Linux hoặc `Option` + `⌘` + `J` trên macOS), chuyển sang tab "Performance", và click vào nút biểu tượng thùng rác – "Collect garbage":

   ![](/article/weakref-finalizationregistry/google-chrome-developer-tools.png)

       
   Functionality này được hỗ trợ trong hầu hết các trình duyệt hiện đại. Sau khi các hành động được thực hiện, `alert` sẽ kích hoạt ngay lập tức.

## [FinalizationRegistry](#finalizationregistry)

Giờ đã đến lúc nói về các finalizers. Trước khi chúng ta chuyển sang tiếp, hãy làm rõ thuật ngữ:

**Cleanup callback (finalizer)** – là một hàm được thực thi, khi một đối tượng, được đăng ký trong `FinalizationRegistry`, bị xóa khỏi bộ nhớ bởi garbage collector.

Mục đích của nó – là cung cấp khả năng thực hiện các thao tác bổ sung, liên quan đến đối tượng, sau khi nó đã bị xóa cuối cùng khỏi bộ nhớ.

**Registry** (hoặc `FinalizationRegistry`) – là một đối tượng đặc biệt trong JavaScript quản lý việc đăng ký và hủy đăng ký các đối tượng và các cleanup callback của chúng.

Cơ chế này cho phép đăng ký một đối tượng để theo dõi và associate một cleanup callback với nó.
Về cơ bản nó là một cấu trúc lưu trữ thông tin về các đối tượng đã đăng ký và các cleanup callback của chúng, và sau đó tự động invoke các callback đó khi các đối tượng bị xóa khỏi bộ nhớ.

Để tạo một instance của `FinalizationRegistry`, nó cần gọi constructor của nó, nhận một đối số duy nhất – cleanup callback (finalizer).

Cú pháp:

```
function cleanupCallback(heldValue) {
  // cleanup callback code
}

const registry = new FinalizationRegistry(cleanupCallback);
```

Ở đây:

- `cleanupCallback` – một cleanup callback sẽ được gọi tự động khi một đối tượng đã đăng ký bị xóa khỏi bộ nhớ.
- `heldValue` – giá trị được truyền làm đối số cho cleanup callback. Nếu `heldValue` là một đối tượng, registry giữ một strong reference đến nó.
- `registry` – một instance của `FinalizationRegistry`.

Các phương thức `FinalizationRegistry`:

- `register(target, heldValue [, unregisterToken])` – được sử dụng để đăng ký các đối tượng trong registry.

  `target` – đối tượng được đăng ký để theo dõi. Nếu `target` bị garbage collected, cleanup callback sẽ được gọi với `heldValue` làm đối số của nó.

  `unregisterToken` tùy chọn – một token hủy đăng ký. Nó có thể được truyền để hủy đăng ký một đối tượng trước khi garbage collector xóa nó. Thông thường, đối tượng `target` được sử dụng làm `unregisterToken`, đó là practice tiêu chuẩn.
- `unregister(unregisterToken)` – phương thức `unregister` được sử dụng để hủy đăng ký một đối tượng khỏi registry. Nó nhận một đối số – `unregisterToken` (token hủy đăng ký được tạo ra khi đăng ký đối tượng).

Giờ hãy chuyển sang một ví dụ đơn giản. Hãy sử dụng đối tượng `user` đã biết và tạo một instance của `FinalizationRegistry`:

```
let user = { name: "John" };

const registry = new FinalizationRegistry((heldValue) => {
  console.log(`${heldValue} has been collected by the garbage collector.`);
});
```

Sau đó, chúng ta sẽ đăng ký đối tượng, yêu cầu một cleanup callback bằng cách gọi phương thức `register`:

```
registry.register(user, user.name);
```

Registry không giữ một strong reference đến đối tượng được đăng ký, vì điều đó sẽ phá vỡ mục đích của nó. Nếu registry giữ một strong reference, thì đối tượng sẽ không bao giờ bị garbage collected.

Nếu đối tượng bị xóa bởi garbage collector, cleanup callback của chúng ta có thể được gọi tại một số điểm trong tương lai, với `heldValue` được truyền cho nó:

```
// Khi đối tượng user bị xóa bởi garbage collector, thông báo sau sẽ được in trong console:
"John has been collected by the garbage collector."
```

Cũng có các tình huống nơi, ngay cả trong các implementation sử dụng cleanup callback, có khả năng nó sẽ không được gọi.

Ví dụ:

- Khi chương trình hoàn toàn kết thúc hoạt động của nó (chẳng hạn, khi đóng một tab trong trình duyệt).
- Khi instance `FinalizationRegistry` bản thân không còn reachable đến mã JavaScript.
  Nếu đối tượng tạo instance `FinalizationRegistry` đi ra khỏi scope hoặc bị xóa, các cleanup callbacks được đăng ký trong registry đó cũng có thể không được invoke.

## [Caching với FinalizationRegistry](#caching-with-finalizationregistry)

Quay lại ví dụ cache *weak* của chúng ta, chúng ta có thể nhận thấy điều sau:

- Ngay cả khi các values được bọc trong `WeakRef` đã bị garbage collector thu thập, vẫn có vấn đề "memory leakage" dưới dạng các keys còn lại, có values đã bị garbage collected.

Đây là một ví dụ caching được cải thiện sử dụng `FinalizationRegistry`:

```
function fetchImg() {
  // abstract function for downloading images...
}

function weakRefCache(fetchImg) {
  const imgCache = new Map();

  const registry = new FinalizationRegistry((imgName) => { // (1)
    const cachedImg = imgCache.get(imgName);
    if (cachedImg && !cachedImg.deref()) imgCache.delete(imgName);
  });

  return (imgName) => {
    const cachedImg = imgCache.get(imgName);

    if (cachedImg?.deref()) {
      return cachedImg?.deref();
    }

    const newImg = fetchImg(imgName);
    imgCache.set(imgName, new WeakRef(newImg));
    registry.register(newImg, imgName); // (2)

    return newImg;
  };
}

const getCachedImg = weakRefCache(fetchImg);
```

1. Để quản lý cleanup của các entries cache "chết", khi các đối tượng `WeakRef` liên kết bị garbage collected, chúng ta tạo một cleanup registry `FinalizationRegistry`.

   Điểm quan trọng ở đây là, trong cleanup callback, nên kiểm tra, nếu entry đã bị garbage collector xóa và không được thêm lại, để không xóa một entry "sống".
2. Một khi value mới (hình ảnh) được tải xuống và đặt vào cache, chúng ta đăng ký nó trong finalizer registry để theo dõi đối tượng `WeakRef`.

Implementation này chỉ chứa các cặp key/value thực tế hoặc "sống".
Trong trường hợp này, mỗi đối tượng `WeakRef` được đăng ký trong `FinalizationRegistry`.
Và sau khi các đối tượng được cleanup bởi garbage collector, cleanup callback sẽ xóa tất cả các values `undefined`.

Đây là biểu diễn trực quan của mã đã cập nhật:

![](/article/weakref-finalizationregistry/weakref-finalizationregistry-05.svg)

Một khía cạnh then chốt của implementation đã cập nhật là các finalizers cho phép tạo các quy trình song song giữa chương trình "chính" và các cleanup callback.
Trong ngữ cảnh của JavaScript, chương trình "chính" – là mã JavaScript của chúng ta, chạy và thực thi trong ứng dụng hoặc trang web của chúng ta.

Do đó, từ thời điểm một đối tượng được đánh dấu để xóa bởi garbage collector, và đến khi thực thi cleanup callback thực tế, có thể có một khoảng thời gian nhất định.
Điều quan trọng là phải hiểu rằng trong khoảng thời gian này, chương trình chính có thể thực hiện bất kỳ thay đổi nào đối với đối tượng hoặc thậm chí đưa nó trở lại bộ nhớ.

Đó là lý do tại sao, trong cleanup callback, chúng ta phải kiểm tra xem một entry đã được thêm lại vào cache bởi chương trình chính để tránh xóa các entries "sống".
Tương tự, khi tìm kiếm một key trong cache, có khả năng value đã bị garbage collector xóa, nhưng cleanup callback chưa được thực thi.

Các tình huống như vậy đòi hỏi sự chú ý đặc biệt nếu bạn đang làm việc với `FinalizationRegistry`.

## [Sử dụng WeakRef và FinalizationRegistry trong thực tế](#using-weakref-and-finalizationregistry-in-practice)

Chuyển từ lý thuyết sang thực tế, hãy tưởng tượng một kịch bản thực tế, nơi một user đồng bộ hóa các bức ảnh của họ trên thiết bị di động với một số dịch vụ cloud
(chẳng hạn như [iCloud](https://en.wikipedia.org/wiki/ICloud) hoặc [Google Photos](https://en.wikipedia.org/wiki/Google_Photos)),
và muốn xem chúng từ các thiết bị khác. Ngoài functionality cơ bản của việc xem ảnh, các dịch vụ như vậy cung cấp rất nhiều tính năng bổ sung, chẳng hạn:

- Chỉnh sửa ảnh và video effects.
- Tạo "memories" và albums.
- Video montage từ một series ảnh.
- …và nhiều hơn nữa.

Ở đây, như một ví dụ, chúng ta sẽ sử dụng một implementation khá primitive của dịch vụ như vậy.
Điểm chính – là show một scenario có thể của việc sử dụng `WeakRef` và `FinalizationRegistry` cùng nhau trong thực tế.

Đây là những gì nó trông như thế nào:

![](/article/weakref-finalizationregistry/weakref-finalizationregistry-demo-01.png)

   
Ở bên trái, có một library ảnh cloud (chúng được hiển thị dưới dạng thumbnails).
Chúng ta có thể chọn các hình ảnh chúng ta cần và tạo một collage, bằng cách click nút "Create collage" ở bên phải của trang.
Sau đó, collage kết quả có thể được tải xuống dưới dạng một hình ảnh.
  

Để tăng tốc độ tải trang, sẽ hợp lý để tải xuống và hiển thị thumbnails ảnh ở chất lượng *compressed*.
Nhưng, để tạo một collage từ các ảnh đã chọn, tải xuống và sử dụng chúng ở chất lượng *full-size*.

Dưới đây, chúng ta có thể thấy, kích thước intrinsic của các thumbnails là 240x240 pixels.
Kích thước được chọn có chủ ý để tăng tốc độ tải xuống.
Hơn nữa, chúng ta không cần ảnh full-size ở chế độ preview.

![](/article/weakref-finalizationregistry/weakref-finalizationregistry-demo-02.png)

  
Hãy giả sử, rằng chúng ta cần tạo một collage của 4 ảnh: chúng ta chọn chúng, và sau đó click nút "Create collage".
Ở giai đoạn này, hàm `weakRefCache` đã biết của chúng ta kiểm tra xem hình ảnh được yêu cầu có trong cache không.
Nếu không, nó tải xuống từ cloud và đặt nó vào cache để sử dụng sau.
Điều đó xảy ra cho mỗi ảnh đã chọn:
  

![](/article/weakref-finalizationregistry/weakref-finalizationregistry-demo-03.gif)

Chú ý đến output trong console, bạn có thể thấy, ảnh nào đã được tải xuống từ cloud – điều đó được chỉ định bởi FETCHED\_IMAGE.
Vì đây là nỗ lực đầu tiên để tạo một collage, điều đó có nghĩa là, ở giai đoạn này "weak cache" vẫn trống, và tất cả các ảnh đã được tải xuống từ cloud và đặt trong nó.

Nhưng, cùng với quá trình tải xuống ảnh, cũng có một quá trình dọn dẹp bộ nhớ bởi garbage collector.
Điều đó có nghĩa là, đối tượng được lưu trữ trong cache, mà chúng ta tham chiếu, bằng một weak reference, bị garbage collector xóa.
Và finalizer của chúng ta thực thi thành công, do đó xóa key, bằng cách hình ảnh được lưu trữ trong cache.
CLEANED\_IMAGE thông báo cho chúng ta về nó:

![](/article/weakref-finalizationregistry/weakref-finalizationregistry-demo-04.jpg)

  
Tiếp theo, chúng ta nhận ra rằng chúng ta không thích collage kết quả, và quyết định thay đổi một trong các ảnh và tạo một cái mới.
Để làm điều đó, chỉ cần deselect ảnh không cần thiết, chọn một ảnh khác, và click nút "Create collage" một lần nữa:
  

![](/article/weakref-finalizationregistry/weakref-finalizationregistry-demo-05.gif)

  
Nhưng lần này không phải tất cả các ảnh được tải xuống từ network, và một trong số chúng đã được lấy từ weak cache: thông báo CACHED\_IMAGE nói cho chúng ta về điều đó.
Điều đó có nghĩa là tại thời điểm tạo collage, garbage collector chưa xóa ảnh của chúng ta, và chúng ta mạnh dạn lấy nó từ cache,
do đó giảm số lượng requests network và tăng tốc tổng thời gian của quá trình tạo collage:
  

![](/article/weakref-finalizationregistry/weakref-finalizationregistry-demo-06.jpg)

  
Hãy "chơi xung quanh" một chút hơn nữa, bằng cách thay đổi một trong các ảnh một lần nữa và tạo một collage mới:
  

![](/article/weakref-finalizationregistry/weakref-finalizationregistry-demo-07.gif)

  
Lần này kết quả thậm chí còn ấn tượng hơn. Trong số 4 ảnh đã chọn, 3 trong số chúng được lấy từ weak cache, và chỉ một phải được tải xuống từ network.
Sự giảm tải network khoảng 75%. Ấn tượng, phải không?
  

![](/article/weakref-finalizationregistry/weakref-finalizationregistry-demo-08.jpg)

Tất nhiên, quan trọng là phải nhớ, rằng hành vi như vậy không được đảm bảo, và phụ thuộc vào implementation cụ thể và operation của garbage collector.

Dựa trên điều đó, một câu hỏi hoàn toàn logic ngay lập tức arises: tại sao chúng ta không sử dụng một cache thông thường, nơi chúng ta có thể quản lý các entities của riêng mình, thay vì dựa vào garbage collector?
Đúng vậy, trong phần lớn các trường hợp không có nhu cầu sử dụng `WeakRef` và `FinalizationRegistry`.

Ở đây, chúng ta đơn giản đã demonstrata một implementation alternative của functionality tương tự, bằng cách sử dụng một approach không tầm thường với các tính năng ngôn ngữ thú vị.
Vẫn còn, chúng ta không thể dựa vào ví dụ này, nếu chúng ta cần một kết quả constant và predictable.

Bạn có thể [mở ví dụ này trong sandbox](https://plnkr.co/edit/tFgkfPkNPQhGOTYu?p=preview).

## [Tóm tắt](#summary)

`WeakRef` – được thiết kế để tạo các weak references đến các đối tượng, cho phép chúng bị xóa khỏi bộ nhớ bởi garbage collector nếu không còn strong references nào đến chúng.
Điều đó có lợi cho việc giải quyết việc sử dụng bộ nhớ quá mức và tối ưu hóa việc sử dụng các tài nguyên hệ thống trong các ứng dụng.

`FinalizationRegistry` – là một công cụ để đăng ký các callbacks, được thực thi khi các đối tượng không còn được reference mạnh, bị hủy.
Điều đó cho phép giải phóng các tài nguyên liên kết với đối tượng hoặc thực hiện các thao tác cần thiết khác trước khi xóa đối tượng khỏi bộ nhớ.
