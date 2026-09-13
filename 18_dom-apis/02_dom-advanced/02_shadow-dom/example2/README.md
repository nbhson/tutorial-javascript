# Shadow DOM — Example 2

## Khái niệm
Shadow DOM kết hợp slot: `<slot name="...">` để nội dung từ bên ngoài chiếu vào bên trong shadow. `::slotted(selector)` style phần slot.

## Điểm mạnh
- Cho phép custom element có template nhưng vẫn nhận content linh hoạt
- Style slot được giới hạn bởi shadow scope

## Khi nào dùng
- Card component; layout framework.

## 📚 Tham khảo
- `app.js`, `index.html`, `style.css`
