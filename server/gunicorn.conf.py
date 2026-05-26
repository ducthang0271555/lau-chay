import multiprocessing

# Bind tới file socket (nhanh hơn bind tới port khi chạy cùng Nginx)
bind = "unix:quickorder.sock"

# Số lượng worker (thường = số nhân CPU * 2 + 1)
workers = multiprocessing.cpu_count() * 2 + 1

# Ghi log lỗi
errorlog = "logs/gunicorn_error.log"
accesslog = "logs/gunicorn_access.log"

# Thời gian chờ
timeout = 120