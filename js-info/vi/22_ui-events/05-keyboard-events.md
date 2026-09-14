# Bàn phím (Keyboard): keydown và keyup

> Source: [https://javascript.info/keyboard-events](https://javascript.info/keyboard-events)

<!-- fetched: 2026-09-14 -->

Trước khi chúng ta đến keyboard, xin lưu ý rằng на các thiết bị hiện đại có các cách khác để "input something". Ví dụ, mọi người sử dụng speech recognition (đặc biệt на các thiết bị di động) hoặc copy/paste bằng chuột.

Vì vậy, nếu chúng ta muốn theo dõi bất kỳ input nào vào một `<input>` field, thì các keyboard events là không đủ. Có một sự kiện khác được đặt tên là `input` để theo dõi các thay đổi của `<input>` field, bằng mọi cách. Và nó có thể là một lựa chọn tốt hơn cho task như vậy. Chúng ta sẽ đề cập đến nó sau trong chương [Events: change, input, cut, copy, paste](/events-change-input).

Keyboard events nên được sử dụng khi chúng ta muốn xử lý các hành động keyboard (virtual keyboard cũng tính). Ví dụ, để phản ứng на các phím mũi tên `Up` và `Down` hoặc hotkeys (bao gồm các tổ hợp phím).

## [Teststand](#keyboard-test-stand)

Để hiểu rõ hơn về các keyboard events, bạn có thể sử dụng teststand bên dưới.

Thử các tổ hợp phím khác nhau trong ô văn bản.

Result

script.js

style.css

index.html

```
kinput.onkeydown = kinput.onkeyup = kinput.onkeypress = handle;

let lastTime = Date.now();

function handle(e) {
  if (form.elements[e.type + 'Ignore'].checked) return;

  area.scrollTop = 1e6;

  let text = e.type +
    ' key=' + e.key +
    ' code=' + e.code +
    (e.shiftKey ? ' shiftKey' : '') +
    (e.ctrlKey ? ' ctrlKey' : '') +
    (e.altKey ? ' altKey' : '') +
    (e.metaKey ? ' metaKey' : '') +
    (e.repeat ? ' (repeat)' : '') +
    "\n";

  if (area.value && Date.now() - lastTime > 250) {
    area.value += new Array(81).join('-') + '\n';
  }
  lastTime = Date.now();

  area.value += text;

  if (form.elements[e.type + 'Stop'].checked) {
    e.preventDefault();
  }
}
```

```
#kinput {
  font-size: 150%;
  box-sizing: border-box;
  width: 95%;
}

#area {
  width: 95%;
  box-sizing: border-box;
  height: 250px;
  border: 1px solid black;
  display: block;
}

form label {
  display: inline;
  white-space: nowrap;
}
```

```
<!DOCTYPE HTML>
<html>

<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="style.css">
</head>

<body>

  <form id="form" onsubmit="return false">

    Prevent default for:
    <label>
      <input type="checkbox" name="keydownStop" value="1"> keydown</label>
    <label>
      <input type="checkbox" name="keyupStop" value="1"> keyup</label>

    <p>
      Ignore:
      <label>
        <input type="checkbox" name="keydownIgnore" value="1"> keydown</label>
      <label>
        <input type="checkbox" name="keyupIgnore" value="1"> keyup</label>
    </p>

    <p>Focus on the input field and press a key.</p>

    <input type="text" placeholder="Press keys here" id="kinput">

    <textarea id="area" readonly></textarea>
    <input type="button" value="Clear" onclick="area.value = ''" />
  </form>
  <script src="script.js"></script>

</body>
</html>
```

## [Keydown và keyup](#keydown-and-keyup)

Các sự kiện `keydown` xảy ra khi một phím được nhấn xuống, và sau đó `keyup` – khi nó được nhả ra.

### [event.code và event.key](#event-code-and-event-key)

Thuộc tính `key` của đối tượng sự kiện cho phép lấy ký tự, trong khi thuộc tính `code` của đối tượng sự kiện cho phép lấy "physical key code".

Ví dụ, cùng một phím `Z` có thể được nhấn với hoặc không có `Shift`. Điều đó cho chúng ta hai ký tự khác nhau: lowercase `z` và uppercase `Z`.

`event.key` chính xác là ký tự, và nó sẽ khác. Nhưng `event.code` thì giống nhau:

| Key | `event.key` | `event.code` |
| --- | --- | --- |
| `Z` | `z` (lowercase) | `KeyZ` |
| `Shift+Z` | `Z` (uppercase) | `KeyZ` |

Nếu người dùng làm việc với nhiều ngôn ngữ, thì chuyển sang ngôn ngữ khác sẽ tạo ra một ký tự hoàn toàn khác thay vì `"Z"`. Điều đó sẽ trở thành giá trị của `event.key`, trong khi `event.code` luôn giống nhau: `"KeyZ"`.

"KeyZ" và các key codes khác

Mỗi key có một code phụ thuộc vào vị trí của nó trên bàn phím. Các key codes được mô tả в [UI Events code specification](https://www.w3.org/TR/uievents-code/).

Ví dụ:

- Letter keys có codes `"Key<letter>"`: `"KeyA"`, `"KeyB"` v.v.
- Digit keys có codes: `"Digit<number>"`: `"Digit0"`, `"Digit1"` v.v.
- Special keys được mã hóa theo tên của chúng: `"Enter"`, `"Backspace"`, `"Tab"` v.v.

Có nhiều keyboard layouts phổ biến, và specification đưa ra key codes cho mỗi layout.

Đọc [alphanumeric section of the spec](https://www.w3.org/TR/uievents-code/#key-alphanumeric-section) để biết thêm codes, hoặc đơn giản là nhấn một key на [teststand](#keyboard-test-stand) bên trên.

Case matters: `"KeyZ"`, không phải `"keyZ"`

Có vẻ hiển nhiên, nhưng mọi người vẫn mắc lỗi.

Hãy tránh các lỗi đánh máy: đó là `KeyZ`, không phải `keyZ`. Phép kiểm tra như `event.code=="keyZ"` sẽ không hoạt động: chữ cái đầu tiên của `"Key"` phải là viết hoa.

Nếu một key không tạo ra bất kỳ ký tự nào? Ví dụ, `Shift` hoặc `F1` hoặc các key khác. Đối với những key đó, `event.key` tương đương với `event.code`:

| Key | `event.key` | `event.code` |
| --- | --- | --- |
| `F1` | `F1` | `F1` |
| `Backspace` | `Backspace` | `Backspace` |
| `Shift` | `Shift` | `ShiftRight` hoặc `ShiftLeft` |

Xin lưu ý rằng `event.code` chỉ định chính xác phím nào được nhấn. Ví dụ, hầu hết các bàn phím có hai phím `Shift`: một ở bên trái và một ở bên phải. `event.code` cho chúng ta biết chính xác phím nào đã được nhấn, và `event.key` chịu trách nhiệm cho "nghĩa" của key: nó là gì (một "Shift").

Hãy nói, chúng ta muốn xử lý một hotkey: `Ctrl+Z` (hoặc `Cmd+Z` đối với Mac). Hầu hết các text editors gắn action "Undo" на nó. Chúng ta có thể đặt một listener на `keydown` và kiểm tra key nào được nhấn.

Có một dilemma ở đây: trong listener như vậy, chúng ta nên kiểm tra giá trị của `event.key` hay `event.code`?

Một mặt, giá trị của `event.key` là một ký tự, nó thay đổi tùy thuộc vào ngôn ngữ. Nếu người truy cập có nhiều ngôn ngữ в OS và chuyển đổi giữa chúng, cùng một key tạo ra các ký tự khác nhau. Vì vậy, có ý nghĩa để kiểm tra `event.code`, nó luôn giống nhau.

Như sau:

```
document.addEventListener('keydown', function(event) {
  if (event.code == 'KeyZ' && (event.ctrlKey || event.metaKey)) {
    alert('Undo!')
  }
});
```

Mặt khác, có một vấn đề với `event.code`. Đối với các keyboard layouts khác nhau, cùng một key có thể có các ký tự khác nhau.

Ví dụ, đây là US layout ("QWERTY") và German layout ("QWERTZ") под nó (từ Wikipedia):

![](/article/keyboard-events/us-layout.svg)

![](/article/keyboard-events/german-layout.svg)

Đối với cùng một key, US layout có "Z", trong khi German layout có "Y" (các chữ cái bị hoán đổi).

Theo đúng nghĩa, `event.code` sẽ bằng `KeyZ` đối với những người có German layout khi họ nhấn `Y`.

Nếu chúng ta kiểm tra `event.code == 'KeyZ'` trong mã của chúng ta, thì đối với những người có German layout, bài kiểm tra đó sẽ vượt qua khi họ nhấn `Y`.

Điều đó nghe có vẻ thực sự kỳ lạ, nhưng đúng như vậy. [Specification](https://www.w3.org/TR/uievents-code/#table-key-code-alphanumeric-writing-system) nêu rõ hành vi như vậy.

Vì vậy, `event.code` có thể khớp với một ký tự sai cho layout không mong muốn. Cùng các chữ cái в các layouts khác nhau có thể ánh xạ đến các physical keys khác nhau, dẫn đến các codes khác nhau. May mắn thay, điều đó chỉ xảy ra với một vài codes, ví dụ `keyA`, `keyQ`, `keyZ` (như chúng ta đã thấy), và không xảy ra với các special keys như `Shift`. Bạn có thể tìm danh sách в [specification](https://www.w3.org/TR/uievents-code/#table-key-code-alphanumeric-writing-system).

Để theo dõi đáng tin cậy các ký tự phụ thuộc vào layout, `event.key` có thể là cách tốt hơn.

Mặt khác, `event.code` có lợi thế luôn giống nhau, liên kết với vị trí physical key. Vì vậy, các hotkeys dựa vào nó hoạt động tốt ngay cả trong trường hợp chuyển đổi ngôn ngữ.

Chúng ta muốn xử lý các keys phụ thuộc vào layout? Thì `event.key` là cách để đi.

Hoặc chúng ta muốn một hotkey hoạt động ngay cả sau khi chuyển đổi ngôn ngữ? Thì `event.code` có thể tốt hơn.

## [Auto-repeat](#auto-repeat)

Nếu một key đang được nhấn trong thời gian đủ lâu, nó bắt đầu "auto-repeat": `keydown` kích hoạt lại và lại, và sau đó khi nó được nhả ra, chúng ta cuối cùng nhận được `keyup`. Vì vậy, nó khá bình thường khi có nhiều `keydown` và một `keyup` duy nhất.

Đối với các sự kiện được trigger bởi auto-repeat, đối tượng sự kiện có thuộc tính `event.repeat` được đặt thành `true`.

## [Default actions](#default-actions)

Default actions khác nhau, vì có nhiều thứ có thể được khởi tạo bởi keyboard.

Ví dụ:

- Một ký tự xuất hiện trên màn hình (kết quả rõ ràng nhất).
- Một ký tự bị xóa (phím `Delete`).
- Trang được scroll (`PageDown` key).
- Browser mở dialog "Save Page" (`Ctrl+S`)
- …và cứ thế.

Ngăn chặn default action trên `keydown` có thể hủy bỏ hầu hết chúng, ngoại trừ các special keys dựa на OS. Ví dụ, на Windows `Alt+F4` đóng cửa sổ browser hiện tại. Và không có cách nào để dừng nó bằng cách ngăn chặn default action в JavaScript.

Ví dụ, `<input>` bên dưới mong đợi một số điện thoại, vì vậy nó không chấp nhận các key ngoại trừ digits, `+`, `()` hoặc `-`:

```
<script>
function checkPhoneKey(key) {
  return (key >= '0' && key <= '9') || ['+','(',')','-'].includes(key);
}
</script>
<input onkeydown="return checkPhoneKey(event.key)" placeholder="Phone, please" type="tel">
```

Handler `onkeydown` ở đây sử dụng `checkPhoneKey` để kiểm tra key được nhấn. Nếu nó hợp lệ (từ `0..9` hoặc một trong `+-()`), thì nó trả về `true`, ngược lại `false`.

Như chúng ta biết, giá trị `false` được trả về từ handler sự kiện, được gán bằng một DOM property hoặc attribute, chẳng hạn như trên, ngăn chặn default action, vì vậy không có gì xuất hiện trong `<input>` đối với các key không vượt qua bài kiểm tra. (Giá trị `true` được trả về không ảnh hưởng gì, chỉ trả về `false` mới quan trọng)

Xin lưu ý rằng các special keys, chẳng hạn như `Backspace`, `Left`, `Right`, không hoạt động trong input. Đó là một tác dụng phụ của bộ lọc nghiêm ngặt `checkPhoneKey`. Các key này khiến nó trả về `false`.

Hãy nới lỏng bộ lọc một chút bằng cách cho phép các phím mũi tên `Left`, `Right` và `Delete`, `Backspace`:

```
<script>
function checkPhoneKey(key) {
  return (key >= '0' && key <= '9') ||
    ['+','(',')','-','ArrowLeft','ArrowRight','Delete','Backspace'].includes(key);
}
</script>
<input onkeydown="return checkPhoneKey(event.key)" placeholder="Phone, please" type="tel">
```

Bây giờ arrows và deletion hoạt động tốt.

Mặc dù chúng ta có bộ lọc key, người dùng vẫn có thể nhập bất kỳ thứ gì bằng cách sử dụng chuột và right-click + Paste. Các thiết bị di động cung cấp các cách khác để nhập giá trị. Vì vậy, bộ lọc không 100% đáng tin cậy.

Cách tiếp cận thay thế sẽ là theo dõi sự kiện `oninput` – nó kích hoạt *sau khi* bất kỳ sửa đổi nào. Ở đó chúng ta có thể kiểm tra `input.value` mới và sửa đổi nó/làm nổi bật `<input>` khi nó không hợp lệ. Hoặc chúng ta có thể sử dụng cả hai event handlers cùng nhau.

## [Legacy](#legacy)

Trong quá khứ, có một sự kiện `keypress`, và cũng có các thuộc tính `keyCode`, `charCode`, `which` của đối tượng sự kiện.

Có quá nhiều incompatibilities của browser в khi làm việc với chúng, mà các nhà phát triển của specification không có cách nào khác ngoài việc deprecated tất cả chúng và tạo ra các sự kiện mới, hiện đại (được mô tả ở trên в chương này). Mã cũ vẫn hoạt động, vì các browser tiếp tục hỗ trợ chúng, nhưng hoàn toàn không cần sử dụng chúng nữa.

## [Mobile Keyboards](#mobile-keyboards)

Khi sử dụng virtual/mobile keyboards, formally known as IME (Input-Method Editor), tiêu chuẩn W3C tuyên bố rằng [`e.keyCode` của KeyboardEvent nên là `229`](https://www.w3.org/TR/uievents/#determine-keydown-keyup-keyCode) và [`e.key` nên là `"Unidentified"`](https://www.w3.org/TR/uievents-key/#key-attr-values).

Trong khi một số keyboards như vậy có thể vẫn sử dụng các giá trị đúng для `e.key`, `e.code`, `e.keyCode`… khi nhấn các key nhất định như arrows hoặc backspace, không có bảo đảm, vì vậy logic keyboard của bạn có thể không luôn hoạt động на các thiết bị di động.

## [Tổng kết](#summary)

Nhấn một key luôn tạo ra một keyboard event, bất kể đó là symbol keys hay special keys như `Shift` hoặc `Ctrl` và cứ thế. Ngoại lệ duy nhất là phím `Fn` đôi khi xuất hiện на laptop keyboard. Không có keyboard event nào cho nó, vì nó thường được triển khai на mức thấp hơn OS.

Các keyboard events:

- `keydown` – khi nhấn key (auto-repeats nếu key được nhấn trong thời gian dài),
- `keyup` – khi nhả key.

Các thuộc tính keyboard event chính:

- `code` – "key code" (`"KeyA"`, `"ArrowLeft"` và v.v.), đặc thù cho vị trí physical của key trên keyboard.
- `key` – ký tự (`"A"`, `"a"` và v.v.), đối với các non-character keys, chẳng hạn như `Esc`, thường có cùng giá trị với `code`.

Trong quá khứ, các keyboard events đôi khi được sử dụng để theo dõi user input trong các form fields. Điều đó không đáng tin cậy, vì input có thể đến từ nhiều nguồn khác nhau. Chúng ta có các sự kiện `input` và `change` để xử lý bất kỳ input nào (được đề cập sau в chương [Events: change, input, cut, copy, paste](/events-change-input)). Chúng kích hoạt sau bất kỳ loại input nào, bao gồm cả copy-pasting hoặc speech recognition.

Chúng ta nên sử dụng các keyboard events khi chúng ta thực sự muốn keyboard. Ví dụ, để phản ứng на hotkeys hoặc special keys.

---

---

## Bài tập

## [Bài tập](#tasks)

### [Extended hotkeys](#extended-hotkeys)

mức độ khó: 5

Tạo một hàm `runOnKeys(func, code1, code2, ... code_n)` chạy `func` на simultaneous pressing của các key có codes `code1`, `code2`, …, `code_n`.

Ví dụ, mã bên dưới hiển thị `alert` khi `"Q"` và `"W"` được nhấn cùng nhau (bất kỳ ngôn ngữ nào, với hoặc không có CapsLock)

```
runOnKeys(
  () => alert("Hello!"),
  "KeyQ",
  "KeyW"
);
```

[Demo trong cửa sổ mới](https://en.js.cx/task/check-sync-keydown/solution/)

lời giải

Chúng ta nên sử dụng hai handlers: `document.onkeydown` và `document.onkeyup`.

Hãy tạo một set `pressed = new Set()` để giữ các key đang được nhấn hiện tại.

Handler đầu tiên thêm vào nó, trong khi handler thứ hai xóa khỏi nó. Mỗi lần trên `keydown` chúng ta kiểm tra xem chúng ta có đủ keys được nhấn hay không, và chạy function nếu đúng như vậy.

[Mở solution trong sandbox.](https://plnkr.co/edit/hEVU2vpjFxTqkowk?p=preview)
