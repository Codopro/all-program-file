//作業データ
let tekitamax //敵弾のX座標
let tekitamay //敵弾のY座標
let shogaia = [] //障害物のリスト

//敵弾の移動
function tekitamaido() {
    if (tekitamay <= window1.sy) { //敵弾が下端じゃない？
        tekitamay += tekitama.my //敵弾下移動
    }
    if (tekitamay >= window1.sy) { //敵弾が下端？
        return 0 //敵弾を消すことにして戻る
    }
    return 1 //そのまま戻る
}

//敵弾発射
function tekikogeki() {
    let d = window1.sx * window1.sx + window1.sy * window1.sy //自機との距離の最小値を仮にウィンドウ最大値２乗とする
    let ni = 32; //自機との距離が最小の敵機を仮に32番とする
    for (let i = 0; i < 32; i++) { //敵機全機について繰返す
        if (tekia[i].f === 1) { //敵機[i]がある？
            //自機との距離の２乗を得る
            let di = (tekia[i].x - playerx) * (tekia[i].x - playerx) + (tekia[i].y - playery) * (tekia[i].y - playery)
            if (di < d) { //最小値更新？
                d = di //最小距離を再設定
                ni = i //最小な敵機を仮定
            }
        }
    }
    tekitamax = tekia[ni].x + teki.sx / 2 //敵弾のX座標を最近敵機の中央とする
    tekitamay = tekia[ni].y + teki.sy //敵弾のY座標を最近敵機の直下とする
}

//敵弾と自機の衝突判定
function tekitamaplayerhit() {
    if (ccheck(tekitamax, tekitamay, tekitama.sx, tekitama.sy, playerx, playery, player.sx, player.sy)) { //衝突?
        mode = 9 //ゲームオーバーにする
        return 0 //ゲームオーバとして戻る
    } else {
        return 1 //そのまま戻る
    }

}

//敵弾と自弾の衝突判定
function tekitamatamahit() {
    if (ccheck(tekitamax, tekitamay, tekitama.sx, tekitama.sy, tamax, tamay, tama.sx, tama.sy)) { //衝突?
        score += 100 //スコア加算
        return 0 //衝突として戻る
    } else {
        return 1 //そのまま戻る
    }

}

//障害物出現処理：ゲーム開始時に呼ばれる
function shogaijunbi() {
    for (let i = 0; i < 24; i++) { //全障害物について繰返す
        let wx = (i % 12) * 20 + shogai.x + Math.floor((i % 12 / 3)) * 100 //X座標
        let wy = (i < 12 ? 0 : 1) * 20 + shogai.y //Y座標
        shogaia[i] = { x:wx, y:wy, f:1 } //敵機[i]のXY座標と有無を指定
    }
}

//敵弾と障害物の衝突判定
function tekitamashogaihit() {
    for (let i = 0; i < 24; i++) { //全障害物について繰返す
        if (shogaia[i].f === 1) { //障害物[i]がある？
               if (ccheck(tekitamax, tekitamay, tekitama.sx, tekitama.sy, shogaia[i].x, shogaia[i].y, shogai.sx, shogai.sy)) { //衝突?
                   shogaia[i].f = 0 //障害物[i]を消す
                   return 0 //衝突として戻る
               }
        }
    }
    return 1 //そのまま戻る
}

//自弾と障害物の衝突判定
function tamashogaihit() {
    for (let i = 0; i < 24; i++) { //全障害物について繰返す
        if (shogaia[i].f === 1) { //障害物[i]がある？
            if (ccheck(tamax, tamay, tama.sx, tama.sy, shogaia[i].x, shogaia[i].y, shogai.sx, shogai.sy)) { //衝突?
                shogaia[i].f = 0 //障害物[i]を消す
                return 0 //衝突として戻る
            }
        }
    }
    return 1 //そのまま戻る
}

//敵機と障害物の衝突判定
function tekishogaihit() {
    for (let i = 0; i < 32; i++) { //敵機全機について繰返す
        if (tekia[i].f === 1) { //敵機[i]がある？
            for (let j = 0; j < 24; j++) { //全障害物について繰返す
                if (shogaia[j].f === 1) { //障害物[i]がある？
                    if (ccheck(tekia[i].x, tekia[i].y, teki.sx, teki.sy, shogaia[j].x, shogaia[j].y, shogai.sx, shogai.sy)) { //衝突?
                        shogaia[j].f = 0 //障害物[j]を消す
                    }
                }
            }
        }
    }
}

