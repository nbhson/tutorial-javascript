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

### Quy tắc key: PHẢI là object
```js
wm.set({}, 'a');     // OK
wm.set([], 'b');     // OK
wm.set(null, 'c');   // TypeError
wm.set('str', 'd');  // TypeError
wm.set(123, 'e');    // TypeError
```

### API WeakMap
| Method | Mô tả |
|---|---|
| `set(key, value)` | Thêm entry |
| `get(key)` | Đọc value |
| `has(key)` | Kiểm tra tồn tại |
| `delete(key)` | Xóa entry |
| Keys iteration | Khong co |
| `.size` | Khong co |

## Điểm mạnh

- Khong gay memory leak — key duoc GC thu hoi tu dong
- Perfect cho private metadata attachment
- Khong enumerable — ben ngoai khong nhin thay
- Tu dong cleanup khi key khong con reference

## Bẫy thường gặp

- Khong iterate duoc — khong co keys()/values()/entries()
- Khong co .size property
- Key phai object — primitive khong duoc
- Entry bi GC khi key khong con referenced

## Khi nao dung

- Private data cho class instances (trước #private)
- Cache metadata attach to DOM nodes
- Event handler registry (avoid leaks)
- Weak reference caching

## Vi du

```js
// Private field simulation (trước ES2022 #private)
class Widget {
  #data = new WeakMap();
  constructor(el) {
    this.#data.set(el, { created: Date.now(), visible: true });
  }
  getCreated(el) { return this.#data.get(el)?.created; }
  isVisible(el) { return this.#data.get(el)?.visible; }
  setVisible(el, val) {
    const d = this.#data.get(el);
    if (d) d.visible = val;
  }
}

// DOM node metadata — tu GC khi node remove
const nodeData = new WeakMap();
document.querySelectorAll('.item').forEach(el => {
  nodeData.set(el, { clickCount: 0, createdAt: Date.now() });
  el.addEventListener('click', () => {
    const d = nodeData.get(el);
    if (d) d.clickCount++;
  });
});
// Khi el bi remove tu DOM va khong con ref -> entry tu GC
```

## Lien ket cheo

- Xem: `03_data-structures/02_keyed-collections/01_map` (Map strong refs)
- Xem: `03_data-structures/02_keyed-collections/04_weakset` (WeakSet)
- Xem: `17_memory-management/01_memory-lifecycle-gc` (GC principles)
