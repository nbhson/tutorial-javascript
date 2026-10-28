# WeakMap — Dictionary Với Object Keys Yếu

> WeakMap: key là object, reference yếu -> GC có thể thu hồi. Không iterable.

## Khái niệm cốt lõi

WeakMap lưu key-value với **weak reference** — nếu key không còn được tham chiếu elsewhere, GC có thể thu hồi cả entry.

```js
const wm = new WeakMap();
const obj = { name: 'test' };
wm.set(obj, 'secret');
// khi obj bị GC, wm[obj] tự động biến mất
```

Hãy hình dung: Map thường là "bộ nhớ ngoài" giữ chặt mọi key bạn từng set — kể cả khi phần còn lại của chương trình đã quên object đó. WeakMap thì ngược lại: nó chỉ "bám theo" object **khi object còn sống**. Bạn không phải tự viết hàm dọn cache — GC dọn hộ bạn.

### Quy tắc key: PHẢI là object

```js
wm.set({}, 'a');     // OK
wm.set([], 'b');     // OK
wm.set(null, 'c');   // TypeError
wm.set('str', 'd');  // TypeError
wm.set(123, 'e');    // TypeError
```

Lý do thiết kế: nếu cho phép key primitive, bạn phải so sánh theo giá trị — nhưng khi đó phải có cách liệt kê key để tìm giá trị, tức là phải giữ strong reference, phủ định luôn ý nghĩa "weak". Đó cũng là lý do WeakMap không có `keys()`, `size`, không iterate được.

### API WeakMap

| Method | Mô tả |
|---|---|
| `set(key, value)` | Thêm entry |
| `get(key)` | Đọc value |
| `has(key)` | Kiểm tra tồn tại |
| `delete(key)` | Xóa entry |
| Keys iteration | Không có |
| `.size` | Không có |

## Điểm mạnh

- Không gây memory leak — key được GC thu hồi tự động
- Perfect cho private metadata attachment
- Không enumerable — bên ngoài không nhìn thấy
- Tự động cleanup khi key không còn reference

## Bẫy thường gặp

- Không iterate được — không có keys()/values()/entries()
- Không có .size property
- Key phải object — primitive không được
- Entry bị GC khi key không còn referenced
- **Value có thể giữ strong ref ngược lại key**: `wm.set(obj, {parent: obj})` — nếu value (hoặc closure bắt nó) tham chiếu key, object vẫn sống. WeakMap chỉ làm key yếu, không làm value yếu.
- **Object literal inline làm key là bẫy kinh điển**: `wm.get({id: 1})` luôn undefined vì mỗi `{}` là object mới.

```js
// Bẫy: set bằng object tạm, get bằng object tạm khác
const wm = new WeakMap();
wm.set({ id: 1 }, "data");
wm.get({ id: 1 }); // undefined — 2 object khác reference!
```

## Khi nào dùng

- Private data cho class instances (trước #private của ES2022)
- Cache metadata attach to DOM nodes
- Event handler registry (avoid leaks)
- Weak reference caching

## Ví dụ 1: Private field simulation (trước ES2022 #private)

```js
const privateData = new WeakMap(); // ngoài module scope, không ai chạm được

class BankAccount {
  constructor(owner, balance) {
    privateData.set(this, { owner, balance }); // "private" thật sự
  }
  deposit(amount) {
    const d = privateData.get(this);
    d.balance += amount;
  }
  get balance() {
    return privateData.get(this).balance;
  }
}

const acc = new BankAccount("Sơn", 1000);
console.log(acc.balance);          // 1000
console.log(acc.owner);            // undefined — không lộ qua property
// JSON.stringify(acc)             // {} — không serialize được private data
```

Ngày nay bạn nên dùng `#balance` (ES2022 private field) — nhưng WeakMap vẫn có ưu điểm riêng: **có thể truy cập từ ngoài class** (ví dụ trong hàm helper/debug) mà `#field` thì không.

## Ví dụ 2: DOM node metadata — tự GC khi node remove

```js
// DOM node metadata — tự GC khi node remove
const nodeData = new WeakMap();
document.querySelectorAll('.item').forEach(el => {
  nodeData.set(el, { clickCount: 0, createdAt: Date.now() });
  el.addEventListener('click', () => {
    const d = nodeData.get(el);
    if (d) d.clickCount++;
  });
});
// Khi el bị remove từ DOM và không còn ref -> entry tự GC
```

Đây là use case quan trọng nhất trong frontend: bạn gắn trạng thái vào từng DOM node mà không cần quan tâm node bị remove lúc nào. Nếu thay WeakMap bằng Map hoặc gắn trực tiếp property lên node, app SPA chạy lâu ngày sẽ rò rỉ bộ nhớ.

⚠️ Lưu ý tinh tế: nếu bạn giữ listener trên node nhưng node vẫn nằm trong DOM, node vẫn sống — điều đó bình thường. WeakMap chỉ giúp khi node đã bị remove khỏi DOM.

## Ví dụ 3: Event handler registry — tránh rò rỉ qua listener

```js
// Vấn đề: listener giữ closure -> closure giữ object -> object không bao giờ GC
const handlers = new WeakMap();

function bind(el, handler) {
  const wrapped = (e) => handler(e);
  handlers.set(el, wrapped);   // tra ngược được wrapped khi cần removeEventListener
  el.addEventListener("click", wrapped);
}

function unbind(el) {
  const wrapped = handlers.get(el);
  if (wrapped) el.removeEventListener("click", wrapped);
  handlers.delete(el);
}
```

Nếu `handlers` là Map thường, mỗi listener đã unbind vẫn nằm trong Map mãi. WeakMap cho phép pattern "bind/unbind đối xứng" mà không cần tự quản lý vòng đời.

## Ví dụ 4: Cache theo object — memoize không rò rỉ

```js
// Cache kết quả tính toán nặng theo object input
const analysisCache = new WeakMap();

function analyze(user) {
  if (analysisCache.has(user)) return analysisCache.get(user);
  const result = /* tính toán nặng theo user */ { score: Math.random() };
  analysisCache.set(user, result);
  return result;
}
// Khi user object bị thay bằng bản mới (state update), cache cũ tự GC.
// Với Map thường, cache sẽ phình vô hạn theo số "user" từng xuất hiện.
```

So sánh trực tiếp Map vs WeakMap cho cache:

| | Map làm cache | WeakMap làm cache |
|---|---|---|
| Cache hit giữa các lần gọi | Có | Có (nếu key còn sống) |
| Bộ nhớ khi key hết dùng | Tăng vô hạn (cần LRU/TTL thủ công) | Tự co lại theo GC |
| Phù hợp | Cache theo string key (URL, id) | Cache theo object sống cùng app |

## Ví dụ 5: Khi nào KHÔNG nên dùng WeakMap

```js
// ❌ Cần duyệt tất cả entries? WeakMap không làm được.
// Ví dụ: "tìm node có clickCount cao nhất" — với WeakMap bạn không liệt kê được key.
// → Cần Map + hàm cleanup thủ công, hoặc cấu trúc dữ liệu khác.

// ❌ Cần biết có bao nhiêu entry (.size)? Không có.

// ❌ Key là primitive (string id)? TypeError.
// → Dùng Map.
```

## Ghi chú: WeakRef & FinalizationRegistry

WeakMap là một thành viên trong "họ weak reference" của JS. Hai thành viên còn lại — `WeakRef` và `FinalizationRegistry` (ES2021) — được trình bày trong overview của nhóm này (`03_data-structures/02_keyed-collections/README.md`) và trong mirror js-info (`js-info/vi/14_misc/weakref-finalizationregistry/`). Tóm tắt: WeakMap gắn dữ liệu vào object; WeakRef giữ tham chiếu yếu để "nhìn xem object còn sống không"; FinalizationRegistry nhận callback khi object bị GC. Với công việc hằng ngày, WeakMap chiếm ~95% nhu cầu.

## Checklist tự kiểm tra

- [ ] Giải thích được vì sao WeakMap key chỉ được là object
- [ ] Biết WeakMap không iterate được và không có .size — và vì sao (thiết kế, không phải thiếu sót)
- [ ] Chỉ ra được memory leak khi dùng Map cho DOM node metadata
- [ ] Hiểu value vẫn có thể giữ strong ref ngược lại key
- [ ] Biết khi nào dùng `#private field` thay vì WeakMap

## Liên kết chéo

- Xem: `03_data-structures/02_keyed-collections/01_map` (Map strong refs)
- Xem: `03_data-structures/02_keyed-collections/04_weakset` (WeakSet)
- Xem: `17_memory-management/01_memory-lifecycle-gc` (GC principles)
- Xem: `14_classes/` (private field `#` — giải pháp hiện đại cho private data)
- Tài liệu: [MDN — WeakMap](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakMap)
