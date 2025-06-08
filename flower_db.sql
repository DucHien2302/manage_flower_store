CREATE DATABASE IF NOT EXISTS DoAnPython;
USE DoAnPython;

-- DROP DATABASE DoAnPython

CREATE TABLE flowers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INT NOT NULL DEFAULT 0,
    image_url VARCHAR(255) NULL,
    flower_type ENUM('daisy', 'dandelion', 'rose', 'sunflower', 'tulip') NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE FlowerTypes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Description TEXT NOT NULL
);

INSERT INTO FlowerTypes (Name, Description) VALUES
('Daisy', 'Một loài hoa vui tươi với tâm màu vàng và cánh hoa màu trắng.'),
('Dandelion', 'Một loài hoa màu vàng biến thành quả cầu hạt màu trắng khi già.'),
('Rose', 'Một loài hoa đẹp có thân gai, nổi tiếng với hương thơm và nhiều màu sắc đa dạng.'),
('Sunflower', 'Một cây thân cao với đầu hoa lớn màu vàng giống như mặt trời.'),
('Tulip', 'Một loài hoa có hình dạng cốc, nhiều màu sắc, nở vào mùa xuân.');

CREATE TABLE Categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Description TEXT NOT NULL
);

INSERT INTO Categories (Name, Description) VALUES
('Chúc mừng Sinh nhật', 'Hoa dùng để tặng và chúc mừng trong dịp sinh nhật.'),
('Chúc mừng Khai trương', 'Hoa gửi tặng để chúc mừng dịp khai trương cửa hàng, công ty.'),
('Tình yêu & Lãng mạn', 'Hoa thể hiện tình cảm yêu đương, lãng mạn, kỷ niệm ngày yêu nhau, Valentine.'),
('Chia buồn', 'Hoa dùng để gửi lời chia buồn, phúng viếng trong tang lễ.'),
('Cảm ơn', 'Hoa thay lời cảm ơn chân thành đến người nhận.'),
('Chúc sức khỏe', 'Hoa gửi gắm lời chúc sức khỏe, thường dùng khi thăm người bệnh hoặc chúc thọ.'),
('Quà đặt biệt', 'Hoa dùng để tặng và chúc mừng dịp đặt biệt'),
('Trang trí', 'Hoa dùng để trang trí');

CREATE  TABLE Products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    Description TEXT NOT NULL,
    Price INT NOT NULL,
    DiscountedPrice INT NOT NULL DEFAULT 0,
    StockQuantity INT DEFAULT 0,
    ImageURL VARCHAR(255) NOT NULL,
    IsFreeship TINYINT(1) DEFAULT 0,
    CategoryID INT NOT NULL,
	FlowerTypeID INT NOT NULL,
    -- Constraint
    FOREIGN KEY (CategoryID) REFERENCES Categories(id),
    FOREIGN KEY (FlowerTypeID) REFERENCES FlowerTypes(id)
);

INSERT INTO Products (Name, Description, Price, DiscountedPrice, StockQuantity, CategoryID, ImageURL, IsFreeship, FlowerTypeID) VALUES
('Hoa tặng sự kiện 2 (+20 bó)', 'Bó hoa nhiều màu sắc cho sự kiện (từ 20 bó).', 200000, 0, 100, 2, '1', 0, 3), -- Giá từ, Hoa hồng
('Điều bất ngờ', 'Bó hoa hồng đỏ nhỏ xinh.', 300000, 0, 100, 1, '2', 0, 3), -- Hoa hồng
('Tinh', 'Bó hoa baby trắng tinh khôi.', 500000, 0, 100, 3, '3', 1, 3), -- Giả sử đây là hoa Baby, không phải hồng? Đặt NULL hoặc ID khác nếu có. Hoặc 3 nếu vẫn là hồng.
('Ấm áp', 'Bó hoa hướng dương nhỏ nhắn.', 250000, 0, 100, 5, '4', 0, 4), -- Giả sử đây là Hướng dương (ID 4)
('Me before you', 'Bó hoa hồng đỏ Ecuador sang trọng.', 750000, 550000, 100, 3, '5', 1, 3), -- Hoa hồng
('Hoa tặng sự kiện 5 (+20 bó)', 'Bó hoa trắng xanh cho sự kiện (từ 20 bó).', 288000, 0, 100, 2, '6', 1, 3), -- Giá từ, Giả sử có hoa hồng trắng
('Thinking of you', 'Bó hoa trắng trang nhã.', 500000, 0, 100, 3, '7', 1, 3), -- Giả sử có hoa hồng trắng
('Lời yêu thương 2', 'Bó hoa hồng kem và tím lãng mạn.', 1050000, 1000000, 100, 3, '8', 1, 3), -- Hoa hồng
('Tình Yêu Vĩnh Cửu 2', 'Bó hoa hồng đỏ lớn thể hiện tình yêu vĩnh cửu.', 3000000, 2500000, 100, 3, '9', 1, 3), -- Hoa hồng
('Giản dị', 'Bó hoa hồng phấn và trắng đơn giản.', 350000, 300000, 100, 5, '10', 0, 3), -- Hoa hồng
('White roses', 'Bó hoa hồng trắng tinh khiết.', 450000, 350000, 100, 3, '11', 0, 3), -- Hoa hồng
('Romantic Date', 'Bó hoa hồng tím nhỏ xinh cho buổi hẹn hò.', 200000, 0, 100, 3, '12', 0, 3); -- Hoa hồng

INSERT INTO Products (Name, Description, Price, DiscountedPrice, StockQuantity, CategoryID, IsFreeship, FlowerTypeID, ImageURL) VALUES
(
    -- Sản phẩm tương ứng ý tưởng từ 13.jpg
    'Bó Hoa Cúc Họa Mi Mộc Mạc',
    'Vẻ đẹp giản dị từ những bông cúc họa mi trắng tinh, bó gọn gàng trong giấy kraft nâu thân thiện. Thích hợp tặng bạn bè, người thân như một lời cảm ơn nhẹ nhàng.',
    280000, 0, 55, 5, 0, 1, '13'-- CategoryID: 5 (Cảm ơn), IsFreeship: 0, FlowerTypeID: 1
),
(
    -- Sản phẩm tương ứng ý tưởng từ 14.jpg
    'Bình Cúc Tana Trắng Tinh Khôi',
    'Bình gốm sứ trắng cắm đầy cúc Tana nhỏ xinh, mang lại cảm giác tươi mới và trong lành cho không gian sống hoặc bàn làm việc. Món quà sinh nhật dễ thương.',
    400000, 380000, 30, 1, 0, 1,'14' -- CategoryID: 1 (Sinh nhật), IsFreeship: 0, FlowerTypeID: 1
),
(
    -- Sản phẩm tương ứng ý tưởng từ 15.jpg
    'Nét Duyên Cúc Trắng Đồng Nội',
    'Bó hoa cúc trắng đồng nội thuần khiết, như một món quà nhỏ xinh từ thiên nhiên, gửi gắm sự quan tâm chân thành và lời cảm ơn.',
    295000, 0, 60, 5, 0, 1 ,'15'-- CategoryID: 5 (Cảm ơn), IsFreeship: 0, FlowerTypeID: 1
),
(
    -- Sản phẩm tương ứng ý tưởng từ 16.jpg (Dữ liệu là Daisy theo yêu cầu)
    'Chậu Cúc Marguerite Rạng Rỡ',
    'Chậu cúc Marguerite với những bông hoa trắng nhụy vàng rạng rỡ, biểu tượng cho niềm vui và sự lạc quan. Thích hợp để bàn làm việc hoặc tặng chúc sức khỏe.',
    430000, 0, 25, 6, 0, 1,'16' -- CategoryID: 6 (Chúc sức khỏe), IsFreeship: 0, FlowerTypeID: 1
),
(
    -- Sản phẩm tương ứng ý tưởng từ 17.jpg (Dữ liệu là Daisy theo yêu cầu)
    'Bó Cúc Trắng Mix Bi Nhẹ Nhàng',
    'Sự kết hợp tinh tế giữa cúc trắng Daisy chủ đạo và điểm xuyết hoa bi trắng, tạo nên bó hoa nhẹ nhàng, thanh thoát. Hoàn hảo cho dịp sinh nhật hoặc lời chúc mừng.',
    390000, 360000, 40, 1, 1, 1,'17' -- CategoryID: 1 (Sinh nhật), IsFreeship: 1, FlowerTypeID: 1
),
(
    -- Sản phẩm tương ứng ý tưởng từ 18.jpg
    'Chậu Cúc Trắng Ban Mai Tươi Sáng',
    'Mang cả khu vườn ban mai vào nhà với chậu cúc trắng Daisy tươi sáng, tràn đầy sức sống. Món quà ý nghĩa chúc sức khỏe, an lành.',
    410000, 0, 28, 6, 0, 1,'18' -- CategoryID: 6 (Chúc sức khỏe), IsFreeship: 0, FlowerTypeID: 1
);

INSERT INTO Products (Name, Description, Price, DiscountedPrice, StockQuantity, CategoryID, IsFreeship, FlowerTypeID, ImageURL) VALUES
(
    'Ảnh Dương',
    'Bó hướng dương nhỏ xinh "Ảnh Dương", mang ánh nắng ấm áp và lời chúc tốt đẹp đến người nhận. Giản dị nhưng đong đầy tình cảm, phù hợp tặng bạn bè hoặc người thân yêu.',
    165000, 150000, 50, 1, 0, 4, '19' -- CategoryID: 1 (Sinh nhật), IsFreeship: 0, FlowerTypeID: 4
),
(
    'Ấm áp',
    'Bó hoa hướng dương "Ấm áp" như vòng tay che chở, gửi gắm sự quan tâm và yêu thương chân thành. Một món quà ý nghĩa cho ngày sinh nhật hoặc đơn giản là thể hiện tình cảm.',
    250000, 0, 45, 1, 0, 4, '20' -- CategoryID: 1 (Sinh nhật), IsFreeship: 0, FlowerTypeID: 4
),
(
    'Tươi vui',
    'Bó hướng dương "Tươi vui" rạng rỡ, lan tỏa năng lượng tích cực và niềm vui ngập tràn. Món quà tuyệt vời để làm bừng sáng ngày sinh nhật hay gửi lời chúc mừng.',
    500000, 0, 35, 1, 1, 4, '21' -- CategoryID: 1 (Sinh nhật), IsFreeship: 1, FlowerTypeID: 4
),
(
    'Sun flower',
    'Giỏ hoa "Sun flower" rực rỡ với những bông hướng dương lớn khoe sắc, tượng trưng cho sự thành công, quyền lực và tinh thần lạc quan vươn lên. Hoàn hảo để chúc mừng khai trương hoặc tốt nghiệp.',
    720000, 600000, 25, 2, 1, 4, '22' -- CategoryID: 2 (Chúc mừng), IsFreeship: 1, FlowerTypeID: 4
),
(
    'Hy Vọng',
    'Lẵng hoa "Hy Vọng" là sự kết hợp tinh tế giữa hướng dương tràn đầy sức sống và các loại hoa lá phụ, mang đến thông điệp về niềm tin và một tương lai tươi sáng phía trước.',
    650000, 0, 30, 2, 1, 4, '23' -- CategoryID: 2 (Chúc mừng), IsFreeship: 1, FlowerTypeID: 4
),
(
    'Ngàn ánh dương',
    'Giỏ hoa "Ngàn ánh dương" hòa quyện sắc vàng rực của hướng dương và nét tinh khôi của hoa phụ trắng, tạo nên vẻ đẹp hài hòa, tươi sáng. Thích hợp tặng sinh nhật hoặc thay lời cảm ơn.',
    550000, 0, 28, 1, 1, 4, '24' -- CategoryID: 1 (Sinh nhật), IsFreeship: 1, FlowerTypeID: 4
),
(
    'Thành Đạt',
    'Kệ hoa "Thành Đạt" hoành tráng với hướng dương là chủ đạo, gửi gắm lời chúc thành công, phát đạt đến đối tác, bạn bè trong các dịp quan trọng như khai trương, kỷ niệm công ty.',
    1200000, 0, 15, 2, 1, 4, '25' -- CategoryID: 2 (Chúc mừng), IsFreeship: 1, FlowerTypeID: 4
),
(
    'Vững Bền',
    'Kệ hoa "Vững Bền" đồ sộ và sang trọng, kết hợp hướng dương và nhiều loại hoa cao cấp khác, thể hiện lời chúc phát triển thịnh vượng, hợp tác bền chặt và thành công rực rỡ.',
    1650000, 1500000, 10, 2, 1, 4, '26' -- CategoryID: 2 (Chúc mừng), IsFreeship: 1, FlowerTypeID: 4
);

INSERT INTO Products (Name, Description, Price, DiscountedPrice, StockQuantity, CategoryID, IsFreeship, FlowerTypeID, ImageURL) VALUES
(
    'Bó Tulip Rực Rỡ Sắc Màu',
    'Bó hoa tulip tươi tắn với nhiều màu sắc rực rỡ như đỏ, vàng, hồng, cam xen kẽ, mang đến niềm vui và sự tươi mới. Món quà hoàn hảo cho sinh nhật bạn bè hoặc lời cảm ơn chân thành.',
    450000, 0, 40, 1, 0, 5, '27' -- CategoryID: 1 (Sinh nhật), IsFreeship: 0, FlowerTypeID: 5
),
(
    'Bó Tulip Đỏ Nồng Nàn Yêu Thương',
    'Những bông tulip đỏ thắm, biểu tượng kinh điển của tình yêu nồng cháy và mãnh liệt. Gửi gắm tình cảm sâu sắc đến người thương trong những dịp đặc biệt như Valentine, kỷ niệm.',
    520000, 499000, 30, 3, 1, 5, '28' -- CategoryID: 3 (Tình yêu), IsFreeship: 1, FlowerTypeID: 5
),
(
    'Bình Tulip Hồng Dịu Dàng',
    'Bình gốm sứ trang nhã cắm đầy tulip hồng pastel nhẹ nhàng, tinh tế. Tượng trưng cho sự ngưỡng mộ, hạnh phúc và tình cảm ngọt ngào, thích hợp tặng sinh nhật hoặc trang trí.',
    680000, 0, 25, 1, 1, 5, '29' -- CategoryID: 1 (Sinh nhật), IsFreeship: 1, FlowerTypeID: 5
),
(
    'Bó Tulip Trắng Thuần Khiết',
    'Vẻ đẹp tinh khôi, thanh lịch và trang nhã từ những bông tulip trắng muốt. Thể hiện sự tôn trọng, lời xin lỗi chân thành hoặc một lời cảm ơn sâu sắc.',
    480000, 0, 35, 5, 0, 5, '30' -- CategoryID: 5 (Cảm ơn), IsFreeship: 0, FlowerTypeID: 5
),
(
    'Bó Tulip Vàng Tươi Sáng',
    'Sắc vàng rạng rỡ của tulip như ánh nắng mặt trời ấm áp, mang đến niềm vui, hy vọng và tượng trưng cho tình bạn bền chặt. Món quà tuyệt vời để chúc mừng hoặc cổ vũ tinh thần.',
    460000, 440000, 38, 2, 0, 5, '31' -- CategoryID: 2 (Chúc mừng), IsFreeship: 0, FlowerTypeID: 5
),
(
    'Lẵng Tulip Cam Nhiệt Huyết',
    'Lẵng hoa tulip cam rực rỡ và nổi bật, biểu tượng cho sự nhiệt tình, đam mê, năng lượng tích cực và sự kết nối. Lời chúc mừng hoàn hảo cho thành công hoặc một dịp kỷ niệm vui tươi.',
    750000, 0, 20, 2, 1, 5, '32' -- CategoryID: 2 (Chúc mừng), IsFreeship: 1, FlowerTypeID: 5
),
(
    'Bó Tulip Tím Lãng Mạn',
    'Sắc tím quyến rũ của tulip tượng trưng cho sự sang trọng, hoàng gia và một tình yêu sét đánh. Món quà độc đáo thể hiện sự ngưỡng mộ sâu sắc hoặc tình cảm thủy chung.',
    550000, 0, 22, 3, 0, 5, '33' -- CategoryID: 3 (Tình yêu), IsFreeship: 0, FlowerTypeID: 5
),
(
    'Tulip Mix Pastel Trong Giỏ Mây',
    'Giỏ mây tre đan xinh xắn cắm đầy tulip các màu pastel (hồng, trắng, vàng nhạt), mang lại cảm giác nhẹ nhàng, thư thái. Thích hợp tặng sinh nhật, cảm ơn hoặc chúc sức khỏe.',
    820000, 790000, 18, 1, 1, 5, '34' -- CategoryID: 1 (Sinh nhật), IsFreeship: 1, FlowerTypeID: 5
),
(
    'Bó Tulip Song Sắc Đỏ Trắng',
    'Sự kết hợp tương phản đầy ấn tượng giữa tulip đỏ nồng nàn và tulip trắng tinh khôi trong cùng một bó hoa, thể hiện sự hòa quyện của tình yêu đam mê và sự tôn trọng.',
    500000, 0, 28, 3, 0, 5, '35' -- CategoryID: 3 (Tình yêu), IsFreeship: 0, FlowerTypeID: 5
);

INSERT INTO Products (Name, Description, Price, DiscountedPrice, StockQuantity, CategoryID, IsFreeship, FlowerTypeID, ImageURL) VALUES
(
    -- Image: 36.jpg (Fluffy seed head closeup)
    'Bông Bồ Công Anh Ước Nguyện',
    'Một bông hoa bồ công anh với những hạt tơ trắng mịn màng, sẵn sàng bay theo gió, tượng trưng cho những điều ước và hy vọng được gửi đi.',
    320000, 299000, 50, 7, 0, 2, '36' -- CategoryID: 7 (Quà tặng đặc biệt), IsFreeship: 0, FlowerTypeID: 2
),
(
    -- Image: 37.jpg (Fluffy seed head closeup)
    'Quả Cầu Lông Bồ Công Anh',
    'Cận cảnh vẻ đẹp mong manh của quả cầu lông bồ công anh trắng muốt, chi tiết từng sợi tơ mềm mại. Mang ý nghĩa về sự tự do và khởi đầu mới.',
    450000, 0, 30, 8, 0, 2, '37' -- CategoryID: 8 (Trang trí), IsFreeship: 0, FlowerTypeID: 2
),
(
    -- Image: 38.jpg (Fluffy seed head closeup)
    'Hoa Gió Bồ Công Anh',
    'Bông hoa gió bồ công anh tròn đầy, sẵn sàng để bạn thổi bay những hạt ước mơ. Món quà tặng độc đáo và đầy ý nghĩa.',
    380000, 0, 25, 7, 0, 2, '38' -- CategoryID: 7 (Quà tặng đặc biệt), IsFreeship: 0, FlowerTypeID: 2
),
(
    -- Image: 39.jpg (Fluffy seed head closeup)
    'Vẻ Đẹp Tinh Khôi Bồ Công Anh',
    'Vẻ đẹp tinh khôi, nhẹ nhàng của hoa bồ công anh giai đoạn phát tán hạt. Thích hợp làm quà tặng tượng trưng hoặc trang trí theo phong cách tối giản.',
    580000, 550000, 20, 8, 1, 2, '39' -- CategoryID: 8 (Trang trí), IsFreeship: 1, FlowerTypeID: 2
),
(
    -- Image: 40.jpg (Fluffy seed head partial closeup, soft focus)
    'Giấc Mơ Bồ Công Anh',
    'Hình ảnh hoa bồ công anh mờ ảo như một giấc mơ, gợi cảm giác lãng mạn và bình yên. Biểu tượng cho những khát khao thầm kín.',
    180000, 0, 60, 7, 0, 2, '40' -- CategoryID: 7 (Quà tặng đặc biệt), IsFreeship: 0, FlowerTypeID: 2
),
(
    -- Image: 41.jpg (Fluffy seed head closeup)
    'Khoảnh Khắc Bồ Công Anh',
    'Ghi lại khoảnh khắc đẹp nhất của hoa bồ công anh trước khi những hạt giống bay xa. Tượng trưng cho sự kiên cường và khả năng thích ứng.',
    250000, 0, 40, 7, 0, 2, '41' -- CategoryID: 7 (Quà tặng đặc biệt), IsFreeship: 0, FlowerTypeID: 2
),
(
    -- Image: 42.jpg (Yellow flowers closeup)
    'Bông Bồ Công Anh Vàng Rực Rỡ',
    'Vẻ đẹp rạng rỡ và tràn đầy sức sống của hoa bồ công anh vàng tươi dưới ánh nắng mặt trời. Biểu tượng cho niềm vui và sự lạc quan.',
    95000, 0, 100, 8, 0, 2, '42' -- CategoryID: 8 (Trang trí), IsFreeship: 0, FlowerTypeID: 2
),
(
    -- Image: 43.jpg (Yellow flower extreme closeup)
    'Sắc Vàng Bồ Công Anh',
    'Cận cảnh chi tiết những cánh hoa mỏng manh màu vàng tươi của bồ công anh. Mang năng lượng tích cực và sức sống mãnh liệt.',
    150000, 135000, 35, 8, 0, 2, '43' -- CategoryID: 8 (Trang trí), IsFreeship: 0, FlowerTypeID: 2
),
(
    -- Image: 44.jpg (Yellow flower extreme closeup)
    'Nắng Vàng Bồ Công Anh',
    'Bông hoa bồ công anh vàng như gom hết ánh nắng mặt trời, rực rỡ và ấm áp. Tượng trưng cho hạnh phúc và sự thịnh vượng nhỏ bé.',
    650000, 0, 15, 8, 1, 2, '44' -- CategoryID: 8 (Trang trí), IsFreeship: 1, FlowerTypeID: 2
),
(
    -- Image: 45.jpg (Whole plant, yellow flower + seed head)
    'Vòng Đời Bồ Công Anh',
    'Hình ảnh cây bồ công anh với cả bông hoa vàng và quả cầu lông trắng, thể hiện trọn vẹn vòng đời và sức sống mãnh liệt của loài hoa dại.',
    280000, 0, 45, 7, 0, 2, '45' -- CategoryID: 7 (Quà tặng đặc biệt), IsFreeship: 0, FlowerTypeID: 2
),
(
    -- Image: 46.jpg (Seed head in grass, framed look)
    'Bồ Công Anh Đồng Nội',
    'Vẻ đẹp mộc mạc của bông bồ công anh trắng giữa đồng cỏ xanh. Gợi nhớ về tuổi thơ, sự bình yên và nét duyên dáng của thiên nhiên.',
    490000, 470000, 28, 8, 0, 2, '46' -- CategoryID: 8 (Trang trí), IsFreeship: 0, FlowerTypeID: 2
);

CREATE TABLE SysUser(
    id INT PRIMARY KEY AUTO_INCREMENT,
    Email VARCHAR(128) NOT NULL UNIQUE,
    Password VARCHAR(1024) NOT NULL
);

CREATE TABLE Informations(
    id INT PRIMARY KEY AUTO_INCREMENT,
    FirstName NVARCHAR(128) NOT NULL,
    LastName NVARCHAR(128) NOT NULL,
    FullName NVARCHAR(256) NOT NULL,
    DateOfBirth DATE NOT NULL,
    Gender NVARCHAR(32) NOT NULL,
    Address TEXT NOT NULL,
    UserId INT NOT NULL,
    -- Constraint
    FOREIGN KEY (UserId) REFERENCES SysUser(id)
);

CREATE TABLE SysRole(
    id INT PRIMARY KEY AUTO_INCREMENT,
    Name NVARCHAR(128) NOT NULL,
    CreateAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdateAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
INSERT INTO SysRole (Name, CreateAt, UpdateAt) VALUES
('Admin', NOW(), NOW()), ('Customer', NOW(), NOW());

CREATE TABLE SysUserRole(
    id INT PRIMARY KEY AUTO_INCREMENT,
    UserId INT NOT NULL,
    RoleId INT NOT NULL,
    -- Constraint
    FOREIGN KEY (UserId) REFERENCES SysUser(id),
    FOREIGN KEY (RoleId) REFERENCES SysRole(id)
);

CREATE TABLE Carts(
    CartId VARCHAR(128) NOT NULL,
    ProductId INT NOT NULL,
    Quantity INT NOT NULL,
    IsChecked TINYINT(1) NOT NULL DEFAULT 0,
    -- Constraint
    PRIMARY KEY (CartId, ProductId),
    FOREIGN KEY (ProductId) REFERENCES Products(id)
);

CREATE TABLE Invoices(
    InvoiceId VARCHAR(128) PRIMARY KEY NOT NULL,
    UserId INT NOT NULL,
    CreateAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Price DECIMAL(10,2) NOT NULL DEFAULT 0,
    Discount DECIMAL(10,2) NOT NULL DEFAULT 0,
    Amount DECIMAL(10,2) NOT NULL DEFAULT 0,
    Status TINYINT(1) NOT NULL DEFAULT 0, -- 0: Chua thanh toan
    -- Constraint
    FOREIGN KEY (UserId) REFERENCES SysUser(id)
);

CREATE TABLE InvoiceDetails(
    id INT PRIMARY KEY AUTO_INCREMENT,
    ProductId INT NOT NULL,
    InvoiceId VARCHAR(128) NOT NULL,
    Quantity INT NOT NULL,
    Price DECIMAL(10,2) NOT NULL,
    -- Constraint
    FOREIGN KEY (ProductId) REFERENCES Products(id),
    FOREIGN KEY (InvoiceId) REFERENCES Invoices(InvoiceId)
);

CREATE TABLE VnPayment(
    TxnRef VARCHAR(128) NOT NULL PRIMARY KEY,
    TmnCode VARCHAR(128) NOT NULL,
    Amount BIGINT NOT NULL,
    BankCode VARCHAR(128) NOT NULL,
    BankTranNo VARCHAR(128) NOT NULL,
    CardType VARCHAR(128) NOT NULL,
    OrderInfo VARCHAR(128) NOT NULL,
    PayDate VARCHAR(128) NOT NULL,
    ResponseCode VARCHAR(128) NOT NULL,
    TransactionNo VARCHAR(128) NOT NULL,
    TransactionStatus VARCHAR(128) NOT NULL
);

-- PROC
DELIMITER //
CREATE PROCEDURE GetCartsById(IN p_CartId VARCHAR(128))
BEGIN
    SELECT 
        A.ProductId, 
        B.Name, 
        B.ImageURL, 
        A.Quantity, 
        B.Price, 
        A.Quantity * B.Price AS Amount, 
        B.FlowerTypeID, 
        A.IsChecked
    FROM 
        Carts A 
    JOIN 
        Products B ON A.ProductId = B.id
    WHERE 
        A.CartId = p_CartId;
END //

DELIMITER ;

-- CALL GetCartsById('9123c875f73c495d9ff68e6bbabc4a03');
DELIMITER //
CREATE PROCEDURE AddInvoice(
    IN p_CartId VARCHAR(128),
    IN p_UserId INT,
    IN p_InvoiceId VARCHAR(128),
    OUT p_Amount DECIMAL(10,2)
)
BEGIN
    -- Tính tổng tiền
    SELECT SUM(C.Quantity * P.Price)
    INTO p_Amount
    FROM Carts C
    JOIN Products P ON C.ProductId = P.id
    WHERE C.IsChecked = 1 AND C.CartId = p_CartId;

    -- Thêm vào bảng Invoices
    INSERT INTO Invoices (InvoiceId, UserId)
    VALUES (p_InvoiceId, p_UserId);

    -- Thêm chi tiết hóa đơn
    INSERT INTO InvoiceDetails (InvoiceId, ProductId, Quantity, Price)
    SELECT p_InvoiceId, C.ProductId, C.Quantity, P.Price
    FROM Carts C
    JOIN Products P ON C.ProductId = P.id
    WHERE C.IsChecked = 1 AND C.CartId = p_CartId;

    -- Xóa giỏ hàng đã chọn
    DELETE FROM Carts
    WHERE CartId = p_CartId AND IsChecked = 1;
END //

DELIMITER ;

DELIMITER //
CREATE PROCEDURE GetCartsByIdWhereChecked(IN p_CartId VARCHAR(128))
BEGIN
    SELECT 
        A.ProductId, 
        B.Name, 
        B.ImageURL, 
        A.Quantity, 
        B.Price, 
        A.Quantity * B.Price AS Amount, 
        B.FlowerTypeID, 
        A.IsChecked
    FROM 
        Carts A 
    JOIN 
        Products B ON A.ProductId = B.id
    WHERE 
        A.CartId = p_CartId AND A.IsChecked = 1;
END //

DELIMITER ;

-- -- Khai báo biến để nhận giá trị OUT
-- SET @amount := 0;

-- -- Gọi thủ tục
-- CALL AddInvoice('913a63659858409cbeff513c81d30276', 1, 'a837d251cf7845d6919728082d8b7acd', @amount);

-- -- Xem kết quả biến OUT
-- SELECT @amount;


-- delete from carts
-- delete from invoices
-- delete from InvoiceDetails

-- UPDATE Carts SET IsChecked = 1 WHERE CartId = '913a63659858409cbeff513c81d30276'
