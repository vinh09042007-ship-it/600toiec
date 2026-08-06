# 600 Steps v2

## Giới thiệu
600 Steps v2 là một dự án game học từ vựng TOEIC. Đây là Phase 1: xây dựng nền móng kiến trúc project. 
Dự án được thiết kế theo hướng OOP, tuân thủ nguyên tắc SOLID, mã nguồn sạch và dễ mở rộng.

## Cấu trúc thư mục
- `assets/`: Chứa tài nguyên game (hình ảnh, âm thanh, v.v.).
- `core/`: Chứa các hệ thống lõi của game (Game, EventBus, GameState).
- `data/`: Chứa dữ liệu tĩnh (từ vựng TOEIC, configs, database).
- `npc/`: Chứa logic liên quan đến Non-Player Characters.
- `player/`: Chứa logic liên quan đến người chơi.
- `save/`: Chứa hệ thống lưu trữ tiến trình game.
- `toeic/`: Chứa logic đặc thù cho bài học/kiểm tra TOEIC.
- `ui/`: Chứa hệ thống User Interface.
- `utils/`: Chứa các hàm tiện ích dùng chung.
- `world/`: Chứa logic về thế giới game, bản đồ, môi trường.

## Cách chạy
Chạy lệnh sau từ thư mục gốc của project:
```bash
python main.py
```

## Yêu cầu môi trường
- Python 3.12+
