//画像のリスト
let candyb = document.getElementsByClassName("candyb")
let candy = document.getElementsByClassName("candy")

//効果音のリスト
let oto = [] 

//固定データ（変わらないデータ）
let window1 = { sx:640, sy:480 } //ウィンドウの横の長さと縦の長さ
let timerno //タイマー制御用
let timerv = 30 //ゲームの実行タイマー値(小さいと速い)
let canvas //キャンバス
let catxys = { x:320, y:240 } //キャッチャーの初期中心座標
let cats = { x:64, y:64 } //キャッチャー画像の大きさ
let stars = { x:64, y:64 } //星画像の大きさ
let ropefrom = { x:320, y:400 } //ロープの開始座標
let ropelen = 10 //ロープの1回の長さ
let netss = { x:202, y:63 } //ネットの大きさの最大値
let netcounts = 20 //ネットを広げられる回数
let candys = { x:32, y:32 } //キャンディ画像の大きさ
let candyspeed = 3 //キャンディの落下スピード
let candyspeeds = [3, 4, 5, 5] //キャンディ群の落下スピード
let point = [10, 20, 30, 40] //キャンディごとのポイント

//作業データ（ゲームの状態によって値が変わります）
let timer = timerv //ゲームの実行タイマー
let mode = 0 //ゲームの状態（ 0:タイトル, 5:プレイ, 9:ゲームオーバー）
let mouse //マウスカーソルの座標
let catxy = { x:catxys.x - (cats.x / 2) , y:catxys.y - (cats.y / 2) } //キャッチャーの中心座標
let stardist = -1 //キャンディバケツから星までの距離(-1:無し)
let starxy = { x:0, y:0 } //星の中心座標（クリック時のキャッチャーの中心座標）
let ropestep = 0 //ロープを星まで伸ばす回数（キャンディバケツから星までの距離÷ロープの1回の長さ）
let ropev = { x:0, y:0 } //ロープを伸ばす長さ1回分
let ropecount = 0 //ロープを伸ばした回数
let ropeto = { x:0, y:0 } //ロープの終了座標
let inaction = 0 //キャッチング状態(0:開始前,1:ロープを伸ばす,2:ネットを広げる,3:ネットを縮める,4:ロープを戻す)
let netxy = { x:0, y:0 } //ネットの中心座標
let nets = { x:0, y:0 } //ネットの大きさ
let netcount = 0 //ネットを広げた回数
let canxy = { x:-1, y:0 } //キャンディの中心座標(x=-1なら無し)
let candyget = 0 //キャンディのゲット数
let score = 0 //スコア
let cantype = 0 //キャンディの種類
let hiscore = [0, 0, 0] //ハイスコア(3位まで)
let catnum = 2 //残りキャッチャー数
let precantype = 0 //１つ前のキャンディの種類

//最初に１回だけやること（起動処理）
function init() {
    canvas = document.getElementById('canvas') //キャンバスを得る
    ctx = canvas.getContext('2d') //キャンバスの情報（コンテキスト）を得る
    canvas.addEventListener('click', onclick_canvas, false) //クリックされた時の処理を指定
    canvas.addEventListener('mousemove', onmove_canvas, false) //マウスが動いた時の処理を指定
    start() //開始処理を呼ぶ
}

//マウスカーソルの座標を得る
function mousezahyo(canvas, event) {
    let rect = canvas.getBoundingClientRect() //キャンバスの位置を得る
    return { //座標を計算して返す
        x: event.clientX - rect.left,
        y: event.clientY - rect.top
    }
}

//キャッチャーを表示する
function drawcatcher(x, y) {
    ctx.drawImage(catcher, x - cats.x / 2, y - cats.y / 2) //キャッチャー画像を表示
}

//キャンディバケツから星までの距離(XとYの長い方)を求める
function getstardist(x, y) {
    if (Math.abs(ropefrom.x - x) > Math.abs(ropefrom.y - y)) { //星とロープ開始位置の座標差がXの方が大きければ
        return Math.abs(ropefrom.x - x) //キャンディバケツから星までの距離は星とロープ開始位置のX座標差(絶対値)とする
    } else { //でなければ
        return Math.abs(ropefrom.y - y) //キャンディバケツから星までの距離は星とロープ開始位置のY座標差(絶対値)とする
    }
}

//ロープを伸ばす長さの1回分を求める
function getropelen(step) {
    let r = { x:0, y:0 } //ロープを伸ばす長さの1回分
    r.x = Math.floor((starxy.x - ropefrom.x) / step) //ロープを伸ばす長さX方向1回分(小数点以下切捨て)を求める
    r.y = Math.floor((starxy.y - ropefrom.y) / step) //ロープを伸ばす長さY方向1回分(小数点以下切捨て)を求める
    return r //ロープを伸ばす長さの1回分を返す
}

//ロープを回数分伸ばした位置の座標を求める
function getropeto(count) {
    let r = { x:0, y:0 } //ロープを回数分伸ばした位置の座標
    r.x = ropefrom.x + ropev.x * count //ロープを回数分伸ばしたX座標を求める
    r.y = ropefrom.y + ropev.y * count //ロープを回数分伸ばしたY座標を求める
    return r //ロープを回数分伸ばした位置の座標を返す
}

//星を表示する
function drawstar(x, y) {
    ctx.drawImage(star, x - stars.x / 2, y - stars.y / 2) //星画像を表示
}

//ロープをえがく
function drawrope(x, y) {
    ctx.lineWidth = "5" //線の幅を設定
    ctx.strokeStyle = "yellow" //線の色を設定
    ctx.beginPath() //線の経路設定開始
    ctx.moveTo(ropefrom.x, ropefrom.y) //線の開始位置設定
    ctx.lineTo(x, y) //線の終了位置設定
    ctx.stroke() //線を描く
}

//ネットを表示する
function drawnet(x, y, c) {
    nets.x = netss.x * c / netcounts //ネットの大きさXを求める
    nets.y = netss.y * c / netcounts //ネットの大きさYを求める
    ctx.drawImage(net, x - nets.x / 2, y - nets.y / 2, nets.x, nets.y) //ネット画像を表示
}

//キャンディのX座標を乱数で決める
function setcandy() {
    let x = 320 //キャンディのX座標を仮に中央にしておく
    do {
        x = Math.floor(Math.random() * (window1.sx - candys.x)) + candys.x / 2 //キャンディのX座標を乱数で決める
    } while (x >= 288 && x <= 354) //中央になったらやり直し
    return x //キャンディのX座標を返す
}

//キャンディを表示する
function drawcandy(x, y, n = 0) {
    ctx.drawImage(candy[n], x - candys.x / 2, y - candys.y / 2) //キャンディ画像[n]を表示
}

//ネットがキャンディにかかっているかチェックする
function netcandycheck() { //ネットがキャンディにかかっているかチェックする
    if (candyget === 0) { //キャンディをゲットしていなければ
        if (starxy.x - nets.x / 2 < canxy.x && starxy.x + nets.x / 2 > canxy.x
         && starxy.y - nets.y / 2 < canxy.y && starxy.y + nets.y / 2 > canxy.y) { //ネットがキャンディにかかっていたら
            canxy.x = -1 //キャンディを消す
            canxy.y = 0 //キャンディの高さを戻す
            precantype = cantype //１つ前のキャンディの種類をセット
            return 1 //かかっていると返す
        }
        return 0 //かかっていないと返す
    }
    return 1 //かかっていると返す
}

//ゲームオーバーを表示
function drawgameover() {
    ctx.font = '80pt Arial' //文字サイズを指定
    ctx.fillStyle = 'Red' //文字を赤色に
    ctx.fillText('Game Over', 42, 260) //文字列'Game Over'を表示
}

//スコアを表示
function drawscore(myscore) {
    ctx.font = '24pt Arial' //文字サイズを指定
    ctx.fillStyle = 'white' //白色に設定
    ctx.fillText("SCORE:" + ("00000" + myscore).slice(-5), 10, 40) //スコアを5桁で表示
}

//ハイスコアの更新
function hiscoreupdate(myscore) {
    if (hiscore[2] < myscore) { //ランクイン（現在の最下位より大）？
        hiscore[2] = myscore //仮に最下位とする
        for (let i = 2; i > 0; i--) { //1位までについてくり返す
            if (hiscore[i - 1] < hiscore[i]) { //逆順になっていたら
                let temp = hiscore[i - 1]
                hiscore[i - 1] = hiscore[i] //交換する
                hiscore[i] = temp
            } else { //でなければ
                break //更新完了
            }
        }
        if (hiscore[0] === myscore) { //ハイスコア1位更新または同点1位ならば
            return 1 //ハイスコア1位を返す
        }
    }
    return 0 //ハイスコア1位ならずを返す
}

//ハイスコアを表示
function drawhiscore(n) {
    ctx.fillText(n + ": " + ("00000" + hiscore[n - 1]).slice(-5), 344, 270 + 34 * n) //中下にハイスコア[n]を表示
}

//"Click to Play Again"を表示
function drawplayagain() {
    ctx.font = '20pt Arial' //文字サイズを指定
    ctx.fillStyle = 'Red' //文字を赤色に
    ctx.fillText('Click to', 200, 457) //文字列'Click to'を表示
    ctx.fillText('Play Again', 358, 457) //文字列'Play Again'を表示
}

//残りキャッチャーを表示
function drawcatnum(num) {
    for (let i = 0; i < num; i++) { //残りキャッチャーの数だけくり返す
        ctx.drawImage(catcher, 610 - 24 * i, 10, 24, 24) //キャッチャー画像を表示
    }
}
