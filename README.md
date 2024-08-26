# RecogBarcodeRTC
- 商品認識用のRTC  
- pythonプログラム  
- 機能：カメラで撮影された画像からバーコードを検出し，商品のIDを抽出する  

# Usage
- ライブラリのインストール：pip install opencv-python pyzbar
- 実行：python RecogBarcodeRTC.py  
  
  ※実行してもdllファイルが見つからないエラーが出る場合，Microsoft公式から Viaual C++ 2013 再配布パッケージをダウンロードしてインストールすると解決した．(vcredist_x64.exe)  
  https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170#visual-studio-2013-vc-120--no-longer-supported

# Specification
- InPort
    - カメラ画像（RTC:CameraImage）
- OutPort
    - 商品ID　or　404(not found) (RTC:TimedLong)
- n秒間撮影中
    - バーコードを見つけたら商品IDを送信
    - 見つけられなかったら404を送信