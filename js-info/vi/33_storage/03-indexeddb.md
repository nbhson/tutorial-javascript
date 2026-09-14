# IndexedDB

> Source: [https://javascript.info/indexeddb](https://javascript.info/indexeddb)

<!-- fetched: 2026-09-14 -->

IndexedDB là cơ sở dữ liệu tích hợp sẵn trong trình duyệt, mạnh hơn nhiều so với `localStorage`.

- Lưu trữ hầu như mọi loại giá trị theo keys, nhiều loại key khác nhau.
- Hỗ trợ transaction để đảm bảo độ tin cậy.
- Hỗ trợ truy vấn theo khoảng key, index.
- Có thể lưu trữ khối lượng dữ liệu lớn hơn nhiều so với `localStorage`.

Sức mạnh đó thường là quá mức đối với các ứng dụng client-server truyền thống. IndexedDB được dành cho các ứng dụng offline, kết hợp với ServiceWorkers và các công nghệ khác.

Giao diện native của IndexedDB, được mô tả trong đặc tả <https://www.w3.org/TR/IndexedDB>, dựa trên sự kiện.

Chúng ta cũng có thể dùng `async/await` với sự trợ giúp của wrapper dựa trên Promise, như <https://github.com/jakearchibald/idb>. Điều đó khá tiện lợi, nhưng wrapper không hoàn hảo, không thể thay thế sự kiện trong mọi trường hợp. Vì vậy chúng ta sẽ bắt đầu với sự kiện, và sau đó, khi đã hiểu rõ IndexedDB, chúng ta sẽ dùng wrapper.

Dữ liệu ở đâu?

Về mặt kỹ thuật, dữ liệu thường được lưu trong thư mục home của khách truy cập, cùng với cài đặt trình duyệt, extension, v.v.

Các trình duyệt khác nhau và người dùng ở cấp hệ điều hành khác nhau có mỗi storage độc lập của riêng họ.

## [Mở cơ sở dữ liệu](#open-database)

Để bắt đầu làm việc với IndexedDB, trước tiên chúng ta cần `open` (kết nối với) cơ sở dữ liệu.

Cú pháp:

```
let openRequest = indexedDB.open(name, version);
```

- `name` – một chuỗi, tên cơ sở dữ liệu.
- `version` – phiên bản số nguyên dương, mặc định là `1` (giải thích bên dưới).

Chúng ta có thể có nhiều cơ sở dữ liệu với các tên khác nhau, nhưng tất cả chúng đều tồn tại trong origin hiện tại (domain/giao thức/cổng). Các trang web khác nhau không thể truy cập cơ sở dữ liệu của nhau.

Lời gọi trả về đối tượng `openRequest`, chúng ta nên lắng nghe các sự kiện trên nó:

- `success`: cơ sở dữ liệu sẵn sàng, đối tượng "database" nằm trong `openRequest.result`, chúng ta nên dùng nó cho các lời gọi tiếp theo.
- `error`: mở thất bại.
- `upgradeneeded`: cơ sở dữ liệu sẵn sàng, nhưng phiên bản của nó đã lỗi thời (xem bên dưới).

**IndexedDB có cơ chế "phiên bản hóa schema" tích hợp sẵn, không có trong các cơ sở dữ liệu phía server.**

Khác với cơ sở dữ liệu phía server, IndexedDB nằm ở phía client, dữ liệu được lưu trong trình duyệt, vì vậy chúng ta, là lập trình viên, không thể tiếp cận nó mọi lúc. Vì vậy, khi chúng ta phát hành phiên bản mới của ứng dụng, và người dùng truy cập trang web của chúng ta, chúng ta có thể cần cập nhật cơ sở dữ liệu.

Nếu phiên bản cơ sở dữ liệu cục bộ nhỏ hơn phiên bản được chỉ định trong `open`, thì sự kiện đặc biệt `upgradeneeded` được kích hoạt, và chúng ta có thể so sánh phiên bản và nâng cấp cấu trúc dữ liệu theo nhu cầu.

Sự kiện `upgradeneeded` cũng kích hoạt khi cơ sở dữ liệu chưa tồn tại (về mặt kỹ thuật, phiên bản của nó là `0`), vì vậy chúng ta có thể thực hiện khởi tạo.

Giả sử chúng ta đã phát hành phiên bản đầu tiên của ứng dụng.

Sau đó chúng ta có thể mở cơ sở dữ liệu với phiên bản `1` và thực hiện khởi tạo trong handler `upgradeneeded` như sau:

```
let openRequest = indexedDB.open("store", 1);

openRequest.onupgradeneeded = function() {
  // triggers if the client had no database
  // ...perform initialization...
};

openRequest.onerror = function() {
  console.error("Error", openRequest.error);
};

openRequest.onsuccess = function() {
  let db = openRequest.result;
  // continue working with database using db object
};
```

Rồi, sau đó, chúng ta phát hành phiên bản thứ 2.

Chúng ta có thể mở nó với phiên bản `2` và thực hiện nâng cấp như sau:

```
let openRequest = indexedDB.open("store", 2);

openRequest.onupgradeneeded = function(event) {
  // the existing database version is less than 2 (or it doesn't exist)
  let db = openRequest.result;
  switch(event.oldVersion) { // existing db version
    case 0:
      // version 0 means that the client had no database
      // perform initialization
    case 1:
      // client had version 1
      // update
  }
};
```

Vui lòng lưu ý: vì phiên bản hiện tại của chúng ta là `2`, handler `onupgradeneeded` có nhánh mã cho phiên bản `0`, phù hợp cho người dùng truy cập lần đầu và chưa có cơ sở dữ liệu, và cũng cho phiên bản `1`, để nâng cấp.

Và sau đó, chỉ khi handler `onupgradeneeded` kết thúc không có lỗi, `openRequest.onsuccess` mới kích hoạt, và cơ sở dữ liệu được coi là đã mở thành công.

Để xóa cơ sở dữ liệu:

```
let deleteRequest = indexedDB.deleteDatabase(name)
// deleteRequest.onsuccess/onerror tracks the result
```

Không thể mở cơ sở dữ liệu bằng phiên bản cũ hơn của lời gọi open

Nếu cơ sở dữ liệu của người dùng hiện tại có phiên bản cao hơn so với trong lời gọi `open`, ví dụ: phiên bản DB hiện có là `3`, và chúng ta cố gắng `open(...2)`, thì đó là lỗi, `openRequest.onerror` kích hoạt.

Điều đó hiếm gặp, nhưng có thể xảy ra khi khách truy cập tải mã JavaScript cũ, ví dụ từ bộ đệm proxy. Vì vậy mã cũ, nhưng cơ sở dữ liệu của anh ta mới.

Để bảo vệ khỏi lỗi, chúng ta nên kiểm tra `db.version` và đề xuất tải lại trang. Sử dụng HTTP caching headers phù hợp để tránh tải mã cũ, để bạn sẽ không bao giờ gặp phải những vấn đề như vậy.

### [Vấn đề cập nhật song song](#parallel-update-problem)

Vì chúng ta đang nói về phiên bản hóa, hãy giải quyết một vấn đề liên quan nhỏ.

Giả sử:

1. Khách truy cập mở trang web của chúng ta trong tab trình duyệt, với phiên bản cơ sở dữ liệu `1`.
2. Sau đó chúng ta triển khai bản cập nhật, vì vậy mã của chúng ta mới hơn.
3. Và rồi cùng khách truy cập đó mở trang web của chúng ta trong một tab khác.

Vì vậy có một tab với kết nối mở tới DB phiên bản `1`, trong khi tab thứ hai cố gắng nâng cấp nó lên phiên bản `2` trong handler `upgradeneeded` của nó.

Vấn đề là cơ sở dữ liệu được chia sẻ giữa hai tab, vì chúng cùng trang web, cùng origin. Và nó không thể vừa là phiên bản `1` vừa là phiên bản `2`. Để thực hiện nâng cấp lên phiên bản `2`, tất cả các kết nối tới phiên bản 1 phải được đóng, bao gồm cả kết nối trong tab đầu tiên.

Để tổ chức điều đó, sự kiện `versionchange` kích hoạt trên đối tượng cơ sở dữ liệu "lỗi thời". Chúng ta nên lắng nghe nó và đóng kết nối cơ sở dữ liệu cũ (và có thể đề xuất tải lại trang, để tải mã đã cập nhật).

Nếu chúng ta không lắng nghe sự kiện `versionchange` và không đóng kết nối cũ, thì kết nối mới thứ hai sẽ không được tạo. Đối tượng `openRequest` sẽ phát sự kiện `blocked` thay vì `success`. Vì vậy tab thứ hai sẽ không hoạt động.

Dưới đây là mã xử lý đúng việc nâng cấp song song. Nó cài đặt handler `onversionchange`, kích hoạt nếu kết nối cơ sở dữ liệu hiện tại trở nên lỗi thời (phiên bản db được cập nhật ở nơi khác) và đóng kết nối.

```
let openRequest = indexedDB.open("store", 2);

openRequest.onupgradeneeded = ...;
openRequest.onerror = ...;

openRequest.onsuccess = function() {
  let db = openRequest.result;

  db.onversionchange = function() {
    db.close();
    alert("Database is outdated, please reload the page.")
  };

  // ...the db is ready, use it...
};

openRequest.onblocked = function() {
  // this event shouldn't trigger if we handle onversionchange correctly

  // it means that there's another open connection to the same database
  // and it wasn't closed after db.onversionchange triggered for it
};
```

…Nói cách khác, ở đây chúng ta làm hai điều:

1. Lắng nghe `db.onversionchange` thông báo cho chúng ta về nỗ lực cập nhật song song, nếu phiên bản cơ sở dữ liệu hiện tại trở nên lỗi thời.
2. Lắng nghe `openRequest.onblocked` thông báo cho chúng ta về tình huống ngược lại: có một kết nối tới phiên bản lỗi thời ở nơi khác, và nó không đóng, vì vậy kết nối mới hơn không thể được tạo.

Chúng ta có thể xử lý mượt mà hơn trong `db.onversionchange`, nhắc khách truy cứu lưu dữ liệu trước khi kết nối được đóng và vân vân.

Hoặc, một cách tiếp cận thay thế là không đóng cơ sở dữ liệu trong `db.onversionchange`, mà thay vào đó dùng handler `onblocked` (trong tab mới) để cảnh báo khách truy cập, cho anh ta biết rằng phiên bản mới hơn không thể được tải cho đến khi họ đóng các tab khác.

Các xung đột cập nhật này xảy ra hiếm, nhưng chúng ta nên ít nhất có một số xử lý cho chúng, ít nhất một handler `onblocked`, để ngăn script của chúng ta chết lặng lẽ.

## [Object store](#object-store)

Để lưu thứ gì đó trong IndexedDB, chúng ta cần một *object store*.

Object store là khái niệm cốt lõi của IndexedDB. Đối ứng trong các cơ sở dữ liệu khác được gọi là "tables" hoặc "collections". Đó là nơi dữ liệu được lưu trữ. Một cơ sở dữ liệu có thể có nhiều store: một cho người dùng, một khác cho hàng hóa, v.v.

Mặc dù được đặt tên là "object store", các primitive cũng có thể được lưu trữ.

**Chúng ta có thể lưu hầu như bất kỳ giá trị nào, bao gồm cả các đối tượng phức tạp.**

IndexedDB sử dụng [thuật toán serialize chuẩn](https://www.w3.org/TR/html53/infrastructure.html#section-structuredserializeforstorage) để clone-và-lưu đối tượng. Nó giống `JSON.stringify`, nhưng mạnh hơn, có khả năng lưu trữ nhiều kiểu dữ liệu hơn.

Một ví dụ về đối tượng không thể lưu: đối tượng có tham chiếu vòng tròn. Những đối tượng như vậy không thể serialize được. `JSON.stringify` cũng thất bại với những đối tượng như vậy.

**Mọi giá trị trong store phải có `key` duy nhất.**

Key phải thuộc một trong các kiểu sau – số, ngày, chuỗi, nhị phân, hoặc mảng. Nó là định danh duy nhất, để chúng ta có thể tìm/xóa/cập nhật giá trị theo key.

![](/article/indexeddb/indexeddb-structure.svg)

Như chúng ta sẽ thấy ngay, chúng ta có thể cung cấp key khi thêm giá trị vào store, tương tự `localStorage`. Nhưng khi lưu các đối tượng, IndexedDB cho phép đặt một thuộc tính của đối tượng làm key, tiện lợi hơn nhiều. Hoặc chúng ta có thể tự động sinh keys.

Nhưng chúng ta cần tạo object store trước.

Cú pháp để tạo object store:

```
db.createObjectStore(name[, keyOptions]);
```

Vui lòng lưu ý, thao tác này đồng bộ, không cần `await`.

- `name` là tên store, ví dụ `"books"` cho sách,
- `keyOptions` là đối tượng tùy chọn với một trong hai thuộc tính:
  - `keyPath` – đường dẫn đến thuộc tính đối tượng mà IndexedDB sẽ dùng làm key, ví dụ `id`.
  - `autoIncrement` – nếu `true`, thì key cho đối tượng mới lưu được sinh tự động, như một số tăng liên tục.

Nếu chúng ta không cung cấp `keyOptions`, thì chúng ta sẽ cần cung cấp key rõ ràng sau đó, khi lưu đối tượng.

Ví dụ, object store này sử dụng thuộc tính `id` làm key:

```
db.createObjectStore('books', {keyPath: 'id'});
```

**Object store chỉ có thể được tạo/sửa đổi khi cập nhật phiên bản DB, trong handler `upgradeneeded`.**

Đó là một hạn chế kỹ thuật. Bên ngoài handler, chúng ta sẽ có thể thêm/xóa/cập nhật dữ liệu, nhưng object stores chỉ có thể được tạo/xóa/đổi khi cập nhật phiên bản.

Để thực hiện nâng cấp phiên bản cơ sở dữ liệu, có hai cách tiếp cận chính:

1. Chúng ta có thể cài đặt các hàm nâng cấp theo từng phiên bản: từ 1 lên 2, từ 2 lên 3, từ 3 lên 4 v.v. Sau đó, trong `upgradeneeded` chúng ta có thể so sánh phiên bản (ví dụ: cũ 2, hiện 4) và chạy các nâng cấp theo từng phiên bản từng bước, cho mọi phiên bản trung gian (từ 2 lên 3, rồi từ 3 lên 4).
2. Hoặc chúng ta chỉ cần xem xét cơ sở dữ liệu: lấy danh sách các object store hiện có như `db.objectStoreNames`. Đối tượng đó là [DOMStringList](https://html.spec.whatwg.org/multipage/common-dom-interfaces.html#domstringlist) cung cấp phương thức `contains(name)` để kiểm tra sự tồn tại. Và sau đó chúng ta có thể thực hiện cập nhật tùy thuộc vào thứ gì tồn tại và thứ gì không.

Với các cơ sở dữ liệu nhỏ, phương án thứ hai có thể đơn giản hơn.

Dưới đây là demo của phương pháp thứ hai:

```
let openRequest = indexedDB.open("db", 2);

// create/upgrade the database without version checks
openRequest.onupgradeneeded = function() {
  let db = openRequest.result;
  if (!db.objectStoreNames.contains('books')) { // if there's no "books" store
    db.createObjectStore('books', {keyPath: 'id'}); // create it
  }
};
```

Để xóa một object store:

```
db.deleteObjectStore('books')
```

## [Transactions](#transactions)

Thuật ngữ "transaction" là thuật ngữ chung, được dùng trong nhiều loại cơ sở dữ liệu.

Transaction là một nhóm các thao tác, phải hoặc tất cả thành công hoặc tất cả thất bại.

Ví dụ, khi một người mua thứ gì đó, chúng ta cần:

1. Trừ tiền khỏi tài khoản của họ.
2. Thêm vật phẩm vào kho của họ.

Sẽ rất tệ nếu chúng ta hoàn thành thao tác 1, rồi có điều gì đó sai, ví dụ: mất điện, và chúng ta không thể thực hiện thao tác 2. Cả hai nên hoặc thành công (mua hàng hoàn tất, tốt!) hoặc cả hai thất bại (ít nhất người đó giữ được tiền, để họ có thể thử lại).

Transactions có thể đảm bảo điều đó.

**Mọi thao tác dữ liệu trong IndexedDB phải được thực hiện trong một transaction.**

Để bắt đầu một transaction:

```
db.transaction(store[, type]);
```

- `store` là tên store mà transaction sắp truy cập, ví dụ `"books"`. Có thể là mảng tên store nếu chúng ta sắp truy cập nhiều store.
- `type` – loại transaction, một trong:
  - `readonly` – chỉ có thể đọc, mặc định.
  - `readwrite` – chỉ có thể đọc và ghi dữ liệu, nhưng không tạo/xóa/đổi object stores.

Cũng có loại transaction `versionchange`: các transaction như vậy có thể làm mọi thứ, nhưng chúng ta không thể tạo chúng thủ công. IndexedDB tự động tạo transaction `versionchange` khi mở cơ sở dữ liệu, cho handler `upgradeneeded`. Đó là lý do tại sao nó là nơi duy nhất chúng ta có thể cập nhật cấu trúc cơ sở dữ liệu, tạo/xóa object stores.

Tại sao lại có các loại transaction khác nhau?

Hiệu năng là lý do mà transactions cần được gán nhãn `readonly` và `readwrite`.

Nhiều transaction `readonly` có thể truy cập cùng một store song song, nhưng transaction `readwrite` thì không được. Transaction `readwrite` "khóa" store để ghi. Transaction tiếp theo phải chờ trước khi transaction trước hoàn tất trước khi truy cập cùng store.

Sau khi transaction được tạo, chúng ta có thể thêm một mục vào store, như thế này:

```
let transaction = db.transaction("books", "readwrite"); // (1)

// get an object store to operate on it
let books = transaction.objectStore("books"); // (2)

let book = {
  id: 'js',
  price: 10,
  created: new Date()
};

let request = books.add(book); // (3)

request.onsuccess = function() { // (4)
  console.log("Book added to the store", request.result);
};

request.onerror = function() {
  console.log("Error", request.error);
};
```

Về cơ bản có bốn bước:

1. Tạo transaction, nêu rõ tất cả các store mà nó sẽ truy cập, tại `(1)`.
2. Lấy đối tượng store bằng `transaction.objectStore(name)`, tại `(2)`.
3. Thực hiện request tới object store `books.add(book)`, tại `(3)`.
4. …Xử lý request thành công/lỗi `(4)`, sau đó chúng ta có thể thực hiện các request khác nếu cần, v.v.

Object stores hỗ trợ hai phương thức để lưu giá trị:

- **put(value, [key])**
  Thêm `value` vào store. `key` chỉ được cung cấp nếu object store không có tùy chọn `keyPath` hoặc `autoIncrement`. Nếu đã có giá trị với cùng key, nó sẽ bị thay thế.
- **add(value, [key])**
  Tương tự `put`, nhưng nếu đã có giá trị với cùng key, thì request thất bại và một lỗi với tên `"ConstraintError"` được tạo ra.

Tương tự việc mở cơ sở dữ liệu, chúng ta có thể gửi một request: `books.add(book)`, rồi chờ các sự kiện `success/error`.

- `request.result` của `add` là key của đối tượng mới.
- Lỗi nằm trong `request.error` (nếu có).

## [Tự động commit của transactions](#transactions-autocommit)

Trong ví dụ trên chúng ta đã bắt đầu transaction và thực hiện request `add`. Nhưng như đã nêu ở trên, một transaction có thể có nhiều request liên kết, tất cả phải hoặc thành công hoặc thất bại. Làm thế nào để đánh dấu transaction hoàn tất, không còn request nào nữa?

Câu trả lời ngắn là: chúng ta không làm vậy.

Trong phiên bản 3.0 tiếp theo của đặc tả, có thể sẽ có cách thủ công để kết thúc transaction, nhưng hiện tại ở phiên bản 2.0 thì chưa có.

**Khi tất cả các request của transaction hoàn tất, và [hàng đợi microtask](/microtask-queue) trống, nó được commit tự động.**

Thường thì, chúng ta có thể giả định rằng transaction được commit khi tất cả request của nó hoàn tất, và mã hiện tại kết thúc.

Vậy, trong ví dụ trên không cần gọi gì đặc biệt để kết thúc transaction.

Nguyên tắc tự động commit của transactions có một tác dụng phụ quan trọng. Chúng ta không thể chèn một thao tác bất đồng bộ như `fetch`, `setTimeout` ở giữa một transaction. IndexedDB sẽ không giữ transaction chờ cho đến khi chúng hoàn tất.

Trong mã bên dưới, `request2` ở dòng `(*)` thất bại, vì transaction đã được commit, và không thể thực hiện request nào trong đó nữa:

```
let request1 = books.add(book);

request1.onsuccess = function() {
  fetch('/').then(response => {
    let request2 = books.add(anotherBook); // (*)
    request2.onerror = function() {
      console.log(request2.error.name); // TransactionInactiveError
    };
  });
};
```

Điều đó là vì `fetch` là thao tác bất đồng bộ, một macrotask. Transactions đóng trước khi trình duyệt bắt đầu thực hiện các macrotask.

Những tác giả của đặc tả IndexedDB tin rằng transactions nên tồn tại ngắn. Phần lớn vì lý do hiệu năng.

Đặc biệt, các transaction `readwrite` "khóa" các store để ghi. Vì vậy nếu một phần của ứng dụng khởi tạo `readwrite` trên object store `books`, thì một phần khác muốn làm tương tự phải chờ: transaction mới "treo" cho đến khi cái đầu tiên hoàn tất. Điều đó có thể dẫn đến các độ trễ kỳ lạ nếu các transaction mất thời gian dài.

Vậy, làm gì bây giờ?

Trong ví dụ trên chúng ta có thể tạo `db.transaction` mới ngay trước request mới `(*)`.

Nhưng sẽ tốt hơn nữa, nếu chúng ta muốn giữ các thao tác cùng nhau trong một transaction, là tách biệt các transaction IndexedDB và các thứ bất đồng bộ "khác".

Trước tiên, thực hiện `fetch`, chuẩn bị dữ liệu nếu cần, sau đó tạo transaction và thực hiện tất cả các request cơ sở dữ liệu, khi đó sẽ hoạt động.

Để phát hiện thời điểm hoàn tất thành công, chúng ta có thể lắng nghe sự kiện `transaction.oncomplete`:

```
let transaction = db.transaction("books", "readwrite");

// ...perform operations...

transaction.oncomplete = function() {
  console.log("Transaction is complete");
};
```

Chỉ `complete` đảm bảo rằng transaction được lưu như một thể thống nhất. Các request riêng lẻ có thể thành công, nhưng thao tác ghi cuối cùng có thể gặp sự cố (ví dụ: lỗi I/O hoặc gì đó).

Để hủy bỏ thủ công transaction, gọi:

```
transaction.abort();
```

Điều đó hủy bỏ tất cả các thay đổi do các request trong đó thực hiện và kích hoạt sự kiện `transaction.onabort`.

## [Xử lý lỗi](#error-handling)

Các request ghi có thể thất bại.

Điều đó là điều dễ hiểu, không chỉ vì các lỗi có thể xảy ra phía chúng ta, mà còn vì những lý do không liên quan đến bản thân transaction. Ví dụ, hạn mức storage có thể bị vượt quá. Vì vậy chúng ta phải sẵn sàng xử lý trường hợp đó.

**Request thất bại sẽ tự động hủy bỏ transaction, hủy bỏ tất cả các thay đổi của nó.**

Trong một số tình huống, chúng ta có thể muốn xử lý sự cố (ví dụ: thử request khác), mà không hủy bỏ các thay đổi hiện có, và tiếp tục transaction. Điều đó hoàn toàn có thể. Handler `request.onerror` có thể ngăn transaction hủy bỏ bằng cách gọi `event.preventDefault()`.

Trong ví dụ bên dưới, một cuốn sách mới được thêm với cùng key (`id`) như cuốn hiện có. Phương thức `store.add` tạo ra `"ConstraintError"` trong trường hợp đó. Chúng ta xử lý nó mà không hủy bỏ transaction:

```
let transaction = db.transaction("books", "readwrite");

let book = { id: 'js', price: 10 };

let request = transaction.objectStore("books").add(book);

request.onerror = function(event) {
  // ConstraintError occurs when an object with the same id already exists
  if (request.error.name == "ConstraintError") {
    console.log("Book with such id already exists"); // handle the error
    event.preventDefault(); // don't abort the transaction
    // use another key for the book?
  } else {
    // unexpected error, can't handle it
    // the transaction will abort
  }
};

transaction.onabort = function() {
  console.log("Error", transaction.error);
};
```

### [ủy quyền sự kiện](#event-delegation)

Liệu chúng ta có cần onerror/onsuccess cho mỗi request? Không phải lúc nào cũng vậy. Chúng ta có thể dùng sự ủy quyền sự kiện thay thế.

**Các sự kiện IndexedDB lan truyền: `request` → `transaction` → `database`.**

Tất cả sự kiện đều là DOM event, có capturing và bubbling, nhưng thường chỉ dùng giai đoạn bubbling.

Vì vậy chúng ta có thể bắt tất cả các lỗi bằng handler `db.onerror`, để báo cáo hoặc cho các mục đích khác:

```
db.onerror = function(event) {
  let request = event.target; // the request that caused the error

  console.log("Error", request.error);
};
```

…Nhưng nếu lỗi đã được xử lý hoàn toàn thì sao? Trong trường hợp đó chúng ta không muốn báo cáo nó.

Chúng ta có thể dừng sự lan truyền và do đó `db.onerror` bằng cách dùng `event.stopPropagation()` trong `request.onerror`.

```
request.onerror = function(event) {
  if (request.error.name == "ConstraintError") {
    console.log("Book with such id already exists"); // handle the error
    event.preventDefault(); // don't abort the transaction
    event.stopPropagation(); // don't bubble error up, "chew" it
  } else {
    // do nothing
    // transaction will be aborted
    // we can take care of error in transaction.onabort
  }
};
```

## [Tìm kiếm](#searching)

Có hai loại tìm kiếm chính trong object store:

1. Theo giá trị key hoặc khoảng key. Trong storage "sách" của chúng ta, đó sẽ là giá trị hoặc khoảng giá trị của `book.id`.
2. Theo trường đối tượng khác, ví dụ `book.price`. Điều này yêu cầu một cấu trúc dữ liệu bổ sung, gọi là "index".

### [Theo key](#by-key)

Trước hết hãy xử lý loại tìm kiếm đầu tiên: theo key.

Các phương thức tìm kiếm hỗ trợ cả giá trị key chính xác và các "khoảng giá trị" – các đối tượng [IDBKeyRange](https://www.w3.org/TR/IndexedDB/#keyrange) chỉ định "khoảng key" chấp nhận được.

Các đối tượng `IDBKeyRange` được tạo bằng các lời gọi sau:

- `IDBKeyRange.lowerBound(lower, [open])` nghĩa là: `≥lower` (hoặc `>lower` nếu `open` là true)
- `IDBKeyRange.upperBound(upper, [open])` nghĩa là: `≤upper` (hoặc `<upper` nếu `open` là true)
- `IDBKeyRange.bound(lower, upper, [lowerOpen], [upperOpen])` nghĩa là: giữa `lower` và `upper`. Nếu cờ open là true, key tương ứng không được bao gồm trong khoảng.
- `IDBKeyRange.only(key)` – khoảng chỉ gồm một `key`, ít được dùng.

Chúng ta sẽ thấy các ví dụ thực tế sử dụng chúng ngay sau đây.

Để thực hiện tìm kiếm thực sự, có các phương thức sau. Chúng nhận đối số `query` có thể là key chính xác hoặc key range:

- `store.get(query)` – tìm giá trị đầu tiên theo key hoặc khoảng.
- `store.getAll([query], [count])` – tìm tất cả các giá trị, giới hạn bằng `count` nếu được chỉ định.
- `store.getKey(query)` – tìm key đầu tiên thỏa mãn truy vấn, thường là khoảng.
- `store.getAllKeys([query], [count])` – tìm tất cả các key thỏa mãn truy vấn, thường là khoảng, tối đa `count` nếu được chỉ định.
- `store.count([query])` – lấy tổng số key thỏa mãn truy vấn, thường là khoảng.

Ví dụ, chúng ta có rất nhiều sách trong store. Nhớ rằng trường `id` là key, vì vậy tất cả các phương thức này có thể tìm kiếm theo `id`.

Ví dụ request:

```
// get one book
books.get('js')

// get books with 'css' <= id <= 'html'
books.getAll(IDBKeyRange.bound('css', 'html'))

// get books with id < 'html'
books.getAll(IDBKeyRange.upperBound('html', true))

// get all books
books.getAll()

// get all keys, where id > 'js'
books.getAllKeys(IDBKeyRange.lowerBound('js', true))
```

Object store luôn được sắp xếp

Object store sắp xếp giá trị theo key bên trong.

Vì vậy các request trả về nhiều giá trị luôn trả về chúng theo thứ tự key đã sắp xếp.

### [Theo trường bằng index](#by-a-field-using-an-index)

Để tìm kiếm theo các trường đối tượng khác, chúng ta cần tạo một cấu trúc dữ liệu bổ sung gọi là "index".

Index là "phụ kiện" của store theo dõi một trường đối tượng cho trước. Với mỗi giá trị của trường đó, nó lưu danh sách các key của các đối tượng có giá trị đó. Sẽ có hình ảnh chi tiết hơn bên dưới.

Cú pháp:

```
objectStore.createIndex(name, keyPath, [options]);
```

- **`name`** – tên index,
- **`keyPath`** – đường dẫn đến trường đối tượng mà index nên theo dõi (chúng ta sắp tìm kiếm theo trường đó),
- **`option`** – đối tượng tùy chọn với các thuộc tính:
  - **`unique`** – nếu true, thì chỉ có thể có một đối tượng trong store với giá trị cho trước tại `keyPath`. Index sẽ thực thi điều đó bằng cách tạo lỗi nếu chúng ta cố thêm trùng lặp.
  - **`multiEntry`** – chỉ dùng nếu giá trị tại `keyPath` là mảng. Trong trường hợp đó, mặc định, index sẽ coi toàn bộ mảng là key. Nhưng nếu `multiEntry` là true, thì index sẽ giữ danh sách các đối tượng store cho mỗi giá trị trong mảng đó. Vậy các thành viên mảng trở thành keys của index.

Trong ví dụ của chúng ta, chúng ta lưu các cuốn sách theo key `id`.

Giả sử chúng ta muốn tìm kiếm theo `price`.

Trước tiên, chúng ta cần tạo index. Nó phải được thực hiện trong `upgradeneeded`, giống như object store:

```
openRequest.onupgradeneeded = function() {
  // we must create the index here, in versionchange transaction
  let books = db.createObjectStore('books', {keyPath: 'id'});
  let index = books.createIndex('price_idx', 'price');
};
```

- Index sẽ theo dõi trường `price`.
- Giá không duy nhất, có thể có nhiều cuốn sách cùng giá, vì vậy chúng ta không đặt tùy chọn `unique`.
- Giá không phải là mảng, vì vậy cờ `multiEntry` không áp dụng.

Hãy tưởng tượng kho của chúng ta có 4 cuốn sách. Đây là hình ảnh cho thấy chính xác index là gì:

![](/article/indexeddb/indexeddb-index.svg)

Như đã nói, index với mỗi giá trị của `price` (tham số thứ hai) giữ danh sách các key có giá đó.

Index tự động giữ cho nó luôn cập nhật, chúng ta không cần bận tâm về điều đó.

Giờ đây, khi chúng ta muốn tìm kiếm theo một giá cho trước, chúng ta chỉ cần áp dụng cùng các phương thức tìm kiếm vào index:

```
let transaction = db.transaction("books"); // readonly
let books = transaction.objectStore("books");
let priceIndex = books.index("price_idx");

let request = priceIndex.getAll(10);

request.onsuccess = function() {
  if (request.result !== undefined) {
    console.log("Books", request.result); // array of books with price=10
  } else {
    console.log("No such books");
  }
};
```

Chúng ta cũng có thể dùng `IDBKeyRange` để tạo khoảng và tìm kiếm sách rẻ/đắt:

```
// find books where price <= 5
let request = priceIndex.getAll(IDBKeyRange.upperBound(5));
```

Các index bên trong được sắp xếp theo trường đối tượng được theo dõi, trong trường hợp của chúng ta là `price`. Vì vậy khi chúng ta tìm kiếm, kết quả cũng được sắp xếp theo `price`.

## [Xóa khỏi store](#deleting-from-store)

Phương thức `delete` tìm các giá trị để xóa bằng truy vấn, định dạng gọi tương tự `getAll`:

- **`delete(query)`** – xóa các giá trị khớp theo truy vấn.

Ví dụ:

```
// delete the book with id='js'
books.delete('js');
```

Nếu chúng ta muốn xóa sách dựa trên giá hoặc một trường đối tượng khác, thì chúng ta nên trước tiên tìm key trong index, rồi gọi `delete`:

```
// find the key where price = 5
let request = priceIndex.getKey(5);

request.onsuccess = function() {
  let id = request.result;
  let deleteRequest = books.delete(id);
};
```

Để xóa mọi thứ:

```
books.clear(); // clear the storage.
```

## [Cursors](#cursors)

Các phương thức như `getAll/getAllKeys` trả về một mảng các keys/giá trị.

Nhưng object storage có thể rất lớn, lớn hơn bộ nhớ khả dụng. Khi đó `getAll` sẽ thất bại trong việc lấy tất cả các bản ghi thành mảng.

Xử lý thế nào?

Cursors cung cấp cách khắc phục điều đó.

***Cursor* là một đối tượng đặc biệt duyệt qua object storage, với một truy vấn cho trước, và trả về một key/value tại mỗi thời điểm, từ đó tiết kiệm bộ nhớ.**

Vì object store được sắp xếp bên trong theo key, cursor đi qua store theo thứ tự key (tăng dần mặc định).

Cú pháp:

```
// like getAll, but with a cursor:
let request = store.openCursor(query, [direction]);

// to get keys, not values (like getAllKeys): store.openKeyCursor
```

- **`query`** là key hoặc key range, giống như đối với `getAll`.
- **`direction`** là tham số tùy chọn, thứ tự nào để dùng:
  - `"next"` – mặc định, cursor đi lên từ bản ghi có key nhỏ nhất.
  - `"prev"` – thứ tự ngược lại: đi xuống từ bản ghi có key lớn nhất.
  - `"nextunique"`, `"prevunique"` – giống như trên, nhưng bỏ qua các bản ghi có cùng key (chỉ cho cursors trên index, ví dụ với nhiều cuốn sách có price=5 chỉ bản ghi đầu tiên được trả về).

**Sự khác biệt chính của cursor là `request.onsuccess` kích hoạt nhiều lần: một lần cho mỗi kết quả.**

Dưới đây là ví dụ cách sử dụng cursor:

```
let transaction = db.transaction("books");
let books = transaction.objectStore("books");

let request = books.openCursor();

// called for each book found by the cursor
request.onsuccess = function() {
  let cursor = request.result;
  if (cursor) {
    let key = cursor.key; // book key (id field)
    let value = cursor.value; // book object
    console.log(key, value);
    cursor.continue();
  } else {
    console.log("No more books");
  }
};
```

Các phương thức chính của cursor là:

- `advance(count)` – tiến cursor `count` lần, bỏ qua các giá trị.
- `continue([key])` – tiến cursor đến giá trị tiếp theo trong khoảng khớp (hoặc ngay sau `key` nếu được chỉ định).

Dù có thêm các giá trị khớp với cursor hay không – `onsuccess` vẫn được gọi, và rồi trong `result` chúng ta có thể lấy cursor trỏ đến bản ghi tiếp theo, hoặc `undefined`.

Trong ví dụ trên cursor được tạo cho object store.

Nhưng chúng ta cũng có thể tạo cursor trên index. Như chúng ta nhớ, index cho phép tìm kiếm theo trường đối tượng. Cursors trên index thực hiện đúng hệt như trên object stores – chúng tiết kiệm bộ nhớ bằng cách trả về một giá trị tại mỗi thời điểm.

Với cursors trên index, `cursor.key` là key của index (ví dụ: price), và chúng ta nên dùng thuộc tính `cursor.primaryKey` cho key của đối tượng:

```
let request = priceIdx.openCursor(IDBKeyRange.upperBound(5));

// called for each record
request.onsuccess = function() {
  let cursor = request.result;
  if (cursor) {
    let primaryKey = cursor.primaryKey; // next object store key (id field)
    let value = cursor.value; // next object store object (book object)
    let key = cursor.key; // next index key (price)
    console.log(key, value);
    cursor.continue();
  } else {
    console.log("No more books");
  }
};
```

## [Promise wrapper](#promise-wrapper)

Thêm `onsuccess/onerror` cho mỗi request là khá phiền phức. Đôi khi chúng ta có thể dễ dàng hơn bằng cách dùng sự ủy quyền sự kiện, ví dụ đặt handlers cho toàn bộ transactions, nhưng `async/await` thì tiện lợi hơn nhiều.

Hãy dùng một promise wrapper mỏng <https://github.com/jakearchibald/idb> trong phần còn lại của chương này. Nó tạo ra một đối tượng toàn cục `idb` với các phương thức IndexedDB [promisify](/promisify).

Rồi, thay vì `onsuccess/onerror` chúng ta có thể viết như thế này:

```
let db = await idb.openDB('store', 1, db => {
  if (db.oldVersion == 0) {
    // perform the initialization
    db.createObjectStore('books', {keyPath: 'id'});
  }
});

let transaction = db.transaction('books', 'readwrite');
let books = transaction.objectStore('books');

try {
  await books.add(...);
  await books.add(...);

  await transaction.complete;

  console.log('jsbook saved');
} catch(err) {
  console.log('error', err.message);
}
```

Vậy chúng ta có toàn bộ các thứ "mã async thuần" ngọt ngào và "try…catch".

### [Xử lý lỗi](#error-handling-2)

Nếu chúng ta không catch một lỗi, thì nó rơi xuyên qua, cho đến `try..catch` gần nhất bên ngoài.

Một lỗi không được catch trở thành sự kiện "unhandled promise rejection" trên đối tượng `window`.

Chúng ta có thể xử lý các lỗi như vậy như sau:

```
window.addEventListener('unhandledrejection', event => {
  let request = event.target; // IndexedDB native request object
  let error = event.reason; //  Unhandled error object, same as request.error
  ...report about the error...
});
```

### [Bẫy "transaction không hoạt động"](#inactive-transaction-pitfall)

Như chúng ta đã biết, transaction tự động commit ngay khi trình duyệt hoàn tất mã hiện tại và microtasks. Vì vậy nếu chúng ta đặt một *macrotask* như `fetch` ở giữa transaction, thì transaction sẽ không chờ nó hoàn tất. Nó chỉ tự động commit. Vì vậy request tiếp theo trong đó sẽ thất bại.

Với promise wrapper và `async/await`, tình huống cũng giống vậy.

Dưới đây là ví dụ `fetch` ở giữa transaction:

```
let transaction = db.transaction("inventory", "readwrite");
let inventory = transaction.objectStore("inventory");

await inventory.add({ id: 'js', price: 10, created: new Date() });

await fetch(...); // (*)

await inventory.add({ id: 'js', price: 10, created: new Date() }); // Error
```

`inventory.add` tiếp theo sau `fetch` `(*)` thất bại với lỗi "inactive transaction", vì transaction đã được commit và đóng vào thời điểm đó.

Cách khắc phục giống như khi làm việc với IndexedDB native: hoặc tạo transaction mới hoặc đơn giản tách các thứ ra.

1. Chuẩn bị dữ liệu và fetch tất cả những gì cần trước.
2. Rồi lưu vào cơ sở dữ liệu.

### [Lấy các đối tượng native](#getting-native-objects)

Bên trong, wrapper thực hiện một request IndexedDB native, thêm `onerror/onsuccess` vào nó, và trả về promise reject/resolve với kết quả.

Điều đó hoạt động tốt phần lớn thời gian. Các ví dụ nằm ở trang thư viện <https://github.com/jakearchibald/idb>.

Trong một vài trường hợp hiếm, khi chúng ta cần đối tượng `request` gốc, chúng ta có thể truy cập nó như thuộc tính `promise.request` của promise:

```
let promise = books.add(book); // get a promise (don't await for its result)

let request = promise.request; // native request object
let transaction = request.transaction; // native transaction object

// ...do some native IndexedDB voodoo...

let result = await promise; // if still needed
```

## [Tóm tắt](#summary)

Có thể coi IndexedDB là "localStorage tăng cường". Đó là cơ sở dữ liệu key-value đơn giản, đủ mạnh cho các ứng dụng offline, nhưng vẫn dễ sử dụng.

Cuốn sách hướng dẫn tốt nhất là đặc tả, [phiên bản hiện tại](https://www.w3.org/TR/IndexedDB-2/) là 2.0, nhưng một vài phương thức từ [3.0](https://w3c.github.io/IndexedDB/) (không khác biệt nhiều) được hỗ trợ một phần.

Cách sử dụng cơ bản có thể được mô tả bằng vài câu:

1. Lấy một promise wrapper như [idb](https://github.com/jakearchibald/idb).
2. Mở cơ sở dữ liệu: `idb.openDb(name, version, onupgradeneeded)`
   - Tạo object storages và indexes trong handler `onupgradeneeded` hoặc thực hiện cập nhật phiên bản nếu cần.
3. Đối với các request:
   - Tạo transaction `db.transaction('books')` (readwrite nếu cần).
   - Lấy object store `transaction.objectStore('books')`.
4. Sau đó, để tìm kiếm theo key, gọi các phương thức trực tiếp trên object store.
   - Để tìm kiếm theo trường đối tượng, tạo một index.
5. Nếu dữ liệu không vừa trong bộ nhớ, dùng cursor.

Dưới đây là một ứng dụng demo nhỏ:

Result

index.html

```
<!doctype html>
<script src="https://cdn.jsdelivr.net/npm/idb@3.0.2/build/idb.min.js"></script>

<button onclick="addBook()">Add a book</button>
<button onclick="clearBooks()">Clear books</button>

<p>Books list:</p>

<ul id="listElem"></ul>

<script>
let db;

init();

async function init() {
  db = await idb.openDb('booksDb', 1, db => {
    db.createObjectStore('books', {keyPath: 'name'});
  });

  list();
}

async function list() {
  let tx = db.transaction('books');
  let bookStore = tx.objectStore('books');

  let books = await bookStore.getAll();

  if (books.length) {
    listElem.innerHTML = books.map(book => `<li>
        name: ${book.name}, price: ${book.price}
      </li>`).join('');
  } else {
    listElem.innerHTML = '<li>No books yet. Please add books.</li>'
  }

}

async function clearBooks() {
  let tx = db.transaction('books', 'readwrite');
  await tx.objectStore('books').clear();
  await list();
}

async function addBook() {
  let name = prompt("Book name?");
  let price = +prompt("Book price?");

  let tx = db.transaction('books', 'readwrite');

  try {
    await tx.objectStore('books').add({name, price});
    await list();
  } catch(err) {
    if (err.name == 'ConstraintError') {
      alert("Such book exists already");
      await addBook();
    } else {
      throw err;
    }
  }
}

window.addEventListener('unhandledrejection', event => {
  alert("Error: " + event.reason.message);
});

</script>
```
