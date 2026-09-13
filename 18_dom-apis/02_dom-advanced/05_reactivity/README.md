# Reactivity — Tự Động Đồng Bộ Dữ Liệu ↔ Giao Diện — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**Reactivity** là khả năng hệ thống **tự theo dõi sự thay đổi của dữ liệu** và **tự cập nhật giao diện** tương ứng — bạn không phải gọi tay "sửa DOM lại" sau mỗi lần đổi state. Mức độ reactivity khác nhau giữa các cách tiếp cận:

### Các mức reactivity

| Mức | Cơ chế | Tự động update UI? | Performance | Framework example |
|---|---|---|---|---|
| **DOM Manipulation** | Thủ công | ❌ Không — developer phải gọi tay `el.textContent = ...` | ⭐⭐⭐ Fastest | jQuery, vanilla JS |
| **Shadow DOM** | Encapsulated subtree | ❌ Không tự động — cần manual update | ⭐⭐⭐ Fast | Web Components |
| **Virtual DOM** | Diff + patch tree | ✅ Có — framework auto diff | ⭐⭐ Medium | React, Preact |
| **Proxy Reactivity** | Trap set/get trên object | ✅ Có — fine-grained update | ⭐⭐ Medium | Vue 2, Polymer |
| **Signals** | Dependency tracking | ✅ Có — most granular | ⭐⭐⭐ Fast | Solid, Svelte, Vue 3 |

### Proxy-based reactivity — cơ chế then chốt

Đoạn code trong thư mục minh họa một **reactive counter** bằng `Proxy`:

- `state` là `new Proxy({ count: 0 }, { set })`.
- Trong trap `set`: gán `target[key] = value` **và trực tiếp** `document.getElementById('counter').innerText = ...`.
- Click nút → `state.count += 1` → trap `set` chạy → UI tự đổi.

**Flow**: User action → modify proxy state → `set` trap fires → read new value → update DOM directly.

### So sánh Virtual DOM vs Proxy Reactivity

| Aspect | Virtual DOM (React) | Proxy Reactivity (Vue 2) |
|---|---|---|
| Update strategy | Re-create whole VTree, diff, patch | Trap set, update only dependent DOM |
| Granularity | Component level | Property level (fine-grained) |
| Overhead | Diff + patch cost | Proxy access cost per property |
| Learning curve | Lower | Higher (understanding traps) |
| Debug difficulty | Easier (clear render cycle) | Harder (implicit updates) |

Tóm lược: *DOM thực = reactivity thấp (thao tác tay)*; *Virtual DOM = reactivity cao (tự diff/patch)*; *Proxy = nền tảng reactivity "fine-grained" dùng trong Vue/Polymer*.

## 📐 Cấu trúc / Cú pháp

### Basic reactive proxy
```js
const state = new Proxy(
  { count: 0 },
  {
    set(target, key, value) {
      target[key] = value;                            // lưu state
      document.getElementById('counter').innerText =
        `Số lần click: ${value}`;                     // tự cập nhật UI
      return true;                                    // báo gán thành công
    },
  }
);

document.getElementById('clickButton')
  .addEventListener('click', () => { state.count += 1; });  // UI tự đổi
```

### Multi-property reactivity
```js
const state = new Proxy({ count: 0, name: 'App' }, {
  set(target, key, value) {
    target[key] = value;
    
    // Update all dependent UI elements
    const countEl = document.getElementById('counter');
    const nameEl = document.getElementById('name-display');
    
    if (countEl) countEl.textContent = `Count: ${target.count}`;
    if (nameEl) nameEl.textContent = `Name: ${target.name}`;
    
    return true;
  }
});
```

### Computed property via getter
```js
const person = { firstName: 'Nguyễn', lastName: 'Sơn' };
const proxy = new Proxy(person, {
  get(target, key) {
    if (key === 'fullName') {
      return `${target.firstName} ${target.lastName}`; // computed on-the-fly
    }
    return Reflect.get(target, key);
  }
});
console.log(proxy.fullName); // "Nguyễn Sơn" — computed, không lưu storage
```

## ✅ Điểm mạnh

1. **Tự động** — UI luôn khớp state, không quên cập nhật, không sai lệch chỗ này chỗ kia.
2. **Giảm code thao tác tay** — bớt boilerplate DOM update lặp lại.
3. **Hiệu năng tốt hơn** với Virtual DOM: chỉ patch phần thực sự đổi (fine-grained).
4. **Proxy không xâm lấn** — đọc/ghi qua state như bình thường, trap làm phần "phản ứng".
5. **Nền tảng của framework hiện đại** — nắm reactivity là hiểu được Vue/Polymer/Svelte.
6. **Debug traceable** — mỗi lần set chạy, có thể log state change dễ dàng.
7. **Composeable** — nhiều proxy nested, computed properties, watchers.
8. **No reconciliation needed** — không cần diff tree, update trực tiếp target DOM node.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Proxy có overhead nhỏ** mỗi lần truy cập và `set` phải `return true` (nếu `false` → gán coi như thất bại).
2. **`Array` qua Proxy cũng bắt được nhưng cần xử lý riêng** (chỉ số, push) — dễ bỏ sót.
3. **Reactivity không miễn phí** — việc re-render quá rộng (diff cả cây) vẫn tốn chi phí ở app lớn.
4. **Khó gỡ lỗi** khi "tự cập nhật" vô hình trung — cần tooling như Vue devtools để nhìn nguồn.
5. **Đừng nhầm reactivity "tự cập nhật" với hiệu năng tự nhiên** — vẫn phải tối ưu đúng chỗ.
6. **Proxy không work với primitive direct** — phải wrap trong object: `new Proxy({ value: 0 }, ...)` not `new Proxy(0, ...)`.
7. **Nested object requires deep proxy** — proxy chỉ trap ở top-level, nested object cần recursive proxy.
8. **Serialization issues** — `JSON.stringify(proxy)` không stringify trap properly — cần `.toJSON()` method.

## 💡 Khi nào dùng — Tình huống thực tến

1. **Ứng dụng có nhiều state** và nhiều nơi phụ thuộc vào state đó (user login, cart, form liên quan).
2. **Chọn framework**: cần reactivity cao → React/Vue (Virtual DOM) hoặc Vue/Polymer (Proxy).
3. **Widget nhỏ cần tự cập nhật** — dùng một `Proxy` reactive thay vì rải `document.getElementById` khắp nơi.
4. **Muốn theo dõi sự thay đổi của một object cụ thể** (log, trigger fetch, save).
5. **Học nền tảng để hiểu cơ chế two-way/tracked state** của các framework.
6. **Audit/logging data changes** — proxy log mọi change vào console/history.
7. **Form state management** — reactive form state tự validate và update UI.
8. **Real-time dashboard** — data changes → UI updates automatically.

## 🎯 Ví dụ minh họa

### Ví dụ 1: Reactive counter cơ bản
```js
const state = new Proxy(
  { count: 0 },
  {
    set(target, key, value) {
      target[key] = value;
      document.getElementById('counter').innerText = `Số lần click: ${value}`;
      return true;
    },
  }
);

document.getElementById('clickButton').addEventListener('click', () => {
  state.count += 1;
});
```

### Ví dụ 2: Multi-target reactive state
```js
const state = new Proxy({ count: 0, name: 'App' }, {
  set(target, key, value) {
    target[key] = value;
    const countEl = document.getElementById('counter');
    const nameEl = document.getElementById('name-display');
    if (countEl) countEl.textContent = `Count: ${target.count}`;
    if (nameEl) nameEl.textContent = `Name: ${target.name}`;
    return true;
  }
});
```

### Ví dụ 3: Validation via proxy set trap
```js
const user = new Proxy(
  { email: '', password: '' },
  {
    set(target, key, value) {
      if (key === 'email' && !value.includes('@')) {
        throw new TypeError('Email phải chứa @');
      }
      if (key === 'password' && value.length < 6) {
        throw new TypeError('Mật khẩu tối thiểu 6 ký tự');
      }
      target[key] = value;
      updateValidationUI(key, value);
      return true;
    }
  }
);
```

### Ví dụ 4: Computed property proxy
```js
const person = { firstName: 'Nguyễn', lastName: 'Sơn', age: 25 };
const proxy = new Proxy(person, {
  get(target, key) {
    if (key === 'fullName') return `${target.firstName} ${target.lastName}`;
    if (key === 'isAdult') return target.age >= 18;
    return Reflect.get(target, key);
  },
  set(target, key, value) {
    const result = Reflect.set(target, key, value);
    if (key === 'firstName' || key === 'lastName') {
      console.log('fullName changed to:', `${target.firstName} ${target.lastName}`);
    }
    return result;
  }
});
```

### Ví dụ 5: Observable pattern với Proxy
```js
function createObservable(initialState) {
  const state = { ...initialState };
  const subscribers = new Set();
  
  return new Proxy(state, {
    set(target, key, value) {
      const oldVal = target[key];
      target[key] = value;
      if (oldVal !== value) {
        subscribers.forEach(fn => fn(key, value, oldVal));
      }
      return true;
    },
    subscribe(fn) {
      subscribers.add(fn);
      return () => subscribers.delete(fn);
    }
  });
}

const observable = createObservable({ count: 0, theme: 'light' });
observable.subscribe((key, newValue, oldValue) => {
  console.log(`${key}: ${oldValue} → ${newValue}`);
});
observable.count++; // logs: "count: 0 → 1"
```

### Ví dụ 6: Reactive list
```js
const listState = new Proxy({ items: [] }, {
  set(target, key, value) {
    if (key === 'items' && Array.isArray(value)) {
      target[key] = value;
      renderList(value);
    } else {
      target[key] = value;
    }
    return true;
  }
});

function renderList(items) {
  const ul = document.getElementById('list');
  ul.innerHTML = items.map(item => `<li>${item}</li>`).join('');
}

listState.items = ['Apple', 'Banana', 'Cherry'];
```

### Ví dụ 7: Form reactive state
```js
const formState = new Proxy(
  { username: '', email: '', errors: {} },
  {
    set(target, key, value) {
      target[key] = value;
      if (key === 'email') {
        target.errors.email = value.includes('@') ? '' : 'Email invalid';
      }
      if (key === 'username') {
        target.errors.username = value.length >= 3 ? '' : 'Username tối thiểu 3 ký tự';
      }
      updateErrorDisplay(target.errors);
      return true;
    }
  }
);
```

### Ví dụ 8: So sánh với Virtual DOM approach
```js
// Proxy Reactivity (direct DOM update)
const proxyState = new Proxy({ count: 0 }, {
  set(target, key, value) {
    target[key] = value;
    document.getElementById('counter').textContent = value;
    return true;
  }
});

// Virtual DOM (diff + patch)
let vdState = { count: 0 };
function render() {
  const vNode = { tag: 'p', children: [`Count: ${vdState.count}`] };
  const patch = diff(oldVNode, vNode);
  applyPatch(document.getElementById('counter'), patch);
  oldVNode = vNode;
}
// Proxy: 1 DOM operation. VDOM: create VNode → diff → patch (3 steps)
```

## 🔬 So sánh với alternatives

| Approach | Automation | Granularity | Performance | Complexity |
|---|---|---|---|---|
| **DOM Manipulation** | ❌ Manual | N/A | ⭐⭐⭐ Fastest | Thấp |
| **Virtual DOM** | ✅ Auto diff/patch | Component level | ⭐⭐ Medium | Trung bình |
| **Shadow DOM** | ❌ Manual update | Component level | ⭐⭐⭐ Fast | Trung bình |
| **Proxy Reactivity** | ✅ Auto via traps | Property level | ⭐⭐ Medium | Cao |
| **Signals** | ✅ Auto tracking | Individual binding | ⭐⭐⭐ Fast | Cao |

## 📊 Performance & Best Practices

- **Proxy overhead**: mỗi access qua proxy ~10-100ns thêm — chấp nhận được cho hầu hết apps.
- **Deep proxy caution**: recursive proxy creation expensive — chỉ proxy level cần thiết.
- **Avoid proxy in hot loops**: nếu vòng lặp chạy hàng ngàn lần/giây, direct access nhanh hơn.
- **Return true from set**: bắt buộc để proxy set hoạt động đúng — false = silent failure.
- **Combine with requestAnimationFrame**: batch DOM updates trong animation frame.
- **Use WeakMap for metadata**: attach reactive metadata không gây memory leak.
- **Test trap return values**: đảm bảo set trap luôn return true (hoặc throw có nghĩa).

## 🔗 Liên kết chéo

- Xem thêm: `17_memory-management/04_meta-programming/` — Proxy/Reflect fundamentals.
- Xem thêm: `18_dom-apis/02_dom-advanced/03_virtual-dom/` — Virtual DOM so với Proxy reactivity.
- Xem thêm: `18_dom-apis/02_dom-advanced/` — DOM advanced concepts overview.
- Xem thêm: `17_memory-management/03_v8-engine/` — hidden class impact khi dùng Proxy.
