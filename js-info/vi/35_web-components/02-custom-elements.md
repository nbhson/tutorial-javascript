# Custom elements (Yếu tố tùy chỉnh)

> Source: [https://javascript.info/custom-elements](https://javascript.info/custom-elements)

<!-- fetched: 2026-09-14 -->

Chúng ta có thể tạo các phần tử HTML tùy chỉnh, được mô tả bởi class của chúng ta, với các phương thức và thuộc tính riêng, events và nhiều hơn nữa.

Một khi custom element được định nghĩa, chúng ta có thể sử dụng nó ngang hàng với các phần tử HTML tích hợp sẵn.

Điều đó rất tuyệt, vì từ điển HTML phong phú nhưng không vô hạn. Không có `<easy-tabs>`, `<sliding-carousel>`, `<beautiful-upload>`… Hãy nghĩ đến bất kỳ thẻ nào khác mà chúng ta có thể cần.

Chúng ta có thể định nghĩa chúng bằng một class đặc biệt, và sau đó sử dụng chúng như thể chúng luôn là một phần của HTML.

Có hai loại custom element:

1. **Autonomous custom elements** – các phần tử “hoàn toàn mới”, kế thừa từ class trừu tượng `HTMLElement`.
2. **Customized built-in elements** – kế thừa các phần tử tích hợp sẵn, ví dụ như một nút tùy chỉnh, dựa trên `HTMLButtonElement`, v.v.

Trước tiên chúng ta sẽ tìm hiểu các phần tử autonomous, sau đó chuyển sang các phần tử built-in đã được tùy chỉnh.

Để tạo một custom element, chúng ta cần cho trình duyệt biết một số chi tiết về nó: cách hiển thị nó, phải làm gì khi phần tử được thêm hoặc xóa khỏi trang, v.v.

Điều đó được thực hiện bằng cách tạo một class với các phương thức đặc biệt. Điều đó đơn giản vì chỉ có một vài phương thức, và tất cả chúng đều là tùy chọn.

Dưới đây là bản phác thảo với danh sách đầy đủ:

```
class MyElement extends HTMLElement {
  constructor() {
    super();
    // element created
  }

  connectedCallback() {
    // browser calls this method when the element is added to the document
    // (can be called many times if an element is repeatedly added/removed)
  }

  disconnectedCallback() {
    // browser calls this method when the element is removed from the document
    // (can be called many times if an element is repeatedly added/removed)
  }

  static get observedAttributes() {
    return [/* array of attribute names to monitor for changes */];
  }

  attributeChangedCallback(name, oldValue, newValue) {
    // called when one of attributes listed above is modified
  }

  adoptedCallback() {
    // called when the element is moved to a new document
    // (happens in document.adoptNode, very rarely used)
  }

  // there can be other element methods and properties
}
```

Sau đó, chúng ta cần đăng ký phần tử:

```
// let the browser know that <my-element> is served by our new class
customElements.define("my-element", MyElement);
```

Giờ đây, với bất kỳ phần tử HTML nào có thẻ `<my-element>`, một instance của `MyElement` sẽ được tạo ra, và các phương thức được nêu ở trên sẽ được gọi. Chúng ta cũng có thể `document.createElement('my-element')` trong JavaScript.

Tên custom element phải chứa dấu gạch nối `-`

Tên custom element phải có dấu gạch nối `-`, ví dụ `my-element` và `super-button` là các tên hợp lệ, nhưng `myelement` thì không.

Điều đó nhằm đảm bảo rằng không có xung đột tên giữa các phần tử HTML tích hợp sẵn và tùy chỉnh.

## [Ví dụ: “time-formatted”](#example-time-formatted)

Ví dụ, trong HTML đã tồn tại phần tử `<time>`, dành cho ngày giờ. Nhưng nó không tự động định dạng gì cả.

Hãy tạo phần tử `<time-formatted>` hiển thị thời gian theo định dạng đẹp, hỗ trợ ngôn ngữ:

```
<script>
class TimeFormatted extends HTMLElement { // (1)

  connectedCallback() {
    let date = new Date(this.getAttribute('datetime') || Date.now());

    this.innerHTML = new Intl.DateTimeFormat("default", {
      year: this.getAttribute('year') || undefined,
      month: this.getAttribute('month') || undefined,
      day: this.getAttribute('day') || undefined,
      hour: this.getAttribute('hour') || undefined,
      minute: this.getAttribute('minute') || undefined,
      second: this.getAttribute('second') || undefined,
      timeZoneName: this.getAttribute('time-zone-name') || undefined,
    }).format(date);
  }

}

customElements.define("time-formatted", TimeFormatted); // (2)
</script>

<!-- (3) -->
<time-formatted datetime="2019-12-01"
  year="numeric" month="long" day="numeric"
  hour="numeric" minute="numeric" second="numeric"
  time-zone-name="short"
></time-formatted>
```

1. Class chỉ có một phương thức `connectedCallback()` – trình duyệt gọi nó khi phần tử `<time-formatted>` được thêm vào trang (hoặc khi trình phân tích HTML phát hiện nó), và nó sử dụng trình định dạng dữ liệu tích hợp sẵn [Intl.DateTimeFormat](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DateTimeFormat), được hỗ trợ tốt trên các trình duyệt, để hiển thị thời gian định dạng đẹp.
2. Chúng ta cần đăng ký phần tử mới bằng `customElements.define(tag, class)`.
3. Và sau đó chúng ta có thể sử dụng nó ở mọi nơi.

Nâng cấp custom element

Nếu trình duyệt gặp bất kỳ phần tử `<time-formatted>` nào trước `customElements.define`, đó không phải là một lỗi. Nhưng phần tử vẫn chưa được biết đến, giống như bất kỳ thẻ nào không chuẩn.

Các phần tử “undefined” như vậy có thể được định style bằng CSS selector `:not(:defined)`.

Khi `customElement.define` được gọi, chúng được “nâng cấp”: một instance mới của `TimeFormatted` được tạo cho mỗi phần tử, và `connectedCallback` được gọi. Chúng trở thành `:defined`.

Để lấy thông tin về các custom element, có các phương thức:

- `customElements.get(name)` – trả về class của custom element với `name` cho trước,
- `customElements.whenDefined(name)` – trả về một promise sẽ resolve (không có giá trị) khi custom element với `name` cho trước trở thành đã định nghĩa.

Render trong `connectedCallback`, không phải trong `constructor`

Trong ví dụ trên, nội dung phần tử được render (tạo) trong `connectedCallback`.

Tại sao không phải trong `constructor`?

Lý do đơn giản là: khi `constructor` được gọi, nó vẫn còn quá sớm. Phần tử được tạo ra, nhưng trình duyệt vẫn chưa xử lý/gán attributes ở giai đoạn này: các lời gọi `getAttribute` sẽ trả về `null`. Vì vậy chúng ta thực sự không thể render ở đó.

Ngoài ra, nếu bạn nghĩ về điều đó, về hiệu suất thì tốt hơn – trì hoãn công việc cho đến khi thực sự cần.

`connectedCallback` được kích hoạt khi phần tử được thêm vào document. Không chỉ được thêm vào một phần tử khác như con, mà thực sự trở thành một phần của trang. Vì vậy chúng ta có thể xây dựng DOM rời, tạo các phần tử và chuẩn bị chúng cho việc sử dụng sau này. Chúng chỉ thực sự được render khi chúng xuất hiện trên trang.

## [Quan sát attributes](#observing-attributes)

Trong triển khai hiện tại của `<time-formatted>`, sau khi phần tử được render, các thay đổi attribute tiếp theo không có tác dụng gì. Điều đó lạ đối với một phần tử HTML. Thông thường, khi chúng ta thay đổi một attribute, như `a.href`, chúng ta mong đợi thay đổi được hiển thị ngay lập tức. Vì vậy hãy sửa điều này.

Chúng ta có thể quan sát attributes bằng cách cung cấp danh sách của chúng trong static getter `observedAttributes()`. Đối với các attribute đó, `attributeChangedCallback` được gọi khi chúng bị thay đổi. Nó không được kích hoạt cho các attribute khác không được liệt kê (đó là vì lý do hiệu suất).

Dưới đây là `<time-formatted>` mới, tự động cập nhật khi attributes thay đổi:

```
<script>
class TimeFormatted extends HTMLElement {

  render() { // (1)
    let date = new Date(this.getAttribute('datetime') || Date.now());

    this.innerHTML = new Intl.DateTimeFormat("default", {
      year: this.getAttribute('year') || undefined,
      month: this.getAttribute('month') || undefined,
      day: this.getAttribute('day') || undefined,
      hour: this.getAttribute('hour') || undefined,
      minute: this.getAttribute('minute') || undefined,
      second: this.getAttribute('second') || undefined,
      timeZoneName: this.getAttribute('time-zone-name') || undefined,
    }).format(date);
  }

  connectedCallback() { // (2)
    if (!this.rendered) {
      this.render();
      this.rendered = true;
    }
  }

  static get observedAttributes() { // (3)
    return ['datetime', 'year', 'month', 'day', 'hour', 'minute', 'second', 'time-zone-name'];
  }

  attributeChangedCallback(name, oldValue, newValue) { // (4)
    this.render();
  }

}

customElements.define("time-formatted", TimeFormatted);
</script>

<time-formatted id="elem" hour="numeric" minute="numeric" second="numeric"></time-formatted>

<script>
setInterval(() => elem.setAttribute('datetime', new Date()), 1000); // (5)
</script>
```

1. Logic render được chuyển vào phương thức helper `render()`.
2. Chúng ta gọi nó một lần khi phần tử được chèn vào trang.
3. Đối với sự thay đổi của một attribute được liệt kê trong `observedAttributes()`, `attributeChangedCallback` được kích hoạt.
4. …và render lại phần tử.
5. Cuối cùng, chúng ta có thể dễ dàng tạo một đồng hồ trực tiếp.

## [Thứ tự render](#rendering-order)

Khi trình phân tích HTML xây dựng DOM, các phần tử được xử lý lần lượt, cha trước con. Ví dụ nếu chúng ta có `<outer><inner></inner></outer>`, thì phần tử `<outer>` được tạo và kết nối với DOM trước, sau đó mới đến `<inner>`.

Điều đó dẫn đến những hệ quả quan trọng đối với custom elements.

Ví dụ, nếu một custom element cố truy cập `innerHTML` trong `connectedCallback`, nó sẽ không nhận được gì:

```
<script>
customElements.define('user-info', class extends HTMLElement {

  connectedCallback() {
    alert(this.innerHTML); // empty (*)
  }

});
</script>

<user-info>John</user-info>
```

Nếu bạn chạy, `alert` sẽ trống.

Điều đó đúng là vì ở giai đoạn đó chưa có con nào cả, DOM chưa hoàn thành. Trình phân tích HTML đã kết nối custom element `<user-info>`, và sắp tiếp tục với các con của nó, nhưng chỉ là vẫn chưa.

Nếu chúng ta muốn truyền thông tin đến custom element, chúng ta có thể sử dụng attributes. Chúng luôn có sẵn ngay lập tức.

Hoặc, nếu thực sự cần các phần con, chúng ta có thể trì hoãn việc truy cập chúng bằng `setTimeout` không độ trễ.

Điều này hoạt động:

```
<script>
customElements.define('user-info', class extends HTMLElement {

  connectedCallback() {
    setTimeout(() => alert(this.innerHTML)); // John (*)
  }

});
</script>

<user-info>John</user-info>
```

Giờ đây `alert` ở dòng `(*)` hiển thị “John”, vì chúng ta chạy nó bất đồng bộ, sau khi phân tích HTML hoàn tất. Chúng ta có thể xử lý các phần con nếu cần và hoàn tất khởi tạo.

Mặt khác, giải pháp này cũng không hoàn hảo. Nếu các custom element lồng nhau cũng sử dụng `setTimeout` để khởi tạo bản thân, chúng sẽ xếp hàng: `setTimeout` bên ngoài kích hoạt trước, sau đó đến cái bên trong.

Vì vậy phần tử bên ngoài hoàn tất khởi tạo trước phần tử bên trong.

Hãy minh họa điều đó bằng ví dụ:

```
<script>
customElements.define('user-info', class extends HTMLElement {
  connectedCallback() {
    alert(`${this.id} connected.`);
    setTimeout(() => alert(`${this.id} initialized.`));
  }
});
</script>

<user-info id="outer">
  <user-info id="inner"></user-info>
</user-info>
```

Thứ tự đầu ra:

1. outer connected.
2. inner connected.
3. outer initialized.
4. inner initialized.

Chúng ta có thể thấy rõ rằng phần tử bên ngoài hoàn tất khởi tạo `(3)` trước phần tử bên trong `(4)`.

Không có callback tích hợp sẵn nào được kích hoạt sau khi các phần tử lồng nhau sẵn sàng. Nếu cần, chúng ta có thể tự triển khai điều đó. Ví dụ, các phần tử bên trong có thể dispatch các event như `initialized`, và các phần tử bên ngoài có thể lắng nghe và phản hồi với chúng.

## [Các phần tử built-in đã tùy chỉnh](#customized-built-in-elements)

Các phần tử mới mà chúng ta tạo, như `<time-formatted>`, không có ngữ nghĩa liên quan nào. Chúng không được các công cụ tìm kiếm biết đến, và các thiết bị accessibility không thể xử lý chúng.

Nhưng những điều như vậy có thể quan trọng. Ví dụ, công cụ tìm kiếm sẽ quan tâm đến việc chúng ta thực sự hiển thị thời gian. Và nếu chúng ta đang tạo một loại nút đặc biệt, tại sao không tái sử dụng chức năng của `<button>` có sẵn?

Chúng ta có thể kế thừa và tùy chỉnh các phần tử HTML tích hợp sẵn bằng cách kế thừa từ class của chúng.

Ví dụ, các nút là các instance của `HTMLButtonElement`, hãy xây dựng dựa trên nó.

1. Kế thừa `HTMLButtonElement` bằng class của chúng ta:

   ```
   class HelloButton extends HTMLButtonElement { /* custom element methods */ }
   ```
2. Cung cấp đối số thứ ba cho `customElements.define`, đó là chỉ định tag:

   ```
   customElements.define('hello-button', HelloButton, {extends: 'button'});
   ```

   Có thể có nhiều tag khác nhau chia sẻ cùng một DOM-class, vì vậy cần chỉ định `extends`.
3. Cuối cùng, để sử dụng custom element của chúng ta, chèn một thẻ `<button>` thường, nhưng thêm `is="hello-button"` vào nó:

   ```
   <button is="hello-button">...</button>
   ```

Dưới đây là một ví dụ đầy đủ:

```
<script>
// The button that says "hello" on click
class HelloButton extends HTMLButtonElement {
  constructor() {
    super();
    this.addEventListener('click', () => alert("Hello!"));
  }
}

customElements.define('hello-button', HelloButton, {extends: 'button'});
</script>

<button is="hello-button">Click me</button>

<button is="hello-button" disabled>Disabled</button>
```

Nút mới của chúng ta kế thừa từ nút tích hợp sẵn. Vì vậy nó giữ các style và tính năng tiêu chuẩn như attribute `disabled`.

## [Tham chiếu](#references)

- HTML Living Standard: <https://html.spec.whatwg.org/#custom-elements>.
- Compatiblity: <https://caniuse.com/#feat=custom-elementsv1>.

## [Tóm tắt](#summary)

Custom element có thể thuộc hai loại:

1. “Autonomous” – các thẻ mới, kế thừa `HTMLElement`.

   Phương án định nghĩa:

   ```
   class MyElement extends HTMLElement {
     constructor() { super(); /* ... */ }
     connectedCallback() { /* ... */ }
     disconnectedCallback() { /* ... */  }
     static get observedAttributes() { return [/* ... */]; }
     attributeChangedCallback(name, oldValue, newValue) { /* ... */ }
     adoptedCallback() { /* ... */ }
    }
   customElements.define('my-element', MyElement);
   /* <my-element> */
   ```
2. “Customized built-in elements” – sự mở rộng của các phần tử có sẵn.

   Cần thêm một đối số `.define` nữa, và `is="..."` trong HTML:

   ```
   class MyButton extends HTMLButtonElement { /*...*/ }
   customElements.define('my-button', MyElement, {extends: 'button'});
   /* <button is="my-button"> */
   ```

Custom elements được hỗ trợ tốt trên các trình duyệt. Có một polyfill <https://github.com/webcomponents/polyfills/tree/master/packages/webcomponentsjs>.

---

---

## Bài tập

## [Tasks](#tasks)

### [Phần tử đồng hồ trực tiếp](#live-timer-element)

Chúng ta đã có phần tử `<time-formatted>` để hiển thị thời gian định dạng đẹp.

Tạo phần tử `<live-timer>` để hiển thị thời gian hiện tại:

1. Nó phải sử dụng `<time-formatted>` bên trong, không sao chép chức năng của nó.
2. Tick (cập nhật) mỗi giây.
3. Với mỗi tick, một custom event tên là `tick` phải được tạo ra, với ngày hiện tại trong `event.detail` (xem chương [Dispatching custom events](/dispatch-events)).

Cách sử dụng:

```
<live-timer id="elem"></live-timer>

<script>
  elem.addEventListener('tick', event => console.log(event.detail));
</script>
```

Demo:

[Open a sandbox for the task.](https://plnkr.co/edit/SiC4UP2HxHDnkHtL?p=preview)

solution

Lưu ý:

1. Chúng ta xóa `setInterval` khi phần tử bị xóa khỏi document. Điều đó quan trọng, nếu không nó tiếp tục tick ngay cả khi không cần nữa. Và trình duyệt không thể giải phóng bộ nhớ của phần tử này và các tham chiếu của nó.
2. Chúng ta có thể truy cập ngày hiện tại như thuộc tính `elem.date`. Tất cả các phương thức và thuộc tính của class tự nhiên là các phương thức và thuộc tính của phần tử.

[Open the solution in a sandbox.](https://plnkr.co/edit/0gsHybZRfaKxKkOm?p=preview)
