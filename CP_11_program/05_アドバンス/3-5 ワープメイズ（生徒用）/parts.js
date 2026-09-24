//画像のリスト
let enemy = document.getElementsByClassName("enemy")
let goal = document.getElementsByClassName("goal")
let message = document.getElementsByClassName("message")

//効果音のリスト
let oto = []

//固定データ（変わらないデータ）
let window1 = { sx:640, sy:480 } //ウィンドウの横の長さと縦の長さ
let timerno //タイマー制御用
let timerv = 30 //ゲームの実行タイマ値(小さいと速い)
let canvas //キャンバス

//作業データ（ゲームの状態によって値が変わります）
let timer = timerv //ゲームの実行タイマー
let mode = 0 //ゲームの状態（0:タイトル画面,4:準備,5:プレイ,6:ワープ,8:ゲームオーバー,9:クリア）
let mouse //マウスの座標
let player = { x:1, y:9 } //プレイヤーの位置
let playeri = { x:1, y:9 } //プレイヤーの初期位置
let playerp = { x:1, y:9 } //プレイヤーの前回の位置
let goalmode = 0 //ゴールの状態(0:無効,1:有効)
let score = 0 //スコア
let teki = { x:9, y:1 } //敵の位置
let tekii = { x:9, y:1 } //敵の初期位置
let tekimuki = 0 //敵の向き（0=左,1=右）
let warpmode = 0 //ワープの移動方向（0=無し,1=左から右へ,2=右から左へ)
let hidariwarp = { x:1, y:1 } //左ワープの位置
let migiwarp = { x:9, y:1 } //右ワープの位置
let fruit = { x:5, y:1 } //フルーツの位置
let fruitari = 1 //フルーツの有無
let warpcount = -99 //ワープカウンタ（47～0:出発、-1～-47:到着）
let warpstart = 47 //ワープカウンタの開始値
let hiscore = [0, 0, 0] //ハイスコア1から3位

//最初に１回だけやること（起動処理）
function init() {
    canvas = document.getElementById('canvas') //キャンバスを得る
    ctx = canvas.getContext('2d') //キャンバスの情報（コンテキスト）を得る
    canvas.addEventListener('click', onclick_canvas, false) //クリックされた時の処理を指定
    canvas.addEventListener('mousemove', onmove_canvas, false) //マウスが動いた時の処理を指定
    start() //開始処理を呼ぶ
}

//マウスの座標を得る
function mousezahyo(canvas, event) {
    let rect = canvas.getBoundingClientRect() //キャンバスの位置を得る
    return { //座標を計算して返す
        x: event.clientX - rect.left,
        y: event.clientY - rect.top
    }
}

//(x1,y1)から(x2,y2)を黒くぬりつぶす
function fillblack(x1, y1, x2, y2) {
    ctx.fillStyle = 'black' //色を黒に
    ctx.fillRect(x1, y1, x2, y2) //ぬりつぶす
}

//画面全体に壁をえがきミニタイトルを表示する
function haikeiwall() {
    for (let j = 0; j < 11; j++) { //画面全体(11行分)についてくり返す
        for (let i = 0; i < 14; i++) { //画面全体(14列分)についてくり返す
            ctx.drawImage(wall, i * 48 - 24, j * 48 - 24) //かべの画像を表示
        }
    }
    ctx.drawImage(minititle, 478, 24) //ミニタイトルを表示
}

//メッセージ画像[n]を表示する
function drawmessage(n) {
    ctx.drawImage(message[n], 478, 128) //メッセージ画像[n]を所定の位置に表示する
}

//完全クリアかどうか調べる
function allclear() {
    for (let i = 0; i < 11; i++) { //迷路全列についてくり返す
        for (let j = 0; j < 11; j++) { //迷路全行についてくり返す
            if (map1[j][i] === 0) { //道ならば
                return 0 //完全クリアではない
            }
        }
    }
    return 1 //完全クリア
}

//マウスがプレイヤーの上にいるかどうか調べる
function onplayer() {
    return mouse.x >= player.x * 48 - 24 && mouse.x <= player.x * 48 + 24 && mouse.y >= player.y * 48 - 24 && mouse.y <= player.y * 48 + 24
}

//初めての通過場所ならスコアをa加算して通過済にし、通過済の場所ならb減点する
function tuukashori(a, b) {
    if (map1[player.y][player.x] === 0) { //道の上なら
        map1[player.y][player.x] = 1 //通過済にする
        score = score + a //スコア加算
    } else if (map1[player.y][player.x] === 1 && (playerp.x !== player.x || playerp.y !== player.y) ) { //通過済の上を移動中で
        if (score >= b) { //スコアが10点以上なら
            score = score - 10 //スコア減点
        } else {
            score = 0 //スコアをマイナスにしない
        }
    }
}

//位置(i,j)を基準に48×48を青くぬりつぶす
function fillblue48(i, j) {
    ctx.fillStyle = 'Blue' //色を青に
    ctx.fillRect(i * 48 - 24, j * 48 - 24, 48, 48) //ぬりつぶす
}

//スコアボードを表示してその上に白でスコアnを6桁でえがく
function drawscore(n) {
    ctx.drawImage(scoreboard, 478, 225) //スコアボードを表示
    ctx.fillStyle = 'White' //色を白に
    ctx.font = '26pt Arial' //文字サイズを指定
    ctx.fillText(("000000" + n).slice(-6), 490, 295) //スコアを6桁で表示
}

//迷路の中央(x,276)から文字列sを白のサイズfのArialでえがく
function drawcenter(s, x, f) {
    ctx.fillStyle = 'White' //色を白に
    ctx.font = f + 'pt Arial' //文字サイズを指定
    ctx.fillText(s, x, 276) //文字列を(x,276)から表示
}

//マウスが左ワープの上にいるかどうか調べる
function onhidariwarp() {
    return mouse.x >= hidariwarp.x * 48 - 24 && mouse.x <= hidariwarp.x * 48 + 24 && mouse.y >= hidariwarp.y * 48 - 24 && mouse.y <= hidariwarp.y * 48 + 24
}

//マウスが右ワープの上にいるかどうか調べる
function onmigiwarp() {
    return mouse.x >= migiwarp.x * 48 - 24 && mouse.x <= migiwarp.x * 48 + 24 && mouse.y >= migiwarp.y * 48 - 24 && mouse.y <= migiwarp.y * 48 + 24
}

//ハイスコアの更新
function hiscoreupdate() {
    if (hiscore[2] < score) { //ランクイン（現在の最下位より大）？
        hiscore[2] = score //仮に最下位とする
        for (let i = 2; i > 0; i--) { //1位までについてくり返す
            if (hiscore[i - 1] < hiscore[i]) { //逆順になっていたら
                let temp = hiscore[i - 1]
                hiscore[i - 1] = hiscore[i] //交換する
                hiscore[i] = temp
            } else { //でなければ
                break //更新完了
            }
        }
    }
}

//プレイヤーが左右移動中でますめの中央にいるか（半歩状態ではないか）
function hcenter() {
    return player.x === Math.floor(player.x)
}

//プレイヤーが上下移動中でますめの中央にいるか（半歩状態ではないか）
function vcenter() {
    return player.y === Math.floor(player.y)
}

//衝突判定
function hantei() {
    //差の絶対値(Math.abs)を用いて座標の差が1未満(0.5以下)かチェックする
    return Math.abs(player.y - teki.y) < 1 && Math.abs(player.x - teki.x) < 1 //プレイヤーと敵のXY座標の差が共に0.5以下か
}

//プレイヤーの動き
function playerdousa() {
    if (hcenter()) { //左右半歩状態でなければ上下移動OK
        let pmy = mouse.y - player.y * 48 //マウスのy座標とプレイヤーの中心のy座標の差を求める
        if (pmy > 24 && map1[Math.floor(player.y) + 1][Math.floor(player.x)] < 8) { //マウスがプレイヤーの下にあり道ならば
            player.y += 0.5 //下へ半歩移動
        } else if (pmy < -24 && map1[Math.ceil(player.y) - 1][Math.ceil(player.x)] < 8) { //マウスがプレイヤーの上にあり道ならば
            player.y -= 0.5 //上へ半歩移動
        }
    }
    if (vcenter()) { //上下半歩状態でなければ左右移動OK
        let pmx = mouse.x - player.x * 48 //マウスのx座標とプレイヤーの中心のx座標の差を求める
        if (pmx > 24 && map1[Math.floor(player.y)][Math.floor(player.x) + 1] < 8) { //マウスがプレイヤーの右にあり道ならば
            player.x += 0.5 //右へ半歩移動
        } else if (pmx < -24 && map1[Math.ceil(player.y)][Math.ceil(player.x) - 1] < 8) { //マウスがプレイヤーの左にあり道ならば
            player.x -= 0.5 //左へ半歩移動
        }
    }
}

//敵の動き
function tekidousa(n) { //n=0(動かない)～100(最高速)
    if (Math.floor(Math.random() * 100) < n) { //0～99の乱数を得てn未満であれば
        if (teki.x === Math.floor(teki.x)) { //左右半歩状態でなければ上下移動OK
            let pmy = player.y - teki.y //敵の位置yとプレイヤーの位置yの差を求める
            if (pmy > 0 && map1[Math.floor(teki.y) + 1][Math.floor(teki.x)] < 8) { //プレイヤーが敵の下方で、敵の下が道ならば
                teki.y += 0.5 //下へ半歩移動
            } else if (pmy < 0 && map1[Math.ceil(teki.y) - 1][Math.ceil(teki.x)] < 8) { //プレイヤーが敵の上方で、敵の上が道ならば
                teki.y -= 0.5 //上へ半歩移動
            }
        }
        if (teki.y === Math.floor(teki.y)) { //上下半歩状態でなければ左右移動OK
            let pmx = player.x - teki.x //敵の位置xとプレイヤーの位置xの差を求める
            if (pmx > 0 && map1[Math.floor(teki.y)][Math.floor(teki.x) + 1] < 8) { //プレイヤーが敵の右方で、敵の右が道ならば
                teki.x += 0.5 //右へ半歩移動
                tekimuki = 1 //敵を右向きに
            } else if (pmx < 0 && map1[Math.ceil(teki.y)][Math.ceil(teki.x) - 1] < 8) { //プレイヤーが敵の左方で、敵の左が道ならば
                teki.x -= 0.5 //左へ半歩移動
                tekimuki = 0 //敵を左向きに
            }
        }
    }
}

function retry() {
    if(confirm("やりなおしますか？")) { //ダイアログを表示しOKがクリックされるかEnterキーが押されたら
        for (let j = 0; j < 11; j++) { //迷路全行についてくり返す
            for (let i = 0; i < 11; i++) { //迷路全列についてくり返す
                map1[j][i] = map0[j][i] //マップを元に戻す
            }
        }
        player.x = playeri.x //プレイヤーの位置を元に戻す
        player.y = playeri.y //プレイヤーの位置を元に戻す
        playerp.x = playeri.x //プレイヤーの前回位置を元に戻す
        playerp.y = playeri.y //プレイヤーの前回位置を元に戻す
        goalmode = 0 //ゴールの状態を無効に戻す
        score = 0 //スコアをゼロに戻す
        teki.x = tekii.x //敵の位置を元に戻す
        teki.y = tekii.y //敵の位置を元に戻す
        fruitari = 1 //フルーツを有りに戻す
        mode = 4 //準備モードに戻す
    }
}
