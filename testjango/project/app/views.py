from django.shortcuts import render
from django.http import HttpResponse
# Create your views here

import cv2
from django.http import StreamingHttpResponse
from django.views import View


# ストリーミング画像・映像を表示するview
class IndexView(View):
    def get(self, request):
        return render(request, 'app/index.html', {})

# ストリーミング画像を定期的に返却するview
def video_feed_view():
    return lambda _: StreamingHttpResponse(generate_frame(), content_type='multipart/x-mixed-replace; boundary=frame')

# フレーム生成・返却する処理
def generate_frame():
    capture = cv2.VideoCapture(0)  # USBカメラから
    count = 0
    if not capture.isOpened():
        print("Capture is not opened.")
    ret, frame = capture.read()
    h,w = frame.shape[:2]
    print("h=",h,", w=",w)


    while True:
        count += 1
        # カメラからフレーム画像を取得
        ret, frame = capture.read()
        if not ret:
            print("Failed to read frame.")
            break
        if(count % 2 == 0):
            # フレーム画像バイナリに変換
            ret, jpeg = cv2.imencode('.jpg', frame)
            byte_frame = jpeg.tobytes()
            # フレーム画像のバイナリデータをユーザーに送付する
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + byte_frame + b'\r\n\r\n')
    capture.release()