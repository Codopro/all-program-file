//基本定義
let window1 = { sx:640, sy:480 } //ウィンドウのX,Y長

//作業データ
let score = 0 //スコア
let playerx //自機のX座標
let playery //自機のY座標
let tamax //自弾のX座標
let tamay //自弾のY座標
let tekimx //敵機の移動量
let tekilast //敵機最下位の番号

//起動時処理：起動時にのみ実行される
function init() {
    playerx  = player.x //自機のX座標
    playery  = player.y //自機のY座標
    tamax = 0 //自弾のX座標
    tamay = playery - tama.sy //自弾のY座標
    tekimx = teki.mx //敵機の移動量
    tekilast = -1 //敵機最下位の番号
    ctx = document.getElementById('canvas').getContext('2d') //コンテントを得る
    addEventListener('keydown', keyDown, true) //キー押下時処理を登録
    addEventListener('keyup', keyUp, true) //キー押下終了時処理を登録
    start() //開始処理を呼ぶ
}

//開始処理：起動時処理などから呼ばれる
function start() {
    Timer = setInterval(mainloop, timer) //主処理ループを呼ぶタイマーを起動
}

//衝突判定処理：図形Aの座標(xa,ya)幅wa高さha、図形Bの座標(xb,yb)の幅wb高さhbを受け取り、衝突ならtrueを返す
function ccheck(xa, ya, wa, ha, xb, yb, wb, hb) {
    xa = xa + Math.floor(wa / 2) //図形Ａの中心x座標を求める
    ya = ya + Math.floor(ha / 2) //図形Ａの中心y座標を求める
    let r1 = (wa < ha) ? Math.floor(wa / 2) : Math.floor(ha / 2) //図形Ａの内径を求める(幅と高さで小さい方の半分)
    xb = xb + Math.floor(wb / 2) //図形Ｂの中心x座標を求める
    yb = yb + Math.floor(hb / 2) //図形Ｂの中心y座標を求める
    let r2 = (wb < hb) ? Math.floor(wb / 2) : Math.floor(hb / 2) //図形Ｂの内径を求める(幅と高さで小さい方の半分)
    //中心座標どうしの距離が内径の和未満なら衝突とする
    if ((xa - xb) * (xa - xb) + (ya - yb) * (ya - yb) < (r1 + r2) * (r1 + r2)) {
        return true
    } else {
        return false
    }
}

//敵機群出現処理：ゲーム開始時と敵機全滅時に呼ばれる
function tekijunbi() {
    for (let i = 0; i < 32; i++) { //敵機全機について繰返す
        let wx = Math.floor(i % 8) * 60 + Math.floor(i % 8 / 4) * 40  + teki.x //X座標を計算(中央を空ける)
        let wy = Math.floor(i / 8) * 60 + teki.y  //Y座標を計算
        tekia[i] = { x:wx, y:wy, f:1 } //敵機[i]のXY座標と有無を指定
    }
    tekinum = 32 //敵機残数
}

//自弾と敵機の衝突判定
function hit() {
    for (let i = 0; i < 32; i++) { //敵機全機について繰返す
        if (tekia[i].f === 1) { //敵機[i]がある？
            if (ccheck(tamax, tamay, tama.sx, tama.sy, tekia[i].x, tekia[i].y, teki.sx, teki.sy)) { //衝突?
                tekia[i].f = 0 //敵機[i]を消す
                tekinum-- //敵機残数カウントダウン
                score += 10 //スコア加算
                return 0 //自弾を消すことにして戻る
            }
        }
    }
    return 1 //衝突していないので何もせずに戻る
}

//自弾の移動
function tamaidou() {
    if (tamay >= tama.sy) { //自弾が上端じゃない？
        tamay -= tama.mx //自弾上移動
    }
    if (tamay <= tama.sy) { //自弾が上端にたっする？
        return 0 //自弾を消すことにして戻る
    } else { //でなければ
        return 1 //自弾は消さないことにして戻る
    }
}

//自弾発射
function tamauchi() {
    tamax = playerx + 10 //自弾のX座標を自機に合わせる
    tamay = playery - tama.sy //自弾のY座標を初期位置にする
}

//自機左移動
function hidariidou() {
    if (playerx >= player.mx) { //左端じゃない？
        playerx -= player.mx //自機を左へ
    }
}

//自機右移動
function migiidou() {
    if (playerx < window1.sx - player.sx) { //右端じゃない？
        playerx += player.mx //自機を右へ
    }
}

//敵機の移動
function tekiidou() {
    let tekilimitl = window1.sx //敵機群の左端を仮にウィンドウの右端とする
    let tekilimitr = 0 ///敵機群の右端を仮にウィンドウの左端とする
    let tekimy = 0 //敵機群の下移動量
    for (let i = 0; i < 32; i++) { //敵機全機について繰返す
        if (tekia[i].f === 1) { //敵機[i]がある？
            if (tekimx > 0 && tekia[i].x > tekilimitr) {//右方向移動中で右端？
                tekilimitr = tekia[i].x //右端とする
            } else if (tekimx < 0 && tekia[i].x < tekilimitl) { //左方向移動中で左端？
                tekilimitl = tekia[i].x //左端とする
            }
        }
    }
    if (tekimx > 0 && tekilimitr >= window1.sx - teki.sx || tekimx < 0 && tekilimitl <= 0) { //左端か右端になった？
        tekimx = -tekimx //敵機横移動方向反転
        tekimy = teki.my //下移動量設定
    }
    for (let i = 0; i < 32; i++) { //敵機全機について繰返す
        if (tekia[i].f === 1) { //敵機[i]がある？
            if (tekimy === 0) { //左右移動のみ？
                tekia[i].x += tekimx //敵機横移動
            } else {
                tekia[i].y += tekimy //敵機下移動
            }
            tekilast = i //最下位の敵機が何番目かを取っておく
        }
    }
}

//征服チェック
function shinryaku() {
    if (tekia[tekilast].y + teki.sy > playery + teki.my) { //最下位の敵機が自機ラインに届いた？
        return 1 //征服されたとして戻る
    } else {
        return 0 //征服されていないとして戻る
    }
}
