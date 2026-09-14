# Multiline mode của anchor ^ $, flag "m"

> Source: [https://javascript.info/regexp-multiline-mode](https://javascript.info/regexp-multiline-mode)

<!-- fetched: 2026-09-14 -->

Multiline mode được bật bằng flag `m`.

Nó chỉ ảnh hưởng đến hành vi của `^` và `$`.

Trong multiline mode, chúng match không chỉ ở đầu và cuối string, mà còn ở đầu/cuối mỗi dòng.

## [Tìm kiếm ở đầu dòng ^](#searching-at-line-start)

Trong ví dụ bên dưới, văn bản có nhiều dòng. Pattern `/^\d/gm` lấy chữ số từ đầu mỗi dòng:

```
let str = `1st place: Winnie
2nd place: Piglet
3rd place: Eeyore`;

console.log( str.match(/^\d/gm) ); // 1, 2, 3
```

Không có flag `m`, chỉ chữ số đầu tiên được match:

```
let str = `1st place: Winnie
2nd place: Piglet
3rd place: Eeyore`;

console.log( str.match(/^\d/g) ); // 1
```

Lý do là mặc định dấu `^` chỉ match ở đầu văn bản, và trong multiline mode – ở đầu bất kỳ dòng nào.

Lưu ý:

“Đầu dòng” theo nghĩa chính thức là “ngay sau một ký tự xuống dòng”: phép thử `^` trong multiline mode match ở mọi vị trí phía trước có ký tự xuống dòng `\n`.

Và ở đầu văn bản.

## [Tìm kiếm ở cuối dòng $](#searching-at-line-end)

Dấu `$` hoạt động tương tự.

Regular expression `\d$` tìm chữ số cuối trong mỗi dòng

```
let str = `Winnie: 1
Piglet: 2
Eeyore: 3`;

console.log( str.match(/\d$/gm) ); // 1,2,3
```

Không có flag `m`, dấu `$` chỉ match ở cuối toàn bộ văn bản, vì vậy chỉ chữ số cuối cùng được tìm thấy.

Lưu ý:

“Cuối dòng” theo nghĩa chính thức là “ngay trước một ký tự xuống dòng”: phép thử `$` trong multiline mode match ở mọi vị trí phía sau có ký tự xuống dòng `\n`.

Và ở cuối văn bản.

## [Tìm \n thay vì ^ $](#searching-for-n-instead-of)

Để tìm ký tự xuống dòng, chúng ta có thể dùng không chỉ anchor `^` và `$`, mà còn ký tự xuống dòng `\n`.

Sự khác biệt là gì? Hãy xem một ví dụ.

Ở đây chúng ta tìm `\d\n` thay vì `\d$`:

```
let str = `Winnie: 1
Piglet: 2
Eeyore: 3`;

console.log( str.match(/\d\n/g) ); // 1\n,2\n
```

Như chúng ta thấy, có 2 match thay vì 3.

Lý do là không có ký tự xuống dòng sau `3` (tuy có cuối văn bản, nên nó match `$`).

Một khác biệt nữa: giờ mỗi match đều chứa ký tự xuống dòng `\n`. Khác với anchor `^` `$` (chỉ kiểm tra điều kiện (đầu/cuối dòng)), `\n` là một ký tự, nên nó trở thành một phần của kết quả.

Vậy, `\n` trong pattern được dùng khi chúng ta cần các ký tự xuống dòng trong kết quả, trong khi anchor được dùng để tìm thứ gì đó ở đầu/cuối dòng.
