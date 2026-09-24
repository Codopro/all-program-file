//作業データ
let ufox //UFOのX座標
let ufoy //UFOのY座標

//UFOの移動
function ufoido() {
    if (ufox + ufo.sx <= window1.sx) { //UFOが右端じゃない？
        ufox += ufo.mx //UFO右移動
    }
    if (ufox + ufo.sx >= window1.sx) { //UFOが右端？
    	ufow = ufo.wait
        return 0 //UFOを消すことにして戻る
    }
    return 1 //戻る
}

//UFO出現
function ufojunbi() {
    ufox = ufo.x //UFOのX座標を初期値とする
    ufoy = ufo.y //UFOのY座標を初期値とする
}

//UFOと自弾の衝突判定
function ufohit() {
    if (ccheck(ufox, ufoy, ufo.sx, ufo.sy, tamax, tamay, tama.sx, tama.sy)) { //衝突?
        score += 200 //スコア加算
    	ufow = ufo.wait
        return 0
    } else {
    	return 1
    }
}

//UFOと自弾の衝突判定(2)
function ufohit2() {
    if (ccheck(ufox, ufoy, ufo.sx, ufo.sy, tamax, tamay, tama.sx, tama.sy)) { //衝突?
        score += 200 //スコア加算
    	ufobw = ufob.wait
        return 2
    } else {
    	return 1
    }
}

