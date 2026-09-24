//画像のリスト
let playerimg = document.getElementsByClassName("playerimg")
let aokage = document.getElementsByClassName("aokage")
let shirokage = document.getElementsByClassName("shirokage")
let akakage = document.getElementsByClassName("akakage")

//効果音のリスト
let oto = []

//固定データ（変わらないデータ）
let window1 = { sx:640, sy:480 } //ウィンドウの横の長さと縦の長さ
let timerno //タイマー制御用
let timerv = 30 //ゲームの実行タイマ値(小さいと速い)
let canvas //キャンバス
let damage = [10, 20, 40, 80] //パンチ力によるダメージ（0:通常,1:ため1,2:ため2,3:ため3）
let shadowcnti = 20 //敵の動作カウンタの初期値(小さいほど速い)

//作業データ（ゲームの状態によって値が変わります）
let timer = timerv //ゲームの実行タイマー
let mode = 0 //ゲームの状態（0:タイトル,4:カウントダウン,5:プレイ,8:KO勝ち,9:KO負け）
let playernow = 0 //プレイヤーの状態（0:上構え,1:下構え,2:上パンチ,3:下パンチ）
let playerpow = 100 //プレイヤーのパワー
let playerpun = -1 //プレーヤーのパンチマーク（-1:なし,0:通常,1:ため1,2:ため2,3:ため3）
let shadowno = 0 //敵の番号(0:青影,1:白影,2:赤影)
let shadownow = 0 //敵の状態（0:上構え,1:下構え,2:上パンチ,3:下パンチ）
let shadowpow = 100 //敵のパワー
let shadowpun = -1 //敵のパンチマーク（-1:なし,0:通常,1:ため1,2:ため2,3:ため3）
let shadowname = [ 'Aokage', 'Shirokage', 'Akakage' ] //敵の名前
let count = 5.0 //カウントダウン用カウンタ
let shadowcnt = shadowcnti //敵の動作カウンタ
let playertame = 0 //プレイヤーのため（0:なし,1:ため1,2:ため2,3:ため3）
let playertamehou = 0 //プレイヤーのための上下（0:上,1:下）
let shadowtame = 0 //敵のため（0:なし,1:ため1,2:ため2,3:ため3）
let shadowtamehou = 0 //敵のための上下（0:上,1:下）
let keycodep = 0 //一つ前におされたキーのコード

//最初に１回だけやること（起動処理）
function init() {
    canvas = document.getElementById('canvas') //キャンバスを得る
    ctx = canvas.getContext('2d') //キャンバスの情報（コンテキスト）を得る
    addEventListener('keydown', keyDown, true) //キーが押し終わった時にやることを示す
    addEventListener('keyup', keyUp, true) //キーが押された時にやることを示す
    start() //開始処理を呼ぶ
}

//プレイヤー名、敵名を名前らんに表示
function drawname(shadowno) {
    ctx.font = '20pt Arial' //文字サイズを指定
    ctx.fillStyle = 'white' //白色に設定
    ctx.fillText('Player', 470, 77) //文字列を表示
    ctx.fillText(shadowname[shadowno], 70, 77) //文字列を表示
}

//カウントダウンのカウンタを表示
function drawcount(counter) {
    ctx.font = '44pt Arial' //文字サイズを指定
    ctx.fillStyle = 'orange' //オレンジ色に設定
    ctx.fillText(Math.ceil(counter), 300, 160) //カウントを切り上げで表示
}

//プレイヤー画像[n]を表示
function drawplayer(n) {
    ctx.drawImage(playerimg[n], 300, 135) //プレイヤー画像を表示
}

//敵[en]の画像[n]を[1/p(未指定なら1)]で表示
function drawshadow(en, n, p=1) {
    if (en === 0) {
        ctx.drawImage(aokage[n], 122, 135, 218, 320 / p) //敵(青影)の画像を表示
    } else if (en === 1) {
        ctx.drawImage(shirokage[n], 122, 135, 218, 320 / p) //敵(白影)の画像を表示
    } else if (en === 2) {
        ctx.drawImage(akakage[n], 122, 135, 218, 320 / p) //敵(赤影)の画像を表示
    }
}

//プレイヤーのパワーメーターを表示
function drawplayerg(power) {
    if (power > 0) {
        ctx.fillStyle = 'red' //色を赤に
        ctx.fillRect(379, 54, Math.floor(260 * power / 100), 29) //ぬりつぶす
    }
}

//敵のパワーメーターを表示
function drawshadowg(power) {
    if (power > 0) {
        ctx.fillStyle = 'red' //色を赤に
        ctx.fillRect(260 - Math.floor(260 * power / 100), 54, Math.floor(260 * power / 100), 29) //ぬりつぶす
    }
}

//プレイヤーのパンチマークを表示
function drawplayerpun(pun) {
    let z = pun + 1 //画像を(パンチ力＋1)倍にする
    if (playernow === 0 || playernow === 2) { //上かまえか上パンチ中なら
        ctx.drawImage(punch, 426 - (50 * z / 2), 285 - (50 * z / 2), 50 * z, 50 * z) //敵の上がわにパンチマーク画像を表示
    } else {
        ctx.drawImage(punch, 426 - (50 * z / 2), 315 - (50 * z / 2), 50 * z, 50 * z) //敵の下がわにパンチマーク画像を表示
    }
}

//敵のパンチマークを表示
function drawshadowpun(pun) {
    let z = pun + 1 //画像を(パンチ力＋1)倍にする
    if (shadownow === 0 || shadownow === 2) { //上かまえか上パンチ中なら
        ctx.drawImage(punch, 206 - (50 * z / 2), 285 - (50 * z / 2), 50 * z, 50 * z) //プレイヤーの上がわにパンチの画像を表示
    } else {
        ctx.drawImage(punch, 206 - (50 * z / 2), 315 - (50 * z / 2), 50 * z, 50 * z) //プレイヤーの上がわにパンチの画像を表示
    }
}

//メッセージを表示
function drawmessage(msg) {
    ctx.font = '44pt Arial' //文字サイズを指定
    ctx.fillStyle = 'orange' //オレンジ色に設定
    ctx.fillText(msg, 250, 160) //メッセージを表示
}

//敵にパンチがあたった時にやること
function shadowdameged(pun) {
    shadowpow = shadowpow - damage[pun] //パンチ力に応じたダメージ量の分だけパワーを下げる
    if (shadowpow <= 0) { //敵のパワーがもうないなら
        mode = 8 //KO勝ちモードにする
    } else {
        playertame = 0 //プレイヤーのためを0に戻す
        shadowtame = 0 //敵のためを0に戻す
    }
}

//プレイヤーにパンチがあたった時にやること
function playerdameged(pun) {
    playerpow = playerpow - damage[pun] //パンチ力に応じたダメージ量の分だけパワーを下げる
    if (playerpow <= 0) { //プレイヤーのパワーがもうないなら
        mode = 9 //KO負けモードにする
    } else {
        playertame = 0 //プレイヤーのためを0に戻す
        shadowtame = 0 //敵のためを0に戻す
    }
}

//プレイヤーのため数を炎の画像で表示
function drawplayert(tame) {
    for (let i = 0; i < tame; i++) { //ため数の分くり返す
        ctx.drawImage(fireimg, 379 + (i * 35), 0) //プレイヤーのパワーメーターの上に炎の画像を表示
    }
}

//敵のため数を炎の画像で表示
function drawshadowt(tame) {
    for (let i = 0; i < tame; i++) { //ため数の分くり返す
        ctx.drawImage(fireimg, 230 - (i * 35), 0) //敵のパワーメーターの上に炎の画像を表示
    }
}

//白影がパンチするかためる
function shirokagepunch(kamae) {
    if (kamae === 0) { //上かまえなら
        if(shadowtame > 2 || shadowtame >= 1 && Math.random() < 0.5) { //ため3またはため1以上の1/2で
            shadownow = 2 //白影の状態を上パンチにする
            shadowpun = shadowtame //ため数をパンチ力にする
            playerdameged(shadowpun) //プレイヤーのパワーメーターを減らし双方のためをゼロにする
        }
    } else { //下かまえなら
        if(shadowtame > 2 || shadowtame >= 1 && Math.random() < 0.5) { //ため3またはため1以上の1/2で
            shadownow = 3 //白影の状態を下パンチにする
            shadowpun = shadowtame //ため数をパンチ力にする
            playerdameged(shadowpun) //プレイヤーのパワーメーターを減らし双方のためをゼロにする
        }
    }
    if (Math.random() < 0.5 && shadowtame < 3) { //50%の確率でため3未満なら
        shadowtame = shadowtame + 1 //ためを1つ進める
    }
}

//白影がかまえを変えるかためる
function shirokagekamae() {
    if (Math.random() < 0.5) { //50%の確率で
        if (shadownow !== 0) { //白影の状態が上かまえでなければ
            shadownow = 0 //白影の状態を上かまえにする
            shadowpun = -1 //パンチマークを消す
            shadowtame = 0 //ためを0に戻す
        } else if (shadowtame < 3) { //ため3未満なら
            shadowtame = shadowtame + 1 //ためを1つ進める
        }
    } else {
        if (shadownow !== 1) { //白影の状態が下かまえでなければ
            shadownow = 1 //白影の状態を下かまえにする
            shadowpun = -1 //パンチマークを消す
            shadowtame = 0 //ためを0に戻す
        } else if (shadowtame < 3) { //ため3未満なら
            shadowtame = shadowtame + 1 //ためを1つ進める
        }
    }
}

//赤影がパンチする
function akakagepunch(kamae) {
    if (kamae === 0) { //上かまえなら
        shadownow = 2 //赤影の状態を上パンチにする
        shadowpun = shadowtame //ため数をパンチ力にする
        playerdameged(shadowpun) //プレイヤーのパワーメーターを減らし双方のためをゼロにする
    } else { //下かまえなら
        shadownow = 3 //赤影の状態を下パンチにする
        shadowpun = shadowtame //ため数をパンチ力にする
        playerdameged(shadowpun) //プレイヤーのパワーメーターを減らし双方のためをゼロにする
    }
}

//赤影がかまえを変える
function akakagekamae() {
    if (Math.random() < 0.5) { //50%の確率で
        if (shadownow !== 0) { //赤影の状態が上かまえでなければ
            shadownow = 0 //赤影の状態を上かまえにする
            shadowpun = -1 //パンチマークを消す
            shadowtame = 0 //ためを0に戻す
        }
    } else {
        if (shadownow !== 1) { //赤影の状態が下かまえでなければ
            shadownow = 1 //赤影の状態を下かまえにする
            shadowpun = -1 //パンチマークを消す
            shadowtame = 0 //ためを0に戻す
        }
    }
}
