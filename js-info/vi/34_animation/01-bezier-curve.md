# Đường cong Bézier

> Source: [https://javascript.info/bezier-curve](https://javascript.info/bezier-curve)

<!-- fetched: 2026-09-14 -->

Các đường cong Bezier được dùng trong đồ họa máy tính để vẽ hình, cho CSS animation và ở nhiều nơi khác.

Chúng là một điều rất đơn giản, đáng học một lần và sau đó sẽ tự tin trong thế giới đồ họa vector và các animation nâng cao.

Một chút lý thuyết, mời bạn

Bài viết này cung cấp một cái nhìn mang tính lý thuyết, nhưng rất cần thiết về đường cong Bezier là gì, trong khi [bài tiếp theo](/css-animations#bezier-curve) cho thấy cách chúng ta có thể sử dụng chúng cho CSS animation.

Hãy dành thời gian đọc và hiểu khái niệm, nó sẽ giúp bạn rất nhiều.

## [Control points](#control-points)

Một [đường cong Bezier](https://en.wikipedia.org/wiki/B%C3%A9zier_curve) được định nghĩa bởi các control points.

Có thể có 2, 3, 4 hoặc nhiều hơn.

Ví dụ, đường cong hai điểm:

![](/article/bezier-curve/bezier2.svg)

Đường cong ba điểm:

![](/article/bezier-curve/bezier3.svg)

Đường cong bốn điểm:

![](/article/bezier-curve/bezier4.svg)

Nếu bạn nhìn kỹ những đường cong này, bạn có thể ngay lập tức nhận thấy:

1. **Các điểm không phải lúc nào cũng nằm trên đường cong.** Điều đó hoàn toàn bình thường, sau này chúng ta sẽ thấy đường cong được xây dựng như thế nào.
2. **Bậc của đường cong bằng số điểm trừ một**.
   Với hai điểm chúng ta có đường cong tuyến tính (đó là một đường thẳng), với ba điểm – đường cong bậc hai (parabolic), với bốn điểm – đường cong bậc ba.
3. **Đường cong luôn nằm bên trong [vỏ lồi](https://en.wikipedia.org/wiki/Convex_hull) của các control points:**

   ![](/article/bezier-curve/bezier4-e.svg) ![](/article/bezier-curve/bezier3-e.svg)

Nhờ đặc tính cuối cùng đó, trong đồ họa máy tính có thể tối ưu hóa các phép thử giao. Nếu các vỏ lồi không giao nhau, thì các đường cong cũng không giao nhau. Vì vậy kiểm tra giao của các vỏ lồi trước có thể cho kết quả "không giao" rất nhanh. Kiểm tra giao của các vỏ lồi dễ hơn nhiều, vì chúng là hình chữ nhật, tam giác và tương tự (xem hình trên), các hình đơn giản hơn nhiều so với đường cong.

**Giá trị chính của đường cong Bezier trong vẽ – bằng cách di chuyển các điểm, đường cong thay đổi *theo cách trực quan rõ ràng*.**

Thử di chuyển các control points bằng chuột trong ví dụ dưới đây:

**Như bạn có thể nhận thấy, đường cong giãn dài dọc theo các đường tiếp tuyến 1 → 2 và 3 → 4.**

Sau một thời gian luyện tập, điều đó trở nên rõ ràng về cách đặt điểm để có được đường cong cần thiết. Và bằng cách nối nhiều đường cong lại với nhau, chúng ta có thể đạt được gần như mọi thứ.

Dưới đây là một vài ví dụ:

![](/article/bezier-curve/bezier-car.svg) ![](/article/bezier-curve/bezier-letter.svg) ![](/article/bezier-curve/bezier-vase.svg)

## [Thuật toán De Casteljau](#de-casteljau-s-algorithm)

Có một công thức toán học cho đường cong Bezier, nhưng hãy để lại nó một chút sau, vì
[thuật toán De Casteljau](https://en.wikipedia.org/wiki/De_Casteljau%27s_algorithm) giống hệt định nghĩa toán học và cho thấy trực quan cách nó được xây dựng.

Trước tiên hãy xem ví dụ 3 điểm.

Đây là demo, và phần giải thích theo sau.

Control points (1, 2 và 3) có thể được di chuyển bằng chuột. Nhấn nút "play" để chạy.

**Thuật toán De Casteljau để xây dựng đường cong Bezier 3 điểm:**

1. Vẽ các control points. Trong demo ở trên chúng được đánh dấu: `1`, `2`, `3`.
2. Xây dựng các đoạn giữa các control points 1 → 2 → 3. Trong demo ở trên chúng có màu nâu.
3. Tham số `t` di chuyển từ `0` đến `1`. Trong ví dụ ở trên bước `0.05` được dùng: vòng lặp chạy qua `0, 0.05, 0.1, 0.15, ... 0.95, 1`.

   Với mỗi giá trị `t` này:

   - Trên mỗi đoạn màu nâu, chúng ta lấy một điểm nằm ở khoảng cách tỷ lệ với `t` từ đầu đoạn. Vì có hai đoạn, chúng ta có hai điểm.

     Ví dụ, với `t=0` – cả hai điểm sẽ ở đầu các đoạn, và với `t=0.25` – ở 25% chiều dài đoạn từ đầu, với `t=0.5` – 50% (điểm giữa), với `t=1` – ở cuối các đoạn.
   - Nối các điểm lại. Trong hình bên dưới đoạn nối được tô màu xanh dương.

| Với `t=0.25` | Với `t=0.5` |
| --- | --- |
|  |  |

4. Giờ trên đoạn màu xanh, lấy một điểm ở khoảng cách tỷ lệ với cùng giá trị `t`. Nghĩa là, với `t=0.25` (hình trái) chúng ta có điểm ở cuối phần tư bên trái của đoạn, và với `t=0.5` (hình phải) – ở giữa đoạn. Trong hình trên điểm đó có màu đỏ.
5. Vì `t` chạy từ `0` đến `1`, mỗi giá trị của `t` thêm một điểm vào đường cong. Tập hợp các điểm như vậy tạo thành đường cong Bezier. Nó có màu đỏ và parabolic trong hình trên.

Đó là quy trình cho 3 điểm. Nhưng đối với 4 điểm cũng tương tự.

Demo cho 4 điểm (các điểm có thể di chuyển bằng chuột):

Thuật toán cho 4 điểm:

- Nối các control points bằng các đoạn: 1 → 2, 2 → 3, 3 → 4. Sẽ có 3 đoạn màu nâu.
- Với mỗi `t` trong khoảng từ `0` đến `1`:
  - Chúng ta lấy các điểm trên những đoạn đó ở khoảng cách tỷ lệ với `t` từ đầu. Những điểm này được nối lại, vì vậy chúng ta có hai đoạn màu xanh lá.
  - Trên những đoạn đó chúng ta lấy các điểm tỷ lệ với `t`. Chúng ta có được một đoạn màu xanh dương.
  - Trên đoạn xanh dương chúng ta lấy một điểm tỷ lệ với `t`. Trong ví dụ ở trên nó có màu đỏ.
- Những điểm này cùng nhau tạo thành đường cong.

Thuật toán là đệ quy và có thể tổng quát hóa cho bất kỳ số lượng control points nào.

Với N control points:

1. Chúng ta nối chúng để ban đầu có N-1 đoạn.
2. Sau đó với mỗi `t` từ `0` đến `1`, chúng ta lấy một điểm trên mỗi đoạn ở khoảng cách tỷ lệ với `t` và nối chúng lại. Sẽ có N-2 đoạn.
3. Lặp lại bước 2 cho đến khi chỉ còn một điểm.

Những điểm này tạo thành đường cong.

**Chạy và tạm dừng các ví dụ để nhìn rõ các đoạn và cách đường cong được xây dựng.**

Một đường cong trông giống `y=1/t`:

Các control points zig-zag cũng hoạt động tốt:

Tạo vòng tròn là hoàn toàn có thể:

Một đường cong Bezier không nhẵn (vâng, điều đó cũng có thể):

Nếu có điều gì không rõ trong mô tả thuật toán, hãy xem các ví dụ trực tiếp ở trên để thấy cách
đường cong được xây dựng.

Vì thuật toán là đệ quy, chúng ta có thể xây dựng đường cong Bezier ở bất kỳ bậc nào, nghĩa là: sử dụng 5, 6 hoặc nhiều control points hơn. Nhưng trong thực tế nhiều điểm ít hữu ích hơn. Thông thường chúng ta lấy 2-3 điểm, và đối với các đường phức tạp thì gắn nhiều đường cong lại với nhau. Điều đó đơn giản hơn để phát triển và tính toán.

Làm thế nào để vẽ một đường cong *đi qua* các điểm cho trước?

Để chỉ định một đường cong Bezier, các control points được sử dụng. Như chúng ta thấy, chúng không nằm trên đường cong, ngoại trừ điểm đầu và điểm cuối.

Đôi khi chúng ta có một bài toán khác: vẽ một đường cong *đi qua một vài điểm*, sao cho tất cả chúng đều nằm trên một đường cong trơn. Bài toán đó được gọi là [interpolation](https://en.wikipedia.org/wiki/Interpolation), và ở đây chúng ta không đề cập đến nó.

Có các công thức toán học cho những đường cong như vậy, ví dụ [đa thức Lagrange](https://en.wikipedia.org/wiki/Lagrange_polynomial). Trong đồ họa máy tính [spline interpolation](https://en.wikipedia.org/wiki/Spline_interpolation) thường được dùng để xây dựng các đường cong trơn nối nhiều điểm.

## [Toán học](#maths)

Một đường cong Bezier có thể được mô tả bằng công thức toán học.

Như chúng ta đã thấy – thực tế không cần phải biết nó, hầu hết mọi người chỉ vẽ đường cong bằng cách di chuyển các điểm bằng chuột. Nhưng nếu bạn thích toán học – đây là công thức.

Cho tọa độ của các control points `Pi`: control point đầu tiên có tọa độ `P1 = (x1, y1)`, điểm thứ hai: `P2 = (x2, y2)`, và cứ như vậy, tọa độ của đường cong được mô tả bởi phương trình phụ thuộc vào tham số `t` từ đoạn `[0,1]`.

- Công thức cho đường cong 2 điểm:

  `P = (1-t)P1 + tP2`
- Với 3 control points:

  `P = (1−t)2P1 + 2(1−t)tP2 + t2P3`
- Với 4 control points:

  `P = (1−t)3P1 + 3(1−t)2tP2 +3(1−t)t2P3 + t3P4`

Đây là các phương trình vector. Nói cách khác, chúng ta có thể thay `P` bằng `x` và `y` để lấy các tọa độ tương ứng.

Ví dụ, đường cong 3 điểm được tạo bởi các điểm `(x,y)` được tính như:

- `x = (1−t)2x1 + 2(1−t)tx2 + t2x3`
- `y = (1−t)2y1 + 2(1−t)ty2 + t2y3`

Thay vì `x1, y1, x2, y2, x3, y3`, chúng ta nên đặt tọa độ của 3 control points, và sau đó khi `t` di chuyển từ `0` đến `1`, với mỗi giá trị của `t` chúng ta sẽ có `(x,y)` của đường cong.

Ví dụ, nếu các control points là `(0,0)`, `(0.5, 1)` và `(1, 0)`, các phương trình trở thành:

- `x = (1−t)2 * 0 + 2(1−t)t * 0.5 + t2 * 1 = (1-t)t + t2 = t`
- `y = (1−t)2 * 0 + 2(1−t)t * 1 + t2 * 0 = 2(1-t)t = –2t2 + 2t`

Giờ khi `t` chạy từ `0` đến `1`, tập hợp các giá trị `(x,y)` cho mỗi `t` tạo thành đường cong với các control points đó.

## [Tóm tắt](#summary)

Các đường cong Bezier được định nghĩa bởi các control points của chúng.

Chúng ta đã thấy hai định nghĩa của đường cong Bezier:

1. Dùng quá trình vẽ: thuật toán De Casteljau.
2. Dùng các công thức toán học.

Các tính năng tốt của đường cong Bezier:

- Chúng ta có thể vẽ các đường trơn bằng chuột bằng cách di chuyển các control points.
- Các hình phức tạp có thể được tạo từ một vài đường cong Bezier.

Ứng dụng:

- Trong đồ họa máy tính, modeling, các editor đồ họa vector. Font được mô tả bằng các đường cong Bezier.
- Trong phát triển web – cho đồ họa trên Canvas và trong định dạng SVG. Nhân tiện, các ví dụ "trực tiếp" ở trên được viết bằng SVG. Chúng thực chất là một tài liệu SVG duy nhất được cho các điểm khác nhau làm tham số. Bạn có thể mở nó trong một cửa sổ riêng và xem source: [demo.svg](/article/bezier-curve/demo.svg?p=0,0,1,0.5,0,0.5,1,1&animate=1).
- Trong CSS animation để mô tả đường đi và tốc độ của animation.
